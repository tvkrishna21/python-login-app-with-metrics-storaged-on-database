from flask import Flask, render_template, request, redirect, url_for
# Initialize the Flask application
from flask import Response, Flask, request
import mysql.connector
import json
import prometheus_client
from prometheus_client.core import CollectorRegistry
from prometheus_client import Summary, Counter, Histogram, Gauge
import time
import os

app = Flask(__name__)

#login_var: int
#success_var=0
#fail_var=0


_INF = float("inf")

graphs = {}
graphs['t'] = Counter('python_login_requests_total', 'The total number of processed login requests')
graphs['s'] = Counter('python_login_requests_processed', 'The total number of successful login requests')
graphs['f'] = Counter('python_login_requests_failed', 'The total number of failed login requests')
graphs['h'] = Histogram('python_request_duration_seconds', 'Histogram for the duration in seconds.', buckets=(1, 2, 3, _INF))


@app.route('/')
def index():
   start = time.time()
   graphs['t'].inc()

#   global login_var
#   login_var+=1
   euser=os.getenv('MY_USER') #, 'root')
   epass=os.getenv('MY_PASS') #, 'root')
   ehost=os.getenv('MY_HOST') #, 'db')
   eport=os.getenv('MY_PORT') #, '3306')
   edb=os.getenv('MY_DB') #, 'custmet')
   
   config = {
       'user': euser,
       'password': epass,
       'host': ehost,
       'port': eport,
       'database': edb
   }
   connection = mysql.connector.connect(**config)
   cursor = connection.cursor()
   sqlo = "SELECT mtype FROM metrics WHERE mname='Login'"
#   valo = ("Login")
   cursor.execute(sqlo)
   recordo = cursor.fetchone()[0]
#   recordo = (for (mtype) in cursor)
#   cursor.close()
#   connection.close()

   recordo+=1

#   config = {
#       'user': 'root',
#       'password': passw,
#       'host': 'db',
#       'port': '3306',
#       'database': 'custmet'
#   }
#   connection = mysql.connector.connect(**config)
#   cursor = connection.cursor()
   sql = "UPDATE metrics SET mtype=%s WHERE mname=%s"
   val = (recordo, "Login")
   cursor.execute(sql, val)
   result="Success"
   connection.commit()
   cursor.close()
   connection.close()

   time.sleep(0.600)
   end = time.time()
   graphs['h'].observe(end - start)

   return render_template("log_in.html")

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST' and request.form['txtemail'] == 'vamshi@kubernetes.com' and request.form['txtpass'] == 'vamshi' :
      return redirect(url_for('success'))
   else:
      return redirect(url_for('errorlogin'))

@app.route('/success')
def success():
   start = time.time()
   graphs['s'].inc()

#   global success_var
#   success_var+=1

   euser=os.getenv('MY_USER') #, 'root')
   epass=os.getenv('MY_PASS') #, 'root')
   ehost=os.getenv('MY_HOST') #, 'db')
   eport=os.getenv('MY_PORT') #, '3306')
   edb=os.getenv('MY_DB') #, 'custmet')

   config = {
       'user': euser,
       'password': epass,
       'host': ehost,
       'port': eport,
       'database': edb
   }
   connection = mysql.connector.connect(**config)
   cursor = connection.cursor()
 
   sqlo = "SELECT mtype FROM metrics WHERE mname='Successful'"
#   valo = ("Login")
   cursor.execute(sqlo)
   recordsf = cursor.fetchone()[0]
#   recordo = (for (mtype) in cursor)
#   cursor.close()
#   connection.close()

   recordsf+=1

   sql = "UPDATE metrics SET mtype=%s WHERE mname=%s"
   val = (recordsf, "Successful")
   cursor.execute(sql, val)
   result="Success"
   connection.commit()
   cursor.close()
   connection.close()

   time.sleep(0.500)
   end = time.time()
   graphs['h'].observe(end - start)

   return '<h1>logged in successfully</h1>'

@app.route('/errorlogin')
def errorlogin():
   start = time.time()
   graphs['f'].inc()

#   global fail_var
#   fail_var+=1

   euser=os.getenv('MY_USER') #, 'root')
   epass=os.getenv('MY_PASS') #, 'root')
   ehost=os.getenv('MY_HOST') #, 'db')
   eport=os.getenv('MY_PORT') #, '3306')
   edb=os.getenv('MY_DB') #, 'custmet')

   config = {
       'user': euser,
       'password': epass,
       'host': ehost,
       'port': eport,
       'database': edb
   }
   connection = mysql.connector.connect(**config)
   cursor = connection.cursor()
 #   sql1 = "INSERT INTO favorite_colors (name, color) VALUES (%s, %s)"
 #   val1 = ("Vamsi", 18)
 #   cursor.execute(sql1, val1)

   sqlo = "SELECT mtype FROM metrics WHERE mname='Failed'"
#   valo = ("Login")
   cursor.execute(sqlo)
   recordf = cursor.fetchone()[0]
#   recordo = (for (mtype) in cursor)
#   cursor.close()
#   connection.close()

   recordf+=1

   sql = "UPDATE metrics SET mtype=%s WHERE mname=%s"
   val = (recordf, "Failed")
   cursor.execute(sql, val)
  #  results = [{name: color} for (name, color) in cursor]
   result="Success"
   connection.commit()
   cursor.close()
   connection.close()

   time.sleep(0.800)
   end = time.time()
   graphs['h'].observe(end - start)

   return '<h1>Bad Credentials. Please login again <a href = "/">login</a></h1>'

@app.route("/metrics")
def requests_count():
    res = []
    for k,v in graphs.items():
        res.append(prometheus_client.generate_latest(v))
    return Response(res, mimetype="text/plain")

@app.route('/reset')
def reset():
   start = time.time()
   graphs['t'].inc()

#   global login_var
#   login_var+=1
   euser=os.getenv('MY_USER') #, 'root')
   epass=os.getenv('MY_PASS') #, 'root')
   ehost=os.getenv('MY_HOST') #, 'db')
   eport=os.getenv('MY_PORT') #, '3306')
   edb=os.getenv('MY_DB') #, 'custmet')

   config = {
       'user': euser,
       'password': epass,
       'host': ehost,
       'port': eport,
       'database': edb
   }
   connection = mysql.connector.connect(**config)
   cursor = connection.cursor()
#   sqlo = "SELECT mtype FROM metrics WHERE mname='Login'"
#   valo = ("Login")
#   cursor.execute(sqlo)
#   recordo = cursor.fetchone()[0]
#   recordo = (for (mtype) in cursor)
#   cursor.close()
#   connection.close()

   recordo=0

#   config = {
#       'user': 'root',
#       'password': passw,
#       'host': 'db',
#       'port': '3306',
#       'database': 'custmet'
#   }
#   connection = mysql.connector.connect(**config)
#   cursor = connection.cursor()
   sql = "UPDATE metrics SET mtype=%s WHERE mname=%s"
   val = (recordo, "Login")
   cursor.execute(sql, val)
   val1=(recordo, "Successful")
   cursor.execute(sql, val1)
   val2=(recordo, "Failed")
   cursor.execute(sql, val2)
   result="Success"
   connection.commit()
   cursor.close()
   connection.close()

   time.sleep(0.600)
   end = time.time()
   graphs['h'].observe(end - start)

   return '<h1>Database Reset Successfull</h1>'

if __name__ == '__main__':
   app.run(debug = True, host='0.0.0.0')

