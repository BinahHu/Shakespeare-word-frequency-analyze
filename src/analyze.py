import re
import nltk
import os
from bs4 import BeautifulSoup
from nltk.tokenize.punkt import PunktLanguageVars
from cltk.stop.middle_english.stops import STOPS_LIST
import json
STOPS_LIST += ['!', ',' ,'.' ,'?', ';', "'", ':', '--', '[', ']']
with open('./stopwords.txt') as f:
    lines = f.readlines()
    for line in lines:
        STOPS_LIST.append(line.strip('\n'))


p = PunktLanguageVars()

root = "./"
plays = os.listdir(root)
for play in plays:
    if play == 'data' or re.match('\..*', play):
        continue
    playdir = root + play + '/'
    if not os.path.isdir(playdir):
        continue
    print(play + " ...")
    scenes = os.listdir(playdir)
    role = dict()
    speechbuf = []
    name = ""
    for file in scenes:
        scene = playdir + '/' + file
        if os.path.isdir(scene):
            continue
        print('\t' + file + "...")
        f = open(scene)
        soup = BeautifulSoup(markup=f.read(), features="html.parser")
        dialogs = soup.find_all('a')
        for dia in dialogs:
            if('href' in dia.attrs):
                continue
            if(dia.b != None):  #A new speech
                if name != "":
                    if not name in role:
                        role[name] = []
                    role[name] += speechbuf
                name = dia.b.contents[0]
                speechbuf = []
            else:
                speechbuf += nltk.word_tokenize(dia.contents[0].lower())
    for r in role:
        speech = role[r]
        speech = [word for word in speech if word not in STOPS_LIST]
        role[r] = dict()
        role[r]['len'] = len(speech)
        role[r]['words'] = dict()
        role[r]['name'] = r
        for word in speech:
            if not word in role[r]['words']:
                role[r]['words'][word] = 0
            role[r]['words'][word] += 1
    role = sorted(role.items(), key = lambda item: -item[1]['len'])
    json.dump(role[0][1], open(root + 'data/' + play + '-' + role[0][0] + '.json', 'w'))
    json.dump(role[1][1], open(root + 'data/' + play + '-' + role[1][0] + '.json', 'w'))
