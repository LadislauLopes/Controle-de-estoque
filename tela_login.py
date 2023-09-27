import tkinter as tk
from tkinter import messagebox
import sqlite3
from tela_home import TelaHome
from hashlib import sha256

class TelaLogin(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Login')
        self.geometry("500x400") 
        self.resizable(False, False)
        self.parent = parent
        self.protocol("WM_DELETE_WINDOW", self.fechar_aplicacao)
        self.criar_interface()

    def criar_interface(self):
        fonte = ("Arial", 14)

        espacamento_superior = tk.Label(self, text="", font=fonte)
        espacamento_superior.pack(pady=30)

        self.label_usuario = tk.Label(self, text="Usuário:", font=fonte)
        self.label_usuario.pack()
        self.entry_usuario = tk.Entry(self, font=fonte)
        self.entry_usuario.pack()

        self.label_senha = tk.Label(self, text="Senha:", font=fonte)
        self.label_senha.pack()
        self.entry_senha = tk.Entry(self, show="*", font=fonte)
        self.entry_senha.pack()

        self.btn_frame = tk.Frame(self)
        self.btn_frame.pack(pady=20)

        btn_fonte = ("Arial", 12)
        
        self.btn_login = tk.Button(self.btn_frame, text="Login", font=btn_fonte, command=self.verificar_login)
        self.btn_login.pack(side="left", padx=10)
        
        self.btn_voltar = tk.Button(self.btn_frame, text="Voltar", font=btn_fonte, command=self.voltar)
        self.btn_voltar.pack(side="left")

        # Centralizar a janela na tela
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def verificar_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
        senha = sha256(senha.encode()).hexdigest()

        
        conn = self.conectar_ao_bd()

        if conn:
            try:
                cursor = conn.cursor()
                
                cursor.execute("SELECT * FROM usuario WHERE user_login = ? AND user_password = ?", (usuario.upper().strip(), senha))
                usuario_encontrado = cursor.fetchone()
                id_usuario = usuario_encontrado[0]
                tema_carregado = usuario_encontrado[-1]
                
                cursor.close()
                
                if usuario_encontrado:
                    self.carregar_tema(tema_carregado)
                    self.acesso_liberado(id_usuario)
                else:
                    messagebox.showerror("Erro", "Credenciais inválidas.")
            except sqlite3.Error as err:
                print(f"Erro no banco de dados: {err}")
                messagebox.showerror("Erro", "Ocorreu um erro no banco de dados.")
                conn.close()
        else:
            messagebox.showerror("Erro", "Erro na conexão com o banco de dados.")

    def acesso_liberado(self,id_usuario):
        self.withdraw()
        self.toplevel = TelaHome(self,id_usuario)
        
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
            self.parent.destroy()

    def carregar_tema(self,tema_novo):
           if tema_novo in self.parent.style.theme_names():  # Verifica se o tema é suportado
                self.parent.style.theme_use(tema_novo)
                self.parent.tema_atual = tema_novo