# -*- coding: utf-8 -*-

import sqlite3
import os
from torrent import app
from flask import g

DATABASE = os.path.join(app.root_path, 'db/database.db')

def init_db():
    with app.app_context():
        db = connect_db()
        with app.open_resource('db/schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def connect_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = dict_factory
    return db

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_connection():
    db = getattr(g, '_db', None)
    if db is None:
        db = g._db = connect_db()
    return db

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, '_db'):
        g._db.close()
