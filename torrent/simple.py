# -*- coding: utf-8 -*-

from flask import request, Response, render_template, send_from_directory
from torrent import app
from torrentTool import change
from .decorator import login_required
from db import sqlite
from task import torrent_task

@app.route('/get-torrent', methods=['GET', 'POST'])
@login_required
def get_torrent():
    if request.method == 'GET':
        return render_template('get-torrent.html')
    else:
        magnet = request.form['magnet']
        db = sqlite.get_connection()

        result = db.execute('select status, name, torrent from torrent where magnet = ?', (magnet,)).fetchone()
        if result is None:
            cur = db.execute('insert into torrent (status, magnet) values (0, ?)', (magnet,))
            db.commit()
            torrent_task.delay(cur.lastrowid)
            return 'add success'
        else:
            if result['status'] != 200:
                return 'get fail'
            else:
                return Response(str(result['torrent']), headers={'Content-Type':'application/octet-stream','Content-Disposition':'filename=' + result['name'] + '.torrent'})

@app.route('/download/<path:filePath>')
@login_required
def get_file(filePath):
    rootPath = '/mdata/data'
    return send_from_directory(rootPath, filePath, as_attachment=True)
