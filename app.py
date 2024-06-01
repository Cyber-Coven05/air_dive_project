from flask import Flask, redirect, url_for, render_template, request, session 
from flask_sqlalchemy import SQLAlchemy
import bcrypt 

app = Flask(__name__) 
app.secret_key = "r@nd0mSk_1" 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app) 


# USER MODEL
class User(db.Model): 
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(80), unique=True, nullable=False) 
    password = db.Column(db.LargeBinary, nullable=False) 


# FUNCTION TO HASH PASSWORD
def hash_password(password): 
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    print(f"Hashed password: {hashed}")
    return hashed

# FUNCTION TO CHECK PASSWORD
def check_hashed_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

# FUNCTION TO REGISTER USER IN DATABASE
def register_user_to_db(username, password):
    hashed_password = hash_password(password)
    print(f"Storing hashed password for {username}: {hashed_password}") 
    new_user = User(username=username, password=hashed_password) 
    db.session.add(new_user)
    db.session.commit()
    print(f"Registered {username} with hashed password.")

# FUNCTION TO CHECK USER CREDENTIALS
def check_user(username, password):
    user = User.query.filter_by(username=username).first()
    print(f"Fetched hashed password from database for {username}: {user.password if user else 'User not found'}")  # Debug statement

    if user and check_hashed_password(password, user.password):
        return True
    else:
        return False

# ROUTES FOR WEBSITE PAGES
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
    return render_template('persondatapolitik.html')

@app.route("/pilot")
def pilot():
    return render_template('pilot.html')

@app.route("/seadoctor")
def seadoctor():
    return render_template('seadoctor.html')

@app.route("/tidsbestilling")
def tidsbestilling():
    return render_template('tidsbestilling.html')


# ROUTES FOR LOGIN SYSTEM
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
        if check_user(username, password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return "Username or Password is wrong!"
    else:
        return render_template('login.html')

@app.route('/home', methods=['POST', "GET"])
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/logout') 
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__': 
    with app.app_context(): 
        db.create_all() 
    app.run(debug=True) 
