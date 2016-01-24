from flask import request,make_response
from torrent import app
from torrentTool import change

@app.route('/get-torrent', methods=['POST'])
def get_torrent():
	result = change.magnet2torrent(request.form['magnet'])
	if 200 != result['status']:
		res = make_response(result['message'], 200)
		# res.headers['Content-Length'] = len(result['message'])
		res.headers['Content-Type'] = 'application/octet-stream'
		res.headers['Content-Disposition'] = 'attachment; filename=' + 'a.toorent'
		return res

	return result['data']
