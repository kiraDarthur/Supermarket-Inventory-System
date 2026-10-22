import mysql.connector
from conexao import conectar


def cadastrar_usuario(usuario, email, senha):
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        sql = "INSERT INTO usuarios (usuario, email, senha) VALUES (%s, %s, %s)"
        cursor.execute(sql, (usuario, email, senha))

        conexao.commit()
        print(f"Sucesso: Utilizador '{usuario}' cadastrado!")

    except mysql.connector.Error as erro:
        print(f"Erro ao cadastrar utilizador: {erro}")

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conexao' in locals() and conexao.is_connected():
            conexao.close()


def validar_login(usuario_informado, senha_informada):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = "SELECT id FROM usuarios WHERE usuario = %s AND senha = %s"
    cursor.execute(sql, (usuario_informado, senha_informada))
    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    if resultado:
        print("Login aprovado! Bem-vindo ao sistema.")
        return True
    else:
        print("Acesso negado: Utilizador ou senha incorretos.")
        return False