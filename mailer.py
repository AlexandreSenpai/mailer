import os, smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Auth:
    def __init__(self, host):
        self.host_name = host or 'gmail'
        self.host = {
            'gmail': 'smtp.gmail.com',
            'hotmail': 'imap-mail.outlook.com'
        }
        self.port = {
                        'gmail': ['465', '587']
                    }


class Mailer(Auth):
    def __init__(self, config):
        super().__init__(config.get('host'))
        self.raw_set = config
        self.config = {
            'host': None,
            'from': None,
            'to': None,
            'cc': None,
            'subject': None,
            'content': None,
        }
    
    def parse_HTML(self, config):
        try:
            with open('mailTemplate.html', 'r') as template:
                HTML = template.read().strip()
                return HTML.format(config.get('user_name'), config.get('user_id'), config.get('type'), config.get('local'), config.get('group_id'))
        except FileNotFoundError as e:
            print('Template HTML não encontrado!')

    def parse_settings(self):
        self.config['host'] = self.raw_set.get('host')
        self.config['from'] = self.raw_set.get('from')
        self.config['to'] = self.raw_set.get('to')
        self.config['cc'] = self.raw_set.get('cc')
        self.config['subject'] = self.raw_set.get('subject')

    def set_content(self, message):
        self.config['content'] = self.parse_HTML(message)

    def mail(self, user, password):
        try:
            with smtplib.SMTP_SSL(host=self.host.get(self.host_name), port=self.port[self.host.get(self.host_name)][0]) as server:
                msg = MIMEMultipart('alternative')
                msg['From'] = self.config.get('from')
                msg['To'] = self.config.get('to')
                msg['Subject'] = self.config.get('subject')
                parse = MIMEText(self.config.get('content'), 'html')
                msg.attach(parse)
                server.login(user=user, password=password)
                server.sendmail(self.config.get('from'), self.config.get('to'), msg.as_string())
                server.quit()
            print('Enviado com sucesso!')
        except Exception as e:
            print('Não foi possível enviar o e-mail!\nLog:', e)
