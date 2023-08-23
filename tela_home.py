import tkinter as tk


class TelaHome(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Esto')
        self.geometry("1024x1024")  
        self.resizable(False, False)
        self.parent = parent
        self.protocol("WM_DELETE_WINDOW", self.fechar_aplicacao)
       # self.criar_interface()

    def fechar_aplicacao(self):
        self.parent.fechar_aplicacao()