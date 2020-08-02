from flask import Flask,render_template,url_for,request,redirect,session
import mysql.connector
import os

app = Flask(__name__)
app.secret_key=os.urandom(24)

conn=mysql.connector.connect(host='remotemysql.com',user="b5l0CiGJb2",password="FShP3SWVKl",database="b5l0CiGJb2")
cursor=conn.cursor()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register')
def about():
    return render_template('register.html')


@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect('/')

@app.route('/login_validation',methods=['POST'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')


    cursor.execute("""SELECT * FROM `user` WHERE `email` LIKE '{}' AND `password` LIKE '{}'"""
                   .format(email,password))
    user=cursor.fetchall()
    if len(user)>0:
        session['user_id']=user[0][0]
        email1 = request.form['email']
        return render_template('home.html',email=email1)
    else:
        return redirect('/')

@app.route('/add_user',methods=['GET','POST'])
def add_user():
    name=request.form.get('uname')
    email=request.form.get('uemail')
    password=request.form.get('upassword')

    cursor.execute("""INSERT INTO `user` (`name`,`email`,`password`) VALUES
    ('{}','{}','{}')""".format(name,email,password))
    conn.commit()
    return redirect('/')

@app.route('/upload',methods=['GET','POST'])
def upload():
    file = request.form.get('inputfile')

    cursor.execute("""INSERT INTO `photo` (`file`) VALUES
    ('{}')""".format(file))
    conn.commit()
    return "<h3>File Upload Done<h3>"

@app.route('/dropsession')
def dropsession():
    session.pop('user_id',None)
    return render_template('login.html')

if __name__=="__main__":
    app.run(debug=True)