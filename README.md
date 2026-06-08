# API de Backup Automatizado para AWS S3

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/Amazon_S3-569A31?style=for-the-badge&logo=amazons3&logoColor=white" alt="AWS S3">
  <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" alt="Git">
</p>

Esta API foi desenvolvida em Flask com o objetivo de atuar como um microsserviço intermediário para a automação de rotinas de backup. A aplicação centraliza e protege a lógica de upload para o Amazon S3, utilizando o SDK oficial `boto3` e isolando as chaves de acesso em variáveis de ambiente, o que evita a exposição de credenciais em aplicações clientes ou scripts locais.

---

## 📌 Arquitetura e Fluxo dos Dados

O fluxo abaixo ilustra o mapeamento da requisição e a integração entre os componentes:

```text
[ Cliente / Sistema Local ]
           │
           ▼ (Requisição HTTP POST - Multipart/Form-Data)
┌────────────────────────────────────────────────────────┐
│                      API FLASK                         │
│                                                        │
│  1. Recebimento do arquivo digital localmente          │
│  2. Validação de presença do campo 'file' no payload   │
│  3. Leitura das credenciais via Python-Dotenv          │
│  4. Inicialização do cliente seguro Boto3              │
└────────────────────────────────────────────────────────┘
           │
           ▼ (Upload via Stream / Transmissão Segura)
[ Amazon Web Services (AWS S3 Bucket) ]
```

## 🛠️ Tecnologias e Dependências

* **Python 3** — Ambiente de execução e linguagem base da aplicação.
* **Flask** — Micro-framework web utilizado para a estruturação das rotas e processamento de requisições.
* **Boto3** — SDK oficial da AWS para Python, responsável pela comunicação nativa com o serviço S3.
* **Python-dotenv** — Biblioteca para carregamento de variáveis de ambiente a partir de arquivos `.env`.

---

## 🛡️ Práticas de Segurança Implementadas

* Camada de Isolamento: O cliente final nunca interage diretamente com a infraestrutura da AWS, eliminando a distribuição indesejada de tokens de acesso.
* Políticas de Ignorados (.gitignore): Configuração estrita do Git para impedir o upload do ambiente virtual (venv/) e, fundamentalmente, do arquivo .env de produção, mantendo chaves de acesso fora do histórico público.
* Exemplificação de Escopo: Disponibilização do .env.example para guiar novos setups sem expor credenciais reais.
  
---

## ⚙️ Configuração e Execução do Ambiente

### 1. Instalação de Dependências
Em um terminal (como o Git Bash), execute os comandos abaixo para configurar o ambiente virtual e instalar os pacotes necessários:

python -m venv venv
.\venv\Scripts\activate
pip install flask boto3 python-dotenv

### 2. Variáveis de Ambiente
Crie uma cópia do arquivo de exemplo para configurar as credenciais locais:

cp .env.example .env

Abra o arquivo `.env` gerado e preencha com os dados correspondentes obtidos no console AWS IAM:

AWS_ACCESS_KEY_ID=sua_chave_de_acesso_aqui
AWS_SECRET_ACCESS_KEY=seu_segredo_de_acesso_aqui
AWS_BUCKET_NAME=nome_do_seu_bucket_s3

### 3. Execução da Aplicação
Para iniciar o servidor de desenvolvimento local, execute:

python app.py

A API estará disponível para receber requisições no endereço: http://127.0.0.1:5000

---

## 🧪 Referência dos Endpoints

### Envio de Arquivo para o S3

* **Rota:** `/upload`
* **Método:** `POST`
* **Content-Type:** `multipart/form-data`

#### Parâmetros do Corpo da Requisição (Body):
- `file`: Arquivo binário correspondente ao backup a ser armazenado (Obrigatório).

#### Respostas do Servidor:

* **Sucesso (HTTP 200 - OK):**
{
  "status": "success",
  "message": "Backup realizado com sucesso no Amazon S3!",
  "filename": "backup_sistema_2026.zip"
}

* **Erro - Payload Inválido (HTTP 400 - Bad Request):**
{
  "status": "error",
  "message": "Nenhum arquivo foi enviado na requisição."
}

* **Erro - Falha na Comunicação AWS (HTTP 500 - Internal Server Error):**
{
  "status": "error",
  "message": "Falha interna ao conectar ou enviar o arquivo para o serviço AWS S3."
}

#### Exemplo de Validação via cURL:
curl -X POST -F "file=@caminho/do/seu/arquivo.txt" http://127.0.0.1:5000/upload
