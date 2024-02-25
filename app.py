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


    @app.route('/mixed.wav')
    def getresultwav():
        return send_file('mixed.wav',
                        mimetype='audio/wav')
                        # as_attachment=True,
                        # attachment_filename="test.wav")


    @app.route('/getaudio', methods=['GET', 'POST'])
    def getaudio():
        prompt = """
        Use this template: 

        Grandeur: Majestic, grand, monumental, heroic
        Orchestral: Symphonic, lush, rich, full-bodied
        Intensity: Powerful, dramatic, intense, thrilling
        Emotion: Emotional, poignant, moving, stirring
        Epic Scale: Massiv, expansive, vast, larger-than-life
        Dynamic Range: Dynamic, constrast, crescendos, swells
        Chorus: Choral, choir, vocal, harmonies 
        Percussion: Percussive, driving, rhythmic, thunderous
        Melodic Themes: Memorable, catchy, thematic, motifs
        Building Tension: Suspenseful, building, climactic, anticipation
        Cinematic Sound Design: Textured, atmospheric, immersive, soundscapes
        Instrumentation: Bass, strings, woodwinds, percussion, synthesizers
        Momentum: Energetic, propulsive, relentless, pulse sounding
        Imagery: Evocative, visual, picturesque, storytelling
        Heroic Journey: Triumph, resolve, determination, perserverance

        Make a similar prompt but not exactly for an audio that encapsulates the content of this text: 

        """
        data = request.json.get('text')
        print(data)

        print("Generating speech")
        text_to_speech(data)
        print("Generating music")
        prompt = llm(prompt + data)
        music_gen(prompt)
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




