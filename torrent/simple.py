# -*- coding: utf-8 -*-

from flask import request, Response, json, send_from_directory, session, make_response
from torrent import app
from .decorator import login_required
from db import sqlite
from task import torrent_task
import os

@app.route('/cgi-bin/get-user')
@login_required
def get_user():
    db = sqlite.get_connection()

    result = db.execute('select id, name from user where id = ?', (session['userId'],)).fetchone()

    if result is not None:
        resp = make_response(json.dumps({
            'code': 200,
            'message': u'获取成功',
            'data': result
        }))
        resp.headers['Content-Type'] = 'application/json'
        return resp
    else:
        del session['userId']

        resp =  make_response(json.jsonify(
            code = 400,
            message = u'获取失败'
        ))
        resp.headers['Content-Type'] = 'application/json'
        return resp

@app.route('/cgi-bin/login', methods=['POST'])
def login():
    db = sqlite.get_connection()

    userName = request.json.get('name')
    userPasw = request.json.get('password')

    if userName is None or userPasw is None:
        resp = make_response(json.jsonify(
            code = 300,
            message = u'参数错误'
        ))
        resp.headers['Content-Type'] = 'application/json'
        return resp

    result = db.execute('select id, name from user where name = ? and passwd = ?', (userName, userPasw)).fetchone()

    if result is not None:
        session['userId'] = result['id']
        session['userName'] = result['name']

        resp = make_response(json.dumps({
            'code': 200,
            'message': u'登陆成功',
            'data': result
        }))
        resp.headers['Content-Type'] = 'application/json'
        return resp
    else:
        resp = make_response(json.jsonify(
            code = 400,
            message = u'用户名或密码错误'
        ))
        resp.headers['Content-Type'] = 'application/json'
        return resp

@app.route('/cgi-bin/get-torrent/', defaults={'id': 0})
@app.route('/cgi-bin/get-torrent/<int:id>')
@login_required
def get_torrent(id):
    db = sqlite.get_connection()

    if not id:
        result = db.execute('select join_user_torrent.id, torrent.status, torrent.name, torrent.magnet from join_user_torrent \
            LEFT OUTER JOIN torrent on join_user_torrent.torrent_id = torrent.id where join_user_torrent.user_id = ?',
            (session['userId'],)).fetchall()
    else:
        result = db.execute('select join_user_torrent.id, torrent.status, torrent.name, torrent.magnet from join_user_torrent \
            LEFT OUTER JOIN torrent on join_user_torrent.torrent_id = torrent.id where join_user_torrent.user_id = ? and join_user_torrent.id = ?',
            (session['userId'], id)).fetchone()

    if result is not None:
        resp = make_response(json.dumps({
            'code': 200,
            'message': u'获取成功',
            'data': result
        }))
        resp.headers['Content-Type'] = 'application/json'
        return resp
    else:
        resp = make_response(json.jsonify(
            code = 300,
            message = u'未获取到数据'
        ))
        resp.headers['Content-Type'] = 'application/json'
        return resp

@app.route('/cgi-bin/add-torrent', methods=['POST'])
@login_required
def add_torrent():
    db = sqlite.get_connection()

    magnet = request.json.get('magnet')
    result = db.execute('select torrent.id from join_user_torrent \
        LEFT OUTER JOIN torrent on join_user_torrent.torrent_id = torrent.id where join_user_torrent.user_id = ? \
        and torrent.magnet = ?', (session['userId'], magnet)).fetchone()

    if result is None:
        cur = db.execute('insert into torrent (status, magnet) values (0, ?)', (magnet,))
        db.execute('insert into join_user_torrent (user_id, torrent_id) values (?, ?)', (session['userId'], cur.lastrowid))
        db.commit()
        torrent_task.delay(cur.lastrowid)
        resp = make_response(json.dumps({
            'code': 200,
            'message': u'添加成功',
            'data': {'id': cur.lastrowid}
        }))
        resp.headers['Content-Type'] = 'application/json'
        return resp
    else:
        resp = make_response(json.jsonify(
            code = 300,
            message = u'已存在'
        ))
        resp.headers['Content-Type'] = 'application/json'
        return resp

@app.route('/cgi-bin/del-torrent/<int:id>', methods=['DELETE'])
@login_required
def del_torrent(id):
    db = sqlite.get_connection()

    db.execute('delete from torrent where id = (\
        select id from join_user_torrent where user_id = ? and id = ?)', (session['userId'], id))
    db.execute('delete from join_user_torrent where user_id = ? and id = ?', (session['userId'], id))
    db.commit()

    resp = make_response(json.dumps({
            'code': 200,
            'message': u'删除成功',
            'data': {'id': id}
        }))
    resp.headers['Content-Type'] = 'application/json'
    return resp

@app.route('/cgi-bin/down-torrent/<int:id>')
@login_required
def down_torrent(id):
    db = sqlite.get_connection()

    result = db.execute('select torrent.id, torrent.name, torrent.torrent from join_user_torrent \
        LEFT OUTER JOIN torrent on join_user_torrent.torrent_id = torrent.id where join_user_torrent.user_id = ? \
        and torrent.status = 200 and join_user_torrent.id = ?', (session['userId'], id)).fetchone()

    if result is not None:
        return Response(result['torrent'], headers={'Content-Type':'application/octet-stream','Content-Disposition':'filename=' + result['name'] + '.torrent'})

@app.route('/cgi-bin/download/<path:filePath>')
@login_required
def get_file(filePath):
    rootPath = '/mdata/data'
    return send_from_directory(rootPath, filePath, as_attachment=True)
