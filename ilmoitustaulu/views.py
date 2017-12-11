import os
import time
from random import randint
from ilmoitustaulu import app, login_manager, ALLOWED_EXTENSIONS, mail
from flask import render_template, redirect, url_for, request, session
from ilmoitustaulu.models import User, Event, UserSavedEvents
from database import db_session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
import hashlib, uuid
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
import json

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
        
        #added functionality to show users own events
        #couldnt get pinnedevents to work yet (events user has favorited) had some db issue fix later
        if current_user.is_authenticated:
                user_info = User.query.filter_by(name = current_user.name).first()
                ownevents = Event.query.filter_by(user = current_user.id).all()
                #pinnedevents = UserSavedEvents.query.filter_by(user = current_user.id).all()
                #pinnedevents = Event.query.filter_by(id = pinnedevents.event).all()
                return render_template('home.html', user_info=user_info, ownevents = ownevents)
        else:
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
				event_category = request.form['event_category']
				
				if event_category != 'bileet' and event_category != 'haat' and event_category != 'opm' and event_category != 'juhlat':
					return redirect('/')
				
				event_category[0].toUpperCase()
                #file upload works, just need to fix the paths to work on production also, anyways the main idea is here
				file = request.files['file']
				if file and allowed_file(file.filename):
                    #change name to time and random integer
					file.filename = '%s%s.%s' % (str(time.time()).replace(".", ""), randint(11111, 99999), file.filename.rsplit('.', 1)[1].lower())
					filename = secure_filename(file.filename)
                    #save file to correct folder in server
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    #save to database path to uploaded files should maybe use url_for() but easy change to be made later
					event_image = '/static/user_media/%s' % (filename)
				else:
                    #if no image attached we can have placeholder images or empty images or whatever
					event_image = '/static/media/placeholder.png'
                
                
				u = Event(event_name, event_description, current_user.id, event_price, event_location, event_image, event_category)
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
        memory = UserSavedEvents.query.filter(UserSavedEvents.user == current_user.id, UserSavedEvents.event == info.id).count()
        return render_template('event.html', info=info, memory=memory)

@app.route('/settings/<username>', methods=['GET', 'POST'])
def user_settings(username):
        
        #check authorization to go to settings        
        if User.query.filter_by(name = username).count() == 0 or current_user.name != username:
                return redirect('/')
                
        info = User.query.filter_by(name = username).first()
        
        if request.method == 'POST':
                user_email = request.form['email']
                if user_email == '' or User.query.filter_by(name=user_email).count() > 0:
                        return render_template('settings.html', info=info)
                else:
                        #if user changes email to something that isnt empty database gets updated
                        info.email = user_email
                        db_session.commit()
                        return redirect('/')
                
        
        return render_template('settings.html', info=info)

@app.route('/settings/<username>/changepassword', methods=['GET','POST'])
def user_settings_change_password(username):
        
         #if user doesnt exist or if current_user is not authorized to enter redirect to front page       
        if User.query.filter_by(name = username).count() == 0 or current_user.name != username:
                return redirect('/')
        
                
        info = User.query.filter_by(name = username).first()
        if request.method == 'POST':
                
                old_password = request.form['old-password']
                salt = info.salt
                hashed_password = hashlib.sha512(old_password + salt).hexdigest()
                if info.password != hashed_password:
                        return 'wrong password'
                elif request.form['new-password'] == '':
                        return 'no new password'
                else:
                        #create new salt and hash, init didnt work on updates for some reason
                        new_password = request.form['new-password']
                        salt = uuid.uuid4().hex
                        
                        new_password = hashlib.sha512(new_password + salt).hexdigest()
                        
                        info.salt = salt
                        info.password = new_password
                
                        db_session.commit()
                        #log user out after changing password
                        logout_user()
                        return redirect(url_for('login'))
                
        return render_template('changepassword.html', info=info)

@app.route('/login/passwordreset', methods=['GET','POST'])
def password_reset():
        if request.method == 'POST':
                user_email = request.form['email']
                #check if email exists
                if User.query.filter_by(email = user_email).count() == 0:
                        return 'Invalid email'
                #send email to user if email exists
                user_account = User.query.filter_by(email = user_email).first()
                msg = Message ('Here is password reset link', sender = 'flaskilmoitustaulu@gmail.com', recipients = [user_email])
                msg.body = "Reset link %s" % (user_account.name)
                mail.send(msg)
                return redirect('/')
                
        return render_template('forgotpassword.html')

@app.route('/search/', methods=['GET'])
def search():
	keyword = request.args.get("search")
	category = request.args.get("category")
	events = Event.query.filter(Event.name.like("%"+keyword+"%"),Event.category == category).all()
	json = '{"events":{'
	for event in events:
		json += '"'+event.name+'":{ "name":"'+ event.name + '","urlid":"' + event.urlid + '"},'
	
	json = json[:-1]

	json += '}}'
	return json

@app.route('/saveevent/<eventid>')
def saveevent(eventid):
	if (UserSavedEvents.query.filter(UserSavedEvents.user == current_user.id, UserSavedEvents.event == eventid).count() == 0):
		u = UserSavedEvents(current_user.id, eventid)
		db_session.add(u)
		db_session.commit()
		return "saved"
	else:
		UserSavedEvents.query.filter(UserSavedEvents.user == current_user.id, UserSavedEvents.event == eventid).delete()
		db_session.commit()
		return "deleted"
	return "False"
		
	
@app.route('/savedevents/')
def savedevents():
	
	eventids = UserSavedEvents.query.all()
	allids = "("
	for ids in eventids:
		allids += str(ids.event) + ","
		
	allids = allids[:-1]
	allids += ")"
	
	print allids
	#events = Event.query.filter(Event.id.in_((allids))).all()
	events = db_session.execute("SELECT * FROM events WHERE id IN "+str(allids))
	return render_template("savedevents.html", events=events)

@app.errorhandler(401)
def unauthorized(e):
        return render_template("401.html")



#just a test to check out how mailing service works
@app.route('/msgtest')
def sendmessage():
        msg = Message('Hello', sender = 'flaskilmoitustaulu@gmail.com', recipients = ['flaskilmoitustaulu@gmail.com'])
        msg.body = "Hello Flask message sent from Flask-Mail"
        mail.send(msg)
        return "Sent"