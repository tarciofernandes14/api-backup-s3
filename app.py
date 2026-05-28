import os
from flask import Flask, jsonify, request
import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv

#Carrega as vairiáveis do arquivo .env
load_dotenv()

app = Flask(__name__)

#configuar a conexão com a AWS usando o Boto3
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'API de Backup rodando localmente!'}), 200
@app.route('/upload', methods=['POST'])
def upload_to_s3():
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'Arquivo sem nome válido'}), 400

    try:
        s3_client.upload_fileobj(
            file,
            BUCKET_NAME,
            file.filename
        )
        return jsonify({
            'message': 'Backup realizado com sucesso!',
            'filename': file.filename,
            'status': 'uploaded'
        }), 200

    except NoCredentialsError:
        return jsonify({'error': 'Credenciais da AWS não encontradas ou inválidas'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)