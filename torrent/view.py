from flask import render_template, request, session, redirect, url_for
from torrent import app

@app.route('/')
def index_view():
	return render_template('view.html')

@app.route('/login', methods=['GET', 'POST'])
def login_view():
	if request.method == 'POST':
		if 'mweb' == request.form['name']:
			session['userName'] = request.form['name']

	if 'userName' in session:
		return redirect(url_for('get_torrent'))

	return render_template('login.html')
