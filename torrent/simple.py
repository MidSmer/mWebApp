from flask import request,make_response
from torrent import app
from torrentTool import change

@app.route('/get-torrent', methods=['POST'])
def get_torrent():
	result = change.magnet2torrent(request.form['magnet'])
	if 200 != result['status']:
		return result['message']

	res = make_response(result['data'], 200)
	res.headers['Content-Type'] = 'application/octet-stream'
	res.headers['Content-Disposition'] = 'attachment; filename=' + 'a.toorent'
	return res
