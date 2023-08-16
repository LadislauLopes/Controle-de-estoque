import tkinter as tk
from tkinter import messagebox

class TelaLogin(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Login')
        self.geometry("500x400")  # Ajuste o tamanho da janela
        self.resizable(False, False)
        self.parent = parent
        self.criar_interface()

    def criar_interface(self):
        # Aumente o tamanho da fonte
        fonte = ("Arial", 14)

        # Adicione espaçamento no topo da janela
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

        # Aumente o tamanho dos botões e da fonte
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

        # Simulação de verificação de credenciais
        if usuario == "usuario" and senha == "senha":
            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
        else:
            messagebox.showerror("Erro", "Credenciais inválidas.")

    def voltar(self):
        self.destroy()
        self.parent.deiconify()

