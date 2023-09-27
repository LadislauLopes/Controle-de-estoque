import tkinter as tk
from tkinter import Label, Entry, Button
import sqlite3

class TelaRelatorioData(tk.Toplevel):
    def __init__(self, parent,callback):
        super().__init__(parent)
        self.title('Relatório por Data')
        self.geometry("400x200")
        self.callback = callback   
        self.resizable(False, False)

        self.label_inicio = Label(self, text="Data de Início:")
        self.label_inicio.pack(pady=10)

        self.entry_inicio = Entry(self)
        self.entry_inicio.pack(pady=5)
        self.entry_inicio.insert(0, "YYYY-MM-DD")
        self.entry_inicio.bind("<KeyRelease>", self.formatar_data_inicio)

        self.label_saida = Label(self, text="Data de Saída:")
        self.label_saida.pack(pady=10)

        self.entry_saida = Entry(self)
        self.entry_saida.pack(pady=5)
        self.entry_saida.insert(0, "YYYY-MM-DD")
        self.entry_saida.bind("<KeyRelease>", self.formatar_data_saida)

        self.button_gerar_relatorio = Button(self, text="Gerar Relatório", command=self.gerar_relatorio)
        self.button_gerar_relatorio.pack(pady=10)

    def formatar_data_inicio(self, event):
        data = self.entry_inicio.get()
        data_formatada = self.formatar_data(data)
        self.entry_inicio.delete(0, tk.END)
        self.entry_inicio.insert(0, data_formatada)

    def formatar_data_saida(self, event):
        data = self.entry_saida.get()
        data_formatada = self.formatar_data(data)
        self.entry_saida.delete(0, tk.END)
        self.entry_saida.insert(0, data_formatada)

    def formatar_data(self, data):
        data = ''.join(filter(str.isdigit, data))

        if len(data) > 4 and data[4] != '-':
            data = f"{data[:4]}-{data[4:]}"
        if len(data) > 7 and data[7] != '-':
            data = f"{data[:7]}-{data[7:]}"

        if len(data) > 10:
            data = data[:10]

        return data

    def gerar_relatorio(self):
        data_inicio = self.entry_inicio.get()
        data_saida = self.entry_saida.get()
        if data_inicio == "YYYY-MM-DD":
            data_inicio = '2000-01-01'
        if data_saida == "YYYY-MM-DD":
            data_saida = '3000-01-10'

        self.realizar_busca(data_inicio, data_saida)

    def realizar_busca(self,data_inicio, data_saida):
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()

        cursor.execute("""
            SELECT u.user_login as 'Login do usuário', e.equipament_patrymony as 'Patrimônio do equipamento',
                r.request_date as 'Data da requisição', r.request_origin as 'Origem da requisição',
                r.request_destiny_local as 'Local de destino da requisição',
                r.request_destiny_person as 'Pessoa de destino da requisição',
                r.request_type as 'Tipo de requisição'
            FROM Requisicao r
            INNER JOIN usuario u ON r.request_user_id = u.user_id
            INNER JOIN equipamentos e ON r.request_equipamento_id = e.equipament_id
            WHERE r.request_date BETWEEN ? AND ?
        """, (data_inicio, data_saida))
        resultados = cursor.fetchall()
        conn.close()

    
        colunas = [description[0] for description in cursor.description]
        self.callback(resultados, colunas)
        self.destroy()

