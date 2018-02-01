#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime

from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker
import json

app = Flask(__name__)
engine = create_engine("mysql+pymysql://root:password@127.0.0.1:3306/test?charset=utf8", echo=True, max_overflow=5)
Base = declarative_base()
DBSession = sessionmaker(bind=engine)
session = DBSession()


class User(Base):
    __tablename__ = 'puser'

    id = Column(String(20), primary_key=True)
    name = Column(String(20), nullable=False)

    def info(self):
        return {"id": self.id, "name": self.name}


class Book(Base):
    __tablename__ = 'book'

    id = Column(String(20), primary_key=True)
    name = Column(String(20))
    user_id = Column(String(20), ForeignKey('user.id'))

    def info(self):
        return {"id": self.id, "name": self.name, "user_id": self.user_id}


@app.route('/book/list', methods=['GET'])
def get_book():
    if not request.args or 'id' not in request.args:
        return jsonify({'state': 1, 'message': "fail", "data": {}})
    else:
        books = list(session.query(Book).all())
        data = []
        for book in books:
            data.append(book.info())
        try:
            return jsonify({'state': 1, 'message': "success", "data": data})
        except Exception as e:
            return jsonify({'state': 1, 'message': "fail", "data": {}})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    # for book in session.query(Book).all():
    #     print(book.info())
