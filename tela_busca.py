import tkinter as tk
import sqlite3
from tkinter import  Button, messagebox, Label, Entry

class TelaBusca(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.title('Buscar Equipamento')
        self.geometry("300x100")
        self.resizable(False, False)
        self.callback = callback  

        label = Label(self, text="Digite o Patrimônio:")
        label.pack(pady=5)

        self.entry_patrimonio = Entry(self)
        self.entry_patrimonio.pack(pady=5)

        button_buscar = Button(self, text="Buscar", command=self.realizar_busca)
        button_buscar.pack(pady=5)

        
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def realizar_busca(self):
        patrimonio = self.entry_patrimonio.get()
        if not patrimonio:
            messagebox.showwarning("Aviso", "Por favor, insira um patrimônio.")
            return
        conn = sqlite3.connect("estoque.db")
        cursor = conn.cursor()  
        cursor.execute("SELECT equipament_patrymony AS patrimonio, equipament_type AS tipo, equipament_status AS status, equipament_room_code AS sala FROM equipamentos WHERE equipament_status2 = 'Ativo' AND equipament_patrymony LIKE ?", ('%' + patrimonio.upper() + '%',))
        resultados = cursor.fetchall()
        conn.close()

    
        colunas = [description[0] for description in cursor.description]
        self.callback(resultados, colunas)
        self.destroy()