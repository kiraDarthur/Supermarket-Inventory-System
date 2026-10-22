import tkinter as tk
from tkinter import messagebox, ttk
import re
from conexao import conectar
from auth import validar_login, cadastrar_usuario
from movimentacoes import registrar_movimentacao, consultar_estoque


def abrir_janela_principal(usuario_logado, janela_login):
    janela_login.withdraw()

    app = tk.Toplevel()
    app.title("Sistema de Gestão de Supermercado")
    app.geometry("650x550")

    tk.Label(app, text=f"Olá, {usuario_logado}! Bem-vindo ao sistema.", font=("Arial", 14, "bold")).pack(pady=10)

    def ver_produtos():
        janela_produtos = tk.Toplevel(app)
        janela_produtos.title("Catálogo de Produtos")
        janela_produtos.geometry("450x400")

        frame_tabela = tk.Frame(janela_produtos)
        frame_tabela.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        colunas = ("ID", "Nome", "Preço")
        tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nome", text="Nome")
        tree.heading("Preço", text="Preço (€)")
        tree.column("ID", width=50)
        tree.column("Nome", width=230)
        tree.column("Preço", width=100)

        scrollbar = ttk.Scrollbar(frame_tabela, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome, preco FROM produtos")
        for linha in cursor.fetchall():
            linha_formatada = (linha[0], linha[1], f"{linha[2]:.2f} €")
            tree.insert("", tk.END, values=linha_formatada)
        cursor.close()
        conexao.close()

    def acao_movimentacao(tipo):
        entrada_id = entry_pid.get().strip()
        entrada_nome = entry_pnome.get().strip()
        qtd_texto = entry_qtd.get().strip()

        try:
            qtd = int(qtd_texto)
        except ValueError:
            messagebox.showerror("Erro", "Insira uma quantidade numérica válida.")
            return

        conexao = conectar()
        cursor = conexao.cursor()
        ids_para_processar = []

        if entrada_id:
            for i in entrada_id.split(","):
                try:
                    ids_para_processar.append(int(i.strip()))
                except ValueError:
                    pass
        elif entrada_nome:
            for n in entrada_nome.split(","):
                sql = "SELECT id FROM produtos WHERE nome LIKE %s"
                cursor.execute(sql, ('%' + n.strip() + '%',))
                for r in cursor.fetchall():
                    ids_para_processar.append(r[0])
        else:
            messagebox.showwarning("Aviso", "Preencha o ID ou o Nome do produto.")
            cursor.close()
            conexao.close()
            return

        if not ids_para_processar:
            messagebox.showerror("Erro", "Nenhum produto encontrado com os dados fornecidos.")
            cursor.close()
            conexao.close()
            return

        for p_id in ids_para_processar:
            registrar_movimentacao(p_id, tipo, qtd)

        cursor.close()
        conexao.close()
        messagebox.showinfo("Sucesso", f"Movimentação de {tipo} aplicada com sucesso!")
        entry_pid.delete(0, tk.END)
        entry_pnome.delete(0, tk.END)
        entry_qtd.delete(0, tk.END)

    def consultar():
        entrada_id = entry_pid.get().strip()
        entrada_nome = entry_pnome.get().strip()

        conexao = conectar()
        cursor = conexao.cursor()
        produtos_encontrados = []

        if entrada_id:
            for i in entrada_id.split(","):
                try:
                    p_id = int(i.strip())
                    cursor.execute("SELECT id, nome FROM produtos WHERE id = %s", (p_id,))
                    res = cursor.fetchone()
                    if res:
                        produtos_encontrados.append(res)
                except ValueError:
                    pass
        elif entrada_nome:
            for n in entrada_nome.split(","):
                cursor.execute("SELECT id, nome FROM produtos WHERE nome LIKE %s", ('%' + n.strip() + '%',))
                for r in cursor.fetchall():
                    if r not in produtos_encontrados:
                        produtos_encontrados.append(r)
        else:
            messagebox.showwarning("Aviso", "Preencha o ID ou o Nome do produto para consultar.")
            cursor.close()
            conexao.close()
            return

        cursor.close()
        conexao.close()

        if not produtos_encontrados:
            lbl_resultado.config(text="Nenhum produto encontrado.")
            return

        detalhes = ""
        for p_id, p_nome in produtos_encontrados:
            saldo = consultar_estoque(p_id)
            detalhes += f"ID: {p_id} | {p_nome} -> Stock: {saldo} un.\n"

        lbl_resultado.config(text=detalhes)

    tk.Button(app, text="Ver Lista de Produtos", width=30, bg="lightblue", command=ver_produtos).pack(pady=5)

    frame_mov = tk.LabelFrame(app, text="Controlo de Stock (Múltiplos separados por vírgula)",
                              font=("Arial", 10, "bold"))
    frame_mov.pack(fill="both", expand="yes", padx=20, pady=10)

    tk.Label(frame_mov, text="ID(s) do Produto (ex: 1, 2, 3):").pack(anchor="w", padx=10)
    global entry_pid
    entry_pid = tk.Entry(frame_mov, width=40)
    entry_pid.pack(anchor="w", padx=10, pady=2)

    tk.Label(frame_mov, text="Ou Nome(s) do Produto (ex: cafe, maca):").pack(anchor="w", padx=10)
    global entry_pnome
    entry_pnome = tk.Entry(frame_mov, width=40)
    entry_pnome.pack(anchor="w", padx=10, pady=2)

    tk.Label(frame_mov, text="Quantidade:").pack(anchor="w", padx=10)
    global entry_qtd
    entry_qtd = tk.Entry(frame_mov, width=20)
    entry_qtd.pack(anchor="w", padx=10, pady=2)

    btn_frame = tk.Frame(frame_mov)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Registar Entrada", bg="lightgreen", command=lambda: acao_movimentacao("ENTRADA")).pack(
        side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Registar Saída", bg="salmon", command=lambda: acao_movimentacao("SAIDA")).pack(
        side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Consultar Stock", bg="lightyellow", command=consultar).pack(side=tk.LEFT, padx=5)

    global lbl_resultado
    lbl_resultado = tk.Label(frame_mov, text="", font=("Arial", 9, "bold"), fg="blue", justify=tk.LEFT)
    lbl_resultado.pack(pady=5)

    def logout():
        app.destroy()
        janela_login.deiconify()

    tk.Button(app, text="Trocar de Utilizador (Logout)", width=30, bg="orange", command=logout).pack(pady=10)
    app.protocol("WM_DELETE_WINDOW", janela_login.destroy)


def iniciar_sistema():
    janela_login = tk.Tk()
    janela_login.title("Login - Supermercado")
    janela_login.geometry("350x260")

    tk.Label(janela_login, text="SISTEMA DE SUPERMERCADO", font=("Arial", 11, "bold")).pack(pady=15)

    tk.Label(janela_login, text="Utilizador:").pack()
    entry_user = tk.Entry(janela_login, width=25)
    entry_user.pack(pady=5)

    tk.Label(janela_login, text="Senha:").pack()
    entry_pass = tk.Entry(janela_login, width=25, show="*")
    entry_pass.pack(pady=5)

    def fazer_login():
        u = entry_user.get()
        s = entry_pass.get()
        if validar_login(u, s):
            abrir_janela_principal(u, janela_login)
        else:
            messagebox.showerror("Erro", "Utilizador ou senha incorretos.")

    def abrir_janela_cadastro():
        janela_cad = tk.Toplevel(janela_login)
        janela_cad.title("Criar Nova Conta")
        janela_cad.geometry("300x280")

        tk.Label(janela_cad, text="Registo de Novo Utilizador", font=("Arial", 10, "bold")).pack(pady=10)

        tk.Label(janela_cad, text="Utilizador:").pack()
        e_user = tk.Entry(janela_cad, width=25)
        e_user.pack(pady=2)

        tk.Label(janela_cad, text="E-mail:").pack()
        e_email = tk.Entry(janela_cad, width=25)
        e_email.pack(pady=2)

        tk.Label(janela_cad, text="Senha:").pack()
        e_pass = tk.Entry(janela_cad, width=25, show="*")
        e_pass.pack(pady=2)

        def salvar_cadastro():
            u = e_user.get().strip()
            email = e_email.get().strip()
            s = e_pass.get().strip()

            padrao_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'

            if not u or not email or not s:
                messagebox.showwarning("Aviso", "Preencha todos os campos!")
            elif not re.match(padrao_email, email):
                messagebox.showerror("Erro", "E-mail inválido! Deve conter '@' e um domínio válido.")
            else:
                cadastrar_usuario(u, email, s)
                messagebox.showinfo("Sucesso", f"Conta para '{u}' criada com sucesso!")
                janela_cad.destroy()

        tk.Button(janela_cad, text="Registar", bg="lightgreen", width=15, command=salvar_cadastro).pack(pady=15)

    botoes_frame = tk.Frame(janela_login)
    botoes_frame.pack(pady=15)

    tk.Button(botoes_frame, text="Entrar", width=10, bg="lightgreen", command=fazer_login).pack(side=tk.LEFT, padx=5)
    tk.Button(botoes_frame, text="Criar Conta", width=12, bg="lightblue", command=abrir_janela_cadastro).pack(
        side=tk.LEFT, padx=5)

    janela_login.mainloop()