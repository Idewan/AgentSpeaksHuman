import json

if __name__ == "__main__":
    identities = {} 
    keep = []

    #Read file identity_CelebA.txt
    with open("identity_CelebA.txt", "r") as f:
        initial = f.readline()

        #Iterate through the file
        while initial != '':

            #Maintain a record of unique images
            split = initial.split(' ')
            if int(split[1]) not in keep:
                keep.append(int(split[1]))
                identities[split[0]] =  int(split[1])
            initial = f.readline()

            

    #Output dictionary as a sorted JSON file  
    with open("photos_identities.json", "w") as fp:
        json.dump(identities, fp, sort_keys=True)

    print("Done!")


    

    
    
    
