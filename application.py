from flask import Flask, render_template, request, redirect, jsonify, make_response
import speech_recognition as sr
import os
from flask_restful import Resource, Api 
import requests 
import re
from zone_data_management import *
import json as j 
import uuid
app = Flask(__name__)
import threading
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

    #try:
    text = ""
    with sr.AudioFile(filename) as source:
        audio_data = translator.record(source)
        #This system uses google translate API under the hood
        text = translator.recognize_google(audio_data)
    return make_response( jsonify({'translation' : text}, 200))
    #except :
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
        return [phrase]



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
    
    return symptoms_found
    return make_response(jsonify({'symptoms_extracted' : symptoms_found }) , 200  )
 

@app.route('/add_to_global_db', methods = ['POST'])

def add_to_global_db():
    '''
    It accepts POST request with inputs as-->
    lat lon  list of all symptoms found
    and adds it to the centralized server for central monitoring
    '''
    
    data = j.loads(request.data)
    lon = data['lon']
    lat = data['lat']
    symptoms = data['symptoms']

    add_entry(lon, lat, symptoms)



    return str(symptoms)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods = ['POST'])
def upload():
    file = request.files['file']
    lat = int(request.form['lat'])
    lon = int(request.form['lon'])
    ext = file.filename.split(sep = '.')[-1]
    fname = str(uuid.uuid4()) +'.' +  str(ext)
    file.save(fname)
    
    url1 = 'http://dismon.herokuapp.com/translate/' + fname
    print(url1)
    translated_text = requests.get(url1).json()[0]['translation']
    print(f"symptoms found{translated_text}")
    url2 = 'http://dismon.herokuapp.com/all_symps'
    all_symptoms = requests.get(url2).json()
    
    symptoms_found = extract_symotoms(all_symptoms, translated_text)
    print(f"symptoms found {symptoms_found}")
    add_entry(lon = lon, lat = lat, symptoms = symptoms_found)
    os.remove(fname)

    print(f'Symptoms found {symptoms_found}')
    return render_template('index.html', alert = symptoms_found)

@app.route('/analyse/<lat>/<lon>')
    
def analyse(lat, lon): 
    lat = int(lat)
    lon = int(lon)
    aux_dict = load_dict()
    zonename = aux_dict[str([lat, lon])]
    zone_obj = load_zone(zonename)
    return render_template('analyze.html', zone_obj = zone_obj)

@app.route('/dashboard', methods = ['POST', 'GET'])

def dashboard():
    if request.method == 'POST': 
        lon = int(request.form['lon'])
        lat = int(request.form['lat'])
        return redirect(f'/analyse/{lat}/{lon}')
    else :
        return render_template('dashboard.html')
    

if __name__ == '__main__':
    clear_zones()
    create_zones()
    threading.Timer(6*60*60, checkpoint_all_zones).start()
    app.run()
