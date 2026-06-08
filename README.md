# API de Backup Automatizado para AWS S3

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![Flask](https://img.shields.io/badge/Flask-latest-lightgrey) ![Amazon S3](https://img.shields.io/badge/Amazon%20S3-orange) ![Git](https://img.shields.io/badge/Git-red)

Esta API foi desenvolvida em Flask com o objetivo de atuar como um microsserviço intermediário para a automação de rotinas de backup. A aplicação centraliza e protege a lógica de upload para o Amazon S3, utilizando o SDK oficial `boto3` e isolando as chaves de acesso em variáveis de ambiente, o que evita a exposição de credenciais em aplicações clientes ou scripts locais.

---

## 🚀 Arquitetura e Fluxo dos Dados

O fluxo abaixo ilustra o mapeamento da requisição e a integração entre os componentes:

```
[ Cliente / Sistema Local ]
          |
          ▼ (Requisição HTTP POST - Multipart/Form-Data)
┌─────────────────────────────────────────┐
│               API FLASK                 │
│                                         │
│  1. Recebimento do arquivo digitalmente │
│  2. Validação do campo 'file' no payload│
│  3. Leitura das credenciais via Dotenv  │
│  4. Inicialização do cliente Boto3      │
└─────────────────────────────────────────┘
          |
          ▼ (Upload via Stream / Transmissão Segura)
[ Amazon Web Services (AWS S3 Bucket) ]
```

---

## ⚙️ Tecnologias e Dependências

- **Python 3** — Ambiente de execução e linguagem base da aplicação.
- **Flask** — Micro-framework web utilizado para a estruturação das rotas e processamento de requisições.
- **Boto3** — SDK oficial da AWS para Python, responsável pela comunicação nativa com o serviço S3.
- **Python-dotenv** — Biblioteca para carregamento de variáveis de ambiente a partir de arquivos `.env`.

---

## 🛡️ Práticas de Segurança Implementadas

- **Camada de Isolamento:** O cliente final nunca interage diretamente com a infraestrutura da AWS, eliminando a distribuição indesejada de tokens de acesso.
- **Políticas de Ignorados (.gitignore):** Configuração estrita do Git para impedir o upload do ambiente virtual (`venv/`) e, fundamentalmente, do arquivo `.env` de produção, mantendo as chaves de acesso fora do histórico público.
- **Exemplificação de Escopo:** Disponibilização do `.env.example` para guiar novos setups sem expor credenciais reais.

---

## ✅ Pré-requisitos

Antes de começar, certifique-se de ter instalado em sua máquina:

- [Python 3.10+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- Uma conta na [AWS](https://aws.amazon.com/) com um bucket S3 criado e as credenciais de acesso (Access Key e Secret Key) geradas via IAM.

---

## ⚙️ Configuração e Execução do Ambiente

### 0. Clonar o Repositório

```bash
git clone https://github.com/tarciofernandes14/api-backup-s3.git
cd api-backup-s3
```

### 1. Instalação de Dependências

Em um terminal (como o Git Bash), execute os comandos abaixo para configurar o ambiente virtual e instalar os pacotes necessários:

```bash
python -m venv venv
.\venv\Scripts\activate
pip install flask boto3 python-dotenv
```

### 2. Variáveis de Ambiente

Crie uma cópia do arquivo de exemplo para configurar as credenciais locais:

```bash
cp .env.example .env
```

Abra o arquivo `.env` gerado e preencha com os dados correspondentes obtidos no console AWS IAM:

```env
AWS_ACCESS_KEY_ID=sua_chave_de_acesso_aqui
AWS_SECRET_ACCESS_KEY=seu_segredo_de_acesso_aqui
AWS_BUCKET_NAME=nome_do_seu_bucket_s3
```

### 3. Execução da Aplicação

Para iniciar o servidor de desenvolvimento local, execute:

```bash
python app.py
```

A API estará disponível para receber requisições no endereço: `http://127.0.0.1:5000`

---

## 📌 Referência dos Endpoints

### Envio de Arquivo para o S3

- **Rota:** `/upload`
- **Método:** `POST`
- **Content-Type:** `multipart/form-data`

**Parâmetros do Corpo da Requisição (Body):**

- `file`: Arquivo binário correspondente ao backup a ser armazenado. **(Obrigatório)**

**Respostas do Servidor:**

- **Sucesso (HTTP 200 - OK):**
  ```json
  { "status": "success", "message": "Backup realizado com sucesso no Amazon S3!", "filename": "backup_sistema_2026.zip" }
  ```

- **Erro - Payload Inválido (HTTP 400 - Bad Request):**
  ```json
  { "status": "error", "message": "Nenhum arquivo foi enviado na requisição." }
  ```

- **Erro - Falha na Comunicação AWS (HTTP 500 - Internal Server Error):**
  ```json
  { "status": "error", "message": "Falha interna ao conectar ou enviar o arquivo para o serviço AWS S3." }
  ```

**Exemplo de Validação via cURL:**

```bash
curl -X POST -F "file=@/caminho/do/seu/arquivo.txt" http://127.0.0.1:5000/upload
```
