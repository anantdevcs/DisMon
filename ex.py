from nltk.corpus import wordnet
synonyms = []
antonyms = []
import requests as r
import json

url = 'https://api.datamuse.com/words'
params = {'ml' : 'Short of breath'}     

resp = r.get(url, params = params).json()

for ent in resp:
	print(ent['word'])