import tkinter as tk
import sqlite3
from tkinter import Button, Label, Entry, messagebox, ttk
import datetime

class TelaTransferir(tk.Toplevel):
    def __init__(self, parent, user_id):
        super().__init__(parent)
        self.title('Transferir Equipamento')
        self.geometry("400x400")
        self.resizable(False, False)
        self.parent = parent
        self.user_id = user_id
        self.salas = self.carregar_salas()

        label_patrimonio = Label(self, text="Patrimônio:",  font=("Arial", 12))
        label_patrimonio.pack(pady=10)

        self.entry_patrimonio = Entry(self, font=("Arial", 12))
        self.entry_patrimonio.pack(pady=5)

        label_origem = Label(self, text="Origem:",  font=("Arial", 12))
        label_origem.pack(pady=10)

        self.combobox_sala_origem = ttk.Combobox(self, values=self.salas, font=("Arial", 12), state="readonly")
        self.combobox_sala_origem.set(self.salas[0])
        self.combobox_sala_origem.pack(pady=5)

        label_destino_sala = Label(self, text="Destino (Sala):",  font=("Arial", 12))
        label_destino_sala.pack(pady=10)

        self.combobox_sala_destino = ttk.Combobox(self, values=self.salas, font=("Arial", 12), state="readonly")
        self.combobox_sala_destino.set(self.salas[0])
        self.combobox_sala_destino.pack(pady=5)

        label_destino_pessoa = Label(self, text="Destino (Pessoa):",  font=("Arial", 12))
        label_destino_pessoa.pack(pady=10)

        self.entry_destino_pessoa = Entry(self, font=("Arial", 12))
        self.entry_destino_pessoa.pack(pady=5)

        button_transferir = Button(self, text="Transferir", command=self.transferir_equipamento, font=("Arial", 12))
        button_transferir.pack(pady=15)

        # Centralizar a janela na tela
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def transferir_equipamento(self):
        patrimonio = self.entry_patrimonio.get().strip().upper()
        origem = self.combobox_sala_origem.get().strip()
        destino_sala = self.combobox_sala_destino.get().strip()
        destino_pessoa = self.entry_destino_pessoa.get().strip()

        if not patrimonio:
            messagebox.showwarning("Aviso", "Preencha o Patrimônio.")
            return

        # Verifique se ambos os destinos foram preenchidos
        if destino_sala !='CAUTELADO' and destino_pessoa :
            messagebox.showwarning("Aviso", "Escolha apenas uma opção de destino (Sala ou Pessoa).")
            return
        if destino_sala =='CAUTELADO' and not destino_pessoa :
            messagebox.showwarning("Aviso","Digite para que pessoa será enviado esse equipamento.")
            return

        try:
            data_atual = datetime.datetime.now()
            data_formatada = data_atual.strftime("%Y-%m-%d")
            conn = sqlite3.connect("estoque.db")
            cursor = conn.cursor()

            # Verifique se o equipamento existe
            cursor.execute("SELECT equipament_id, equipament_status FROM equipamentos WHERE equipament_patrymony = ?", (patrimonio,))
            equipamento = cursor.fetchone()

            if not equipamento:
                messagebox.showerror("Erro", "Equipamento não encontrado.")
                return

            equipamento_id = equipamento[0]

            if destino_sala:
                # Transferir para uma sala
                cursor.execute("UPDATE equipamentos SET equipament_room_code = ? WHERE equipament_id = ?", (destino_sala, equipamento_id))
                conn.commit()
            if destino_pessoa and destino_sala == 'CAUTELADO':
                # Transferir para uma pessoa (marcar como CAUTELADO)
                cursor.execute("UPDATE equipamentos SET equipament_room_code = ? WHERE equipament_id = ?", ("CAUTELADO", equipamento_id))
                conn.commit()

            # Insira a ação de transferência na tabela Requisicao
            cursor.execute("INSERT INTO Requisicao (request_user_id, request_date, request_equipamento_id, request_origin, request_destiny_local, request_destiny_person, request_type) VALUES (?,?,?,?,?,?,?)",
                            (self.user_id, data_formatada, equipamento_id, origem, destino_sala, destino_pessoa, 'Transferência'))
            conn.commit()

            conn.close()

            messagebox.showinfo("Sucesso", "Equipamento transferido com sucesso.")
            self.entry_patrimonio.delete(0, tk.END)
            self.entry_destino_pessoa.delete(0, tk.END)
        except sqlite3.Error as err:
            print(f"Erro ao transferir equipamento: {err}")
            messagebox.showerror("Erro", "Ocorreu um erro ao transferir o equipamento.")
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
