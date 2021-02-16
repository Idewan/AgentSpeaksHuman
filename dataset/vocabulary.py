import json

from collections import Counter

if __name__ == "__main__":
    with open("captions.json") as jf:
        data = json.load(jf)
        
        vocabulary = {}
        lstm_labels = {}
        longest_caption = 0 

        #Unique identities
        for i in range(1,10178):
            sentences = data[str(i)]

            #Sentences
            for j in range(len(sentences)):
                words = sentences[j][:-1].split(" ")
                if len(words) > longest_caption:
                    longest_caption = len(words)
                
                #Words
                for k in range(len(words)):
                    c_word = words[k]
                    if c_word not in vocabulary:
                        vocabulary[c_word] = 1
                    else:
                        vocabulary[c_word] += 1

        vocabulary_size = len(vocabulary.keys())
        c = Counter(vocabulary).most_common()
        
        for z in range(len(c)):
            lstm_labels[z] = c[z][0]
        with open("captions.json", "w") as wjf:
            data["lstm_labels"] = {}
            data["lstm_labels"]['labels'] = lstm_labels
            data["lstm_labels"]['vocab_size'] = vocabulary_size
            data["lstm_labels"]['longest_caption'] = longest_caption

            json.dump(data, wjf)

