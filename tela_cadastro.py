import tkinter as tk
from tkinter import messagebox
import sqlite3
from hashlib import sha256


class TelaCadastro(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Cadastro de Usuário')
        self.geometry("600x500")  
        self.resizable(False, False)
        self.parent = parent
        self.protocol("WM_DELETE_WINDOW", self.fechar_aplicacao)


        
        self.db_connection = self.conectar_ao_bd()

        self.criar_interface()

    def criar_interface(self):
        
        fonte = ("Arial", 14)

        # Labels
        label_nome = tk.Label(self, text="Nome:", font=fonte)
        label_usuario = tk.Label(self, text="Usuário:", font=fonte)
        label_matricula = tk.Label(self, text="Matrícula:", font=fonte)
        label_senha = tk.Label(self, text="Senha:", font=fonte)
        label_confirma_senha = tk.Label(self, text="Confirmar Senha:", font=fonte)
        label_gerente_senha = tk.Label(self, text="Senha do Gerente:", font=fonte)

        # Entradas
        entry_nome = tk.Entry(self, font=fonte)
        entry_usuario = tk.Entry(self, font=fonte)
        entry_matricula = tk.Entry(self, font=fonte)
        entry_senha = tk.Entry(self, show="*", font=fonte)
        entry_confirma_senha = tk.Entry(self, show="*", font=fonte)
        entry_gerente_senha = tk.Entry(self, show="*", font=fonte)

        # Botão de Cadastro
        botao_cadastrar = tk.Button(self, text="Cadastrar", font=fonte, command=lambda: self.realizar_cadastro(
            entry_nome.get(), entry_usuario.get(), entry_matricula.get(), entry_senha.get(), entry_confirma_senha.get(), entry_gerente_senha.get()))

        # Botão de Voltar
        botao_voltar = tk.Button(self, text="Voltar", font=fonte, command=self.voltar)

        # Posicionamento dos elementos na grade
        label_nome.grid(row=1, column=0, padx=20, pady=10)
        entry_nome.grid(row=1, column=1, padx=20, pady=10)
        label_usuario.grid(row=2, column=0, padx=20, pady=10)
        entry_usuario.grid(row=2, column=1, padx=20, pady=10)
        label_matricula.grid(row=3, column=0, padx=20, pady=10)
        entry_matricula.grid(row=3, column=1, padx=20, pady=10)
        label_senha.grid(row=4, column=0, padx=20, pady=10)
        entry_senha.grid(row=4, column=1, padx=20, pady=10)
        label_confirma_senha.grid(row=5, column=0, padx=20, pady=10)
        entry_confirma_senha.grid(row=5, column=1, padx=20, pady=10)
        label_gerente_senha.grid(row=6, column=0, padx=20, pady=10)
        entry_gerente_senha.grid(row=6, column=1, padx=20, pady=10)
        botao_cadastrar.grid(row=7, column=1, padx=20, pady=30)
        botao_voltar.grid(row=7, column=2, padx=20, pady=30)

        
       
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def realizar_cadastro(self, nome, usuario, matricula, senha, confirma_senha, senha_gerente):
        # Verificar se as senhas coincidem
        if not (nome and usuario and matricula and senha):
            messagebox.showerror("Erro", "Preencha todos campos.")
            return
        elif senha != confirma_senha:
            messagebox.showerror("Erro", "As senhas não coincidem.")
            return
        elif senha_gerente != 'TESI2':
            messagebox.showerror("Erro", "Senha do gerente incorreta")
            return

        senha = sha256(senha.encode()).hexdigest()
        # Inserir dados na tabela de usuários
        try:
            cursor = self.db_connection.cursor()
            sql = "INSERT INTO usuario (user_name, user_login, user_registration, user_password, user_theme) VALUES (?, ?, ?, ?, ?)"
            val = (nome, usuario.upper().strip(), matricula, senha, self.parent.style.theme_use() )  
            cursor.execute(sql, val)
            self.db_connection.commit()
            cursor.close()
            messagebox.showinfo("Cadastro", "Usuário cadastrado com sucesso!")
        except sqlite3.Error as err:
            print(f"Erro no banco de dados: {err}")
            messagebox.showerror("Erro", "Ocorreu um erro no banco de dados.")

    def voltar(self):
        self.destroy()
        self.parent.deiconify()

    def fechar_aplicacao(self):
        self.parent.fechar_aplicacao()

    def conectar_ao_bd(self):
        try:
            conn = sqlite3.connect("estoque.db")
            return conn
        except sqlite3.Error as err:
            print(f"Erro na conexão com o banco de dados: {err}")
            messagebox.showerror("Erro", "Ocorreu um erro na conexão com o banco de dados.")
            self.fechar_aplicacao()

