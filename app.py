import os, time, json, shutil, pathlib

from flask import Flask, render_template, request, send_file
# from flask_sqlalchemy import SQLAlchemy, event
# import pandas as pd
from werkzeug.utils import secure_filename
# from sqlalchemy.sql import func



def create_app(test_config=None):

    app = Flask(__name__)


    @app.route('/data.html')
    def contentdata():
        return render_template('data.html')


    @app.route('/sample-file-4.wav')
    def getwav():
        return send_file('sample-file-4.wav',
                        mimetype='audio/wav')
    

    @app.route('/getaudio', methods=['GET', 'POST'])
    def getaudio():
        # sample-file-4.wav
        return send_file('sample-file-4.wav',
                        mimetype='audio/wav')
                        # as_attachment=True)


    @app.route('/')
    def main():
        # return 'Hello, World!'
        return render_template('mainpage.html')

    return app