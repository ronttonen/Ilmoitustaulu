from ilmoitustaulu import app
from flask import render_template, redirect, url_for, request



@app.route('/')
def index():
	return render_template('home.html')

@app.route("/joel")
def joelsivu():
	return render_template("joelsivu.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			error = 'Pls try again'
		else:
			
			return redirect(url_for('index'))
			
	return render_template("login.html", error=error)

@app.route('/logout')
def logout():
	return render_template("joelsivu.html")

@app.route('/create_event')
def create_event():
	return render_template("create_event.html")

@app.route('/list_events')
def list_events():
	return render_template("list_events.html")