import smtplib
import email.mime.multipart

msg = email.mime.multipart.MIMEMultipart()
msg['to'] = "gonza337@purdue.edu"
msg['from'] = 'do-not-reply@gestureclean.com'
msg['subject'] = 'Your Experiment  information'
server = smtplib.SMTP('smtp.domain.com')
server.sendmail(msg['from'], [msg['to']], msg.as_string())
