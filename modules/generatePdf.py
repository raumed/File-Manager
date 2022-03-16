from fpdf import FPDF

def cellSize(n):
    x = 0.76
    if n == 1:
      return 45 *x
    elif n == 3:
      return 80 *x
    elif n == 4:
      return 40 *x
    elif n == 5:
      return 40 *x


def simple_table(outputLocation, header, copy, i, rowFinal):
    pdf = FPDF('p', 'mm', 'Letter')
    pdf.set_margins(3.0, 15.2)
    pdf.add_page()
    columnControl = 1
    rowControl = 1
    aux = 20000   
    # Header format 
    pdf.set_font("Arial", size=7.5)
    col_width = pdf.w *0.95
    row_height = pdf.font_size *1.2
    for item in header:
        if item == None:
          pdf.cell(col_width, row_height,txt="", border=0)  
        else:
          pdf.cell(col_width, row_height,txt=str(item), border=0, align='C')
        pdf.ln(row_height)
    pdf.set_left_margin(30.0)
    pdf.cell(col_width, row_height,txt="", border=0)
    pdf.ln(row_height)
    # Table format
    borderValue = 0
    alignValue = 'C'
    row_height = 4 #pdf.font_size * 2
    
    for row in copy:
        for item in row:
              pdf.set_font("Arial", size=float(item.font.sz)-1.5)
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
                  if (isinstance(item.value, int) or isinstance(item.value, float)) and columnControl >= 4:
                    borderValue = 'LR'
                    alignValue = 'R'
                  if(item.value == 'TOTAL GASTOS NO COMUNES'):
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
                    else:
                      borderValue = 1
                      alignValue = 'L'
                    if (isinstance(item.value, int) or isinstance(item.value, float)) and columnControl >= 4:
                      borderValue = 1
                      alignValue = 'R'
                if item.value == None:
                  pdf.cell(col_width, row_height,txt="", border = borderValue)
                elif(str(item.value).__contains__('mailto:')): 
                  pdf.cell(col_width, row_height,txt="", border = borderValue) 
                elif(isinstance(item.value, float)):
                  auxE = int(item.value)
                  auxD = abs(int((item.value - int(item.value))*100))
                  auxS = str(auxE) + ',' + str(auxD)
                  pdf.cell(col_width, row_height,txt=auxS, border = borderValue, align = alignValue)
                elif isinstance(item.value, int) and not(columnControl == 1) and not(rowControl == 8):
                  pdf.cell(col_width, row_height,txt=str(item.value)+',00', border = borderValue, align = alignValue)
                else:
                  pdf.cell(col_width, row_height,txt=str(item.value), border = borderValue, align = alignValue)
              columnControl+=1
        columnControl=1
        rowControl += 1
        pdf.ln(row_height)
    pdf.output(outputLocation+'/Recibo '+ str(i)+'.pdf')
    