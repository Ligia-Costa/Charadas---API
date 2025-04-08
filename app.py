from flask import Flask, jsonify, request
import random
import firebase_admin
from firebase_admin import credentials, firestore
from flask_cors import CORS
import os
import json
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

load_dotenv()

FBKEY = json.loads(os.getenv('CONFIG_FIREBASE')) #pega a variável de ambiente e converte todas as informações no formato JSON

cred = credentials.Certificate(FBKEY)
firebase_admin.initialize_app(cred)

#Conectando com o Firestore da Firebase
db = firestore.client()

#Rota principal de teste
@app.route('/', methods=['GET'])
def index():
    return 'CHARADA API ESTÁ ON!! RIA!'

#Método GET -- Charada aleatória
@app.route('/charadas', methods=['GET'])
def charada_aleatoria():
    charadas = []
    lista = db.collection('charadas').stream()
    for item in lista:
        charadas.append(item.to_dict())

    if charadas:
        return jsonify(random.choice(charadas)), 200
    else:
        return jsonify({'mensagem': 'ERRO! Nenhuma charada encontrada.'}), 404
    
#Método GET -- Listar charadas
@app.route('/charadas/lista', methods=['GET'])
def charada_lista():
    charadas = []
    lista = db.collection('charadas').stream()
    
    for item in lista:
        charadas.append(item.to_dict())

    if charadas:
        return jsonify(charadas), 200
    else:
        return jsonify({'mensagem': 'ERRO! Nenhuma charada encontrada.'}), 404

#Método GET -- Charada por ID
@app.route('/charadas/<id>', methods=['GET'])
def busca(id):
    doc_ref = db.collection('charadas').document(id) #encontra o endereço do documento que vai se utilizar
    doc = doc_ref.get().to_dict() #pega e abre o documento

    if doc:
        return jsonify(doc), 200
    else:
        return jsonify({'mensagem': 'ERRO! Charada não encontrada.'}), 404
    
#Método POST -- Adicionar charada
@app.route('/charadas/', methods=['POST'])
def adicionar_charada():
    dados = request.json

    if "pergunta" not in dados or "resposta" not in dados:
        return jsonify({'mensagem': 'ERRO! Campos Perguntas e Respostas são obrigatórios.'}), 400
    
    #Contador
    contador_ref = db.collection('controle_id').document('contador')
    contador_doc = contador_ref.get().to_dict()
    ultimo_id = contador_doc.get('id')
    novo_id = int(ultimo_id) + 1
    contador_ref.update({'id': novo_id}) #atualização da correção

    db.collection('charadas').document(str(novo_id)).set({
        "id": novo_id,
        "pergunta": dados['pergunta'],
        "resposta": dados['resposta']
    }) #set == gravar

    return jsonify({'mensagem': 'Charada cadastrada com sucesso!'}), 201

#Método PUT -- Alterar charada
@app.route('/charadas/<id>', methods=['PUT'])
def alterar_charada(id):
    dados = request.json

    if "pergunta" not in dados or "resposta" not in dados:
        return jsonify({'mensagem': 'ERRO! Campos Perguntas e Respostas são obrigatórios.'}), 400
    
    doc_ref = db.collection('charadas').document(id)
    doc = doc_ref.get()

    if doc.exists:
        doc_ref.update({
        "pergunta": dados['pergunta'],
        "resposta": dados['resposta']
        })
        return jsonify({'mensagem': 'Charada atualizada com sucesso!'}), 201
    else:
        return jsonify({'mensagem': 'ERRO! Charada não encontrada.'}), 404

#Método DELETE -- Apagar charada
@app.route('/charadas/<id>', methods=['DELETE'])
def excluir_charada(id):
    doc_ref = db.collection('charadas').document(id)
    doc = doc_ref.get()

    if doc.exists:
        return jsonify({'mensagem': 'ERRO! Charada não encontrada.'}), 404
    
    doc_ref.delete()
    return jsonify({'mensagem': 'Charada excluída com sucesso!'}), 200


if __name__ == '__main__':
    app.run(debug=True)