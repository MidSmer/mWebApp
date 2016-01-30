from flask import request, Response, render_template
from torrent import app
from torrentTool import change
from .decorator import login_required

@app.route('/get-torrent', methods=['GET', 'POST'])
@login_required
def get_torrent():
    if request.method == 'GET':
        return render_template('get-torrent.html')
    else:
        result = change.magnet2torrent(request.form['magnet'])
        if 200 != result['status']:
            return result['message']

        return Response(result['data'], headers={'Content-Type':'application/octet-stream','Content-Disposition':'filename=' + result['name'] + '.torrent'})
