# API de Backup Automatizado para AWS S3

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/Amazon_S3-569A31?style=for-the-badge&logo=amazons3&logoColor=white" alt="AWS S3">
  <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" alt="Git">
</p>

Esta API foi desenvolvida em Flask com o objetivo de atuar como um microsserviço intermediário seguro para automação de rotinas de backup. Em vez de expor chaves de acesso diretamente em aplicações clientes (frontend, scripts locais ou rotinas expostas), a API centraliza e protege a lógica de upload para o Amazon S3 utilizando chaves de acesso isoladas em variáveis de ambiente e o SDK oficial boto3.

---

## 📌 Arquitetura e Fluxo dos Dados

O fluxo abaixo ilustra como a aplicação intermedia a requisição de maneira isolada e segura:

[ Cliente / Sistema Local ]
           │
           ▼ (Envia arquivo via POST Multipart/Form-Data)
┌────────────────────────────────────────────────────────┐
│                      API FLASK                         │
│                                                        │
│  1. Recebe a requisição HTTP localmente                │
│  2. Valida se o payload contém o campo 'file'          │
│  3. Lê as credenciais protegidas via Python-Dotenv     │
│  4. Inicializa o cliente seguro do Boto3               │
└────────────────────────────────────────────────────────┘
           │
           ▼ (Upload via Stream Seguro / Sem expor chaves)
[ Amazon Web Services (AWS S3 Bucket) ]

---

## 🛠️ Tecnologias e Dependências

As seguintes ferramentas foram utilizadas para a construção do microsserviço:

* Python 3 — Linguagem base para construção do script.
* Flask — Framework micro-web focado em performance, simplicidade e rotas enxutas.
* Boto3 — SDK oficial da AWS para Python, utilizado para comunicação nativa com a API do S3.
* Python-dotenv — Biblioteca utilizada para ler e injetar arquivos .env como variáveis de ambiente locais, mitigando riscos de vazamento de credenciais.

---

## 🛡️ Práticas de Segurança Implementadas

* Camada de Isolamento: O cliente final nunca interage diretamente com a infraestrutura da AWS, eliminando a distribuição indesejada de tokens de acesso.
* Políticas de Ignorados (.gitignore): Configuração estrita do Git para impedir o upload do ambiente virtual (venv/) e, fundamentalmente, do arquivo .env de produção, mantendo chaves de acesso fora do histórico público.
* Exemplificação de Escopo: Disponibilização do .env.example para guiar novos setups sem expor credenciais reais.

---

## ⚙️ Como Configurar e Executar o Projeto

### 1. Clonar e Instalar Dependências
No seu terminal preferido (recomendado Git Bash no Windows), execute o isolamento do ambiente e instale os pacotes:

python -m venv venv
.\venv\Scripts\activate
pip install flask boto3 python-dotenv

### 2. Variáveis de Ambiente
Duplique o arquivo de exemplo e configure o ambiente com suas respectivas chaves geradas no painel do AWS IAM:

cp .env.example .env

Abra o arquivo .env recém-criado e insira suas credenciais:
AWS_ACCESS_KEY_ID=sua_chave_de_acesso_aqui
AWS_SECRET_ACCESS_KEY=seu_segredo_de_acesso_aqui
AWS_BUCKET_NAME=nome_do_seu_bucket_s3

### 3. Inicialização da API
Com o ambiente ativo e configurado, execute o servidor de desenvolvimento:

python app.py

A API iniciará localmente no endereço padrão: http://127.0.0.1:5000

---

## 🧪 Referência dos Endpoints (Documentação da API)

### Realizar Upload de Arquivo

* Rota: /upload
* Método: POST
* Tipo de Conteúdo: multipart/form-data

Parâmetros da Requisição (Body):
- file: Arquivo físico contendo o backup a ser armazenado (Obrigatório)

Respostas Esperadas:

* Sucesso (HTTP 200 - OK):
{
  "status": "success",
  "message": "Backup realizado com sucesso no Amazon S3!",
  "filename": "backup_sistema_2026.zip"
}

* Erro - Requisição Inválida (HTTP 400 - Bad Request):
{
  "status": "error",
  "message": "Nenhum arquivo foi enviado na requisição."
}

* Erro - Falha na Comunicação AWS (HTTP 500 - Internal Server Error):
{
  "status": "error",
  "message": "Falha interna ao conectar ou enviar o arquivo para o serviço AWS S3."
}

Exemplo de Teste Prático usando cURL:
curl -X POST -F "file=@caminho/do/seu/arquivo.txt" http://127.0.0.1:5000/upload
