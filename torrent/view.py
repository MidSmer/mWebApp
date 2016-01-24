from flask import render_template
from torrent import app

@app.route('/')
def index_view():
	return render_template('view.html')

@app.route('/hi')
def hi_view():
	return 'hi'
