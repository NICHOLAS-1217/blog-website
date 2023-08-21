from flask import Flask, redirect, render_template, request, session, url_for
from datetime import datetime
import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="nicholas",
  password="Tanzhixuan_1217",
  database = 'blogdb'
)

c = db.cursor()

app = Flask(__name__)

app.secret_key = 'heisenberg'

@app.route('/base')
def base():
    return render_template('base.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST' and 'username' in request.form and 'email' in request.form and 'password' in request.form :
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        c.execute('INSERT INTO user VALUES (NULL, %s, %s, %s)', (username, email, password))
        db.commit()
        print('register success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form.get('username')
        password = request.form.get('password')
        c.execute('SELECT * FROM user WHERE user_name = %s AND user_password = %s', (username, password))
        user = c.fetchone()
        if user:
            session['loggedin'] = True
            session['id'] = user[0]
            session['username'] = user[1]
            session['email'] = user[2]
            session['password'] = user[3]
            return redirect(url_for('home'))
        else:
            return 'nahnah'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/posts/create', methods = ['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        author_id = session.get('id')
        now = datetime.now()
        date_time = now.strftime("%d/%m/%Y, %H:%M:%S")
        c.execute('INSERT INTO post VALUES (NULL, %s, %s, %s, %s)', (title, content, author_id, date_time))
        db.commit()
        print('create success') 
    return render_template('create.html')

@app.route('/posts')
def posts():
    c.execute('SELECT * FROM post')
    posts = c.fetchall()
    return render_template('posts.html', posts = posts)

@app.route('/posts/<post_id>', methods=['GET', 'POST'])
def postdetails(post_id):   
    post_id = request.view_args['post_id']
    c.execute('SELECT * FROM post WHERE post_ID = %s', (post_id,))
    post = c.fetchone()
    c.execute('SELECT * FROM comment WHERE post_ID = %s', (post_id,))
    comments = c.fetchall()
    if request.method == 'POST' and 'comment' in request.form:
        comment_content = request.form.get('comment')
        post_ID = post_id
        user_ID = session.get('id')
        now = datetime.now()
        date_time = now.strftime("%d/%m/%Y, %H:%M:%S")
        c.execute('INSERT INTO comment VALUES (NULL, %s, %s, %s, %s)', (comment_content, post_ID, user_ID, date_time))
        db.commit()
        print('comment success') 
        return redirect(url_for('postdetails', post_id=post[0]))
    return render_template('comments.html', post=post, comments=comments)

if __name__ == '__main__':
    app.run(debug = True)