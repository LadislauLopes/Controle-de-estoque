import tkinter as tk
from tkinter import messagebox
import sqlite3
from hashlib import sha256

class TelaEditar(tk.Toplevel):
    def __init__(self, parent, user_id):
        super().__init__(parent)
        self.title('Editar Perfil')
        self.geometry("500x400")
        self.resizable(False, False)
        self.parent = parent
        self.user_id = user_id
        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)
        self.db_connection = self.conectar_ao_bd()
        self.criar_interface()

    def criar_interface(self):
        fonte = ("Arial", 14)

        espacamento_superior = tk.Label(self, text="", font=fonte)
        espacamento_superior.pack(pady=30)

        self.label_nome = tk.Label(self, text="Nome:", font=fonte)
        self.label_nome.pack()
        self.entry_nome = tk.Entry(self, font=fonte)
        self.entry_nome.pack()

        self.label_usuario = tk.Label(self, text="Usuário:", font=fonte)
        self.label_usuario.pack()
        self.entry_usuario = tk.Entry(self, font=fonte)
        self.entry_usuario.pack()

        self.label_senha = tk.Label(self, text="Nova Senha:", font=fonte)
        self.label_senha.pack()
        self.entry_senha = tk.Entry(self, show="*", font=fonte)
        self.entry_senha.pack()

        self.label_confirma_senha = tk.Label(self, text="Confirmar Senha:", font=fonte)
        self.label_confirma_senha.pack()
        self.entry_confirma_senha = tk.Entry(self, show="*", font=fonte)
        self.entry_confirma_senha.pack()

        self.btn_frame = tk.Frame(self)
        self.btn_frame.pack(pady=20)

        btn_fonte = ("Arial", 12)

        self.btn_salvar = tk.Button(self.btn_frame, text="Salvar", font=btn_fonte, command=self.salvar_perfil)
        self.btn_salvar.pack(side="left", padx=10)

        self.btn_voltar = tk.Button(self.btn_frame, text="Voltar", font=btn_fonte, command=self.voltar)
        self.btn_voltar.pack(side="left")

        self.carregar_dados_usuario()

        # Centralizar a janela na tela
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def carregar_dados_usuario(self):
        conn = self.conectar_ao_bd()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT user_name, user_login FROM usuario WHERE user_id = ?", (self.user_id,))
                dados_usuario = cursor.fetchone()
                cursor.close()
                if dados_usuario:
                    self.entry_nome.insert(0, dados_usuario[0])
                    self.entry_usuario.insert(0, dados_usuario[1])
            except sqlite3.Error as err:
                print(f"Erro no banco de dados: {err}")
                messagebox.showerror("Erro", "Ocorreu um erro no banco de dados.")
                conn.close()
        else:
            messagebox.showerror("Erro", "Erro na conexão com o banco de dados.")

    def salvar_perfil(self):
        nome = self.entry_nome.get()
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
        confirma_senha = self.entry_confirma_senha.get()

        if not (nome and usuario):
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios.")
            return
        elif senha != confirma_senha:
            messagebox.showerror("Erro", "As senhas não coincidem.")
            return
        usuario = usuario.upper().strip()
        conn = self.conectar_ao_bd()
        if conn:
            try:
                cursor = conn.cursor()

                if senha:
                    senha = sha256(senha.encode()).hexdigest()
                    cursor.execute("UPDATE usuario SET user_name = ?, user_login = ?, user_password = ? WHERE user_id = ?",
                                   (nome, usuario, senha, self.user_id))
                else:
                    cursor.execute("UPDATE usuario SET user_name = ?, user_login = ? WHERE user_id = ?",
                                   (nome, usuario, self.user_id))

                conn.commit()
                cursor.close()
                messagebox.showinfo("Perfil Atualizado", "Perfil do usuário atualizado com sucesso!")
            except sqlite3.Error as err:
                print(f"Erro no banco de dados: {err}")
                messagebox.showerror("Erro", "Ocorreu um erro no banco de dados.")
                conn.close()
        else:
            messagebox.showerror("Erro", "Erro na conexão com o banco de dados.")

    def voltar(self):
        self.destroy()
        self.parent.deiconify()

    def fechar_janela(self):
        self.destroy()
        self.parent.deiconify()

    def conectar_ao_bd(self):
        try:
            conn = sqlite3.connect("estoque.db")
            return conn
        except sqlite3.Error as err:
            print(f"Erro na conexão com o banco de dados: {err}")
            messagebox.showerror("Erro", "Ocorreu um erro na conexão com o banco de dados.")
            self.parent.fechar_aplicacao()
