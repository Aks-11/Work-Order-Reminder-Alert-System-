from email.message import EmailMessage
import smtplib
import alert as al
import pandas
import datetime
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# creates SMTP session
class mail():
    def __init__(self, data,email):
        self.msg=data
        self.s = smtplib.SMTP('smtp.office365.com', 587)
        self.sender_id=""#email_id
        self.sender_password=""#password
        self.to_email=email
        self.send_mail()
        # print(email, data)

    def send_mail(self):
        # start TLS for security
        self.s.starttls()

        # Authentication
        # message=MIMEMultipart()
        self.s.login(self.sender_id,self.sender_password )
        
        # html = f"""\

        # <html>

        #   <header> Alert_Message -> " Alert " </header>

        #   <body>

          

        #     <p>New data '{self.msg}' table</p>

               


                

        #     <p>This mail is automatically generated  </p>

        #   </body>

        # </html>

        # """

 

        # part1 = MIMEText(html, 'html')

        # message.attach(part1)
        # message to be sent
        
        # message = f"""
        # Subject:Notification for work order {datetime.datetime.today()}
          
          
          
        
        # {self.msg}
        # """
        # print(message)
        
        message = EmailMessage()
        message.set_content(str(f'{self.msg}'))

        message['Subject'] =str( f"Notification for work order {datetime.datetime.today()}")
        message['From'] = "test.yuvraj@outlook.com"
        message['To'] = self.to_email
        # sending the mail
        self.s.sendmail(self.sender_id, "abssiwan@gmail.com", message.as_string())
        print("\n\n\MAIL SEND\n\n")
        # terminating the session
        self.s.quit()



