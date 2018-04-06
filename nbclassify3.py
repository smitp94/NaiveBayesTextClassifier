import json
import sys
import math
import re


file_read = "data/nbmodel.txt"
file_write = "data/nboutput.txt"

Totals = {}
Prior_Totals = {}
words = {}
len_unique = 0


def read_param():
    global Totals
    global Prior_Totals
    global words
    global len_unique

    fh = open(file_read, encoding='utf8')

    all_dict = json.load(fh)
    Prior_Totals = all_dict[0]
    Totals = all_dict[1]
    words = all_dict[2]
    len_unique = all_dict[3]


def remove_punctuation_lower(contents):
    text = ' '.join(contents)
    regex = re.compile('[%s]' % re.escape("!\"#$%&()*+,-./:;<=>?@[\]^_{|}~"))
    text = regex.sub(' ', text)
    text = text.lower()
    return text.split()


def is_stopword(word):
    stopwords = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from", "further", "had", "has", "have", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "I", "I'd", "I'll", "I'm", "I've", "if", "in", "into", "is", "it", "it's", "its", "itself", "let's", "me", "more", "most", "my", "myself", "nor", "of", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "she", "she'd", "she'll", "she's", "should", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "we", "we'd", "we'll", "we're", "we've", "were", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "would", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"]
    stop_wo_punc = remove_punctuation_lower(stopwords)
    if word in set(stop_wo_punc):
        return True
    else:
        return False


def classify():
    global Totals
    global Prior_Totals
    global words
    global len_unique
    answer = {}

    with open("data/dev-text.txt", encoding='utf8') as f:
    # with open(sys.argv[1], encoding='utf8') as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    for line in content:
        contents = line.split()
        # Initializing
        id = contents[0]
        prob_pos = math.log(Prior_Totals["Pos"])
        prob_neg = math.log(Prior_Totals["Neg"])
        prob_true = math.log(Prior_Totals["True"])
        prob_fake = math.log(Prior_Totals["Fake"])

        answer[id] = {}
        answer[id]["pos_neg"] = ""
        answer[id]["true_fake"] = ""

        text = remove_punctuation_lower(contents[1:])
        for w in text:
            if w in words.keys():
                prob_true += math.log(words[w]["True"])
                prob_fake += math.log(words[w]["Fake"])
                prob_pos += math.log(words[w]["Pos"])
                prob_neg += math.log(words[w]["Neg"])
        if prob_true > prob_fake:
            answer[id]["true_fake"] = "True"
        else:
            answer[id]["true_fake"] = "Fake"
        if prob_pos > prob_neg:
            answer[id]["pos_neg"] = "Pos"
        else:
            answer[id]["pos_neg"] = "Neg"
    write_file(answer)


def write_file(answer):
    fh = open(file_write, 'w', encoding='utf8')
    flag = 0
    for k in answer.keys():
        if flag == 0:
            flag = 1
            fh.write(k)
        else:
            fh.write("\n"+k)
        fh.write(" " + answer[k]["true_fake"])
        fh.write(" " + answer[k]["pos_neg"])
    fh.close()


read_param()
classify()
