from flask import Flask, jsonify
import random

app = Flask(__name__)

charadas = [
    {'id': 1, 'pergunta': 'O que é, o que é? Quanto mais rugas têm mais novo é.', 'resposta': 'O pneu.' },
    {'id': 2, 'pergunta': 'O que é, o que é? Feito para andar e não anda.', 'resposta': 'A rua.' },
    {'id': 3, 'pergunta': 'O que é, o que é? Dá muitas voltas e não sai do lugar.', 'resposta': 'O relógio.' },
    {'id': 4, 'pergunta': 'O que é, o que é? Uma impressora disse para a outra.', 'resposta': 'Essa folha é tua ou é impressão minha?' },
    {'id': 5, 'pergunta': 'O que é, o que é? O 4 disse para o 40.', 'resposta': 'Passa a bola.' },
    {'id': 6, 'pergunta': 'O que é, o que é? A esfera disse para o cubo.', 'resposta': 'Deixa de ser quadrado.' },
    {'id': 7, 'pergunta': ' O que é, o que é? O nadador faz para bater o recorde.', 'resposta': 'Nada' },
    {'id': 8, 'pergunta': 'Qual a diferença entre o padre e o bule?', 'resposta': 'O padre é de muita fé, e o bule é de por café.' },
    {'id': 9, 'pergunta': 'O que é, o que é? Todo mês tem, menos abril.', 'resposta': ' A letra O.' },
    {'id': 10, 'pergunta': 'Por que Thor foi preso?', 'resposta': 'Porque ele tinha enTHORpecente.' },
    {'id': 11, 'pergunta': 'Qual o contrário de diabetes?', 'resposta': 'Noitebetes.' }
]

@app.route('/', methods=['GET'])
def index():
    return 'CHARADA API ESTÁ ON!! RIA!'

@app.route('/charadas', methods=['GET'])
def charada():
    charada = random.choice(charadas)
    return charada

@app.route('/charadas/<campo>/<busca>', methods=['GET'])
def busca(campo, busca):
    if campo not in ['id', 'pergunta', 'resposta']:
        return jsonify({'mensagem': 'ERRO - Campo não encontrado.'}), 404

    if campo == 'id':
        busca = int(busca)

    for charada in charadas:
        if charada[campo] == busca:
            return jsonify(charada), 200
    else: 
        return jsonify({'mensagem': 'ERRO! Usuário não encontrado.'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
