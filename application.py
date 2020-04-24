from flask import Flask, render_template, request, redirect, jsonify, make_response
import speech_recognition as sr
import os
from flask_restful import Resource, Api 
import requests 


import uuid
app = Flask(__name__)

@app.route('/all_symps')

def all_symps():
        '''
        This API endpoint takes no input and returns list of all core symptoms
        supported
        '''
        try:
            symptoms_list = open('symptoms.txt').read().split(sep = '\n')
            for i in range(len(symptoms_list)):
                symptoms_list[i] = symptoms_list[i].lower()
            return make_response(jsonify(symptoms_list), 200)
        except:
            return make_response( jsonify({'error' : 'symptoms list missing'}), 404)

            
@app.route('/translate/<filename>', methods = ['GET'])

def translate(filename):
    '''
    This API endpoint takes a filename of a file stored on the disc and generates
    the appropiate english captions for the conversation
    Make sure sound file is in wav format
    '''

    translator = sr.Recognizer()

    try:
        text = ""
        with sr.AudioFile(filename) as source:
            audio_data = translator.record(source)
            #This system uses google translate API under the hood
            text = translator.recognize_google(audio_data)
        return make_response( jsonify({'translation' : text}, 200))
    except :
        return make_response( jsonify({'error' : 'can not translate'}), 400)


        
    
    




if __name__ == '__main__':
    app.run(debug = True)