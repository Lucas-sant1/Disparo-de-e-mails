import requests
from bs4 import BeautifulSoup
import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

# Configuração do log
logging.basicConfig(
    filename='log_envio_email.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Carrega variáveis de ambiente
load_dotenv()
remetente = os.getenv('EMAIL_USER')
senha = os.getenv('EMAIL_PASSWORD')

# Sessão para manter login
manter_cookies = requests.Session()

# Acessa a página de login e extrai o token
pagina_login = manter_cookies.get('LINK_DA_PAGINA_DE_LOGIN')
soup = BeautifulSoup(pagina_login.text, 'html.parser')
token_input = soup.find('input', {'name': '__RequestVerificationToken'})
token = token_input['value'] if token_input else None

# Dados de login
dados_login = {
    'UserName': 'usuario_exemplo',
    'Password': 'senha_exemplo'
}
if token:
    dados_login['__RequestVerificationToken'] = token

# Envia requisição de login
res_login = manter_cookies.post(
    'LINK_DO_POST_LOGIN',
    data=dados_login
)

# Função para gerar corpo do e-mail
def gerar_corpo_email(nome):
    return f"""
<!DOCTYPE html> 
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body {{
      font-family: Arial, sans-serif;
      background-color: #f9f9f9;
      margin: 0;
      padding: 0;
    }}
    .outer-container {{
      max-width: 600px;
      margin: 0 auto;
      background-color: #323232;
      border-radius: 10px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.08);
      overflow: hidden;
    }}
    .header img {{
      display: block;
      width: 100%;
      height: auto;
    }}
    .container {{
      padding: 30px;
    }}
    .title {{
      color: #1ed760;
      font-size: 22px;
      font-weight: bold;
      margin-top: 0;
    }}
    .content {{
      margin-top: 10px;
      color: #f0f0f0;
      line-height: 1.6;
    }}
    .highlight {{
      font-weight: bold;
    }}
    a {{
      color: #1ed760 !important;
      text-decoration: none;
    }}
    a:hover {{
      text-decoration: underline;
    }}
    .links a {{
      margin-right: 15px;
    }}
    .footer {{
      margin-top: 30px;
      font-size: 14px;
      color: #cccccc;
    }}
    .emoji {{
      font-size: 20px;
    }}
  </style>
</head>
<body>
  <div class="outer-container">
    <div class="header">
      <img src="https://i.imgur.com/zTfQBQl.jpeg" alt="Banner Bolão">
    </div>
    <div class="container">
      <div class="title">
        🏆 Bem-vindo ao Bolão!
      </div>
      <div class="content">
        <p>Olá <strong>{nome}</strong>,</p>

        <p>Estamos muito felizes com sua participação no <span class="highlight">nosso Bolão!</span> ⭐</p>

        <p>Aproveite para conferir nosso <span class="highlight">cardápio de campeonatos disponíveis</span>, crie seu próprio bolão e desafie seus amigos!</p>

        <p>Muitas novidades estão chegando — siga-nos nas redes sociais e fique por dentro de tudo:</p>

        <p class="links">
          <a href="#">Instagram</a> |
          <a href="#">Facebook</a>
        </p>

        <p>Quer saber mais sobre o Bolão? Acesse nosso <a href="#">site oficial</a> com campeonatos, parceiros e planos incríveis!</p>
      </div>

      <hr style="margin-top: 30px; border: none; border-top: 1px solid #444444;">

      <div class="footer">
        <p><strong>Atendimento:</strong></p>
        <p>📞 Telefone: (00) 0000-0000<br>
           📱 WhatsApp: (00) 0000-0000<br>
           📧 E-mail: <a href="mailto:contato@exemplo.com">contato@exemplo.com</a></p>

        <p style="margin-top: 20px;">Grande abraço,<br><strong>Equipe Bolão</strong></p>
      </div>
    </div>
  </div>
</body>
</html>
"""

# Configura servidor SMTP
servidor = smtplib.SMTP('smtp.gmail.com', 587)
servidor.starttls()
servidor.login(remetente, senha)

# Loop para buscar dados e enviar e-mails
for pagina in range(1, 5):  
    url = f'LINK_DA_PAGINA_DE_PARTICIPANTES?page={pagina}'
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

            assunto = 'Convite especial para nosso bolão'
            corpo = gerar_corpo_email(nome)

            mensagem = MIMEMultipart()
            mensagem['From'] = remetente
            mensagem['To'] = email
            mensagem['Subject'] = assunto
            mensagem.attach(MIMEText(corpo, 'html'))

            try:
                servidor.sendmail(remetente, email, mensagem.as_string())
                print(f'E-mail enviado para {nome} ({email})')
                logging.info(f'E-mail enviado com sucesso para {nome} - {email}')
            except Exception as e:
                print(f'Erro ao enviar para {nome} ({email}): {e}')
                logging.error(f'Erro ao enviar e-mail para {nome} - {email}: {e}')

# Encerra o servidor
servidor.quit()