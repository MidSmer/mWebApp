from flask import request, Response
from torrent import app
from torrentTool import change

@app.route('/get-torrent', methods=['POST'])
def get_torrent():
	result = change.magnet2torrent(request.form['magnet'])
	if 200 != result['status']:
		return result['message']

	return Response(result['data'], headers={'Content-Type':'application/octet-stream','Content-Disposition':'filename=' + result['name'] + '.torrent'})
