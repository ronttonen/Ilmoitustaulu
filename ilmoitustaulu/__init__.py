
from flask import Flask
from flask.ext.login import LoginManager
from ilmoitustaulu.database import db_session

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

import ilmoitustaulu.views
import ilmoitustaulu.database
import ilmoitustaulu.models
