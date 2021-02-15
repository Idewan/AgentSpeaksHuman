import json
import os, sys


if __name__ == "__main__":
    #import json file photos_identities.json
    with open("photos_identities.json") as jf:
        data = json.load(jf)
    
    serial = 1

    for keys in data:
        source =  os.path.expanduser('~/Documents/UoM/AgentSpeaksHuman/dataset/raw_data/{}'.format(keys))
        destination =  os.path.expanduser('~/Documents/UoM/AgentSpeaksHuman/dataset/prep_data/{}.jpg'.format(serial))
        os.rename(source, destination)
        serial += 1
    
    print("Done!")
