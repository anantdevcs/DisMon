import pickle
import requests
import uuid
import os

class Zone:
    def __init__(self, lon, lat, zone_uniquename):
        self.lon = lon
        self.lat = lat
        self.zone_uniquename = zone_uniquename
        self.symptom_counts = {}
        self.checkpoint_list = [] #List of symptom_count dicts
        self.all_symptoms = []

    def update_symptomlist(self):
        self.all_symptoms = requests.get('http://dismon.herokuapp.com//all_symps').json()
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
                    raise KeyError(f"This symptom {symptom} is not found")

            else :
                print(symptom)
                self.symptom_counts[symptom] += 1

    def checkpoint(self):
        self.checkpoint_list.append(self.symptom_counts.copy())
        for key in self.symptom_counts.keys():
            self.symptom_counts[key] = 0

   
    def show_checks(self) :
        print(f'Printing the checkpoints for file with {self.lat} {self.lon} ')
        for i in range(len(self.checkpoint_list)):
            print(f'{i} Th checkpoint')
            print(self.checkpoint_list[i])


    def __str__(self):
        s = f'Num of checkpoints : {len(self.checkpoint_list)} LAT {self.at} LON {self.lon} '
        return s



filename_to_zonename_mapper = {}

def create_zones():
    for lat in range(-30, 30):
        for lon in range(-30, 30):
            zname = str(uuid.uuid4())
            cur_zone = Zone(lon, lat, zone_uniquename=zname )
            filename_to_zonename_mapper[str([lat, lon ])] = zname
            cur_zone.save_zonefile()
    dict_file = open('Master_dict', 'wb')
    pickle.dump(filename_to_zonename_mapper, dict_file)
    dict_file.close()
    return filename_to_zonename_mapper




def load_zone(filename):
    obj = pickle.load(open('zones/' + filename, 'rb'))
    print(f'Loaded {obj.zone_uniquename}')
    return obj

def load_dict():
    obj = pickle.load(open( 'Master_dict', 'rb'))

    return obj
    

#from zone_data_management import *

def add_entry(lon, lat, symptoms) :
    
    filename_to_zonename_mapper = load_dict()
    zonename = filename_to_zonename_mapper[str([lon, lat])]
    zone_obj = load_zone(zonename)
    zone_obj.add_symptom(symptoms)
    #zone_obj.print() 
    zone_obj.save_zonefile()   


def clear_zones():
    for path in os.listdir('./zones'):
        name = './zones/' + path
        os.remove(name)
    os.remove('Master_dict')

def checkpoint_all_zones():
    filename_to_zonename_mapper = load_dict()
    for zonename in filename_to_zonename_mapper.values():
        
        zone_obj = load_zone(zonename)
        zone_obj.checkpoint()
        zone_obj.save_zonefile()
        #zone_obj.show_checks()

    

    





        




    
        
                


