# API de Backup Automatizado para AWS S3

Esta API em Flask foi desenvolvida para intermediar o upload de arquivos de backup para o Amazon S3 de forma segura e automatizada.

Em vez de expor credenciais da AWS no cliente ou fazer uploads manuais pelo console da Amazon, a API funciona como um microsserviço de backend que recebe o arquivo via requisição HTTP, valida o payload e realiza o upload usando chaves de acesso protegidas em variáveis de ambiente.

## Tecnologias Utilizadas
* Python 3
* Flask (Framework Web)
* Boto3 (SDK oficial da AWS para Python)
* Python-dotenv (Gerenciamento de variáveis de ambiente)

## Como Configurar e Rodar

### 1. Instalação das Dependências
Clone o repositório, ative o ambiente virtual e instale os pacotes necessários:

```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente (Windows)
.\venv\Scripts\activate

# Instalar os pacotes
pip install flask boto3 python-dotenv

### 2. Configuração do Ambiente
O projeto utiliza variáveis de ambiente para não expor credenciais sensíveis. Para configurar:

1. Duplique o arquivo `.env.example` e renomeie a cópia para `.env`.
2. Abra o arquivo `.env` e preencha as variáveis `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` e `AWS_BUCKET_NAME` com as credenciais da própria conta AWS.

### 3. Execução da API
Para iniciar o servidor Flask localmente, execute:

```bash
python app.py

### 4. Como Testar
Para testar o endpoint de upload, envie um arquivo via requisição `POST` para a rota `/upload`. Exemplo utilizando `curl`:

```bash
curl -X POST -F "file=@caminho/do/arquivo.txt" [http://127.0.0.1:5000/upload](http://127.0.0.1:5000/upload)