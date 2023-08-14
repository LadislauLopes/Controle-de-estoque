import xlsxwriter
import webbrowser

# Criar um arquivo Excel
excel_filename = 'Relatorio Exemplo.xlsx'
workbook = xlsxwriter.Workbook(excel_filename)
worksheet = workbook.add_worksheet()

# Definir os dados
data = {'Patrimonio': [2018048788, 2020021568, 2020021506, 2014052820, 2018001196],
        'Tipo': ['Desktop', 'Notebook', 'Dockstation', 'Monitor', 'Impressora'],
        '':[''],
        'Sala': ['W2-08','S2-04','N1-03', 'S3-05', 'NW-32']}

# Adicionar os cabeçalhos
header_format = workbook.add_format({'bold': True, 'bg_color': '#cccccc'})
worksheet.write_row('A1', data.keys(), header_format)

# Definir as cores para linhas intercaladas (verde e verde claro)
even_row_format = workbook.add_format({'bg_color': '#E2F0D9'})  # Verde claro
odd_row_format = workbook.add_format({'bg_color': '#C5E0B4'})   # Verde

# Adicionar os dados e aplicar a formatação de cores intercaladas
for row_num, (patrimonio, tipo, sala) in enumerate(zip(data['Patrimonio'], data['Tipo'], data['Sala']), start=1):
    row_format = even_row_format if row_num % 2 == 0 else odd_row_format
    worksheet.write(row_num, 0, patrimonio, row_format)
    worksheet.write(row_num, 1, tipo, row_format)
    worksheet.write(row_num, 2, '', row_format)  # Aplicar a formatação à coluna vazia
    worksheet.write(row_num, 3, sala, row_format)

# Aumentar a largura da primeira coluna para 15
worksheet.set_column('A:Z', 15)

# Fechar o arquivo Excel
workbook.close()

print(f"Arquivo Excel '{excel_filename}' criado com sucesso.")
webbrowser.open('Relatorio Exemplo.xlsx')
