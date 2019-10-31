# -*- coding: utf-8 -*-
import MySQLdb 
import datetime
import time
from datetime import  timedelta


DBHOST = "localhost"
DBUSER = "root"
DBNAME = "rngmini"
DBPASS = ""
con = MySQLdb.connect(db=DBNAME, host=DBHOST, user=DBUSER, passwd=DBPASS)
cur = con.cursor()
now = datetime.datetime.now()
dt = now-timedelta(seconds=1*60*60)
#cur.execute("delete FROM ImpersonalRNG_Request WHERE datetime < '"+dt.strftime("%Y-%m-%d %H:%M:%S")+".000000'")
#cur.execute("delete FROM ImpersonalRNG_Response WHERE datetime < '"+dt.strftime("%Y-%m-%d %H:%M:%S")+".000000'")
cur.execute("delete FROM ImpersonalRNG_Request")
cur.execute("delete FROM ImpersonalRNG_Response")
con.commit()
con.close()
print (dt.strftime("%Y-%m-%d %H:%M:%S"))
