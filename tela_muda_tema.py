import tkinter as tk

class TelaMudaTema(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Altera tema')
        self.geometry("960x300")
        self.parent = parent
        self.protocol("WM_DELETE_WINDOW", self.fechar_aplicacao)

        self.temas = [
            "cosmo", "flatly", "litera", "minty", "lumen", "sandstone", "yeti",
            "pulse", "united", "morph", "journal", "darkly", "superhero", "solar",
            "cyborg", "vapor", "cerculean",'simplex' 
        ]
        self.selecionar_tema = tk.StringVar()
        self.criar_interface()

    def criar_interface(self):
        for i, tema in enumerate(self.temas):
            rb = tk.Radiobutton(self, text=tema, variable=self.selecionar_tema, value=tema, command=self.mudar_tema)
            linha = (i // 9) + 3
            coluna = i % 9
            rb.grid(row=linha, column=coluna, sticky="w", padx=10, pady=10)
        self.selecionar_tema.set(self.parent.tema_atual)
        btn_voltar = tk.Button(self, text='Voltar', width=10, height=5, font=10, activebackground='#0525f7', command=self.voltar)
        btn_voltar.grid(row=10, column=10, sticky="w", padx=10, pady=10)

    def mudar_tema(self):
        tema_novo = self.selecionar_tema.get()
        if tema_novo != self.parent.tema_atual:
            if tema_novo in self.parent.style.theme_names():  # Verifica se o tema é suportado
                self.parent.style.theme_use(tema_novo)
                self.parent.tema_atual = tema_novo
            
    def voltar(self):
        self.destroy()
        self.parent.deiconify()


    def fechar_aplicacao(self):
        self.parent.destroy()