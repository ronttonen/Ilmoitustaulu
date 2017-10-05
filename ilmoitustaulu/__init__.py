from ilmoitustaulu.models import User, Event
from flask import Flask, session
from flask_login import LoginManager, current_user, UserMixin
from ilmoitustaulu.database import db_session



app = Flask(__name__)

app.secret_key = 'ron'

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