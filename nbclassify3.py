import json

file_read = "sys.argv[1]"
file_read = "data/dev-text.txt"

Totals = {}
Prior_Totals = {}
words = {}
len_unique = 0


def read_param():
    global Totals
    global Prior_Totals
    global words
    global len_unique

    fh = open("data/nbmodel.txt", encoding='utf8')

    all_dict = json.load(fh)
    Prior_Totals = all_dict[0]
    Totals = all_dict[1]
    words = all_dict[2]
    len_unique = all_dict[3]


def classify():
    global Totals
    global Prior_Totals
    global words
    global len_unique
    answer = {}

    prob_pos = Prior_Totals["Pos"]
    prob_neg = Prior_Totals["Neg"]
    prob_true = Prior_Totals["True"]
    prob_fake = Prior_Totals["Fake"]

    with open(file_read, encoding='utf8') as f:
        content = f.readlines()
    content = [x.strip() for x in content]


    for line in content:
        contents = line.split()
        id = contents[0]

        if id not in answer:
            answer[id] = {}
            answer[id]["pos_neg"] = ""
            answer[id]["true_fake"] = ""

        text = contents[1]
        for w in text:
            if w in words.keys():
                prob_true *= words[w]["True"]
                prob_fake *= words[w]["Fake"]
                prob_pos *= words[w]["Pos"]
                prob_neg *= words[w]["Neg"]
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
    fh = open('data/nboutput.txt', 'w', encoding='utf8')
    for k in answer.keys():
        fh.write(k)
        fh.write(" "+answer[k]["true_fake"])
        fh.write(" " + answer[k]["pos_neg"]+"\n")
    fh.close()


read_param()
classify()
