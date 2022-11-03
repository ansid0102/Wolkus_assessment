from flask import *
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re;
import requests

app = Flask(__name__)
app.config['MYSQL_HOST']='35.232.77.155'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='hari2801'
app.config['MYSQL_DB']='cinelist_db'
app.secret_key='\x96\xd5\xb1\x00\xfb>\x8b\xb6\xbc};\xccO\x0e\x04\x12\x81\x00\xe9V\x155\x00\x8b'
mysql = MySQL(app)
API_KEY='da979bab'
@app.route("/",methods=['GET','POST'])
def index():
    msg=''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username=%s AND password=%s',(username,password))
        
        account = cursor.fetchone()

        if account:
            session['loggedin']=True
            session['id']=account['id']
            session['username']=account['username']
            
            # return 'Logged in Successfully'
            return render_template('home.html',username=username)
        else:
            msg='Incorrect username/password!'
    
    return render_template('index.html',msg=msg)

@app.route("/logout")
def logout():
    session.pop('loggedin',None)
    session.pop('id',None)
    session.pop('username',None)

    return redirect(url_for('index'))

@app.route("/register",methods=['POST','GET'])
def register():
    msg=''
    
    if request.method=='POST' and 'username' in request.form and 'password' in request.form:

        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        cursor = mysql.connection.cursor()
        print(cursor)
        cursor.execute('SELECT * FROM accounts WHERE username=%s',(username,))
        account = cursor.fetchone()
        if account:
            msg='Account Already Exists'
        elif not re.match(r'[A-Za-z0-9]+',username):
            msg='Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg='Please, fill all the details'
        else:
            cursor.execute('INSERT INTO accounts VALUES(NULL,%s,%s,%s)',(username,password,email,))
            mysql.connection.commit()
            msg='You have successfully Registered'

    return render_template('register.html',msg=msg)

@app.route('/home')
def home():
    
    if 'loggedin' in session:
        # print('loggedin')
        # print(session['username'])
        print("HOME")
        
        return render_template('home.html',username=session['username'])

    return redirect(url_for('index'))

@app.route('/search',methods=['POST','GET'])
def search():
    if 'loggedin' in session:
        query = request.form.get('query')
        search_url = f'http://www.omdbapi.com/?apikey={API_KEY}&'
        print(search_url)
        search_params={
            # 'key':API_KEY,
             's':request.form.get('query'),
             'type':'movie',
             'r':'json'
        }
        global r
        r = requests.get(search_url,params=search_params)
        # print(type(r))
        return render_template('results.html',result=r.json(),query=query,username=session['username'])

@app.route('/addList',methods=['POST','GET'])
def addList():
    imdbId = request.form.get('btn')
    # msg='Added'
    # return render_template('results.html',result=search.r,msg=msg)
if __name__ == '__main__':
    app.run(debug=True)