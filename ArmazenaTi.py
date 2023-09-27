import tkinter as tk
from tela_cadastro import TelaCadastro
from tela_login import TelaLogin
from ttkbootstrap import Style
from tela_muda_tema import TelaMudaTema


class Tela(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ArmazenaTI")
        self.geometry("800x600")  
        
        self.tema_atual = "lumen"
        self.style = Style(self.tema_atual)
        self.resizable(False, False) 
        self.primeiro_frame()

    def primeiro_frame(self):
        # Título
        self.label_tema = tk.Label(self, text="Bem-vindo ao ArmazenaTI", font=("Arial", 30, "bold"))
        self.label_tema.pack(pady=50) 

        # Botões
        self.botao_Login = tk.Button(self, text='Login', width=20, height=2, font=("Arial", 16, "bold"), command=self.tela_Login)
        self.botao_Login.pack(pady=20)

        self.botao_Cadastro = tk.Button(self, text='Cadastro', width=20, height=2, font=("Arial", 16, "bold"), command=self.tela_cadastro)
        self.botao_Cadastro.pack(pady=20)

        self.botao_Muda_Tema = tk.Button(self, text='Mudar tema', width=20, height=2, font=("Arial", 16, "bold"), command=self.tela_muda_tema)
        self.botao_Muda_Tema.pack(pady=20)

        
      
        # Centralizar a janela na tela
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

        self.label_made_by = tk.Label(self, text="made by Ladislau", font=("Arial", 10))
        self.label_made_by.place(x=self.winfo_width() - 120, y=10)

    def voltar(self):
        self.toplevel.destroy()
        self.deiconify()

    def tela_cadastro(self):
        self.withdraw()
        self.toplevel = TelaCadastro(self)

    def tela_Login(self):
        self.withdraw()
        self.toplevel = TelaLogin(self)

    def fechar_aplicacao(self):
        self.destroy()


    def tela_muda_tema(self):
        self.withdraw()
        self.toplevel = TelaMudaTema(self)

if __name__ == "__main__":
    app = Tela()
    app.mainloop()
