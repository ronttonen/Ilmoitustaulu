from ilmoitustaulu import app
from flask import render_template

@app.route('/')
def index():
	return render_template('home.html')

@app.route("/joel")
def joelsivu():
	return render_template("joelsivu.html")
