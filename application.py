from flask import Flask, render_template, request, redirect, jsonify
import speech_recognition as sr
import os
from flask_restful import Resource, Api 
import requests 


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
        




api = Api(app) 

class Square(Resource): 
  
    def get(self):
        return jsonify({'info':'fu'})
    
    def post(self): 
        inp = request.get_json()


        return ((inp))
  

api.add_resource(Square, '/square')


@app.route('/sympts')

def sympts():
    text = open('symptoms.txt').read()
    sympts_list = text.split(sep= '\n')
    
    return jsonify(sympts_list)

# @app.route('/parse', methods = )

# def parse():
@app.route('/demo')
def demo():
    uri = 'http://127.0.0.1:5000/square'
    data = ({'num':10})
    r = requests.post(url = uri, data = data) 
    return r.text


if __name__ == '__main__':
    app.run(debug = True)