from flask import Flask, render_template, request, redirect
import speech_recognition as sr
import os

import uuid
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')



@app.route('/upload', methods=['POST'])

def upload():
    f = request.files['file']
    name = str(uuid.uuid4())
    fname = f'{name}.wav' 
    f.save(fname)
    # import simpleaudio as sa

    # filename = 'myfile.wav'
    # wave_obj = sa.WaveObject.from_wave_file(fname)
    # play_obj = wave_obj.play()
    # play_obj.wait_done()  # Wait until sound has finished playing

    r = sr.Recognizer()
    with sr.AudioFile(fname) as source:


        audio_data = r.record(source)
        text = r.recognize_google(audio_data)
        print(text)
        



    return redirect('/')
        




if __name__ == '__main__':
    app.run(debug = True)