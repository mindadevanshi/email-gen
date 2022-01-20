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
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        gmail_id = request.form['gmail_id']
        if username != 'abc.xyz@login.com' or password != '1234':
            error = 'Invalid Credentials. Please try again.'
        else:
            # return redirect(url_for('dashboard'))
            re = []
            re.append(gmail_id)
            msg = Message('Login mail', sender = 'devanshi16.minda@gmail.com', recipients = re)#['devanshi16.minda@gmail.com'])  
            msg.body = 'Hi, You have succesfully logged in.' 
            mail.send(msg) 
            return render_template('home.html',username=username)
    else:
        return render_template('login.html', error=error)
    

if __name__ == "__main__":
    app.run(debug=True)
