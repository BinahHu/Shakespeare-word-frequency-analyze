import re
import os
import json
import matplotlib.pyplot as plt
import matplotlib

MAX_LEN = 25
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

comedy = ['allswell', 'asyoulikeit', 'comedy_errors', 'cymbeline', 'lll', 'measure', 'merry_wives', 'merchant', 'midsummer', 'much_ado', 'pericles', 'taming_shrew', 'tempest', 'troilus_cressida', 'twelfth_night', 'two_gentlemen', 'winters_tale']
comedy = set(comedy)
tragedy = ['cleopatra', 'coriolanus', 'hamlet', 'julius_caesar', 'lear', 'macbeth', 'othello', 'romeo_juliet', 'timon', 'titus']
tragedy = set(tragedy)
history = ['1henryiv', '1henryvi', '2henryiv', '2henryvi', '3henryvi', 'john', 'henryv', 'henryviii', 'richardii', 'richardiii']
history = set(history)

Classes = [comedy, tragedy, history]
Classname = ['comedy', 'tragedy', 'history', 'total']
ClassWords = dict()
ClassWords[3] = dict()
Classnum = [0,0,0,0]

roles = os.listdir('./data')
for role in roles:
    if re.match('\..*', role):
        continue
    info = json.load(open('./data/' + role))
    m = re.match("(.*)-(.*).json", role)
    play = m.group(1)
    Class = -1
    for i in range(3):
        Class = Classes[i]
        if play in Class:
            Class = i
            break
    if not Class in ClassWords:
        ClassWords[Class] = dict()
    for word in info['words']:
        Classnum[Class] += info['words'][word]
        Classnum[3] += info['words'][word]
        if word not in ClassWords[Class]:
            ClassWords[Class][word] = 0
        if word not in ClassWords[3]:
            ClassWords[3][word] = 0
        ClassWords[Class][word] += info['words'][word]
        ClassWords[3][word] += info['words'][word]
for i in range(4):
    ClassWords[i] = dict(sorted(ClassWords[i].items(), key = lambda item : -item[1]))
    x = []
    y = []
    j = 0
    for item in ClassWords[i].items():
        x.append(item[1])
        y.append(item[0])
        j += 1
        if j >= MAX_LEN:
            break
    plt.figure()
    plt.barh(range(MAX_LEN), x, height=0.7, color='steelblue', alpha=0.8)
    plt.yticks(range(MAX_LEN), y)
    plt.xlabel("Frequency of words")
    plt.title(Classname[i])
    for xx, yy in enumerate(x):
        plt.text(yy + 0.2, xx - 0.1, '%s' % yy)
    plt.savefig("../pic/" + Classname[i] + ".png")

for i in range(4):
    print("Class " + Classname[i] + ", num of words = " + str(Classnum[i]))
