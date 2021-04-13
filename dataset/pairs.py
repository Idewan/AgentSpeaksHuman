import json
import random

from tqdm import trange

#Test set heuristic
WEAKER_WORDS = ["He", "She", "she", "he", "big", "rosy", "a", "wearing", "receding","oval","hair","pointy", "pale"]
STRONG_WORDS = ["lips.", "nose.", "black", "blond", "brown", "gray", "face.",
             "skin.", "hairline.", "cheeks.", "smiling.",
             "straight", "wavy", "earings.", "lipstick.", "necklace.",
            "necktie.", "younger.", "older.",  "double chin."]
VERY_STRONG_WORDS = ["chubby.", "eyeglasses.", "bangs.", "sideburns.", "beard.", "goatee.", "mustache.", "bald.", "hat."]

def heuristic_listener(s1, s2):
    """
        :s1: List of strings for the target image
        :s2: List of strings for the distractor image
        :return: Closeness value
    """
    #O(n^3)
    #create a dict with sentence words
    #check numbers of in 
    #add it all up divide by length add to an array
    #pick argmax return the best_caption
    best_score = 0
    best_cap = 0
    word_choices = {}

    for j in range(len(s2)):
        c_score = 0
        d_s = s2[j].split(" ")

        for k in range(len(d_s)):
            if d_s[k] not in word_choices:
                word_choices[d_s[k]] = 1

    for i in range(len(s1)):
        t_s = s1[i].split(" ")
        c_score = 0 
        for k in range(len(t_s)):
            if t_s[k] not in word_choices:
                if t_s[k] in VERY_STRONG_WORDS:
                    c_score += 30
                    print("yes sir")
                elif t_s[k] in STRONG_WORDS:
                    c_score += 5
                elif t_s[k] in WEAKER_WORDS:
                    c_score += 2
                else:
                    c_score += 1
        if c_score > best_score:
            best_score = c_score
            best_cap = i
    
    return s1[best_cap]

def heuristic(s1, s2):
    """
        :s1: List of strings for the target image
        :s2: List of strings for the distractor image
        :return: Closeness value
    """

    score = 0

    for t_sent in s1:
        if t_sent in s2:
            score += 1

    return score / len(s1)

if __name__ == "__main__":
    with open("captions.json", "r") as jf:
        data = json.loads(jf.read())
    data.pop("lstm_labels")
    image_paths = list(data.keys())


    #Split dataset do not train on images with everything in common
    record = {} #Keeps a record of pairs id1 - id2 and id2 - id1
    target_paths = list()
    distractor_paths = list()
    best_captions = list()

    for _ in trange(2200):
        random_numbers = []
        image_base = image_paths[0]

        while len(random_numbers) < 10:
            num = random.randint(1, len(image_paths)-1)

            image_pot = image_paths[num]

            score = heuristic(data[image_base], data[image_pot])

            in_record = (image_base in record and record[image_base] == image_pot) or (image_pot in record and record[image_pot] == image_base)

            if (num not in random_numbers) and (score == 0) and (not in_record):
                random_numbers.append(num)
        
        for k in random_numbers:
            image_distractor = image_paths[k]
            
            record[image_base] = image_distractor
            record[image_distractor] = image_base

            target_paths.append(image_base)
            distractor_paths.append(image_distractor)

        random.shuffle(image_paths)
    
    json_f = {}
    json_f['target_paths'] =  target_paths
    json_f['distractor_paths'] = distractor_paths

    print(len(target_paths))
    print(len(distractor_paths))

    for i in trange(len(target_paths)):
        c_tp = target_paths[i]
        c_dp = distractor_paths[i]
        
        c_tp_c = data[c_tp]
        c_dp_c = data[c_dp]

        best_caption = heuristic_listener(c_tp_c,c_dp_c)
        best_captions.append(best_caption)
        
    json_f['easy_captions'] = best_captions

    with open('easy_captions.json', 'w') as jfw:
        json.dump(json_f, jfw)

    print('Done!')