import json
import sys
import re
import string

file_write = 'data/nbmodel.txt'

records = []
unique_words = set()
Totals = {}
Prior_Totals = {}


class Record:
    def __init__(self, id, t_f, pos_neg, text):
        self.id = id
        self.t_f = t_f
        self.pos_neg = pos_neg
        self.text = text


def remove_punctuation_lower(contents):
    translator = str.maketrans('', '', string.punctuation)

    text = ' '.join(contents)
    # text = text.translate(translator) ?,!.;:\"-'
    regex = re.compile('[%s]' % re.escape("!\"#$%&()*+,-./:;<=>?@[\]^_{|}~"))
    text = regex.sub(' ', text)
    text = text.lower()
    return text.split()


def read_file():
    global records
    with open("data/train-labeled.txt", encoding='utf8') as f:
    # with open(sys.argv[1], encoding='utf8') as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    for line in content:
        contents = line.split()
        id = contents[0]
        t_f = contents[1]
        pos_neg = contents[2]

        # For Punctuation Removal
        text = remove_punctuation_lower(contents[3::])

        r = Record(id, t_f, pos_neg, text)
        records.append(r)
    # print(records[959].text)


def is_stopword(word):
    stopwords = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from", "further", "had", "has", "have", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "I", "I'd", "I'll", "I'm", "I've", "if", "in", "into", "is", "it", "it's", "its", "itself", "let's", "me", "more", "most", "my", "myself", "nor", "of", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "she", "she'd", "she'll", "she's", "should", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "we", "we'd", "we'll", "we're", "we've", "were", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "would", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"]
    stop_wo_punc = remove_punctuation_lower(stopwords)
    if word in set(stop_wo_punc):
        return True
    else:
        return False


def count_words():
    global Totals
    global records
    global unique_words
    global Prior_Totals

    words = {}
    Totals["True"] = 0
    Totals["Fake"] = 0
    Totals["Pos"] = 0
    Totals["Neg"] = 0

    Prior_Totals["True"] = 0
    Prior_Totals["Fake"] = 0
    Prior_Totals["Pos"] = 0
    Prior_Totals["Neg"] = 0

    for r in records:
        # Counting Priors
        if r.t_f == "True":
            Prior_Totals["True"] += 1
        else:
            Prior_Totals["Fake"] += 1
        if r.pos_neg == "Pos":
            Prior_Totals["Pos"] += 1
        else:
            Prior_Totals["Neg"] += 1

        # Optimize get list of words w/o stopwords from stopword func
        for t in r.text:

            if not is_stopword(t):
                if t not in unique_words:
                    unique_words.add(t)
                if t not in words:
                    words[t] = {}
                    words[t]["True"] = 0
                    words[t]["Fake"] = 0
                    words[t]["Pos"] = 0
                    words[t]["Neg"] = 0

                if r.t_f == "True":
                    words[t]["True"] += 1
                    Totals["True"] += 1
                else:
                    words[t]["Fake"] += 1
                    Totals["Fake"] += 1

                if r.pos_neg == "Pos":
                    words[t]["Pos"] += 1
                    Totals["Pos"] += 1
                else:
                    words[t]["Neg"] += 1
                    Totals["Neg"] += 1
    for k in Prior_Totals.keys():
        Prior_Totals[k] /= len(records)
    len_unique = len(unique_words)
    # print(Prior_Totals)
    for k in words.keys():
        words[k]["True"] = (words[k]["True"] + 1)/(Totals["True"] + len_unique)
        words[k]["Fake"] = (words[k]["Fake"] + 1)/(Totals["Fake"] + len_unique)
        words[k]["Pos"] = (words[k]["Pos"] + 1)/(Totals["Pos"] + len_unique)
        words[k]["Neg"] = (words[k]["Neg"] + 1)/(Totals["Neg"] + len_unique)
    nbmodel_write(words, len_unique)


def nbmodel_write(words, len_unique):
    global Prior_Totals
    global Totals
    f = open(file_write, 'w', encoding='utf8')
    c = json.loads("[{0},{1},{2},{3}]".format(json.dumps(Prior_Totals), json.dumps(Totals), json.dumps(words), json.dumps(len_unique)))
    f.write(json.dumps(c))


read_file()
count_words()
