from generatePdf import simple_table
import openpyxl as xl
from fpdf import FPDF
import os
from getpass import getuser
from datetime import date

#Día actual
def createFiles(inputLocation, outputLocation = 'C:Users/'+getuser()+'/desktop/Facturas'):
  pdf = FPDF()
  today = date.today()
  aux = outputLocation
  # Crea la carpeta contenedora
  try:
    outputLocation = aux +'/'+str(today)
    os.mkdir(outputLocation)
  except:
    print("This folder already exists")
    k = 1
    flag = True
    while(flag): 
      try:
        outputLocation = aux +'/'+str(today)+'-'+str(k)
        os.mkdir(outputLocation)
        flag = False
      except:
        k += 1

  book = xl.load_workbook(inputLocation, data_only = True)
  sheetActive = book.active
  sheet2 = book.get_sheet_by_name('DIRECCION')
  cells = sheetActive['C']
  mails = []
  # Seccion que recoge todos los correos
  for cell in cells:
      if isinstance(cell.value, str):
          if cell.value.__contains__("@"):
              mails.append(cell.value)

  # Seccion que define la cabecera del documento
  header = []
  cells = sheet2['A']
  for cell in cells:
    if isinstance(cell.value, str):
      header.append(cell.value)

  # Define los limites de una hoja            
  limits = [0]
  i = 1
  cells = sheetActive['D']
  for cell in cells:
      if isinstance(cell.value, str):
          if cell.value.__contains__("NETO A PAGAR"):
              limits.append(i)
      i += 1
  copy = []
  j = len(limits)
  i = 1

  while i < j:
    lowerLimit = 'E'+ str(limits[i])
    upperLimit = 'A'+ str(limits[i-1]+1)
    cells = sheetActive[upperLimit:lowerLimit]
    copy.clear()
    for row in cells:
        copy.append([cell.value for cell in row])
    #generar documento nuevo
    rowFinal = (limits[i]-limits[i-1]+1)
    simple_table(outputLocation, header, copy, i, rowFinal)
    i += 1
  if i-1 != len(mails):
      print("La cantidad de archivos creados no coincide con la cantidad de correos existentes")  
  try:
    recivers = open(outputLocation +'/Destinatarios.txt', 'w')
    for mail in mails:
      recivers.write(mail+'\n')
    recivers.close()
  except:
    print("Error")
  return(outputLocation)