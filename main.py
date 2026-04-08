import oracledb
import json
from datetime import datetime

# --- CONFIGURAÇÕES DE CONEXÃO ---
# Requisito: Conexão com Banco de Dados (Oracle)
DB_CONFIG = {
    "user": "SYSTEM",
    "password": "oracle",
    "dsn": "localhost:1521/xe"
}

# --- SUBALGORITMOS DE SUPORTE ---

def carregar_limites_txt():
    """
    REQUISITO: Manipulação de arquivos (TXT).
    Lê os thresholds de um arquivo externo.
    """
    limites = {"temp_limite": 95.0, "pressao_limite": 160.0}
    try:
        with open('config.txt', 'r') as f:
            for linha in f:
                if ':' in linha:
                    chave, valor = linha.strip().split(':')
                    limites[chave] = float(valor)
        print("⚙️ Configurações de limites carregadas via TXT.")
    except (FileNotFoundError, ValueError):
        print("⚠️ Usando limites padrão (config.txt não encontrado ou inválido).")
    return limites

def registrar_log_txt(maquina, status, mensagem):
    """Grava um histórico de eventos em arquivo de texto."""
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open('log_atividades.txt', 'a', encoding='utf-8') as f:
        f.write(f"[{data_hora}] Máquina: {maquina} | Status: {status} | Obs: {mensagem}\n")

def obter_conexao():
    try:
        return oracledb.connect(**DB_CONFIG)
    except Exception as e:
        print(f"❌ Erro de conexão Oracle: {e}")
        return None

# --- SUBALGORITMOS DE REGRAS DE NEGÓCIO ---

def calcular_status_ativo(telemetria, limites):
    """
    REQUISITO: Subalgoritmo com passagem de parâmetros e Dicionários.
    Determina a saúde do ativo com base nos limites carregados.
    """
    temp = telemetria.get('temp_motor')
    pressao = telemetria.get('pressao_hidraulica')
    
    if temp > limites['temp_limite']:
        return "CRÍTICO", f"Superaquecimento! (Limite: {limites['temp_limite']}°C)"
    elif pressao < limites['pressao_limite']:
        return "ALERTA", f"Pressão hidráulica baixa! (Mínimo: {limites['pressao_limite']} PSI)"
    return "NORMAL", "Operação estável."

# --- SUBALGORITMOS DE PERSISTÊNCIA ---

def salvar_leitura_banco(dados, status):
    conn = obter_conexao()
    if conn:
        try:
            cursor = conn.cursor()
            sql = """INSERT INTO TB_TELEMETRIA 
                     (ID_MAQUINA, TEMP_MOTOR, PRESSAO_HIDR, HORIMETRO_ATU, ALERTA_GERADO) 
                     VALUES (:1, :2, :3, :4, :5)"""
            cursor.execute(sql, (
                dados['id_maquina'], 
                dados['temp_motor'], 
                dados['pressao_hidraulica'],
                dados['horimetro_atu'],
                status
            ))
            conn.commit()
            print("✅ Dados persistidos no Oracle.")
        except oracledb.IntegrityError:
            print(f"❌ ERRO: A máquina {dados['id_maquina']} não está cadastrada no sistema.")
            print("Cadastre-a no banco de dados antes de enviar telemetrias.")
        finally:
            conn.close()

def exportar_diagnostico_json():
    """
    REQUISITO: Manipulação de arquivo JSON.
    Gera relatório estruturado para integração/dashboards.
    """
    conn = obter_conexao()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM TB_TELEMETRIA ORDER BY DATA_LEITURA DESC")
            colunas = [col[0] for col in cursor.description]
            historico = [dict(zip(colunas, row)) for row in cursor]
            
            for item in historico:
                if 'DATA_LEITURA' in item:
                    item['DATA_LEITURA'] = str(item['DATA_LEITURA'])

            with open('relatorio_ativos.json', 'w', encoding='utf-8') as f:
                json.dump(historico, f, indent=4, ensure_ascii=False)
            
            print(f"📂 Relatório exportado: {len(historico)} registros em 'relatorio_ativos.json'.")
        finally:
            conn.close()

# --- FLUXO PRINCIPAL ---

def menu():
    # Carrega limites no início da execução
    limites_config = carregar_limites_txt()

    while True:
        print("\n" + "="*40)
        print("      FARMTECH: MONITORAMENTO DE ATIVOS")
        print("="*40)
        print("1. Registrar Telemetria (Campo)")
        print("2. Gerar Relatório JSON (Completo)")
        print("3. Sair")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "1":
            try:
                # REQUISITO: Consistência de dados (Tratamento de tipos)
                id_maq = input("ID da Máquina: ").upper()
                temp = float(input("Temperatura do Motor (°C): "))
                pressao = float(input("Pressão Hidráulica (PSI): "))
                horimetro = float(input("Horímetro Atual: "))
                
                # REQUISITO: Estrutura de dados (Dicionário)
                dados = {
                    "id_maquina": id_maq,
                    "temp_motor": temp,
                    "pressao_hidraulica": pressao,
                    "horimetro_atu": horimetro
                }
                
                status, msg = calcular_status_ativo(dados, limites_config)
                print(f"\nDIAGNÓSTICO: {status}")
                print(f"MENSAGEM: {msg}")
                
                # Persistência em Banco e Log TXT
                salvar_leitura_banco(dados, status)
                registrar_log_txt(id_maq, status, msg)
                
            except ValueError:
                print("❌ ERRO: Use apenas números para Temperatura, Pressão e Horímetro.")
        
        elif opcao == "2":
            exportar_diagnostico_json()
            
        elif opcao == "3":
            print("Finalizando sistema FarmTech...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()