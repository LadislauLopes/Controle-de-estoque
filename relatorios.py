import xlsxwriter
import sqlite3
import webbrowser
def gerar_relatorio_equipamento():
    try:
        #Conectando ao banco
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()

        cursor.execute("SELECT equipament_patrymony, equipament_type, equipament_status, equipament_room_code FROM equipamentos WHERE equipament_status2 = 'Ativo'")
        equipamentos = cursor.fetchall()


        # Criando o arquivo 
        workbook = xlsxwriter.Workbook('Relatorio_Equipamento.xlsx')
        worksheet = workbook.add_worksheet()

        # cabeçalhos
        header_format = workbook.add_format({'bold': True, 'bg_color': '#cccccc'})
        headers = ['Patrimônio', 'Tipo', 'Status', 'Sala']
        worksheet.write_row('A1', headers, header_format)

        # D cores 
        even_row_format = workbook.add_format({'bg_color': '#E2F0D9'})  # Verde claro
        odd_row_format = workbook.add_format({'bg_color': '#C5E0B4'})   # Verde

        # Escrevendo as linhas 
        for row_num, equipamento in enumerate(equipamentos, start=1):
            row_format = even_row_format if row_num % 2 == 0 else odd_row_format
            worksheet.write_row('A' + str(row_num + 1), equipamento, row_format)

        worksheet.set_column('A:D', 20)
        worksheet.set_column('B:B', 30)
        workbook.close()

        webbrowser.open('Relatorio_Equipamento.xlsx')
    except sqlite3.Error as err:
        print(f"Erro ao buscar dados no banco de dados: {err}")
    finally:
        if conn:
            conn.close()


