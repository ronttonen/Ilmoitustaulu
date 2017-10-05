from ilmoitustaulu import app
from ilmoitustaulu import login_manager
from flask import render_template, redirect, url_for, request, session
from ilmoitustaulu.models import User, Event
from database import db_session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin

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

@app.route("/joel")
def joelsivu():
	return render_template("joelsivu.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		post_username = request.form['username']
		post_password = request.form['password']
		if User.query.filter_by(name=post_username).count() == 0:
			return 'wrong username'
		user = User.query.filter_by(name=post_username).first()
		if user.password != post_password:
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
                db_session.add(Event(request.form['event_name']))
                db_session.commit()
                return redirect('/')
        
        return render_template("create_event.html")

@app.route('/list_events')
def list_events():
        events = Event.query.all()
        return render_template("list_events.html", events=events)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect('/')

@app.route('/event/<eventurlid>')
def event(eventurlid):
        info = Event.query.filter_by(urlid = eventurlid).first()
        return render_template('event.html', info=info)