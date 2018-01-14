from flask import Flask, session, redirect, render_template, request, make_response, g, flash
from redis import Redis
import os
import socket
import random
import json


hostname = socket.gethostname()

app = Flask(__name__)

def get_redis():
    if not hasattr(g, 'redis'):
        g.redis = Redis(host="redis", db=0, socket_timeout=5)
    return g.redis

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hello Boss!  <a href='/logout'>Logout</a>"
 
@app.route('/login', methods=['POST', 'GET'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        redis = get_redis()
        session['logged_in'] = True
        username = request.form['username']
        password = request.form['password']
        data = json.dumps({'username': username, 'password': password})
        redis.rpush('loginData', data)


    else:
        flash('wrong password!')
        return home()

    resp = make_response(render_template(
        'index.html',
        hostname=hostname,
        loginData=data,
    ))
    return resp
    
 
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()
 

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
