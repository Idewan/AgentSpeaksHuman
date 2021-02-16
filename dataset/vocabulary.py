import json

from collections import Counter

if __name__ == "__main__":
    with open("captions.json", "r") as jf:
        data = json.load(jf)
        
        vocabulary = {}

        #Unique identities
        for i in range(10178):
            sentences = data[i]

            #Sentences
            for j in range(len(sentences)):
                words = sentences[j][:-1].split(" ")
                
                #Words
                for k in range(lem(words)):
                    c_word = words[k]
                    if c_word not in vocabulary:
                        vocabulary[c_word] = 1
                    else:
                        vocabulary[c_word] += 1

        c = Counter(vocabulary).most_common()
