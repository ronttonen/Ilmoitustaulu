from ilmoitustaulu.models import User, Event, UserSavedEvents
from flask import Flask, session
from flask_login import LoginManager, current_user, UserMixin
from ilmoitustaulu.database import db_session
from flask_mail import Mail, Message


#maili tili flaskilmoitustaulu@gmail.com // kikkeli15!
app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'flaskilmoitustaulu@gmail.com'
app.config['MAIL_PASSWORD'] = 'kikkeli15!'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail=Mail(app)





app.secret_key = 'ron'

UPLOAD_FOLDER = '/home/ron/Ilmoitustaulu/ilmoitustaulu/static/media'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

login_manager = LoginManager()
login_manager.init_app(app)



    
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.cli.command('initdb')
def initialize_db_command():
    from ilmoitustaulu.database import init_db
    init_db()
    print('Database initialized')

import ilmoitustaulu.database
import ilmoitustaulu.models
import ilmoitustaulu.views