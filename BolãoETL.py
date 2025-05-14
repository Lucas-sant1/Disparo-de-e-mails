import pandas as pd
import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


load_dotenv()
remetente = os.getenv('EMAIL_USER')
senha = os.getenv('EMAIL_PASSWORD')


df = pd.read_csv('participanteteste.csv', sep=';')
print(df)


servidor = smtplib.SMTP('smtp.gmail.com', 587)
servidor.starttls()
servidor.login(remetente, senha)


for index, row in df.iterrows():
    destinatario = row['Email']
    nome = row['Nome']

    assunto = 'Convite especial para nosso bolão'
    corpo = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
    <div style="max-width: 600px; margin: auto; padding: 20px; 
            border-radius: 8px; background-color: #ffffff; 
            border: 3px solid #FFE2AA;">

    <img src="https://i.imgur.com/tTAs8NR.jpeg" alt="Banner" style="width: 100%; border-radius: 8px 8px 0 0;">

      <h2 style="color: #28B463;">🏆 Bem-vindo ao Bolão!</h2>

      <p>Olá <strong>{nome}</strong>,</p>

      <p>
        Estamos muito felizes com sua participação no <strong>nosso Bolão</strong>! ⭐
      </p>

      <p>
        Aproveite para conferir nosso <strong>cardápio de campeonatos disponíveis</strong>, crie seu próprio bolão e desafie seus amigos!
      </p>

      <p>
        Muitas novidades estão chegando — siga-nos nas redes sociais e fique por dentro de tudo que rola no Bolão:
      </p>

      <p>
        <a href="https://www.instagram.com/exemplo/" style="color: #28B463;">Instagram</a> | 
        <a href="https://www.facebook.com/exemplo" style="color: #28B463;">Facebook</a>
      </p>

      <p>
        Quer saber mais sobre o Bolão? Acesse nosso <strong><a href="https://www.exemplo.com.br/" style="color: #28B463;">site oficial</a></strong> com campeonatos, parceiros e planos incríveis!
      </p>

      <hr style="margin: 20px 0;">

      <p><strong>Atendimento:</strong></p>
      <ul style="list-style: none; padding-left: 0;">
        <li>📞 Telefone: (00) 0000-0000</li>
        <li>📱 WhatsApp: (00) 0000-0000</li>
        <li>📧 E-mail: <a href="mailto:contato@exemplo.com" style="color: #28B463;">contato@exemplo.com</a></li>
      </ul>

      <p style="margin-top: 30px;">
        Grande abraço,<br>
        <strong>Equipe Bolão</strong>
      </p>
    </div>
  </body>
</html>
    """

    mensagem = MIMEMultipart()
    mensagem['From'] = remetente
    mensagem['To'] = destinatario
    mensagem['Subject'] = assunto

    mensagem.attach(MIMEText(corpo, 'html'))

    servidor.sendmail(remetente, destinatario, mensagem.as_string())
    print(f'E-mail enviado para {nome} ({destinatario})')

servidor.quit()
