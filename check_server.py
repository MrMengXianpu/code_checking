# -*- coding: utf-8 -*-
from flask import Flask, redirect, url_for, request, flash, render_template  
# from flask_login import LoginManager, login_user, login_required, logout_user
from flask_cors import *

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        code_id = request.form['code_id']
        print code_id
        for file in request.files:
            file_name = request.files[file].filename
            request.files[file].save('/Users/MrM/Desktop/' + file_name)
            # print file
        return 'succ'

if __name__ == '__main__':
    app.run(
        host = '0.0.0.0',
        port = 8085,
        debug = True
    )
