from flask import Flask, request, redirect, url_for, send_from_directory, session
import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


def conectar_banco():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        ssl_disabled=False
    )


@app.route("/")
def inicio():
    return send_from_directory(".", "index.html")


@app.route("/index.html")
def pagina_index():
    return send_from_directory(".", "index.html")


@app.route("/historia.html")
def pagina_historia():
    return send_from_directory(".", "historia.html")


@app.route("/impactos.html")
def pagina_impactos():
    return send_from_directory(".", "impactos.html")


@app.route("/referencias.html")
def pagina_referencias():
    return send_from_directory(".", "referencias.html")


@app.route("/sistema.html")
def pagina_sistema():
    return send_from_directory(".", "sistema.html")


@app.route("/css/<path:arquivo>")
def css(arquivo):
    return send_from_directory(
        "css",
        arquivo,
        max_age=3600
    )


@app.route("/img/<path:arquivo>")
def img(arquivo):
    return send_from_directory(
        "img",
        arquivo,
        max_age=3600
    )


@app.route("/diagramas/<path:arquivo>")
def diagramas(arquivo):
    return send_from_directory(
        "diagramas",
        arquivo,
        max_age=3600
    )


@app.route("/login.html")
def login_html():
    return redirect(url_for("pagina_login"))


@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    senha = request.form["senha"]

    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    comando = "SELECT * FROM usuarios WHERE email = %s AND senha = %s"
    cursor.execute(comando, (email, senha))
    usuario = cursor.fetchone()

    cursor.close()
    conexao.close()

    if usuario:
        session["usuario"] = usuario["nome"]
        return redirect(url_for("admin"))

    return redirect("/login?erro=1")


@app.route("/admin")
def admin():
    if "usuario" not in session:
        return redirect(url_for("pagina_login"))

    return send_from_directory(".", "admin.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("pagina_login"))


if __name__ == "__main__":
    app.run(debug=False)
