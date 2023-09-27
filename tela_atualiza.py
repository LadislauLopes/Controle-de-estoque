import tkinter as tk
import sqlite3
from tkinter import Button, Label, Entry, messagebox, ttk
import datetime

class TelaAtualiza(tk.Toplevel):
    def __init__(self, parent, user_id):
        super().__init__(parent)
        self.title('Atualizar Status do Equipamento')
        self.geometry("400x250")

        self.resizable(False, False)
        self.parent = parent
        self.user_id = user_id

        label_patrimonio = Label(self, text="Digite o Patrimônio do Equipamento:",  font=("Arial", 12))
        label_patrimonio.pack(pady=10)

        self.entry_patrimonio = Entry(self, font=("Arial", 12))
        self.entry_patrimonio.pack(pady=5)

        label_status = Label(self, text="Novo Status:",  font=("Arial", 12))
        label_status.pack(pady=10)

        
        self.combobox_status = ttk.Combobox(self, values=["funcionando", "com defeito"], font=("Arial", 12))
        self.combobox_status.set("funcionando")  
        self.combobox_status.pack(pady=5)

        button_atualizar = Button(self, text="Atualizar", command=self.atualizar_status,  font=("Arial", 12))
        button_atualizar.pack(pady=15)

        
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def atualizar_status(self):
        patrimonio = self.entry_patrimonio.get().strip().upper()
        novo_status = self.combobox_status.get().strip()

        if not patrimonio or not novo_status:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return

        try:
            data_atual = datetime.datetime.now()
            data_formatada = data_atual.strftime("%Y-%m-%d")
            conn = sqlite3.connect("estoque.db")
            cursor = conn.cursor()
            
            
            cursor.execute("SELECT equipament_id FROM equipamentos WHERE equipament_patrymony = ?", (patrimonio,))
            equipamento_id = cursor.fetchone()

            if not equipamento_id:
                messagebox.showerror("Erro", "Equipamento não encontrado.")
                return

            
            cursor.execute("UPDATE equipamentos SET equipament_status = ? WHERE equipament_id = ?", (novo_status, equipamento_id[0]))
            conn.commit()

            
            cursor.execute("INSERT INTO Requisicao (request_user_id, request_date, request_equipamento_id, request_destiny_Local, request_type) VALUES (?,?,?,?,?)",
                            (self.user_id, data_formatada, equipamento_id[0], '', 'Atualização'))
            conn.commit()

            conn.close()

            messagebox.showinfo("Sucesso", "Status do equipamento atualizado com sucesso.")
            self.entry_patrimonio.delete(0, tk.END)
            self.combobox_status.set("funcionando")  
        except sqlite3.Error as err:
            print(f"Erro ao atualizar status do equipamento: {err}")
            messagebox.showerror("Erro", "Ocorreu um erro ao atualizar o status do equipamento.")

