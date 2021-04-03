import json
import random

from tqdm import tqdm

#Test set heuristic
STRONG_WORDS = ["bald.", "bangs.", "big lips.", "big nose.", "black", "blond", "brown", "chubby.",
             "double chin.", "eyeglasses.", "goatee.", "gray", "", "mustache.", "beard.", "oval face.",
             "pale skin.", "pointy nose.", "receding hairline.", "rosy cheeks.", "sideburns.", "smiling.",
             "straight", "wavy", "wearing earings.", "wearing a hat.", "wearing lipstick.", "wearing a necklace.",
              "wearing a necktie.", "younger.", "older.", "hair", "He", "She", "she", "he"]

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
    worst_score = 10000
    best_cap = 0

    for i in range(len(s1)):
        t_s = s1[i].split(" ")
        t_s_dict = dict.fromkeys(t_s, 1)

        for j in range(len(s2)):
            c_score = 0
            d_s = s2[j].split(" ")

            for k in range(len(d_s)):
                if d_s[k] in t_s_dict:
                    if d_s[k] in STRONG_WORDS:
                        c_score += 10
                    else:
                        c_score += 1
            print(c_score, worst_score)
            if c_score < worst_score:
                worst_score = c_score
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

    for _ in range(2200):
        random_numbers = []
        image_base = image_paths[0]

        while len(random_numbers) < 10:
            num = random.randint(1, len(image_paths)-1)

            image_pot = image_paths[num]

            score = heuristic(data[image_base], data[image_pot])

            in_record = (image_base in record and record[image_base] == image_pot) or (image_pot in record and record[image_pot] == image_base)

            if (num not in random_numbers) and (score < 1) and (not in_record):
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

    for i in range(len(target_paths)):
        c_tp = target_paths[i]
        c_dp = distractor_paths[i]
        
        c_tp_c = data[c_tp]
        c_dp_c = data[c_dp]

        best_caption = heuristic_listener(c_tp_c,c_dp_c)
        best_captions.append(best_caption)
        
    json_f['best_captions'] = best_captions

    with open('best_captions.json', 'w') as jfw:
        json.dump(json_f, jfw)

    print('Done!')