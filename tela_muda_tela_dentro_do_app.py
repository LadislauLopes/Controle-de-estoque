import tkinter as tk
import sqlite3

class TelaAlteraTema(tk.Toplevel):
    def __init__(self, parent, user_id, tema_atual, style):
        super().__init__(parent)
        self.title('Altera tema')
        self.geometry("960x300")
        self.parent = parent
        self.tema_atual = tema_atual
        self.style = style
        self.user_id = user_id

        self.temas = [
            "cosmo", "flatly", "litera", "minty", "lumen", "sandstone", "yeti",
            "pulse", "united", "morph", "journal", "darkly", "superhero", "solar",
            "cyborg", "vapor", "cerculean", 'simplex'
        ]
        self.selecionar_tema = tk.StringVar()
        self.criar_interface()

    def criar_interface(self):
        for i, tema in enumerate(self.temas):
            rb = tk.Radiobutton(self, text=tema, variable=self.selecionar_tema, value=tema, command=self.mudar_tema)
            linha = (i // 9) + 3
            coluna = i % 9
            rb.grid(row=linha, column=coluna, sticky="w", padx=10, pady=10)
        self.selecionar_tema.set(self.tema_atual)
        btn_voltar = tk.Button(self, text='Voltar', width=10, height=5, font=10, activebackground='#0525f7', command=self.voltar)
        btn_voltar.grid(row=10, column=10, sticky="w", padx=10, pady=10)

    def mudar_tema(self):
        tema_novo = self.selecionar_tema.get()
        tema_atual = self.parent.parent.parent.tema_atual

        if tema_novo != self.tema_atual:
            if tema_novo in self.style.theme_names():  # Verifica se o tema é suportado
                self.style.theme_use(tema_novo)
                self.tema_atual = tema_novo
                
                self.atualizar_tema_no_bd(tema_novo)

    def voltar(self):
        self.destroy()
        self.parent.deiconify()

    def atualizar_tema_no_bd(self, novo_tema):
        # Conectar-se ao banco de dados SQLite
        conn = self.conectar_ao_bd()
        
        if conn:
            try:
                cursor = conn.cursor()
                # Atualizar o tema no banco de dados para o usuário atual
                cursor.execute("UPDATE usuario SET user_theme = ? WHERE user_id = ?", (novo_tema, self.user_id))
                conn.commit()
                cursor.close()
            except sqlite3.Error as err:
                print(f"Erro no banco de dados: {err}")
                conn.rollback()
            finally:
                conn.close()
        else:
            print("Erro na conexão com o banco de dados.")

    def conectar_ao_bd(self):
        try:
            conn = sqlite3.connect("estoque.db")
            return conn
        except sqlite3.Error as err:
            print(f"Erro na conexão com o banco de dados: {err}")
            return None
