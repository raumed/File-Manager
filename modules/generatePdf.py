from fpdf import FPDF

def cellSize(n):
    if n == 1:
      return 42
    elif n == 3:
      return 62
    elif n == 4:
      return 40
    elif n == 5:
      return 40


def simple_table(outputLocation, header, copy, i, rowFinal):
    pdf = FPDF('p', 'mm', 'Letter')
    pdf.set_font("Arial", size=8)
    pdf.add_page()
    columnControl = 1
    rowControl = 1
    aux = 20000   
    # Header format 
    col_width = pdf.w
    row_height = pdf.font_size *1.5
    for item in header:
        if item == None:
          pdf.cell(col_width, row_height,txt="", border=0)  
        else:
          pdf.cell(col_width, row_height,txt=str(item), border=0, align='C')
        pdf.ln(row_height)
    pdf.cell(col_width, row_height,txt="", border=0)
    pdf.ln(row_height)
    # Table format
    borderValue = 0
    alignValue = 'C'
    row_height = pdf.font_size * 1.5
    for row in copy:
        for item in row:
              if columnControl != 2:
                col_width = cellSize(columnControl)
                if columnControl == 1:
                  borderValue = 0
                  alignValue = 'C'
                elif rowControl <= 9:
                  borderValue = 1
                  alignValue = 'C'
                elif(columnControl >= 3):
                  borderValue = 'LR'
                  alignValue = 'L'
                  if isinstance(item, int) or isinstance(item, float):
                    borderValue = 'LR'
                    alignValue = 'R'
                  if(item == 'TOTAL GASTOS NO COMUNES'):
                    aux = rowControl
                  if(aux < rowControl):
                    if(columnControl == 3):
                      borderValue = 'LR'
                      alignValue = 'L'
                      if(rowControl+1 == rowFinal):
                        if(row[4] != 0):
                          pdf.set_text_color(255,0,0)
                        borderValue ='LRB'
                        alignValue = 'L'
                    elif isinstance(item, int) or isinstance(item, float):
                      borderValue = 1
                      alignValue = 'R'
                    else:
                      borderValue = 1
                      alignValue = 'L'
                if item == None:
                  pdf.cell(col_width, row_height,txt="", border = borderValue)
                elif(str(item).__contains__('mailto:')): 
                  pdf.cell(col_width, row_height,txt="", border = borderValue) 
                elif(isinstance(item, float)):
                  auxE = int(item)
                  auxD = abs(int((item - int(item))*100))
                  auxS = str(auxE) + ',' + str(auxD)
                  pdf.cell(col_width, row_height,txt=auxS, border = borderValue, align = alignValue)
                elif isinstance(item, int):
                  pdf.cell(col_width, row_height,txt=str(item)+',00', border = borderValue, align = alignValue)
                else:
                  pdf.cell(col_width, row_height,txt=str(item), border = borderValue, align = alignValue)
              columnControl+=1
        columnControl=1
        rowControl += 1
        pdf.ln(row_height)
    pdf.output(outputLocation+'/Recibo '+ str(i)+'.pdf')
    