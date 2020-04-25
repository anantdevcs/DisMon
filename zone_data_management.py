import pickle
import requests
import uuid

class Zone:
    def __init__(self, lon, lat, zone_uniquename):
        self.lon = lon
        self.lat = lat
        self.zone_uniquename = zone_uniquename
        self.symptom_counts = {}
        self.checkpoint_list = [] #List of symptom_count dicts
        self.all_symptoms = []

    def update_symptomlist(self):
        self.all_symptoms = requests.get('http://127.0.0.1:5000/all_symps').json()
        for sympts in self.all_symptoms:
            self.symptom_counts[sympts] = 0
        

    def save_zonefile(self):
        ''' Saves this object to Disk '''
        
        tobesaved = open('zones/' + self.zone_uniquename, 'wb')
        pickle.dump(self, tobesaved)
        tobesaved.close()


    def add_symptom(self, symptoms_list) :
        for symptom in symptoms_list:
            if symptom not in self.all_symptoms:
                self.update_symptomlist()
                if symptom not in self.all_symptoms:
                    raise KeyError("This symptom is not found")

            else :
                print(symptom)
                self.symptom_counts[symptom] += 1

    def checkpoint(self):
        self.checkpoint_list.append(self.symptom_counts)
        self.symptom_counts.clear()

    def print(self):
        ''' Aux func for debug purposes'''
        for dict in self.checkpoint_list:
            print(dict)



filename_to_zonename_mapper = {}

def create_zones():
    for lat in range(-1, 5):
        for lon in range(-1, 3):
            zname = str(uuid.uuid4())
            cur_zone = Zone(lon, lat, zone_uniquename=zname )
            filename_to_zonename_mapper[str([lat, lon ])] = zname
            cur_zone.save_zonefile()
    dict_file = open('Master_dict', 'wb')
    pickle.dump(filename_to_zonename_mapper, dict_file)
    dict_file.close()




def load_zone(filename):
    obj = pickle.load(open('zones/' + filename, 'rb'))
    obj.print()
    return obj

def load_dict():
    obj = pickle.load(open( 'Master_dict', 'rb'))

    return obj
    

#from zone_data_management import *

create_zones()





        




    
        
                


