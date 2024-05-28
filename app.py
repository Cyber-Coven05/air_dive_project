# Flask application
import sqlite3
from flask import Flask, redirect, url_for, render_template, request, session


app = Flask(__name__)
app.secret_key = "r@nd0mSk_1"

# FUNKTIONER
def register_user_to_db(username, password):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('INSERT INTO users(username,password) values (?,?)', (username, password))
    con.commit()
    con.close()


def check_user(username, password):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('Select username,password FROM users WHERE username=? and password=?', (username, password))

    result = cur.fetchone()
    if result:
        return True
    else:
        return False


# DECORATORS WEBSITE
@app.route("/")
def index():
    return render_template('forside.html')

@app.route("/base")
def base():
    return render_template('base.html')

@app.route("/forside")
def forside():
    return render_template('forside.html')

@app.route("/om")
def om():
    return render_template('om.html')

@app.route("/kontakt")
def kontakt():
    return render_template('kontakt.html')

@app.route("/dykker")
def dykker():
    return render_template('dykker.html')

@app.route("/persondatapolitik")
def persondatapolitik():
    return render_template ('persondatapolitik.html')

@app.route("/pilot")
def pilot():
    return render_template ('pilot.html')


@app.route("/seadoctor")
def seadoctor():
    return render_template ('seadoctor.html')

@app.route("/tidsbestilling")
def tidsbestilling():
    return render_template ('tidsbestilling.html')





@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        register_user_to_db(username, password)
        return redirect(url_for('index'))

    else:
        return render_template('register.html')


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(check_user(username, password))
        if check_user(username, password):
            session['username'] = username

        return redirect(url_for('base'))
    else:
        return redirect(url_for('index'))


@app.route('/login', methods=['POST', "GET"])
def home():
    if 'username' in session:
        return render_template('forside.html', username=session['username'])
    else:
        return "Username or Password is wrong!"


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('base'))


if __name__ == '__main__':
    app.run(debug=True)