import os, time, json, shutil, pathlib

from flask import Flask, render_template, request, send_file
# from flask_sqlalchemy import SQLAlchemy, event
# import pandas as pd
from werkzeug.utils import secure_filename
# from sqlalchemy.sql import func
from pipelineutils import *

def create_app(test_config=None):

    app = Flask(__name__)


    @app.route('/data.html')
    def contentdata():
        return render_template('data.html')


    @app.route('/sample-file-4.wav')
    def getwav():
        return send_file('sample-file-4.wav',
                        mimetype='audio/wav')
                        # as_attachment=True,
                        # attachment_filename="test.wav")

    @app.route('/getaudio', methods=['GET', 'POST'])
    def getaudio():
        data = request.json.get('text')
        print(data)

        print("Generating speech")
        text_to_speech(data)
        print("Generating music")
        music_gen(data)
        print("Combining speech and music")
        combine()

        print("Returning audio file")

        return send_file('mixed.wav',
                        mimetype='audio/wav')
                        # as_attachment=True)


    @app.route('/')
    def main():
        # return 'Hello, World!'
        return render_template('mainpage.html')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)




