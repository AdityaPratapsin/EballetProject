from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

DATABASE = 'userdata.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def create_tables():
    db = get_db()
    db.execute('CREATE TABLE IF NOT EXISTS userdata (name TEXT, email TEXT PRIMARY KEY, psw TEXT)')
    db.commit()

@app.route('/')
def index():
    if 'email' in session:
        return redirect(url_for('success'))
    else:
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        db = get_db()
        db.execute('INSERT INTO userdata (name, email, psw) VALUES (?, ?, ?)', (name, email, password))
        db.commit()

        flash('Registration successful, please log in')
        return redirect(url_for('login'))
    else:
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = get_db()
        user = db.execute('SELECT * FROM userdata WHERE email = ?', (email,)).fetchone()
        if user is None or user['psw'] != password:
            flash('Invalid email or password')
            return redirect(url_for('login'))
        session['name']=user['name']
        session['email'] = user['email']
        return redirect(url_for('success'))
    else:
        return render_template('login.html')

@app.route('/success')
def success():
    if 'email' in session:
        return render_template('success.html', name=session['name'])
    else:
        return redirect(url_for('login'))
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
