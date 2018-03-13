from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
# set up the SMTP server


my_login = 'cborkar18@gsb.columbia.edu'
my_server = 'smtp.office365.com'
my_port = '587'









my_password = '#Fibo358132134#'

















































def send_mail(to, subject, body):
    msg = MIMEMultipart()  # create a message

    # setup the parameters of the message
    msg['From'] = my_login
    msg['To'] = to
    msg['Subject'] = subject

    # add in the message body
    msg.attach(MIMEText(body, 'plain'))

    s = smtplib.SMTP(my_server, my_port)
    s.starttls()
    s.login(my_login, my_password)

    # send the message via the server set up earlier.
    s.send_message(msg)

    del msg

    s.quit()