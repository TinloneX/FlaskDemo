#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
engine = create_engine("mysql+pymysql://root:password@127.0.0.1:3306/test?charset=utf8", max_overflow=5)
Base = declarative_base()
session_db = sessionmaker(bind=engine)()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    username = Column(String, nullable=False)
    age = Column(Integer())
    salary = Column(Float(8, 2))
    pid = Column(Integer())

    def info(self):
        return {'id': self.id, 'username': self.username, 'age': int(self.age), 'salary': float(self.salary)}


def response2(state=0, message='error', data=None):
    return jsonify({'state': state, 'message': message, 'data': data})


def safe_insert(user=None, username='Alex'):
    users = session_db.quary(User).all()
    for u in users:
        if u.username == username:
            return -1, '用户名已存在'
    if user is None:
        return -2, '用户信息不存在'
    try:
        session_db.add(user)
        return 1, '添加用户成功'
    except Exception as ignore:
        print(ignore)
        return -3, '添加用户失败'


def json_array(datas):
    L = []
    for d in datas:
        L.append(d.info())
    return L


@app.route('/users/', methods=['GET', 'POST'])
def users_about():
    if request.method == 'GET':
        datas = session_db.query(User).all()
        return response2(1, 'success', json_array(datas))
    else:
        name = request.values.get('username')
        sly = request.values.get('salary')
        nuser = User(username=name, salary=sly, pid=0)
        code, message = safe_insert(nuser, name)
        return response2(code, message, None)


if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=5000)
