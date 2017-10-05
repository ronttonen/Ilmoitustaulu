from ilmoitustaulu import app
from flask import render_template

@app.route('/')
def index():
	return render_template('home.html')

@app.route("/joel")
def joelsivu():
	return render_template("joelsivu.html")

@app.route('/login')
def login():
	return render_template("joelsivu.html")

@app.route('/logout')
def logout():
	return render_template("joelsivu.html")

@app.route('/create_event')
def create_event():
	return render_template("joelsivu.html")

@app.route('/list_events')
def list_events():
	return render_template("joelsivu.html")