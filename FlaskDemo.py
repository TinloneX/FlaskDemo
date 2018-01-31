from flask import Flask, request, session, redirect, render_template, url_for

app = Flask(__name__)
users = {'Alex': "alex", 'Bob': "bob", 'Candy': "candy"}
USER_NAME = 'username'
PASSWORD = 'password'


def check_user():
    """验证账户是否登录过,是否在用户系统中,登录信息是否正确"""
    if USER_NAME in session:
        if session[USER_NAME] in users:
            if session[PASSWORD] == users[session[USER_NAME]]:
                return True, True, True
            else:
                return True, True, False
        else:
            return True, False, False
    else:
        return False, False, False


@app.route('/homepage/')
@app.route('/')
def hello_world():
    loged, insys, logok = check_user()
    if logok:
        return render_template('message.html', title='Hello', name=session[USER_NAME])
    elif insys:
        return render_template('formtemp.html', titlt='Login', rout='login', message='登录信息已过期')
    else:
        return redirect(url_for('login'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form[USER_NAME]
        password = request.form[PASSWORD]
        print(name, password)
        if name in users and password == users[name]:
            session[USER_NAME] = name
            session[PASSWORD] = password
            return render_template('message.html', title='Hello', name=name)
    return render_template('formtemp.html', titlt='Login', rout='login')


@app.route('/sign/', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        name = request.form[USER_NAME]
        password = request.form[PASSWORD]
        print(name, password)
        if name in users:
            return render_template('formtemp.html',
                                   title='SignIn', rout='sign',
                                   message='用户名%s已被注册,您可以试下%s2' % (name, name))
        else:
            if password is not None:
                users[name] = password
                session[USER_NAME] = name
                session[PASSWORD] = password
                return redirect(url_for('hello_world'))
            else:
                return render_template('formtemp.html',
                                       title='SignIn', rout='sign',
                                       message='密码不能为空')
    else:
        return render_template('formtemp.html',
                                       title='SignIn', rout='sign')


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'this is a key'
    app.run()
