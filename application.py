from flask import Flask, render_template, request, redirect, jsonify, make_response
import speech_recognition as sr
import os
from flask_restful import Resource, Api 
import requests 
import re


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

cache = {} 

def top_synonyms(phrase, max_lim = 10):
    '''
    return top max_lim # of similarly meaning words to phrase
    Uses DataMuse free API
    '''
    if phrase in cache:
        return cache[phrase]

    try:
        url = 'https://api.datamuse.com/words'
        params = {'ml' : phrase}
        resp_json = requests.get(url, params = params).json()
        synonyms = [phrase]
        for entry in resp_json:
            synonyms.append(entry['word'])
            if len(synonyms) == max_lim:
                break

        cache[phrase] = synonyms
        return synonyms
    except :
        raise KeyError("Internet not working")



def extract_symotoms(all_symps, conversation_text):
    '''
    all_symps = list of all symptoms supported
    conversation_text = transcript/ text of the conversation

    This function extracts all the possible symptoms form conversation_text
    It uses simple string matching algorithm but it can be possible improved to
    deep-learning based context analysis
    '''

    symptoms_found = []
    for possible_symptom in all_symps:
        sypm_translations = top_synonyms(possible_symptom)
        #print(sypm_translations)
        for cur_search_word in sypm_translations:
            match = re.search(cur_search_word, conversation_text)
            if match:
                symptoms_found.append(possible_symptom)
                break
    
    return make_response(jsonify({'symptoms_extracted' : symptoms_found }) , 200  )
 

@app.route('/add_to_global_db', methods = ['POST'])

def add_to_global_db():
    '''
    It accepts POST request with inputs as-->
    lat lon time list of all symptoms found
    and adds it to the centralized server for central monitoring
    '''
    return 'work under progress'







@app.route('/test')

def test():
    all_symps = requests.get('http://127.0.0.1:5000/all_symps').json()
    print(type(all_symps))
    text = 'i was bleeding and coughing badly. i am not able to walk. legs are fractured. can not eat'
     
    return extract_symotoms(all_symps, text)



    


        
    
    




if __name__ == '__main__':
    app.run(debug = True)