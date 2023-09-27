import tkinter as tk
import sqlite3
from tkinter import Button, Label, Entry, messagebox, ttk
import datetime

class TelaInsere(tk.Toplevel):
    def __init__(self, parent, user_id):
        super().__init__(parent)
        self.title('Inserir Equipamento')
        self.geometry("400x400")
        self.resizable(False, False)
        self.parent = parent
        self.user_id = user_id
        self.salas = self.carregar_salas()
        
        

        label_patrimonio = Label(self, text="Patrimônio:",  font=("Arial", 12))
        label_patrimonio.pack(pady=10)

        self.entry_patrimonio = Entry(self, font=("Arial", 12))
        self.entry_patrimonio.pack(pady=5)

        label_tipo = Label(self, text="Tipo:",  font=("Arial", 12))
        label_tipo.pack(pady=10)

        self.entry_tipo = Entry(self, font=("Arial", 12))
        self.entry_tipo.pack(pady=5)

        label_sala = Label(self, text="Sala:",  font=("Arial", 12))
        label_sala.pack(pady=10)

        # # Carregando as salas do banco de dados
        # self.salas = self.carregar_salas()

        # Criando o Combobox para as salas
        self.combobox_sala = ttk.Combobox(self, values=self.salas, font=("Arial", 12), state="readonly")
        self.combobox_sala.set(self.salas[0])
        self.combobox_sala.pack(pady=5)

        label_status = Label(self, text="Status:",  font=("Arial", 12))
        label_status.pack(pady=10)

        # Criando o Combobox para o status com 'funcionando' como padrão
        self.combobox_status = ttk.Combobox(self, values=["funcionando", "com defeito"], font=("Arial", 12),state="readonly")
        self.combobox_status.set("funcionando")  # Definindo 'funcionando' como padrão
        self.combobox_status.pack(pady=5)

        button_inserir = Button(self, text="Inserir", command=self.inserir_equipamento,  font=("Arial", 12))
        button_inserir.pack(pady=15)

        # Centralizar a janela na tela
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")


    def inserir_equipamento(self):
        patrimonio = self.entry_patrimonio.get().strip().upper()
        tipo = self.entry_tipo.get().strip().upper()
        sala = self.combobox_sala.get().strip()
        status = self.combobox_status.get().strip() 

        if not patrimonio or not tipo or not sala or not status:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return

        try:
            data_atual = datetime.datetime.now()
            data_formatada = data_atual.strftime("%Y-%m-%d")
            conn = sqlite3.connect("estoque.db")
            cursor = conn.cursor()
            
            # Primeira inserção na tabela equipamentos
            cursor.execute("INSERT INTO equipamentos (equipament_patrymony, equipament_type, equipament_room_code, equipament_status, equipament_status2) VALUES (?, ?, ?, ?,?)",
                        (patrimonio, tipo, sala, status,'Ativo'))
            conn.commit()

            # Recupere o ID do equipamento inserido
            cursor.execute("SELECT last_insert_rowid()")
            equipamento_id = cursor.fetchone()[0]

            # Segunda inserção na tabela Requisicao
            cursor.execute("INSERT INTO Requisicao (request_user_id, request_date, request_equipamento_id, request_destiny_Local, request_type) VALUES (?,?,?,?,?)",
                        (self.user_id, data_formatada, equipamento_id, sala, 'Inserção'))
            conn.commit()

            conn.close()

            messagebox.showinfo("Sucesso", "Equipamento inserido com sucesso.")
            self.entry_patrimonio.delete(0, tk.END)
            self.entry_tipo.delete(0, tk.END)
            self.combobox_sala.set(self.salas[0])  
            self.combobox_status.set("funcionando")  
        except sqlite3.Error as err:
            print(f"Erro ao inserir equipamento: {err}")
            messagebox.showerror("Erro", "Ocorreu um erro ao inserir o equipamento.")

    def carregar_salas(self):
        try:
            conn = sqlite3.connect("estoque.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sala")
            salas = cursor.fetchall()  
            salas = [sala[0] for sala in salas]  
            conn.close()  
            return salas
        except sqlite3.Error as err:
            print(f"Erro ao consultar salas: {err}")

