# -*- coding: utf-8 -*-
import sqlite3 as lite
import datetime
import time
from datetime import  timedelta
from smtplib import SMTP
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

dirtobase="C:\\xampp\\apache\\RNGmini\\db.sqlite3"

con = lite.connect(dirtobase)
cur = con.cursor()
now = datetime.datetime.now()
dt = now-timedelta(seconds=5000*60)
cur.execute("select datetime,method from ImpersonalRNG_Request WHERE isdead  and datetime between '"+dt.strftime("%Y-%m-%d %H:%M:%S")+".000000' and '"+now.strftime("%Y-%m-%d %H:%M:%S")+".000000'")
data = cur.fetchall()
body = '''<html>
<head>
<title>Запросы, не дождавшиеся ответов</title>
</head>
<body>
<table border="1" cellspacing="0" cellpadding="12">
<tr>
<td width="200" height="100">Дата запроса</td>
<td>Метод</td>
</tr>'''
for d in data:
    body =body+"<tr><td>"+d[0]+"</td><td>"+d[1]+"</td></tr>"
body = body+'''
</table> 
</body>
</html>'''

COMMASPACE = ', ';
debuglevel = 0
smtp = SMTP()
smtp.set_debuglevel(debuglevel)
smtp.connect('10.4.144.41', 25)
smtp.login('f044notify', 'Notify135711')
from_addr = "f044notify@gas-kostroma.ru"
to_addr = ["O.Kashin@gas-kostroma.ru"]
msg = MIMEMultipart()
msg['Subject'] = 'Новое сообщение в голосовой почте!'+basename(pathwav[:(len(pathwav)-4)]) 
msg['From'] = from_addr
msg['To'] = COMMASPACE.join(to_addr)
msg['Body'] = body
smtp.sendmail(from_addr, to_addr, msg.as_string())
smtp.quit()
print (body)

