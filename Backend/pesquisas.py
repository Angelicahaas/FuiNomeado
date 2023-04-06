from selenium import webdriver
import mysql.connector
import pandas as pd
from email.mime.text import MIMEText
import smtplib

cnx = mysql.connector.connect(
    user="root",
    password="",
    host="127.0.0.1",
    database="pessoasparana"
)
cursor = cnx.cursor()

df = pd.read_csv(filepath_or_buffer='../Nomeados.csv', sep=';', header=0)

for inscricao in df['inscrição']:
    pesquisa = "SELECT email FROM pessoas WHERE inscrição = %s"
    cursor.execute(pesquisa, (inscricao,))
    resultado = cursor.fetchone()
    if resultado is not None and len(resultado) == 2 and resultado[1] is not None:
        inscricao = resultado[0]
        email = resultado[1]
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('seu_email@gmail.com', 'sua_senha_de_app')
        msg = MIMEText(f"Olá, você foi nomeado!")
        msg['Subject'] = 'Nomeado'
        msg['From'] = 'seu_email@gmail.com'
        msg['To'] = email
        server.sendmail('seu_email@gmail.com', [email], msg.as_string())
        server.quit()
    else:
        print("O email não foi cadastrado para a inscrição ", inscricao)

cursor.close()
cnx.close()
