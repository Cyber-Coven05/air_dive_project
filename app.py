from flask import Flask, redirect, url_for, render_template, request, session # Flask; micro web framwork skrevet i Python
from flask_sqlalchemy import SQLAlchemy # sqlalchemy er et sql toolkit, og et ORM (object-relational mapping) bibliotek for Python
import bcrypt # bibliotek for hashing, her passwords

app = Flask(__name__) # det som gør, at flask ved hvad den skal lede efter, instansten af flask applikationen.
app.secret_key = "r@nd0mSk_1" # bruges til lave sikekr session data - nødvendig?
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # sqlalchemy, konfigurerer sqlite databasen
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # gør at tracking systemet kan spare resoucer

db = SQLAlchemy(app) # sqlalchemy objekt som intitialiseres med flask appen

# User model
class User(db.Model): # sqlalchemy, class med en model for databasen, herunder viser dem USER table i databasen
    # db.model er en sqlalchemy class som definerer strukturer og opførsel af database models i Flask-SQLAlchemy applications.
    # netop model gør, at vores User class får adgang til forskellige funktioner fra SQLAlchemy, som at definere columns, queries osv.
    id = db.Column(db.Integer, primary_key=True) # column i USER table
    username = db.Column(db.String(80), unique=True, nullable=False) # column, string på max 80, skal være unik, må ikke være null
    password = db.Column(db.LargeBinary, nullable=False) # largebianry, from at kunne oplagre større binære data, såsom hashed passwords. 
    # hashed passw. bliver typisk lagret som binær data, fordi de kan indeholde karakterer som ikke kan printes

# FUNCTION TO HASH PASSWORD
def hash_password(password): #funktion til at hashe password plaintext
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())# genererer et SALTET hash af det 
    print(f"Hashed password: {hashed}")  # Debug statement to check the hashed password
    return hashed

# FUNCTION TO CHECK PASSWORD
def check_hashed_password(password, hashed): # funktion til at tjekke om plain-textpassworded matcher det hashede password
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

# FUNCTION TO REGISTER USER IN DATABASE
def register_user_to_db(username, password): # funktion som laver et nyt user-objekt og gemmer den i databasen, ved nye brugere. Hasher passwordsene. 
    hashed_password = hash_password(password) # kalder hash_password funktionen ovenfor, passer det indtastede passrod som argument. Hash_password laver 
    # hashing af passworded, ved at bruge bcrypt, og returnerer et hash. Det hashede password gemmes i en variabel 'hashed_passwords'
    print(f"Storing hashed password for {username}: {hashed_password}")  # Debug statement, printer det givne username og hashede password, så vi kan ase at det virker
    new_user = User(username=username, password=hashed_password) # laver en ny instans af vores klasse USER, som repræsenterer en USER enhed i en database. 
    # Den initialiserer USERNAME og PASSWORD attributter af USER objektet, med den givne uasername og det hashede password.
    db.session.add(new_user) # # tilføjer USER til sessionen, fra new_user. Sessionen er en slags'plads' hvor ændringer til databasen trackes før de commites til databasen.
    db.session.commit() # comitter transationen, gemmer ændringerne til databasen. VEd at comitte transactionen, bliver new_user indsat i database tablen, associreret med USER model.
    print(f"Registered {username} with hashed password.")

# FUNCTION TO CHECK USER CREDENTIALS
def check_user(username, password): # funktion som henter USER ved username, og tjekker om det indtastede password, matcher det gemte hashed password
    user = User.query.filter_by(username=username).first()
    print(f"Fetched hashed password from database for {username}: {user.password if user else 'User not found'}")  # Debug statement

    if user and check_hashed_password(password, user.password):
        return True
    else:
        return False

# ROUTES FOR WEBSITE PAGES
@app.route("/") # routes hpndterer forskellige sider af hjemmesiden, og renderer de templates vi beder om i de forskellige funktioner
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
@app.route('/register', methods=["POST", "GET"]) # bruger POST og GET for at nå hjemmesiden?
def register(): # funktion som håndterer registrering. På POST requests, samler den username og password, registerer brugeren og videresender og til index page..
    # på GET request, renderer den registration formen.
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        register_user_to_db(username, password)
        return redirect(url_for('index'))
    else:
        return render_template('register.html')

@app.route('/login', methods=["POST", "GET"]) 
def login(): # funktion som håndterer login. På POST request tjekker den brugerens credentials, sætter session, videresender til 'home' hvis det er en succes.
    # på GET request, renderer den login form. 
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
def home(): # funktion som viser 'home' page, hvis brugeren er logget ind, ellers redirect til login page
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/logout') 
def logout(): # funktion som clearer sessionen, og redirects til index
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__': # sikrer at appen kun kører hvis scriptet executes direkte
    with app.app_context(): # gør at application context er sat op til database tables
        db.create_all()  # Create database tables ONCE, defineret af MODELS
    app.run(debug=True) # Kører flask applicationen i debug mode
    # app.run(host='0.0.0.0', debug=True)  # Uncomment if running on a server
