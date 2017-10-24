import os
import time
from random import randint
from ilmoitustaulu import app, login_manager, ALLOWED_EXTENSIONS
from flask import render_template, redirect, url_for, request, session
from ilmoitustaulu.models import User, Event
from database import db_session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
import hashlib, uuid
from werkzeug.utils import secure_filename


#check if uploaded file extension is in ALLOWED_EXTENSIONS (defined in __init__.py)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@login_manager.user_loader
def load_user(user_id):
        
        return User.query.get(user_id)


@app.route('/', methods=['GET','POST'])
def index():
	error = None
	if request.method == 'POST':
		post_username = request.form['username']
		post_email = request.form['email']
		post_password = request.form['password']
		if User.query.filter_by(name=post_username).count() > 0:
			return render_template('joelsivu.html')
		elif User.query.filter_by(email=post_email).count() > 0:
			return render_template('joelsivu.html')
		else:
			u = User(post_username, post_email, post_password)
			db_session.add(u)
			db_session.commit()
			return redirect(url_for('login'))
		
	return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		post_username = request.form['username']
		post_password = request.form['password']
		if User.query.filter_by(name=post_username).count() == 0:
			return 'wrong username'
		user = User.query.filter_by(name=post_username).first()
                salt = user.salt
                hashed_password = hashlib.sha512(post_password + salt).hexdigest()
                if user.password != hashed_password:
                        return 'wrong password'
		else:
			login_user(user, post_username)
			
			##next = app.request.args.get('next')
			##if not is_safe_url(next):
				##return flask.abort(400)
			return redirect('/')

			
	return render_template("login.html", error=error)


@app.route('/create_event', methods=['GET','POST'])
@login_required
def create_event():
        if request.method == 'POST':
                event_name = request.form['event_name']
                event_description = request.form['event_description']
                event_price = request.form['event_price']
                event_location = request.form['event_location']
                #file upload works, just need to fix the paths to work on production also, anyways the main idea is here
                file = request.files['file']
                if file and allowed_file(file.filename):
                        #change name to time and random integer
                        file.filename = '%s%s.%s' % (str(time.time()).replace(".", ""), randint(11111, 99999), file.filename.rsplit('.', 1)[1].lower())
                        filename = secure_filename(file.filename)
                        #save file to correct folder in server
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        #save to database path to uploaded files should maybe use url_for() but easy change to be made later
                        event_image = '/static/media/%s' % (filename)
                else:
                        #if no image attached we can have placeholder images or empty images or whatever
                        event_image = '/PATH/TO/PLACE/HOLDER'
                
                
                u = Event(event_name, event_description, current_user.id, event_price, event_location, event_image)
                db_session.add(u)
                db_session.commit()
                e = Event.query.filter_by(user=current_user.id).all()
                e=e[-1]
                return redirect('/event/%s' %(str(e.urlid)))
        
        
        
        return render_template("create_event.html")

#here we list eventws

@app.route('/list_events', methods=['GET', 'POST'])
def list_events():
        if request.method == 'POST':
                if current_user.id != None:
                        event = request.form['event_id']
                        db_session.add(current_user.id, event)
                        db_session.commit()
        events = Event.query.all()
        return render_template("list_events.html", events=events)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect('/')

@app.route('/event/<eventurlid>')
def event(eventurlid):
        
        if Event.query.filter_by(urlid = eventurlid).count == 0:
                return redirect('/')
        
        info = Event.query.filter_by(urlid = eventurlid).first()
        
        return render_template('event.html', info=info)

@app.route('/settings/<username>', methods=['GET', 'POST'])
def user_settings(username):
        
                
        if User.query.filter_by(name = username).count() == 0:
                return redirect('/')
                
        info = User.query.filter_by(name = username).first()
        
        if request.method == 'POST':
                user_email = request.form['email']
                if user_email == '' or User.query.filter_by(name=user_email).count() > 0:
                        return render_template('settings.html', info=info)
                else:
                        info.email = user_email
                        db_session.commit()
                        return redirect('/')
                
        
        return render_template('settings.html', info=info)

@app.route('/settings/<username>/changepassword', methods=['GET','POST'])
def user_settings_change_password(username):
        
                
        if User.query.filter_by(name = username).count() == 0:
                return redirect('/')
        
                
        info = User.query.filter_by(name = username).first()
        if request.method == 'POST':
                old_password = request.form['old-password']
                salt = info.salt
                hashed_password = hashlib.sha512(old_password + salt).hexdigest()
                if info.password != hashed_password:
                        return 'wrong password'
                else:
                        new_password = request.form['new-password']
                        salt = uuid.uuid4().hex
                        
                        new_password = hashlib.sha512(new_password + salt).hexdigest()
                        
                        info.salt = salt
                        info.password = new_password
                
                        db_session.commit()
                        logout_user()
                        return redirect(url_for('login'))
                
        return render_template('changepassword.html', info=info)


@app.errorhandler(401)
def unauthorized(e):
        return render_template("401.html")


