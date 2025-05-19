import requests
from bs4 import BeautifulSoup
import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()
remetente = os.getenv('EMAIL_USER')
senha = os.getenv('EMAIL_PASSWORD')

manter_cookies = requests.Session()

pagina_login = manter_cookies.get('link_do_login')
soup = BeautifulSoup(pagina_login.text, 'html.parser')
token_input = soup.find('input', {'name': '__RequestVerificationToken'})
token = token_input['value'] if token_input else None

dados_login = {
    'UserName': 'usuario_exemplo',
    'Password': 'senha_exemplo'
}

if token:
    dados_login['__RequestVerificationToken'] = token

res_login = manter_cookies.post(
    'Link_pagina_scraping',
    data=dados_login
)

servidor = smtplib.SMTP('smtp.gmail.com', 587)
servidor.starttls()
servidor.login(remetente, senha)

for pagina in range(1, 5):
    url = f'Link_pagina_scraping={pagina}'
    res_user = manter_cookies.get(url)
    soup_user = BeautifulSoup(res_user.text, 'html.parser')
    dados_usuario = soup_user.find_all('tr', class_='gridrow')

    if not dados_usuario:
        break

    for linha in dados_usuario:
        colunas = linha.find_all('td')
        if len(colunas) >= 3:
            nome = colunas[0].text.strip()
            email = colunas[2].text.strip()

            assunto = 'Convite especial para nosso evento'
            corpo = f"""
            <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
            <div style="max-width: 600px; margin: auto; padding: 20px; 
                    border-radius: 8px; background-color: #ffffff; 
                    border: 3px solid #FFE2AA;">
            <h2 style="color: #28B463;">🏆 Bem-vindo!</h2>
            <p>Olá <strong>{nome}</strong>,</p>
            <p>Estamos muito felizes com sua participação no nosso evento!</p>
            <p>Confira as novidades e convide seus amigos!</p>
            <p>Siga-nos nas redes sociais:</p>
            <p><a href="https://www.instagram.com/exemplo/" style="color: #28B463;">Instagram</a> | 
            <a href="https://www.facebook.com/exemplo" style="color: #28B463;">Facebook</a></p>
            <p><strong><a href="https://www.seusite.com/" style="color: #28B463;">site oficial</a></strong></p>
            <hr style="margin: 20px 0;">
            <p><strong>Atendimento:</strong></p>
            <ul style="list-style: none; padding-left: 0;">
              <li>📞 Telefone: (00) 0000-0000</li>
              <li>📱 WhatsApp: (00) 0000-0000</li>
              <li>📧 E-mail: <a href="mailto:contato@seudominio.com" style="color: #28B463;">contato@seudominio.com</a></li>
            </ul>
            <p style="margin-top: 30px;">
              Grande abraço,<br>
              <strong>Equipe Organizadora</strong>
            </p>
            </div>
            </body>
            </html>
            """

            mensagem = MIMEMultipart()
            mensagem['From'] = remetente
            mensagem['To'] = email
            mensagem['Subject'] = assunto
            mensagem.attach(MIMEText(corpo, 'html'))
            servidor.sendmail(remetente, email, mensagem.as_string())
            print(f'E-mail enviado para {nome} ({email})')

servidor.quit()