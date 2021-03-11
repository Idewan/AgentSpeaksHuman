import json
import statistics

THRESHOLD = 0
STRONG_WORDS = ["bald.", "bangs.", "big lips.", "big nose.", "black", "blond", "brown", "chubby.",
             "double chin.", "eyeglasses.", "goatee.", "gray", "", "mustache.", "beard.", "oval face.",
             "pale skin.", "pointy nose.", "receding hairline.", "rosy cheeks.", "sideburns.", "smiling.",
             "straight", "wavy", "wearing earings.", "wearing a hat.", "wearing lipstick.", "wearing a necklace.",
              "wearing a necktie.", "younger.", "older.", "hair", "He", "She", "she", "he"]

def heuristic(s1, s2):
    """
        :s1: List of strings for the target image
        :s2: List of strings for the distractor image
        :return: Closeness value
    """
    score = 0

    # for t_sent in s1:
    #     for d_sent in s2:
    #         words = t_sent.split(" ")
    #         total_words += len(words)
    #         for w in words:
    #             if w not in unique and w in d_sent:
    #                 if w in STRONG_WORDS:
    #                     score += 10
    #                 else:
    #                     score += 1

    #                 unique[w] = 1
    for t_sent in s1:
        if t_sent in s2:
            score += 1

    return score / len(s1)

if __name__ == "__main__":
    pairs = {} #Key id of first and second "id1-id2"
    data_split = {"easy":[], "hard":[]}
    total_scores = []

    with open("captions.json", "r") as jf:
        data = json.load(jf)
        n = 0
        for keys in data:
            n+= 1
            for keys_2 in data:
                f_s = keys + "-" + keys_2
                r_s = keys_2 + "-" + keys
                if keys != keys_2:
                    if (r_s not in pairs) and (f_s not in pairs):
                        score = heuristic(data[keys], data[keys_2])
                        pairs[f_s]=score
                        total_scores.append(score)
        k=0
        z=0

        #ensure to differentiate between r_s and f_s
        for key in pairs:
            if pairs[key] <= THRESHOLD:
                #Second key is the target image and f_s is the distractor image
                data_split["easy"].append(key)
                k+=1
            else:
                data_split["hard"].append(key)
                z+=1
                
        print(f"Easy {k}")
        print(f"Hard {z}")
        print(f"Mean {statistics.mean(total_scores)}")
        print(f"Mode {statistics.mode(total_scores)}")
        print(f"Median {statistics.median(total_scores)}")
        print(f"Max {max(total_scores)}")
        print(f"Min {min(total_scores)}")

    with open("datasplit.json", "w") as wjf:
        json.dump(data_split, wjf)

    print('Done!')