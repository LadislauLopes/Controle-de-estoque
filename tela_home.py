import tkinter as tk
import sqlite3
from tkinter import Frame, Button, messagebox, ttk, Menu
import xlsxwriter
from tela_busca import TelaBusca
from tela_insere import TelaInsere
from tela_deleta import TelaDeleta
from tela_tranferir import TelaTransferir
from relatorios import *
from tela_relatorio_historico import TelaRelatorioData
from tela_atualiza import TelaAtualiza
from tela_muda_tela_dentro_do_app import TelaAlteraTema
from tela_editar import TelaEditar
class TelaHome(tk.Toplevel):
    def __init__(self, parent, id_usuario):
        super().__init__(parent)
        self.title('Estoque')
        self.geometry("900x600")  #
        self.resizable(True, True)  
        self.parent = parent
        self.protocol("WM_DELETE_WINDOW", self.fechar_aplicacao)
        self.id_usuario = id_usuario
        self.menubar = Menu(self)
        self.config(menu=self.menubar) 
        self.frames_da_tela()
        self.botoes()

    def frames_da_tela(self):
        self.frame_1 = Frame(self, bg="white", highlightbackground="black", highlightthickness=5)
        self.frame_1.place(relx=0.04, rely=0.04, relwidth=0.9, relheight=0.4)

        self.frame_2 = Frame(self, bg="white", highlightbackground="black", highlightthickness=5)
        self.frame_2.place(relx=0.04, rely=0.5, relwidth=0.9, relheight=0.4)

    def botoes(self):
        # Primeira linha de botões
        
        # Botão Buscar 
        botao_buscar = Button(self.frame_1, text="Buscar", command=self.abrir_janela_busca)
        botao_buscar.place(relx=0.03, rely=0.1, relheight=0.1, relwidth=0.20)
        # Botão Inserir
        botao_inserir = Button(self.frame_1, text="Inserir", command=self.abrir_janela_insercao)
        botao_inserir.place(relx=0.25, rely=0.1, relheight=0.1, relwidth=0.20)

        # Botão deleta
        botao_apagar = Button(self.frame_1, text="Apagar", command=self.abrir_janela_deleta)
        botao_apagar.place(relx=0.47, rely=0.1, relheight=0.1, relwidth=0.20)

        #Botão tranfere
        botao_tranfere = Button(self.frame_1, text="Transferir", command=self.abrir_janela_Tranfere)
        botao_tranfere.place(relx=0.69, rely=0.1, relheight=0.1, relwidth=0.20)

        # Segunda linha de botões

        # Botão relatorio de equipamento
        botao_relatorio_equipamento = Button(self.frame_1, text="Relatório Equipamento", command=gerar_relatorio_equipamento)
        botao_relatorio_equipamento.place(relx=0.03, rely=0.3, relheight=0.1, relwidth=0.20)

        # Botão relatorio historico
        botao_relatorio_historico = Button(self.frame_1, text="Relatório Histórico", command=self.abrir_janela_Relatorio_historico)
        botao_relatorio_historico.place(relx=0.25, rely=0.3, relheight=0.1, relwidth=0.20)

        # Botão atualiza
        botao_atualizar = Button(self.frame_1, text="atualizar status", command=self.abrir_janela_atualiza)
        botao_atualizar.place(relx=0.47, rely=0.3, relheight=0.1, relwidth=0.20)

        botao_muda_tema = Button(self.frame_1, text="mudar tema", command=self.abrir_janela_muda_tema)
        botao_muda_tema.place(relx=0.69, rely=0.3, relheight=0.1, relwidth=0.20)


        #menubar
        opcoes_menu = Menu(self.menubar, tearoff=0)

        opcoes_menu.add_command(label="Editar Perfil", command=self.editar_perfil)

        opcoes_menu.add_separator()

        opcoes_menu.add_command(label="Sair", command=self.voltar)

        self.menubar.add_cascade(label="Opções", menu=opcoes_menu)








        
    def abrir_janela_insercao(self):
        janela_insercao = TelaInsere(self,self.id_usuario)

    def abrir_janela_atualiza(self):
        janela_atualiza = TelaAtualiza(self,self.id_usuario)

    def abrir_janela_Tranfere(self):
        janela_Tranfere = TelaTransferir(self,self.id_usuario)

    def abrir_janela_busca(self):
        janela_busca = TelaBusca(self, self.mostrar_resultados)

    def abrir_janela_deleta(self):
        janela_deleta = TelaDeleta(self, self.id_usuario)

    def abrir_janela_Relatorio_historico(self):
        janela_relatorio = TelaRelatorioData(self, self.mostrar_resultados)


    def abrir_janela_muda_tema(self):
        janela_muda_tema = TelaAlteraTema(self,self.id_usuario, self.parent.parent.tema_atual,self.parent.parent.style )

    def editar_perfil(self):
        janela_edita = TelaEditar(self, self.id_usuario)


    def mostrar_resultados(self, resultados, colunas):
        # Limpar o conteúdo atual do segundo frame
        for widget in self.frame_2.winfo_children():
            widget.destroy()

        # Exibir cabeçalhos
        self.treeview = ttk.Treeview(self.frame_2, columns=colunas, show="headings")
        self.treeview.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        for coluna in colunas:
            self.treeview.heading(coluna, text=coluna)

        for resultado in resultados:
            # Verificar e substituir valores None por strings vazias ("")
            resultado = ["" if value is None else value for value in resultado]
            self.treeview.insert("", "end", values=resultado)

        self.frame_2.rowconfigure(0, weight=1)
        self.frame_2.columnconfigure(0, weight=1)

        # Criar o botão "Exportar Excel"
        exportar_excel_button = tk.Button(self.frame_2, text="Exportar Excel", command=lambda: self.exportar_excel(colunas))
        exportar_excel_button.grid(row=1, column=0, padx=5, pady=5, sticky="sw")

    def exportar_excel(self, colunas):
        # Obtenha os resultados da Treeview
        resultados = []
        for item in self.treeview.get_children():
            resultados.append(self.treeview.item(item, "values"))

        # Criar o arquivo Excel
        workbook = xlsxwriter.Workbook('Relatorio.xlsx')
        worksheet = workbook.add_worksheet()

        # Definindo formatos de cores
        even_row_format = workbook.add_format({'bg_color': '#E2F0D9'})  # Verde claro
        odd_row_format = workbook.add_format({'bg_color': '#C5E0B4'})   # Verde
        header_format = workbook.add_format({'bg_color': '#cccccc', 'bold': True})

        # Escrevendo as linhas no arquivo Excel
        for row_num, resultado in enumerate(resultados, start=1):
            row_format = even_row_format if row_num % 2 == 0 else odd_row_format
            worksheet.write_row(row_num, 0, resultado, row_format)

        # Escrevendo os nomes das colunas no arquivo Excel com formato de cabeçalho cinza
        worksheet.write_row(0, 0, colunas, header_format)

        # Ajustando a largura das colunas
        for i, coluna in enumerate(colunas):
            worksheet.set_column(i, i, len(coluna) + 2)  # +2 para acomodar o texto com espaço extra
        worksheet.set_column('A:H', 20)
        # Fechando o arquivo Excel
        workbook.close()

        # Abrindo o arquivo Excel no navegador padrão
        webbrowser.open('Relatorio.xlsx')



    def fechar_aplicacao(self):
        self.parent.fechar_aplicacao()

    def conectar_ao_bd(self):
        try:
            conn = sqlite3.connect("estoque.db")
            return conn
        except sqlite3.Error as err:
            print(f"Erro na conexão com o banco de dados: {err}")
            messagebox.showerror("Erro", "Ocorreu um erro na conexão com o banco de dados.")
            self.parent.fechar_aplicacao()

    def voltar(self):
        self.destroy()
        self.parent.deiconify()
        self.parent.voltar()


