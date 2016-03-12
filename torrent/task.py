from torrent import celery
from db import sqlite
from torrentTool import change

@celery.task
def torrent_task(id):
    db = sqlite.connect_db()
    data = db.execute('select magnet from torrent where id = ?', (id,)).fetchone()
    if data is not None:
        result = change.magnet2torrent(data['magnet'])
        if 200 == result['status']:
            db.execute('update torrent set status = 200, name = ? , torrent = ? where id = ?', (result['name'], result['data'], id))
            db.commit()
