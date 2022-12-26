from flask import Flask, redirect, render_template,request, url_for,flash, session, abort, send_file, get_flashed_messages
from Database.database import *
from CryptographyAES.AES import *
import os
import hashlib
import pyotp
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY']='SK'
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','gif'}

@app.route('/',methods=['GET','POST'])
def index():
    if 'email' not in session:
        return redirect(url_for('signIn'))
    if request.method=='POST':
        search=request.form['search']
        return redirect(url_for('search',word=search))
    data=get_all_books()
    newdata = []
    for i in data:
        i = list(i)
        if i[6] == None:
            with open(os.path.join(app.config['UPLOAD_FOLDER'], get_image(i[1])[1]), 'wb') as f:
                f.write(get_image(i[1])[2])
            i[6] = str(url_for('static', filename='uploads/'+get_image(i[1])[1]))
        newdata.append(i)
    return render_template('index.html',data=newdata)

@app.route('/signUp',methods=['POST','GET'])
def signUp():
    if request.method=="POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        repPassword = request.form['repPassword']
        credit = request.form['credit']
        credit = encrypt(credit)
        if password==repPassword:
            password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if insert_user(name, email, password, **credit):
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
    if 'email' in session:
        session.clear()
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']
        if 'wait' in session:
            delta = (datetime.now()-datetime.strptime(session['wait'], "%Y-%m-%d %H:%M:%S.%f")).total_seconds()
            if delta >= 60*10:
                session.clear()
        if 'wait' in session:
            delta = (datetime.now()-datetime.strptime(session['wait'], "%Y-%m-%d %H:%M:%S.%f")).total_seconds()
            if delta < 60*10:
                flash(f"Wrong password, you have 0 tries left. You have to wait {10-int(delta)//60} minutes.")
                return render_template('SignIn.html')
        elif email == 'admin@domain.com' and password == 'admin':
            session.clear()
            session['email'] = email
            session['admin_access'] = True
            return redirect(url_for('admin'))
        elif authentication(email, hashlib.sha256(password.encode('utf-8')).hexdigest()):
            session.clear()
            session['temp_email'] = email
            return redirect(url_for('two_factor_authentication'))
        else:
            if 'one_minute_time' not in session:
                session['one_minute_time'] = str(datetime.now())
            if (datetime.now()-datetime.strptime(session['one_minute_time'], "%Y-%m-%d %H:%M:%S.%f")).total_seconds()<60:
                if 'login_attempts' not in session:
                    session['login_attempts'] = 3
                if session['login_attempts'] > 0:
                    session['login_attempts'] -= 1
                    if session['login_attempts'] != 0:
                        flash(f"Wrong password, you have {session['login_attempts']} tries left.")
                if session['login_attempts'] == 0:
                    session['wait'] = str(datetime.now())
                    flash(f"Wrong password, you have {session['login_attempts']} tries left. You have to wait 10 minutes.")
            else:
                session.clear()
            return render_template('SignIn.html')
    else:
        return render_template('SignIn.html')

@app.route('/book/<int:id>',methods=['GET','POST'])
def book(id):
    if 'email' not in session:
        return redirect(url_for('signIn'))
    data = list(get_book(id))
    if request.method=='POST':
        comme = request.form['comm']
        insert_comment(id, get_user_id(session['email']), comme)
    comments = get_comments(id)
    if data[6] == None:
        with open(os.path.join(app.config['UPLOAD_FOLDER'], get_image(data[1])[1]), 'wb') as f:
            f.write(get_image(data[1])[2])
        data[6] = str(url_for('static', filename='uploads/'+get_image(data[1])[1]))
    return render_template('book.html', data=data, comments=comments)
 
@app.route('/search/<word>',methods=['GET','POST'])
def search(word):
    if 'email' not in session:
        return redirect(url_for('signIn'))
    if request.method=='POST':
        search=request.form['search']
        word=search
    rows = search_book(word)
    newdata = []
    for i in rows:
        i = list(i)
        if i[6] == None:
            with open(os.path.join(app.config['UPLOAD_FOLDER'], get_image(i[1])[1]), 'wb') as f:
                f.write(get_image(i[1])[2])
            i[6] = str(url_for('static', filename='uploads/'+get_image(i[1])[1]))
        newdata.append(i)
    return render_template('search.html',rows=newdata)

@app.route('/about')
def about():
    return render_template('about.html')
#admin check /admin will go to admin page not admin unathourized
@app.route('/admin')
def admin():
    if 'admin_access' not in session:
        return abort(401)
    return render_template('admin.html')
#Bath Traversl downlaod
@app.route('/admin/<path:filepath>')
def download(filepath):
    if 'admin_access' in session:
        safe_path = 'files/safe/'
        safe_path = os.path.realpath(safe_path)
        print(safe_path)
        print(os.path.realpath(filepath))
        if os.path.commonprefix((os.path.realpath(filepath),safe_path)) == safe_path:
            return send_file(filepath)
        else:
            return abort(401)
    else:
        return abort(401)
# Identification and Authentication Failure
#
@app.route('/signIn/2fa', methods=['GET', 'POST'])
def two_factor_authentication():
    if request.method == 'GET':
        secret = pyotp.random_base32()
        return render_template('twofa.html', secret=secret)
    else:
        secret = request.form.get("secret")
        otp = int(request.form.get("otp"))

        if pyotp.TOTP(secret).verify(otp):
            session['email'] = session['temp_email']
            return redirect(url_for("index"))
        else:
            flash("You have supplied an invalid 2FA token!", "danger")
            return redirect(url_for("two_factor_authentication"))
#  Security Misconfiguration only image extensions. Size limitation should be applied
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if 'admin_access' in session:
        if request.method == 'GET':
            return render_template('AddBook.html')
        else:
            book_title = request.form['book_title']
            book_author = request.form['book_author']
            book_category = request.form['book_category']
            book_stars = request.form['book_stars']
            book_description = request.form['book_description']
            book_image = request.files['book_image']
            if book_image.filename.split('.')[-1] in ALLOWED_EXTENSIONS:
                filename = secure_filename(book_image.filename)
                book_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image = None
                with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb') as f:
                    image = f.read()
                if len(image) <= 5*1024*1024:
                    insert_book(book_title, book_author, book_category, book_stars, book_description,filename, image)
                    flash("Book inserted successfully.",'success')
                else:
                    flash("Invalid Size",'danger')
            else:
                flash("Invalid Extension",'danger')
            return render_template('AddBook.html')
    else:
        return abort(401)