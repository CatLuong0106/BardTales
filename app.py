import os, time, json, shutil, pathlib, psycopg2
import config
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
                        # as_attachment=True,
                        # attachment_filename="test.wav")

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
    
    @app.route('/saveAudio', methods = ['POST'])
    #This definition is to save the audio 
    def saveAudio():
        file = request.files['audioFile']
        if file.filename != '':
            fileContent = ''
            fileContent = psycopg2.Binary(open(file.filename, 'rb').read())
            userName = request.form['userName']
            textPrompt = request.form['text']
            saveStatus = postgreSave(fileContent, userName, textPrompt)
            return saveStatus
    
    def postgreSave(data, userName, textPrompt):
        conn = None
        try:
            conn = psycopg2.connect(database = config.connectionPool['database'], 
                        user = config.connectionPool['user'], 
                        host= config.connectionPool['host'],
                        password = config.connectionPool['password'],
                        port = config.connectionPool['port'])
            qr = conn.cursor()
            qr.execute(f"INSERT INTO Audio_Data(username, text, audiofile) VALUES('{userName}', '{textPrompt}', {data})")
            conn.commit()
            return {
            'message': 'Prompt Successfully saved.',
            'status': 200
        }
        except Exception as e:
            print(e)
            return {
                'message': 'Save failed due to an error',
                'status': 500
            }
        finally:
            if conn is not None:
                conn.close()
    @app.route('/getAudioList', methods = ['GET'])
    def getAudioList():
        username = request.args['username']
        conn = None
        try:
            conn = psycopg2.connect(database = config.connectionPool['database'], 
                        user = config.connectionPool['user'], 
                        host= config.connectionPool['host'],
                        password = config.connectionPool['password'],
                        port = config.connectionPool['port'])
            qr = conn.cursor()
            qr.execute(f"SELECT username, text, encode(audiofile, 'base64') FROM Audio_Data where username = '{username}';")
            audioList = qr.fetchall()
            conn.commit()
            return {
            'audioList': audioList,
            'status': 200
        }
        except Exception as e:
            print(e)
            return {
                'audioList': None,
                'status': 500
            }
        finally:
            if conn is not None:
                conn.close()
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)