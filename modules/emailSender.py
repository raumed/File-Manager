import os
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from tkinter import messagebox

def sendEmails(sender, password, subject, body, route, emails, amount, progbar):
    try:
        i = 1
        path, dirs, files = next(os.walk(route))
        file_count = len(files)
        if file_count-1 != amount:
            raise RuntimeError('La cantidad de archivos no coincide con la cantidad de remitentes')
        sesion_smtp = smtplib.SMTP('smtp.gmail.com', 587)
        sesion_smtp.starttls()
        sesion_smtp.login(sender, password)
        print('Sesion iniciada')
        for email in emails:
            attached_name = 'Recibo '+str(i)+'.pdf'
            messageFile = MIMEMultipart()
            messageFile['From'] = sender
            messageFile['To'] = email
            messageFile['Subject'] = subject
            
            messageFile.attach(MIMEText(body, 'plain'))
            fileRoute = route + '/'+ attached_name
            attached_file =  open(fileRoute, 'rb')
            attached_MIME = MIMEBase('application', 'octet-stream')
            attached_MIME.set_payload((attached_file).read())

            encoders.encode_base64(attached_MIME)
            attached_MIME.add_header('Content-Disposition', 'attachement; filename = %s' % attached_name)
            
            messageFile.attach(attached_MIME)

            
            text = messageFile.as_string()
            sesion_smtp.sendmail(sender, email, text)
            i += 1
            progbar['value'] += 100/amount
        sesion_smtp.quit()
        print("Sesion finalizada")
        messagebox.showinfo(title = 'Correcto', message="Correos enviados satisfactoriamente")
        progbar['value'] = 0
        progbar.pack_forget
    except RuntimeError:
        messagebox.showerror(title = 'Error', message ='La cantidad de recibos no coincide con la cantidad de remitentes, verifique los archivos o genere nuevamente los recibos')
        print("Unexpected error:", sys.exc_info()[0])
    except smtplib.SMTPAuthenticationError:
        messagebox.showerror(title = 'Error', message ='Error de autenticacion, verifique los datos de la cuenta')
        print("Error:", sys.exc_info()[0])
    except:
        messagebox.showerror(title = 'Error', message ='Error de conceccion')
        print("Unexpected error:", sys.exc_info()[0])


