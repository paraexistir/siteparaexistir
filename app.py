from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from jinja2 import TemplateNotFound
import json
import os

app = Flask(__name__)
app.secret_key = "para-existir-chave-secreta-2026"  # troque por algo seguro


# =========================================================
# ARQUIVOS DE DADOS (JSON simples)
# =========================================================

ARQUIVO_USUARIOS = "usuarios.json"
ARQUIVO_CONTATOS = "contatos.json"


def carregar_json(caminho):
    """Carrega um arquivo JSON ou retorna lista vazia."""
    if not os.path.exists(caminho):
        return []
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def salvar_json(caminho, dados):
    """Salva dados em um arquivo JSON."""
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


# =========================================================
# ROTAS PRINCIPAIS
# =========================================================

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/produtos")
def produtos():
    return render_template("produtos.html")


@app.route("/equipe")
def equipe():
    return render_template("equipe.html")


@app.route("/ia")
def ia():
    return render_template("ia.html")


# =========================================================
# ROTAS DINÂMICAS — PRODUTOS E CATEGORIAS
# =========================================================

@app.route("/produtos/<nome_produto>")
def produto_detalhe(nome_produto):
    """
    Serve qualquer página de produto em templates/produtos/.
    Ex: /produtos/popit-circular  →  templates/produtos/popit-circular.html
    """
    try:
        return render_template(f"produtos/{nome_produto}.html")
    except TemplateNotFound:
        return render_template("404.html"), 404


@app.route("/categorias/<nome_categoria>")
def categoria_detalhe(nome_categoria):
    """
    Serve qualquer página de categoria em templates/categorias/.
    Ex: /categorias/estimulo-tatil  →  templates/categorias/estimulo-tatil.html
    """
    try:
        return render_template(f"categorias/{nome_categoria}.html")
    except TemplateNotFound:
        return render_template("404.html"), 404


# =========================================================
# ROTAS DE AUTENTICAÇÃO
# =========================================================

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":

        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        confirmar = request.form.get("confirmar", "")

        if not nome or not email or not senha:
            flash("Preencha todos os campos.", "erro")
            return redirect(url_for("cadastro"))

        if len(senha) < 6:
            flash("A senha deve ter no mínimo 6 caracteres.", "erro")
            return redirect(url_for("cadastro"))

        if confirmar and senha != confirmar:
            flash("As senhas não coincidem.", "erro")
            return redirect(url_for("cadastro"))

        usuarios = carregar_json(ARQUIVO_USUARIOS)

        if any(u.get("email") == email for u in usuarios):
            flash("Este e-mail já está cadastrado.", "erro")
            return redirect(url_for("cadastro"))

        usuarios.append({
            "nome": nome,
            "email": email,
            "senha": generate_password_hash(senha)
        })

        salvar_json(ARQUIVO_USUARIOS, usuarios)

        flash("Cadastro realizado com sucesso! Faça login.", "sucesso")
        return redirect(url_for("login"))

    return render_template("cadastro.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        lembrar = request.form.get("lembrar")

        if not email or not senha:
            flash("Preencha e-mail e senha.", "erro")
            return redirect(url_for("login"))

        usuarios = carregar_json(ARQUIVO_USUARIOS)

        usuario = next(
            (u for u in usuarios if u.get("email") == email),
            None
        )

        if usuario and check_password_hash(usuario.get("senha", ""), senha):

            session["usuario_nome"] = usuario["nome"]
            session["usuario_email"] = usuario["email"]

            if lembrar:
                session.permanent = True

            flash(f"Bem-vindo(a), {usuario['nome']}!", "sucesso")
            return redirect(url_for("index"))

        else:
            flash("E-mail ou senha incorretos.", "erro")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Você saiu da sua conta.", "sucesso")
    return redirect(url_for("index"))


# =========================================================
# ROTA DE CONTATO
# =========================================================

@app.route("/salvar_contato", methods=["POST"])
def salvar_contato():

    nome = request.form.get("nome", "").strip()
    email = request.form.get("email", "").strip()
    mensagem = request.form.get("mensagem", "").strip()

    if not nome or not email or not mensagem:
        flash("Preencha todos os campos do formulário.", "erro")
        return redirect(url_for("index") + "#contato")

    contatos = carregar_json(ARQUIVO_CONTATOS)

    contatos.append({
        "nome": nome,
        "email": email,
        "mensagem": mensagem
    })

    salvar_json(ARQUIVO_CONTATOS, contatos)

    flash("Mensagem enviada com sucesso!", "sucesso")
    return redirect(url_for("index") + "#contato")


# =========================================================
# ROTAS DE POLÍTICAS
# =========================================================

@app.route("/politica-privacidade")
def politica_privacidade():
    return render_template("politica_privacidade.html")


@app.route("/termos-condicoes")
def termos_condicoes():
    return render_template("termos_condicoes.html")


# =========================================================
# ERRO 404 PERSONALIZADO
# =========================================================

@app.errorhandler(404)
def pagina_nao_encontrada(erro):
    return render_template("404.html"), 404


# =========================================================
# INICIALIZAÇÃO
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)