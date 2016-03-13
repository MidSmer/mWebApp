# -*- coding: utf-8 -*-

from flask import Flask
from celery import Celery

app = Flask(__name__)

app.secret_key = '\xa2\xd7\xb4\xb4\xeb\xd6\x06\x87h\xe6\xab\xf8\xcd0\xea\x05\xa9\xcc\xed\xa2\x90\x95e\xe9\xb2\xa6\xd1\xe4\xb6\xe4\xf5\xd0'

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

import view
import simple
import db.sqlite
