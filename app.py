from flask import Flask, redirect, render_template,request, url_for,flash, session
import sqlite3
import GLOBAL
from Database.database import *

app = Flask(__name__)
app.config['SECRET_KEY']='SK'
@app.route('/',methods=['GET','POST'])
def index():
    if 'email' not in session:
        return redirect(url_for('signIn'))
    if request.method=='POST':
        search=request.form['search']
        return redirect(url_for('search',word=search))
    data=get_all_books()
    return render_template('index.html',data=data)

@app.route('/signUp',methods=['POST','GET'])
def signUp():
    if request.method=="POST":
        name = request.form['name']
        email = request.form['email']
        
        password = request.form['password']
        repPassword = request.form['repPassword']
        if password==repPassword:
            if insert_user(name, email, password):
                session['email']= email
            else:
                flash("User has an account with this email.")
            return redirect(url_for('index'))
        else:
            flash("Password doesn't match!!")  
            return render_template('SignUp.html') 
    else:
        return render_template('SignUp.html')

@app.route('/signIn',methods=['POST','GET'])
def signIn():
    session.clear()
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']
        if authentication(email, password):
            session['email']= email
            return redirect(url_for('index'))
        else:
            flash("Password doesn't match!!") 
            return render_template('SignIn.html')
    else:
        return render_template('SignIn.html')

@app.route('/book/<int:id>',methods=['GET','POST'])
def book(id):
    if 'email' not in session:
        return redirect(url_for('signIn'))
    data = get_book(id)
    if request.method=='POST':
        comme = request.form['comm']
        insert_comment(id, get_user_id(session['email']), comme)
    comments = get_comments(id)
    return render_template('book.html', data=data, comments=comments)
 
@app.route('/search/<word>',methods=['GET','POST'])
def search(word):
    if 'email' not in session:
        return redirect(url_for('signIn'))
    if request.method=='POST':
        search=request.form['search']
        word=search
    rows = search_book(word)
    return render_template('search.html',rows=rows)

@app.route('/about')
def about():
    return render_template('about.html')

