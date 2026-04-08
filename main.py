import oracledb
import json
from datetime import datetime

# --- CONFIGURAÇÕES ---
DB_CONFIG = {"user": "SYSTEM", "password": "oracle", "dsn": "localhost:1521/xe"}

# --- SUBALGORITMOS DE APOIO (TXT) ---

def carregar_limites_txt():
    limites = {"temp_limite": 95.0, "pressao_limite": 160.0}
    try:
        with open('config.txt', 'r') as f:
            for linha in f:
                if ':' in linha:
                    chave, valor = linha.strip().split(':')
                    limites[chave.strip()] = float(valor)
    except:
        pass
    return limites

def registrar_log_txt(maquina, status, mensagem):
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open('log_atividades.txt', 'a', encoding='utf-8') as f:
        f.write(f"[{data_hora}] Máquina: {maquina} | Status: {status} | Obs: {mensagem}\n")

# --- CONSISTÊNCIA DE DADOS (REQUISITO AVALIADO) ---

def obter_entrada_float(prompt, min_val=0, max_val=1000):
    """Garante que a entrada seja numérica e dentro de um range lógico."""
    while True:
        try:
            valor = float(input(prompt))
            if min_val <= valor <= max_val:
                return valor
            print(f"❌ Valor fora do intervalo permitido ({min_val} a {max_val}).")
        except ValueError:
            print("❌ Entrada inválida! Digite apenas números (use ponto para decimais).")

# --- LÓGICA E PERSISTÊNCIA (ORACLE / JSON) ---

def salvar_no_oracle(dados, status):
    try:
        conn = oracledb.connect(**DB_CONFIG)
        cursor = conn.cursor()
        sql = """INSERT INTO TB_TELEMETRIA 
                 (ID_MAQUINA, TEMP_MOTOR, PRESSAO_HIDR, HORIMETRO_ATU, ALERTA_GERADO) 
                 VALUES (:1, :2, :3, :4, :5)"""
        cursor.execute(sql, (dados['id'], dados['temp'], dados['pressao'], dados['horimetro'], status))
        conn.commit()
        conn.close()
        return True
    except oracledb.IntegrityError:
        print(f"❌ Erro: Máquina {dados['id']} não cadastrada no banco.")
        return False
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return False

def gerar_relatorio_json():
    try:
        conn = oracledb.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM TB_TELEMETRIA ORDER BY DATA_LEITURA DESC")
        colunas = [col[0] for col in cursor.description]
        dados = [dict(zip(colunas, row)) for row in cursor]
        
        for d in dados: d['DATA_LEITURA'] = str(d['DATA_LEITURA'])
        
        with open('relatorio_saude.json', 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        print(f"📂 Relatório gerado com sucesso ({len(dados)} registros).")
        conn.close()
    except Exception as e:
        print(f"❌ Falha ao gerar JSON: {e}")

# --- MENU PRINCIPAL ---

def menu():
    limites = carregar_limites_txt()
    while True:
        print("\n--- FARMTECH SOLUTIONS: MONITORAMENTO ---")
        print("1. Registrar Telemetria")
        print("2. Exportar JSON")
        print("3. Sair")
        
        op = input("Opção: ")
        if op == "1":
            id_maq = input("ID da Máquina: ").upper().strip()
            if not id_maq: continue
            
            # Aplicando a consistência pedida no enunciado
            temp = obter_entrada_float("Temperatura (°C): ", 0, 200)
            pres = obter_entrada_float("Pressão (PSI): ", 0, 1000)
            hori = obter_entrada_float("Horímetro: ", 0, 99999)
            
            # Lógica de Diagnóstico
            status = "NORMAL"
            msg = "Operação Estável"
            if temp > limites['temp_limite']:
                status, msg = "CRÍTICO", "Superaquecimento detectado!"
            elif pres < limites['pressao_limite']:
                status, msg = "ALERTA", "Baixa pressão hidráulica!"
            
            print(f"\n>> Resultado: {status} ({msg})")
            
            dados = {"id": id_maq, "temp": temp, "pressao": pres, "horimetro": hori}
            if salvar_no_oracle(dados, status):
                registrar_log_txt(id_maq, status, msg)
                
        elif op == "2":
            gerar_relatorio_json()
        elif op == "3":
            break

if __name__ == "__main__":
    menu()