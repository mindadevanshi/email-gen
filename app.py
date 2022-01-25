from flask import *
from flask_mail import * 


app = Flask(__name__)
 
app.config['MAIL_SERVER']='smtp.gmail.com'  
app.config['MAIL_PORT']=465  
app.config['MAIL_USERNAME'] = 'devanshi16.minda@gmail.com'  
app.config['MAIL_PASSWORD'] = 'kbehjtptbpvsjjjl'  
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True 

mail = Mail(app) 

@app.route('/')
def dashboard():
    return render_template('dashboard.html')
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with app.app_context():
            re = []
            re.append(username)
            msg = Message('Login mail', sender = 'devanshi16.minda@gmail.com', recipients = re)  
            msg.body = 'Hi, You have succesfully logged in.' 
            mail.send(msg) 
            return render_template('home.html',username=username)
    else:
        return render_template('login.html')
    

if __name__ == "__main__":
    app.run(debug=True)
