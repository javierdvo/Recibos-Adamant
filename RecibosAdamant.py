import csv
import numpy as np
import datetime
from pyjasper.jasperpy import JasperPy
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import sys


def send_mail(send_from, send_to, subject, text, filename, filepath, password):
    msg = MIMEMultipart()

    msg['From'] = send_from
    msg['To'] = send_to
    msg['Subject'] = subject
    body = text
    msg.attach(MIMEText(body, 'plain'))
    attachment = open(filepath, "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(send_from, password)
    text = msg.as_string()
    server.sendmail(send_from, send_to, text)
    server.quit()


def processing(numDpto, gas, agua, dia, mesS, ano, lectAnt, lectAct, cons, total,MonthReal,YearReal,MonthNextReal,YearNextReal):
    if getattr(sys, 'frozen', False):
        input_file = os.path.dirname(sys.executable) + \
                     '\\reciboAdamant.jrxml'
        output = os.path.dirname(sys.executable) + \
                 '\\Recibos'
        photo1 = os.path.dirname(sys.executable) + \
                 '\\adamant1.jpg'
        photo2 = os.path.dirname(sys.executable) + \
                 '\\adymco.jpg'
    else:
        input_file = os.path.dirname(os.path.abspath(__file__)) + \
                     '\\reciboAdamant.jrxml'
        output = os.path.dirname(os.path.abspath(__file__)) + \
                 '\\Recibos'
        photo1 = os.path.dirname(os.path.abspath(__file__)) + \
                 '\\adamant1.jpg'
        photo2 = os.path.dirname(os.path.abspath(__file__)) + \
                 '\\adymco.jpg'
    jasper = JasperPy()
    jasper.process(
        input_file, output_file=output, format_list=["pdf"],
        parameters={"Departamento": numDpto, "Gas": gas, "Agua": agua, "Date": dia, "Month": mesS, "Year": ano,
                    "LectAntGas": lectAnt, "LectActGas": lectAct, "photo1": photo1, "photo2": photo2, "ConsGas": cons,
                    "Total": total,
                    "MonthReal": MonthReal,
                    "MonthNextReal": MonthNextReal,
                    "YearReal": YearReal,
                    "YearNextReal": YearNextReal})

def processingPago(numDpto, gas, agua, dia, mesS, ano, lectAnt, lectAct, cons, total,MonthReal,YearReal):
    if getattr(sys, 'frozen', False):
        input_file = os.path.dirname(sys.executable) + \
                     '\\pagoAdamant.jrxml'
        output = os.path.dirname(sys.executable) + \
                 '\\Recibos'
        photo1 = os.path.dirname(sys.executable) + \
                 '\\adamant1.jpg'
        photo2 = os.path.dirname(sys.executable) + \
                 '\\adymco.jpg'
    else:
        input_file = os.path.dirname(os.path.abspath(__file__)) + \
                     '\\pagoAdamant.jrxml'
        output = os.path.dirname(os.path.abspath(__file__)) + \
                 '\\Recibos'
        photo1 = os.path.dirname(os.path.abspath(__file__)) + \
                 '\\adamant1.jpg'
        photo2 = os.path.dirname(os.path.abspath(__file__)) + \
                 '\\adymco.jpg'
    jasper = JasperPy()
    jasper.process(
        input_file, output_file=output, format_list=["pdf"],
        parameters={"Departamento": numDpto, "Gas": gas, "Agua": agua, "Date": dia, "Month": mesS, "Year": ano,
                    "LectAntGas": lectAnt, "LectActGas": lectAct, "photo1": photo1, "photo2": photo2, "ConsGas": cons,
                    "Total": total,
                    "MonthReal": MonthReal,
                    "YearReal": YearReal})

def mesStr(mes):
    if mes == 1:
        mesStr = "Enero"
    elif mes == 2:
        mesStr = "Febrero"
    elif mes == 3:
        mesStr = "Marzo"
    elif mes == 4:
        mesStr = "Abril"
    elif mes == 5:
        mesStr = "Mayo"
    elif mes == 6:
        mesStr = "Junio"
    elif mes == 7:
        mesStr = "Julio"
    elif mes == 8:
        mesStr = "Agosto"
    elif mes == 9:
        mesStr = "Septiembre"
    elif mes == 10:
        mesStr = "Octubre"
    elif mes == 11:
        mesStr = "Noviembre"
    else:
        mesStr = "Diciembre"
    return mesStr


def init():
    condoInit = list()
    with open("recibosAdamant.csv") as csvfile:
        iterator = csv.reader(csvfile)
        for row in iterator:
            insert = False
            for a in row:
                if a != '':
                    insert = True
            if insert:
                condoInit.append(row)
    condoArr = np.array(condoInit)
    i = 0
    titlesPresent = condoArr[0][condoArr[0] != '']
    if np.unique(titlesPresent, return_counts=True)[1].sum() != len(np.unique(titlesPresent)):
        print("Favor de asegurarse de que no hay campos repetidos\n")
        input("Presione enter para cerrar...")
        quit()
        # Agregar Break

    for a in titlesPresent:
        titlesPresent[i] = str.lower(a)
        i += 1
    titlesExpected = ["departamento", "email principal", "email secundario", "email alternativo", "consumo de gas",
                      "consumo de agua", "año",
                      "mes", "enviado", "lectura anterior gas", "lectura actual gas"]
    titleIds = np.zeros(len(titlesExpected))
    i = 0
    missing = False
    for b in range(len(titlesExpected)):
        try:
            titleIds[i] = int(np.where(titlesPresent == titlesExpected[i])[0][0])
        except:
            missing = True
            print("Falta el campo de " + titlesExpected[i] + "\n")
        i += 1
    if missing:
        input("Presione enter para cerrar...")
        quit()
    return condoArr, titlesPresent, titleIds


def genPDFs(array, titleIds, view, months):
    month = mesStr(int(datetime.date.today().month))
    year = str(int(datetime.date.today().year))
    day = str(int(datetime.date.today().day))
    file = open("login.txt", "r")
    email = file.readline()
    password = file.readline()
    for row in array:
        if months:
            monthReal = mesStr(int(row[int(titleIds[7])]))
            yearReal = str(row[int(titleIds[6])])
            if (int(row[int(titleIds[7])]) == 12):
                monthnextReal = mesStr(1)
                yearnextReal = str(int(row[int(titleIds[6])]) + 1)
            else:
                monthnextReal = mesStr(int(row[int(titleIds[7])]) + 1)
                yearnextReal = yearReal
        email1 = str(row[int(titleIds[1])])
        email2 = str(row[int(titleIds[2])])
        email3 = str(row[int(titleIds[3])])
        dept = str(row[int(titleIds[0])])


        gas = "${0:.0f}".format(row[int(titleIds[4])].astype(float))
        agua = "${0:.0f}".format(row[int(titleIds[5])].astype(float))
        lectAnt = "%i".format(row[int(titleIds[9])].astype(int))
        lectAct = "%i".format(row[int(titleIds[10])].astype(int))
        cons = "{0:.0f} dm3".format(row[int(titleIds[10])].astype(float) - row[int(titleIds[9])].astype(float))
        total = "${0:.0f}".format(row[int(titleIds[4])].astype(float) + row[int(titleIds[5])].astype(float))

        gas = "${0:.0f}".format(row[int(titleIds[4])].astype(float))
        agua = "${0:.0f}".format(row[int(titleIds[5])].astype(float))
        lectAnt = "{0} dm3".format(row[int(titleIds[9])].astype(int))
        lectAct = "{0} dm3".format(row[int(titleIds[10])].astype(int))
        cons = "{0} dm3".format(row[int(titleIds[10])].astype(int) - row[int(titleIds[9])].astype(int))
        total = "${0:.0f}".format(row[int(titleIds[4])].astype(float) + row[int(titleIds[5])].astype(float))

        processing(dept, gas, agua, day, month, year, lectAnt, lectAct, cons, total,monthReal,yearReal,monthnextReal,yearnextReal)
        if getattr(sys, 'frozen', False):
            newStr = os.path.dirname(sys.executable) + \
                     '\\Recibos\\Recibo ' + dept + ' ' + monthReal + ' ' + yearReal + '.pdf'
            name = 'Recibo ' + dept + ' ' + monthReal + ' ' + yearReal + '.pdf'
            pdfpath = os.path.dirname(sys.executable) + \
                  '\\Recibos\\reciboAdamant.pdf'
        else:
            # unfrozen
            newStr = os.path.dirname(os.path.abspath(__file__)) + \
                     '\\Recibos\\Recibo ' + dept + ' ' + monthReal + ' ' + yearReal + '.pdf'
            name = 'Recibo ' + dept + ' ' + monthReal + ' ' + yearReal + '.pdf'
            pdfpath = os.path.dirname(os.path.abspath(__file__)) + \
                      '\\Recibos\\reciboAdamant.pdf'

        if (view == True):
            os.system(pdfpath)
            os.remove(pdfpath)
        else:
            try:
                os.remove(newStr)
            except OSError:
                pass

            os.rename(pdfpath, newStr)
            text = "Estimado condómino de Adamant " + dept + ":\n\nLe adjuntamos su recibo de servicios del mes de " + monthReal + " de "+ yearReal+" por un total de " + total + "\nQuedamos a su disposición por cualquier duda que tenga\n\nAtentamente,\nCobranzas Adamant"
            try:
                send_mail(email, email1, "Recibo de Servicios Adamant " + monthReal+" de "+yearReal, text, name, newStr, password)
            except:
                print("Error al enviar el email al condominio " + dept + " con email " + email1)
            if (email2 != ''):
                try:
                    send_mail(email, email2, "Recibo de Servicios Adamant " + monthReal+" de "+yearReal, text, name, newStr, password)
                except:
                    print("Error al enviar el email al condominio " + dept + " con email " + email2)
            if (email3 != ''):
                try:
                    send_mail(email, email3, "Recibo de Servicios Adamant " + monthReal+" de "+yearReal, text, name, newStr, password)
                except:
                    print("Error al enviar el email al condominio " + dept + " con email " + email3)


def viewPDF(row, titleIds,months):
    month = mesStr(int(datetime.date.today().month))
    year = str(int(datetime.date.today().year))
    day = str(int(datetime.date.today().day))
    if months:
        monthReal = mesStr(int(row[int(titleIds[7])]))
        yearReal = str(row[int(titleIds[6])])
        if(int(row[int(titleIds[7])])==12):
            monthnextReal =mesStr(1)
            yearnextReal =str(int(row[int(titleIds[6])])+1)
        else:
            monthnextReal = mesStr(int(row[int(titleIds[7])])+1)
            yearnextReal = yearReal
    else:
        monthReal = month
        yearReal = year
    dept = str(row[int(titleIds[0])])

    gas = "${0:.0f}".format(row[int(titleIds[4])].astype(float))
    agua = "${0:.0f}".format(row[int(titleIds[5])].astype(float))
    lectAnt = "{0} dm3".format(row[int(titleIds[9])].astype(int))
    lectAct = "{0} dm3".format(row[int(titleIds[10])].astype(int))
    cons = "{0} dm3".format(row[int(titleIds[10])].astype(int) - row[int(titleIds[9])].astype(int))
    total = "${0:.0f}".format(row[int(titleIds[4])].astype(float) + row[int(titleIds[5])].astype(float))

    processing(dept, gas, agua, day, month, year, lectAnt, lectAct, cons, total,monthReal,yearReal,monthnextReal,yearnextReal)
    if getattr(sys, 'frozen', False):
        newStr = os.path.dirname(sys.executable) + \
                 '\\Recibos\\ReciboEjemplo.pdf'
        pdfpath = os.path.dirname(sys.executable) + \
                  '\\Recibos\\reciboAdamant.pdf'
    else:
        # unfrozen
        newStr = os.path.dirname(os.path.abspath(__file__)) + \
                 '\\Recibos\\ReciboEjemplo.pdf'
        pdfpath = os.path.dirname(os.path.abspath(__file__)) + \
                  '\\Recibos\\reciboAdamant.pdf'
    removed = True
    while (removed):
        try:
            os.remove(newStr)
            removed = False
        except OSError:
            input("Asegurese de que no tenga abierto ningún archivo de Recibos, y dele enter al cerrarlos")
    os.rename(pdfpath, newStr)
    os.system(newStr)


while True:
    print("Hola! ¿Qué deseas hacer hoy?\n")
    print("[1] Enviar los recibos de este mes a todos")
    print("[2] Salir\n")
    try:
        method = int(input("Escribe el número que deseas y dale click a enter:\n"))
    except:
        print("\nNo ingresaste un número")
        method=0
    if method == 2:
        print("Adiós!")
        quit()
    elif method == 1:
        condoArr, titlesPresent, titleIds = init()
        month = int(datetime.date.today().month)
        year = int(datetime.date.today().year)
        validRows = np.zeros(len(condoArr))
        monthRows = np.zeros(len(condoArr))
        i = 0
        for row in condoArr[1:]:
            valid = True
            for a in titleIds:
                if row[int(a)] == '' and a != int(titleIds[2]) and a != int(titleIds[3]):
                    valid = False
                    thisRun = True
                    if a == 0:
                        print("Para la fila número " + str(i + 1) + " falta el número de departamento ")
                        thisRun = False
                    if thisRun:
                        print("Para el departamento " + str(row[int(titleIds[0])]) + " falta el campo " + titlesPresent[
                            int(a)])
            if valid:
                validRows[i + 1] = 1
                if row[int(titleIds[8])].lower() == "no":
                    monthRows[i + 1] = 1
            i += 1
        print("\nSe encontraron " + str(int(sum(validRows))) + " registros completos y " + str(
            int(len(validRows) - sum(validRows)) - 1) + " registros con campos vacíos")
        print("De estos " + str(int(sum(validRows))) + " registros completos se tienen " + str(
            int(sum(monthRows))) + " marcados como no enviados")
        print("¿Qué deseas realizar?\n")
        done = False
        while not done:
            print("\n[1] Enviar los recibos automáticamente")
            print("[2] Ver un ejemplo de como quedaría un recibo")
            print("[3] Ver todos los recibos")
            print("[4] Revisar la lista de condominios a enviar junto con sus respectivos montos")
            print("[5] Actualizar el Listado")
            print("[6] Regresar al menú principal")
            print("[7] Salir de la aplicación\n")
            try:
                select = int(input("Escribe el número que deseas y dale click a enter:\n"))
            except:
                print("\nNo ingresaste un número")
                select = 0
            if select == 6:
                done = True
            elif select == 7:
                print("Adiós!")
                quit()
            elif select == 5:
                condoArr, titlesPresent, titleIds = init()
                month = int(datetime.date.today().month)
                year = int(datetime.date.today().year)
                validRows = np.zeros(len(condoArr))
                monthRows = np.zeros(len(condoArr))
                i = 0
                for row in condoArr[1:]:
                    valid = True
                    for a in titleIds:
                        if row[int(a)] == '' and a != int(titleIds[2]) and a != int(titleIds[3]):
                            valid = False
                            thisRun = True
                            if a == 0:
                                print("Para la fila número " + str(i + 1) + " falta el número de departamento ")
                                thisRun = False
                            if thisRun:
                                print("Para el departamento " + str(row[int(titleIds[0])]) + " falta el campo " +
                                      titlesPresent[
                                          int(a)])
                    if valid:
                        validRows[i + 1] = 1
                        if row[int(titleIds[8])].lower() == "no":
                            monthRows[i + 1] = 1
                    i += 1
                print("\nSe encontraron " + str(int(sum(validRows))) + " registros completos y " + str(
                    int(len(validRows) - sum(validRows) - 1)) + " registros con campos vacíos")
                print("De estos " + str(int(sum(validRows))) + " registros completos se tienen " + str(
                    int(sum(monthRows))) + " marcados como no enviados")
                print("¿Qué deseas realizar?\n")
            elif select == 4:
                if (int(sum(monthRows)) >0 ):
                    print("\nLos registros a enviar son los siguientes \n")
                    for row in condoArr[monthRows == 1]:
                        print("Al departamento " + str(row[int(titleIds[0])]) + " se le van a cobrar $" + str(
                            row[int(titleIds[4])]) + " de gas y $" + str(row[int(titleIds[5])]) + " de agua")
                else:
                    print("\nNo hay ningún registro que mostrar!")
            elif select == 1:
                if (int(sum(monthRows)) >0 ):
                    print("\nEnviando sus recibos, tenga paciencia")
                    genPDFs(condoArr[monthRows == 1], titleIds, False,True)
                    saved = False
                    condoArrNew = condoArr.copy()
                    condoArrNew[monthRows == 1, int(titleIds[8])] = 'Si'
                    while (saved == False):
                        try:
                            np.savetxt("recibosAdamant.csv", condoArrNew.astype(str), delimiter=',', fmt="%s")
                            saved = True
                        except:
                            input("\nPor Favor cierre el archivo de Recibos de Adamant y de enter")
                    print("\nListo! Se han enviado tus recibos. Puedes ver una copia en la carpeta de Recibos")
                else:
                    print("\nNo hay ningún registro que enviar!")
            elif select == 2:
                if (int(sum(monthRows)) >0 ):
                    print("\nMostrando un ejemplo")
                    viewPDF(condoArr[np.unique(monthRows == 1, return_index=True)[1][1]], titleIds,True)
                else:
                    print("\nNo hay ningún registro que mostrar!")
            elif select == 3:
                if (int(sum(monthRows)) >0 ):
                    print("\nMostrando sus recibos")
                    genPDFs(condoArr[monthRows == 1], titleIds, True,True)
                else:
                    print("\nNo hay ningún registro que mostrar!")
            else:
                print("\nPor favor indique una opción válida")

    else:
        print("Elección inválida\n")
