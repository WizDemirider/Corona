from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
def sendmail(receiver,name,sub,mess):
    msg = MIMEMultipart()
    msg['From'] = "psycho.saiyan20@gmail.com"
    password='Abba@harmonium'
    greet = "Hey {},".format(name)
    msg['To']= receiver
    msg['Subject'] = sub
    msg.attach(MIMEText(greet))
    msg.attach(MIMEText(mess, 'html'))

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(msg['From'],password)
    s.sendmail(msg['From'],msg['To'],msg.as_string())
    s.quit()
