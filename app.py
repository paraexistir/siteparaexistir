from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)



# =========================================================
# CONEXÃO COM O BANCO DE DADOS
# =========================================================

def conectar():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", 3306))
    )


# =========================================================
# PÁGINA INICIAL
# =========================================================

@app.route("/")
def index():
    return render_template("index.html")


# =========================================================
# PRODUTOS
# =========================================================

@app.route("/produtos")
def produtos():
    return render_template("produtos.html")

# =========================================================
# ia
# =========================================================

@app.route("/ia")
def ia():
    return render_template("ia.html")


# =========================================================
# LOGIN
# =========================================================
# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    # ---------------------------------------------------------
    # ACESSO À PÁGINA DE LOGIN
    # ---------------------------------------------------------

    if request.method == "GET":
        return render_template("login.html")


    # ---------------------------------------------------------
    # ENVIO DO FORMULÁRIO
    # ---------------------------------------------------------

    email = request.form.get("email", "").strip()
    senha = request.form.get("senha", "")


    # ---------------------------------------------------------
    # VALIDAÇÃO
    # ---------------------------------------------------------

    if not email or not senha:

        return render_template(
            "login.html",
            erro="Preencha o e-mail e a senha."
        )


    conexao = None
    cursor = None


    try:

        # -----------------------------------------------------
        # CONECTA AO BANCO
        # -----------------------------------------------------

        conexao = conectar()

        cursor = conexao.cursor()


        # -----------------------------------------------------
        # PROCURA O USUÁRIO
        # -----------------------------------------------------

        cursor.execute(
            """
            SELECT id, nome, email, senha
            FROM usuarios
            WHERE email = %s
            """,
            (email,)
        )

        usuario = cursor.fetchone()


        # -----------------------------------------------------
        # VERIFICA USUÁRIO E SENHA
        # -----------------------------------------------------

        if usuario:

            id_usuario = usuario[0]
            nome_usuario = usuario[1]
            email_usuario = usuario[2]
            senha_banco = usuario[3]


            if senha == senha_banco:

                print(
                    "Login realizado:",
                    email_usuario
                )

                return redirect(url_for("index"))


        # -----------------------------------------------------
        # LOGIN INCORRETO
        # -----------------------------------------------------

        return render_template(
            "login.html",
            erro="E-mail ou senha incorretos."
        )


    except mysql.connector.Error as erro:

        print(
            "Erro ao realizar login:",
            erro
        )

        return render_template(
            "login.html",
            erro="Erro ao conectar ao banco de dados."
        )


    finally:

        if cursor:
            cursor.close()

        if conexao:
            conexao.close()

# =========================================================
# CADASTRO
# =========================================================

@app.route("/cadastro", methods=["GET"])
def cadastro():
    return render_template("cadastro.html")


@app.route("/salvar_usuarios", methods=["POST"])
def salvar_usuarios():

    nome = request.form["nome"]
    email = request.form["email"]
    senha = request.form["senha"]

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        INSERT INTO usuarios (nome, email, senha)
        VALUES (%s, %s, %s)
        """,
        (nome, email, senha)
    )

    conexao.commit()

    cursor.close()
    conexao.close()

    return render_template("login.html")


# =========================================================
# CONTATOS
# =========================================================

@app.route("/contatos", methods=["GET"])
def contatos():
    return render_template("index.html")


@app.route("/salvar_contato", methods=["POST"])
def salvar_contato():

    nome = request.form["nome"]
    email = request.form["email"]
    mensagem = request.form.get("mensagem")

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        INSERT INTO contatos (nome, email, mensagem)
        VALUES (%s, %s, %s)
        """,
        (nome, email, mensagem)
    )

    conexao.commit()

    cursor.close()
    conexao.close()

    return redirect("/")


# =========================================================
# EQUIPE
# =========================================================

@app.route("/equipe")
def equipe():
    return render_template("equipe.html")


# =========================================================
# POLÍTICA DE PRIVACIDADE
# =========================================================

@app.route("/politica-privacidade")
def politica_privacidade():
    return render_template("politica-privacidade.html")


# =========================================================
# TERMOS E CONDIÇÕES
# =========================================================

@app.route("/termos-condicoes")
def termos_condicoes():
    return render_template("termos-condicoes.html")


# =========================================================
# EXECUTAR SERVIDOR
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)