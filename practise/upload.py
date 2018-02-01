#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import request, Flask
import  werkzeug

app = Flask(__name__)


@app.route('/upload/',methods=['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('./static/' + werkzeug.secure_filename(f.filename))




if __name__ == '__main__':
    app.run()