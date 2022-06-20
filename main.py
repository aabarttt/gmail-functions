import os
import smtplib
from dotenv import load_dotenv
from passwords import GMAIL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage


class GmailAdapter:
    def __init__(self, host: str, port: int, username: str, password: str):
        self.username = username
        self.password = password
        self.server = smtplib.SMTP_SSL(host, port)

    def login(self):
        self.server.ehlo()
        self.server.login(self.username, self.password)

    def send_mail(self, recipient_email: str, subject: str, content: str):
        message = self._compose_message(content, recipient_email, subject)
        self.server.sendmail(self.username, recipient_email, message.as_string())

    def send_mail_with_img(self, recipient_email: str, subject: str, content: str):
        ImgFileName = content
        with open(ImgFileName, 'rb') as f:
            img_data = f.read()

        message = MIMEMultipart('alternative')
        message['Subiect'] = 'Hello World!'
        message['From'] = self.username
        message['To'] = recipient_email

        image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
        message.attach(image)

        self.server.sendmail(self.username, recipient_email, message.as_string())

    def _compose_message(self, content, recipient_email, subject):
        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = self.username
        message['To'] = recipient_email
        message.attach(
            MIMEText(content, 'HTML')
        )

        return message

    def __del__(self):
        self.server.close()


load_dotenv()
mailer = GmailAdapter(
    host='smtp.gmail.com',
    port=465,
    username=GMAIL['login'],
    password=GMAIL['password']
)

mailer.login()
mailer.send_mail('RECIPIEMENT_EMAIL', 'Welcome Sir!', "Hope you are not tired enought to go to sleep ;)")
mailer.send_mail_with_img('RECIPIEMENT_EMAIL', 'img.png')

