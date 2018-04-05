import json
import sys
import math

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

        if id not in answer:
            answer[id] = {}
            answer[id]["pos_neg"] = ""
            answer[id]["true_fake"] = ""

        text = contents[1:]
        # print(text)
        for w1 in text:
            w = w1.lower()
            if w in words.keys():
                prob_true += math.log(words[w]["True"])
                prob_fake += math.log(words[w]["Fake"])
                prob_pos += math.log(words[w]["Pos"])
                prob_neg += math.log(words[w]["Neg"])
            else:
                prob_true += math.log(1/(Totals["True"] + len_unique))
                prob_fake += math.log(1/(Totals["Fake"] + len_unique))
                prob_pos += math.log(1/(Totals["Pos"] + len_unique))
                prob_neg += math.log(1/(Totals["Neg"] + len_unique))
            # print(id+" "+str(prob_pos)+" "+str(prob_neg)+" "+str(prob_true)+" "+str(prob_fake))
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
