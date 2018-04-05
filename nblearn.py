
# file_read = "sys.argv[1]"
# file_read = "data/train-labeled.txt"
file_read = "data/test.txt"

records = []
unique_words = []
Totals = {}
Prior_Totals = {}


class Record:
    def __init__(self, id, t_f, pos_neg, text):
        self.id = id
        self.t_f = t_f
        self.pos_neg = pos_neg
        self.text = text


def read_file():
    global records
    with open(file_read, encoding='utf8') as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    for line in content:
        contents = line.split()
        id = contents[0]
        t_f = contents[1]
        pos_neg = contents[2]
        text = contents[3::]
        r = Record(id,t_f,pos_neg,text)
        records.append(r)
    # print(records[3].text)      # exclamation...punctions????


def is_stopword(word):
    stopwords = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from", "further", "had", "has", "have", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "I", "I'd", "I'll", "I'm", "I've", "if", "in", "into", "is", "it", "it's", "its", "itself", "let's", "me", "more", "most", "my", "myself", "nor", "of", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "she", "she'd", "she'll", "she's", "should", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "we", "we'd", "we'll", "we're", "we've", "were", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "would", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"]
    if word in stopwords:
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

        for t in r.text:
            if t not in unique_words:
                unique_words.append(t)
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
    print(Prior_Totals)


read_file()
count_words()
