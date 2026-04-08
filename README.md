# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img width="2385" height="642" alt="logo-fiap" src="https://github.com/user-attachments/assets/52fe0ec7-99f9-427c-9a6d-9d31a41834b6" /></a>
</p>

<br>

# FarmTech Solutions: Monitoramento Preventivo de Ativos

## Nome do grupo

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/company/inova-fusca">Gustavo do Carmo Kamitani</a>
- <a href="https://www.linkedin.com/company/inova-fusca">Renan Carmo Menezes</a>

## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/company/inova-fusca">Nicolly Candida Rodrigues de Souza</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/company/inova-fusca">André Godoi Chiovato</a>


## 📜 Descrição

O FarmTech Solutions é uma solução de inteligência voltada para o setor de máquinas e insumos do agronegócio. O projeto atende à necessidade crítica de reduzir as perdas na colheita mecanizada (que podem chegar a 15% segundo a SOCICANA) através do monitoramento em tempo real da telemetria de tratores e colhedoras.

A aplicação, desenvolvida em Python, integra-se a um banco de dados Oracle para registrar histórico de temperatura e pressão hidráulica, processando esses dados para gerar diagnósticos preventivos (Normal, Alerta ou Crítico). O sistema visa evitar a fundição de motores e falhas hidráulicas, otimizando o tempo de vida útil dos ativos e garantindo a continuidade da produção agrícola.


## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>main.py</b>: Código fonte py.

- <b>config.txt</b>: Arquivos de parâmetros e ajustes.

- <b>log_atividades.txt</b>: Logs e documentos complementares.

- <b>relatorio_saude.json</b>: Documentos gerados pelo sistema.



## 🔧 Como executar o código

O projeto foi desenvolvido para rodar em ambiente local com suporte a contêineres para o banco de dados. Siga os passos abaixo:

Pré-requisitos
Python 3.10 ou superior: Download Python

Docker Desktop: Necessário para rodar a instância do Oracle Database.

Biblioteca oracledb: Driver oficial para comunicação com o banco.

IDE Recomendada: VS Code.

Passo 1: Configuração do Banco de Dados (Oracle)
O projeto utiliza o Oracle XE 21c via Docker. No terminal, execute:

Bash
docker run -d --name oracle-db -p 1521:1521 -e ORACLE_PASSWORD=oracle gvenzl/oracle-xe
Aguarde cerca de 2 minutos para a inicialização completa do serviço na primeira execução.

Passo 2: Preparação do Schema
Utilize um cliente SQL (DBeaver, SQL Developer ou a extensão do VS Code).

Conecte-se com: user: SYSTEM, pass: oracle, dsn: localhost:1521/xe.

Execute o script localizado em /schema.sql para criar as tabelas e a carga inicial de máquinas (TRT-001 e TRT-002).

Passo 3: Instalação de Dependências e Execução
No terminal do seu projeto:

Bash
# Instalação do driver
pip install oracledb

# Execução do sistema
python src/main.py
Passo 4: Operação do Sistema
No menu, escolha a opção 1 para registrar uma telemetria.

Utilize IDs válidos como TRT-001.

Após os registros, escolha a opção 2 para exportar o relatório.

Verifique os arquivos gerados em /document/other/.

## 🗃 Histórico de lançamentos

* 1.0.0 - 08/04/2026

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>


