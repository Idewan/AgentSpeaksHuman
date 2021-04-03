import json
import pandas as pd
# Retreive labels (desired)

# Create templates for the different labels depending on whether they are male or female
# Priorities over certain labels

#  Use JSON file identities - photos

def is_male(s):
    return f"He is {s}"

def has_a_male(s):
    return f"He has a {s}"

def has_male(s):
    return f"He has {s}"

def has_hair_male(s):
    return f"He has {s} hair"

def is_female(s):
    return f"She is {s}"

def has_a_female(s):
    return f"She has a {s}"

def has_female(s):
    return f"She has {s}"

def has_hair_female(s):
    return f"She has {s} hair."

def has_an_female(s):
    return f"She has an {s}"

def has_an_male(s):
    return f"He has an {s}"

if __name__ == "__main__":
    df = pd.read_csv("labels.csv", index_col="n")
    index_has = [1,2,9,16,19,20]
    index_is = [0,7,21,24,25,26,27,28,29,30]
    index_hair = [4,5,6,11,22,23]
    index_has_a = [3,8,10,13,14,17,18]
    index_has_an = [15]
    words = ["bald.", "bangs.", "big lips.", "big nose.", "black", "blond", "brown", "chubby.",
             "double chin.", "eyeglasses.", "goatee.", "gray", "", "mustache.", "beard.", "oval face.",
             "pale skin.", "pointy nose.", "receding hairline.", "rosy cheeks.", "sideburns.", "smiling.",
             "straight", "wavy", "wearing earings.", "wearing a hat.", "wearing lipstick.", "wearing a necklace.",
              "wearing a necktie.", "younger.", "older."]
            
    sentence_dic = {} #unique identity -> setences
    female_func = {}  #index -> function (male/female)
    male_func = {}  #index ->  function (male/female)

    for k in range(31):
        #Use built arrays to introduce appropriate functions
        if k in index_has:
            #Has functions
            female_func[k] = has_female
            male_func[k] = has_male
        elif k in index_is:
            #Is functions
            female_func[k] = is_female
            male_func[k] = is_male
        elif k in index_hair:
            #Has hair functions
            female_func[k] = has_hair_female
            male_func[k] = has_hair_male
        elif k in index_has_a:
            #Has a functions
            female_func[k] = has_a_female
            male_func[k] = has_a_male
        elif k in index_has_an:
            #Has an functions
            female_func[k] = has_an_female
            male_func[k] = has_an_male

    with open("captions.json", "w") as jf:
        for j in range(10177):
            c_row = df.iloc[j]
            male = c_row['Male']

            u_ind = int(j+1)
            sentence_dic[u_ind] = []

            for i in range(len(c_row)):
                on = c_row[i]
                if male:
                    if on and i != 12 and i != 29 and i != 14:
                        sentence_dic[u_ind].append(male_func[i](words[i]))
                    elif i==29:
                        age = words[i] if on else words[i+1]
                        sentence_dic[u_ind].append(male_func[i](age))
                    elif not on and i==14:
                        sentence_dic[u_ind].append(male_func[i](words[i]))
                else:
                    if on and i != 12 and i != 29 and i != 14:
                        sentence_dic[u_ind].append(female_func[i](words[i]))
                    elif i==29:
                        age = words[i] if on else words[i+1]
                        sentence_dic[u_ind].append(female_func[i](age))
                    elif not on and i==14:
                        sentence_dic[u_ind].append(female_func[i](words[i]))
            
        json.dump(sentence_dic, jf)
    

