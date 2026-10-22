import tkinter as tk
from tkinter import messagebox, ttk
import re
from auth import validar_login, cadastrar_usuario
from dashboard_interface import abrir_janela_principal


def iniciar_sistema():
    global janela_login, entry_user, entry_pass

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