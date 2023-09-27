import tkinter as tk
import sqlite3
from tkinter import Button, Label, Entry, messagebox
import datetime
from hashlib import sha256


class TelaDeleta(tk.Toplevel):
    def __init__(self, parent, user_id):
        super().__init__(parent)
        self.title('Deletar Equipamento')
        self.geometry("400x250")
        self.resizable(False, False)
        self.parent = parent
        self.user_id = user_id

        label_patrimonio = Label(self, text="Digite o Patrimônio a ser deletado:", font=("Arial", 12))
        label_patrimonio.pack(pady=10)

        self.entry_patrimonio = Entry(self, font=("Arial", 12))
        self.entry_patrimonio.pack(pady=5)

        label_senha = Label(self, text="Digite sua senha:", font=("Arial", 12))
        label_senha.pack(pady=10)

        self.entry_senha_usuario = Entry(self, show="*", font=("Arial", 12))
        self.entry_senha_usuario.pack(pady=5)

        button_deletar = Button(self, text="Deletar", command=self.deletar_equipamento, font=("Arial", 12))
        button_deletar.pack(pady=15)

        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def deletar_equipamento(self):
        patrimonio = self.entry_patrimonio.get().strip().upper()
        senha_usuario = self.entry_senha_usuario.get().strip()
        senha_usuario = sha256(senha_usuario.encode()).hexdigest()

        if not patrimonio or not senha_usuario:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return

        try:
            data_atual = datetime.datetime.now()
            data_formatada = data_atual.strftime("%Y-%m-%d")
            conn = sqlite3.connect("estoque.db")
            cursor = conn.cursor()

            # Verificando se o equipamento existe antes de excluir
            cursor.execute("SELECT equipament_id FROM equipamentos WHERE equipament_patrymony = ?", (patrimonio,))
            equipamento_id = cursor.fetchone()
            equipamento_id= equipamento_id[0]
            if not equipamento_id:
                messagebox.showerror("Erro", "Equipamento não encontrado.")
                return

            # Verificando se a senha do usuário está correta
            cursor.execute("SELECT user_password FROM usuario WHERE user_id = ?", (self.user_id,))
            senha_armazenada = cursor.fetchone()[0]

            if senha_usuario != senha_armazenada:
                messagebox.showwarning("Aviso", "Senha incorreta.")
                return

            # Deletando o equipamento da tabela equipamentos
            cursor.execute("UPDATE equipamentos SET equipament_status2 = 'Desativado' WHERE equipament_id = ?", (equipamento_id,))
            conn.commit()

            # Inserindo na tabela Requisicao
            cursor.execute("INSERT INTO Requisicao (request_user_id, request_date, request_equipamento_id,  request_type) VALUES (?,?,?,?)",
                            (self.user_id, data_formatada, equipamento_id, 'Exclusão'))
            conn.commit()

            conn.close()

            messagebox.showinfo("Sucesso", "Equipamento deletado com sucesso.")
            self.entry_patrimonio.delete(0, tk.END)
            self.entry_senha_usuario.delete(0, tk.END)
        except sqlite3.Error as err:
            print(f"Erro ao deletar equipamento: {err}")
            messagebox.showerror("Erro", "Ocorreu um erro ao deletar o equipamento.")
