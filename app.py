from flask import *
from flask_mail import * 
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegisterForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '!9m@S-dThyIlW[pHQbN^'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://bgvlrpiwwdaddu:98d51038aca03a85c6e564a2fb2676fbcba92c14514f73304247d98d0cff2a40@ec2-35-174-118-71.compute-1.amazonaws.com:5432/d1d0mro4faj9jl'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
app.config['MAIL_SERVER']='smtp.gmail.com'  
app.config['MAIL_PORT']=465  
app.config['MAIL_USERNAME'] = 'devanshi16.minda@gmail.com'  
app.config['MAIL_PASSWORD'] = 'kbehjtptbpvsjjjl'  
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True 

mail = Mail(app) 

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    name= db.Column(db.String(15), unique=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True, primary_key=True)
    password = db.Column(db.String(256), unique=True)
    
    
@app.route('/')
def dashboard():
    return render_template('dashboard.html')
    
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate:
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                flash('You have successfully logged in.', "success")
                session['logged_in'] = True
                session['email'] = user.email 
                session['username'] = user.username
                re = []
                re.append(user.email)
                msg = Message('Login mail', sender = 'devanshi16.minda@gmail.com', recipients = re)#['devanshi16.minda@gmail.com'])  
                msg.body = 'Hi, You have succesfully created an account.' 
                mail.send(msg) 
                return render_template('home.html',username=user.username)
            else:
                flash('Username or Password Incorrect', "Danger")
                return redirect(url_for('login'))
        else:
            flash('User not found, Please register first', "Danger")
    return render_template('login.html', form = form)


@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(
            name = form.name.data, 
            username = form.username.data, 
            email = form.email.data, 
            password = hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('You have successfully registered', 'success')
        return redirect(url_for('login'))
    else:
        return render_template('register.html', form = form)


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('dashboard'))
    
    
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
