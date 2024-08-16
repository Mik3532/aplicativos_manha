from flask import Flask, render_template, redirect, request
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from aluno import Aluno

app = Flask(__name__)

import urllib.parse

# Configuração da conexão com o banco de dados
user = 'root'
password = urllib.parse.quote_plus('senai@123')
host = 'localhost'
database = 'projetodiario1'
connection_string = f'mysql+pymysql://{user}:{password}@{host}/{database}'

# Criar a engine e refletir o banco de dados existente
engine = create_engine(connection_string)
metadata = MetaData()
metadata.reflect(engine)

# Mapeamento automático das tabelas para classes Python
Base = automap_base(metadata=metadata)
Base.prepare()

# Acessando a tabela 'aluno' mapeada
Aluno = Base.classes.aluno

# Criar a sessão do SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
def index():
    return render_template('index.html')
# Define a rota para a página inicial ('/'). Quando essa rota é acessada,
# a função 'index' é chamada e renderiza o template HTML 'index.html'.

@app.route('/novoaluno')
def cadastrar_aluno():
    return render_template('novoaluno.html')
# Define a rota para o caminho '/novoaluno', que renderiza a página 'novoaluno.html'.
# Esta página provavelmente contém o formulário para cadastro de um novo aluno.

@app.route('/logar', methods=["POST"])
def logar_ra():
    ra = request.form["ra"]
    # Quando a rota '/logar' é acessada via método POST, a função 'logar_ra' é chamada.
    # O valor do campo "ra" do formulário enviado é recuperado usando 'request.form'.

    if ra == "12345678":
        return render_template("diariobordo.html", ra=ra)
    # Se o RA enviado pelo formulário for igual a "12345678",
    # a página 'diariobordo.html' é renderizada, passando o valor do RA como contexto.

    else:
        mensagem = "RA INVALIDO."
        return render_template("index.html", mensagem=mensagem)
    # Caso o RA não seja "12345678", uma mensagem de erro "RA INVALIDO." é enviada de volta para a página inicial.

@app.route("/diariobordo")
def diariobordo():
    return render_template("diariobordo.html")
# Define a rota '/diariobordo', que renderiza a página 'diariobordo.html'.
# Esta rota pode ser usada para mostrar o diário de bordo de um aluno logado.

@app.route('/novoaluno', methods=['POST'])
def criar():
    ra = request.form['ra']
    Nome = request.form['Nome']
    tempoestudo = int(request.form['tempoestudo'])
    rendafamiliar = float(request.form['rendafamiliar'])
    # Ao acessar a rota '/criaraluno' via método POST, a função 'criar' é chamada.
    # Ela captura os dados enviados pelo formulário: RA, nome, tempo de estudo e renda familiar.

    aluno = Aluno(ra=ra, Nome=Nome, tempoestudo=tempoestudo, rendafamiliar=rendafamiliar)
    # Cria uma nova instância de um objeto 'Aluno' (a classe 'Aluno' é refletida do banco de dados).
    # Essa instância é preenchida com os dados recebidos do formulário.

    session.add(aluno)
    session.commit()
    # Adiciona o novo aluno ao banco de dados e salva as alterações usando 'session.add' e 'session.commit'.

    mensagem = "Cadastro efetuado com sucesso"
    return render_template('index.html',msgbanco=mensagem)
    # Após o cadastro ser bem-sucedido, a página inicial é exibida.

if __name__ == "__main__":
    app.run(debug=True)
# Verifica se o script está sendo executado diretamente (não importado como módulo).
# Se for o caso, a aplicação Flask é iniciada em modo de depuração ('debug=True'), o que permite ver erros detalhados.
