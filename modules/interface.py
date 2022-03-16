from cProfile import label
from tkinter import filedialog
import tkinter.font as tkFont
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
import os

import sys
from threading import Thread

from emailSender import sendEmails
from fileManagement import createFiles

def interface():
    # -------------------------------Definicion de frames-------------------------------
    root = Tk(className ='File manager', screenName = 'File manager', baseName = 'File manager')
    root.iconbitmap(os.path.abspath('./assets/condominio.ico'))
    root.title('Generador de recibos de condominio')
    root.geometry("800x700+50+50")
    frameMenu = Frame(root, width = 800, height = 600)
    frameA = Frame(root, width = 800, height = 600)
    frameB = Frame(root, width = 800, height = 600)
    frameMenu.pack()


    progbar = ttk.Progressbar(root, orient=HORIZONTAL, length=300, mode='determinate', value=0)

    # -------------------------------Definicion de etiquetas-------------------------------
    # Elementos del frame A
    labelA1 = Label(frameA, text = 'Ruta del archivo:', font = 'Arial')
    labelA1.place(x=120, y = 70)
    labelA2 = Label(frameA, text = 'Carpeta destino:', font = 'Arial')
    labelA2.place(x=120, y = 170)

    # Elementos del frame B
    labelB1 = Label(frameB, text = 'Ruta de los archivos:', font = 'Arial')
    labelB1.place(x=120, y = 20)
    labelB2 = Label(frameB, text = 'Usuario:', font = 'Arial')
    labelB2.place(x=120, y = 120)
    labelB3 = Label(frameB, text = 'Contraseña:', font = 'Arial')
    labelB3.place(x=120, y = 220)
    labelB4 = Label(frameB, text = 'Asunto:', font = 'Arial')
    labelB4.place(x=120, y = 320)
    labelB5 = Label(frameB, text = 'Mensaje:', font = 'Arial')
    labelB5.place(x=120, y = 420)

    # Elementos del menu
    labelM1 = Label(frameMenu, text = 'Guardar recibos como pdf:', font = 'Arial')
    labelM1.place(x=150, y = 120)
    labelM2 = Label(frameMenu, text = 'Enviar recibos:', font = 'Arial')
    labelM2.place(x=500, y = 120)


    # -------------------------------Definicion de cuadros de texto-------------------------------
    # Elementos del frame A
    textFieldA1 = Entry(frameA)
    textFieldA1.place(x = 120, y = 100, width=500)
    textFieldA2 = Entry(frameA)
    textFieldA2.place(x = 120, y = 200, width=500)

    #Elementos del frame B
    textFieldB1 = Entry(frameB)
    textFieldB1.place(x = 120, y = 50, width=500)
    textFieldB2 = Entry(frameB)
    textFieldB2.place(x = 120, y = 150, width=500)
    textfieldB3 = Entry(frameB) #, show = '*')
    textfieldB3.place(x = 120, y = 250, width=500)
    textFieldB4 = Entry(frameB)
    textFieldB4.place(x = 120, y = 350, width=500)

    messageB1 = Text(frameB)
    messageB1.place(x = 120, y = 450, width=500, height = 100)
    scrollVert = Scrollbar(frameB, command = messageB1.yview)
    scrollVert.place(x=620, y= 450, height=100)


    # -------------------------------Definicion de los eventos-------------------------------
    def fileSearch():
        root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Plantillas de excel","*.xlsm"), ("Archivos de excel","*.xlsx"),("Todos los archivos","*.*") ))
        textFieldA1.delete(0, 'end')
        textFieldA1.insert(0, root.filename)

    def routeSearchA():
        root.filename =  filedialog.askdirectory()
        textFieldA2.delete(0, 'end')
        textFieldA2.insert(0, root.filename)

    def routeSearchB():
        root.filename =  filedialog.askdirectory()
        textFieldB1.delete(0, 'end')
        textFieldB1.insert(0, root.filename)

    def saveFiles():
        if(textFieldA1.get() == "" or textFieldA2.get() == ""):
            messagebox.showwarning(title='Advertencia', message='No puede dejar los campos en blanco')
        else:
            try:
                outputLocation = createFiles(textFieldA1.get(), textFieldA2.get())
                messagebox.showinfo(title='Correcto', message = 'Archivos creados satisfactoriamente')
                frameA.pack_forget()
                frameB.pack()
                textFieldB1.delete(0, 'end')
                textFieldB1.insert(0, outputLocation) 
            except:
                messagebox.showwarning(title='Advertencia', message='Archivo no compatible')
                print("Error:", sys.exc_info()[0])
            try:
                with open('dir_cache.txt', 'w') as archivo:
                    archivo.write(textFieldA2.get())
            except:
                print('Error al crear el archivo cache')
                print("Error:", sys.exc_info()[0])

    def sendMessages():
        if(progbar['value'] == 0):
            if(textFieldB1.get() == "" or textFieldB2.get() == "" or textfieldB3.get() == ""or textFieldB4.get() == ""):
                messagebox.showwarning(title='Advertencia', message='No puede los campos en blanco')
            else:
                try:
                    recivers = open(textFieldB1.get() +'/Destinatarios.txt', 'r')
                    mails = []
                    n = 0
                    for line in recivers:
                        mails.append(line[0:line.__len__()-1])
                        n += 1
                    recivers.close()
                    if(messagebox.askokcancel(title='Advertencia', message='Esta a punto de enviar '+str(n)+' correos ¿Desea continuar?')):
                        labelProgbar = Label(frameB, text = 'Enviando...  '+str(progbar['value'])+'%', font = 'Arial')
                        labelProgbar.place(x=330, y = 580)
                        progbar.pack(pady = 20)
                        Thread(target = sendEmails, name='Email sender', args=(textFieldB2.get(),textfieldB3.get(), textFieldB4.get(), messageB1.get('1.0', END), textFieldB1.get(), mails, n, progbar, labelProgbar, buttonB1)).start()
                except:
                    messagebox.showerror(title = 'Error', message ='No se pudo encontrar a los destinatarios')
                    print("Error:", sys.exc_info()[0])
        else:
            print('Bandera creada a la perfeccion')
                

    def showFrameA():
        try:
            textFieldA2.delete(0, 'end')
            with open('dir_cache.txt', 'r') as archivo:
               textFieldA2.insert(0,archivo.read())  
        except:
            print('Error al leer el archivo cache')
            print("Error:", sys.exc_info()[0])
        frameMenu.pack_forget()
        frameB.pack_forget()
        frameA.pack()

    def showFrameB():
        frameMenu.pack_forget()
        frameA.pack_forget()
        frameB.pack()

    def showFrameMenu():
        frameA.pack_forget()
        frameB.pack_forget()
        frameMenu.pack()


    # -------------------------------Definicion de los botones-------------------------------
    # Fuente de las descripciones de los botones
    fontStyle = tkFont.Font(family="Arial", size=8)

    # Rutas usadas en varios frames
    routeG1 = os.path.abspath('./assets/back.png')
    photoG1 = PhotoImage(file = routeG1)
    photoG1 = photoG1.subsample(15, 15)

    routeG2 = os.path.abspath('./assets/folder.png')
    photoG2 = PhotoImage(file = routeG2)
    photoG2 = photoG2.subsample(18, 18)

    # Elementos del frame A

    buttonA1 = Button(frameA, image = photoG2, compound = LEFT, command = fileSearch)
    buttonA1.place(x = 640, y = 90, width = 40, height = 40)
    labelButtonA1 = Label(frameA, text = 'Buscar carpeta', font = fontStyle)
    labelButtonA1.place(x=620, y = 135)


    buttonA2 = Button(frameA, image = photoG2, compound = LEFT, command = routeSearchA)
    buttonA2.place(x = 640, y = 190, width = 40, height = 40)
    labelButtonA2 = Label(frameA, text = 'Buscar carpeta', font = fontStyle)
    labelButtonA2.place(x=620, y = 235)


    routeA2 = os.path.abspath('./assets/save.png')
    photoA2 = PhotoImage(file = routeA2)
    photoA2 = photoA2.subsample(18, 18)
    buttonA3 = Button(frameA, image = photoA2, compound = LEFT, command = saveFiles)
    buttonA3.place(x = 400, y = 300, width = 40, height = 40)
    labelButtonA3 = Label(frameA, text = 'Guardar archivos como pdf', font = fontStyle)
    labelButtonA3.place(x=348, y = 345)


    buttonA4 = Button(frameA, image = photoG1, compound = LEFT, command = showFrameMenu)
    buttonA4.place(x = 0, y = 0, width = 60, height = 60)

    # Elementos del frame B
    routeB1 = os.path.abspath('./assets/send.png')
    photoB1 = PhotoImage(file = routeB1)
    photoB1 = photoB1.subsample(18, 18)
    buttonB1 = Button(frameB, image = photoB1, compound = LEFT, command = sendMessages)
    buttonB1.place(x = 640, y = 490, width = 40, height = 40)
    labelButtonB2 = Label(frameB, text = 'Enviar', font = fontStyle)
    labelButtonB2.place(x=642, y = 535)

    buttonB2 = Button(frameB, image = photoG2, compound = LEFT, command = routeSearchB)
    buttonB2.place(x = 640, y = 40, width = 40, height = 40)
    labelButtonB2 = Label(frameB, text = 'Buscar carpeta', font = fontStyle)
    labelButtonB2.place(x=620, y = 85)

    buttonB3 = Button(frameB, image = photoG1, compound = LEFT, command = showFrameMenu)
    buttonB3.place(x = 0, y = 0, width = 60, height = 60)

    # Elementos del menu
    routeM1 = os.path.abspath('./assets/pdf.png')
    photoM1 = PhotoImage(file = routeM1)
    photoM1 = photoM1.subsample(4, 4)
    buttonM1 = Button(frameMenu, image = photoM1, command = showFrameA)
    buttonM1.place(x = 150, y = 170, width = 200, height = 200)

    routeM2 = os.path.abspath('./assets/gmail.png')
    photoM2 = PhotoImage(file = routeM2)
    photoM2 = photoM2.subsample(5, 5)
    buttonM2 = Button(frameMenu, image = photoM2, command = showFrameB)
    buttonM2.place(x = 450, y = 170, width = 200, height = 200)


    root.mainloop()

