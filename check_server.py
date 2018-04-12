# -*- coding: utf-8 -*-
from flask import Flask, redirect, url_for, request, flash, render_template  
# from flask_login import LoginManager, login_user, login_required, logout_user
from flask_cors import *
import os

app = Flask(__name__)
CORS(app, supports_credentials=True)

code_id = ''

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():

    global code_id

    if request.method == 'POST':
        code_id = request.form['code_id']
        print code_id
        file_path = '/Users/MrM/Desktop/' + code_id + '/'
        
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        print request.files

        for file in request.files:
            file_name = request.files[file].filename
            print 'file name is --- '
            print '/Users/MrM/Desktop/img_test/'+file_name
            request.files[file].save('/Users/MrM/Desktop/img_test/'+file_name)
            # print file
        return 'succ'

@app.route('/check', methods=['GET', 'POST'])
def start_check():
    for root, dirs, files in os.walk('/Users/MrM/Desktop/' + code_id):
        print files


if __name__ == '__main__':
    app.run(
        host = '0.0.0.0',
        port = 8085,
        debug = True
    )
