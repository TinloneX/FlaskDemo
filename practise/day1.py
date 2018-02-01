#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, session, redirect, url_for, render_template, request

app = Flask(__name__)
USERNAME = 'username'
PASSWORD = 'password'
users = {'Alex': "alex", 'Candy': "candy"}


def log(*args,**value):
    print(*args,**value)


def check_info():
    in_sys, log_ok = False, False
    if USERNAME in session and session[USERNAME] in users:
        in_sys = True
        if session[PASSWORD] == users[session[USERNAME]]:
            log_ok = True
    log('check_info',in_sys, log_ok)
    return in_sys, log_ok


@app.route('/')
def index():
    in_sys, log_ok = check_info()
    if log_ok:
        log('index, log_ok')
        return redirect(url_for('user_info'))
    else:
        log('index, going to signUp')
        return render_template('message.html', title='Homepage', message='Welcome to HomePage, Please ', href='/login/',
                               text='SignUp')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form[USERNAME]
        pwd = request.form[PASSWORD]
        if name in users and pwd == users[name]:
            session[USERNAME] = name
            session[PASSWORD] = pwd
            log('POST -- ', name, pwd)
            return redirect(url_for('user_info'))
        else:
            log('POST -- to login')
            return render_template('formTemp.html', title='Login', action='/login/', text='Login')
    else:
        log('GET -- to login')
        return render_template('formTemp.html', title='Login', action='/login/', text='Login')


@app.route('/logout/')
def logout():
    if USERNAME in session:
        session.pop(USERNAME)
        session.pop(PASSWORD)
    return redirect(url_for('login'))


@app.route('/user/info/')
def user_info():
    in_sys, log_ok = check_info()
    if log_ok:
        log('user_info , log_ok')
        return render_template('message.html', title='UserInfo', message='Welcome,%s' % session[USERNAME],href='/logout/',text='Logout')
    else:
        log('user_info , to signUp')
        return render_template('message.html', title='UserInfo', message='Wrong sign up message',
                               href='/login/', text='SignUp')


if __name__ == '__main__':
    app.debug = False
    app.secret_key = 'secret_key'
    app.run(host='0.0.0.0', port=5000)
