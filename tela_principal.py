import tkinter as tk
from ttkbootstrap import Style
from tela_muda_tema import TelaMudaTema
from tela_cadastro import TelaCadastro

class Tela(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Atividade Limeira")
        self.geometry("1280x720")
        self.resizable(False, False) 
        self.tema_atual = "vapor"
        self.style = Style(self.tema_atual)
        self.primeiro_frame()

    def primeiro_frame(self):
        self.label_tema = tk.Label(self, text="Controle de Estoque - Ladislau", font=("Helvetica", 20, "bold"))
        self.label_tema.place(relx=0.1, rely=0.1) 

        self.botao_Login = tk.Button(self, text='Login', width=20, height=4, font=("Helvetica", 20, "bold"), command=self.acao_botao)
        self.botao_Login.place(relx=0.2, rely=0.465)

        self.botao_Cadastro = tk.Button(self, text='Cadastro', width=20, height=4, font=("Helvetica", 20, "bold"), command=self.tela_cadastro)
        self.botao_Cadastro.place(relx=0.6, rely=0.465)

        self.botao_Muda_Tema = tk.Button(self, text='Mudar tema', width=20, height=2, font=("Helvetica", 10, "bold"), command=self.tela_muda_tema)
        self.botao_Muda_Tema.place(relx=0.8, rely=0.865)

    def mudar_tema(self):
        tema_novo = self.selecionar_tema.get()
        if tema_novo != self.tema_atual:
            self.style = Style(tema_novo)
            self.tema_atual = tema_novo
            
    def voltar(self):
        self.toplevel.destroy()
        self.deiconify()

    def acao_botao(self):
        print("Botão com imagem clicado!")
        
    def tela_cadastro(self):
        self.withdraw()
        self.toplevel = TelaCadastro(self)

    def tela_muda_tema(self):
        self.withdraw()
        self.toplevel = TelaMudaTema(self)

if __name__ == "__main__":
    app = Tela()
    app.mainloop()
