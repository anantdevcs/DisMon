'''
A file for testing only
'''


import requests

url = 'http://127.0.0.1:5000/translate/s.wav'

print(requests.get(url).text  )
