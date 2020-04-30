from application import app
from zone_data_management import Zone, create_zones, load_zone, load_dict, add_entry, clear_zones, checkpoint_all_zones, checkpoint_all_zones
import threading

def main():
    clear_zones()
    create_zones()
    threading.Timer(6*60*60, checkpoint).start()
    app.run()

    
def checkpoint():
    checkpoint_all_zones()




if __name__ == '__main__':
    main()