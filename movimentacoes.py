import mysql.connector
from conexao import conectar

def registrar_movimentacao(produto_id, tipo, quantidade):
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        sql = "INSERT INTO movimentacoes (produto_id, tipo, quantidade) VALUES (%s, %s, %s)"
        cursor.execute(sql, (produto_id, tipo.upper(), quantidade))

        conexao.commit()
        print(f"Movimentação de {tipo} ({quantidade} unidades) registada com sucesso!")

    except mysql.connector.Error as erro:
        print(f"Erro ao registar movimentação: {erro}")

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conexao' in locals() and conexao.is_connected():
            conexao.close()

def consultar_estoque(produto_id):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        SELECT 
            COALESCE(SUM(CASE WHEN tipo = 'ENTRADA' THEN quantidade ELSE 0 END), 0) - 
            COALESCE(SUM(CASE WHEN tipo = 'SAIDA' THEN quantidade ELSE 0 END), 0) AS estoque_atual
        FROM movimentacoes 
        WHERE produto_id = %s
    """
    cursor.execute(sql, (produto_id,))
    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    return resultado[0] if resultado else 0