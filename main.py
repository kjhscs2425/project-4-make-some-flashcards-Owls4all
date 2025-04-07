# Write your code here
import os
import time
from utility import *
questionList = []
source_file = ''
thisRunData = {
    "asked":0,
    "wrong":0,
    "accuracy":0,
    "order":''
}
boxes = [100,95,90,85,80]
class quest:
    def __init__(self,dataDict:dict):
        self.data = dataDict
        self.ask = 0
        self.wrong = 0
        if type(self.data)==dict:
            for key in self.data.keys():
                if key in ["wrong","asked","show",'box']:
                    self.data[key] = int(self.data[key])
                elif key == 'accuracy':
                    self.data[key] = float(self.data[key])
            if 'box' not in self.data.keys():
                self.data["box"] = 0
        else:
            print(f"self.data is a {type(self.data)}")
    def stringify(self):
        return dict_to_str(self.data,"|||","<<>>")
    def oneLessQuestion(self):
        if self.data["show"] >=2:
            self.data["show"] -=1
    def askUser(self):
        if type(self.data) != dict:
            print(f"self.data is a {type(self.data)}")
            return
        if "question" not in self.data.keys():
            return
        response = ask(self.data["question"]).lower()
        self.data["asked"] +=1
        self.ask +=1
        thisRunData["asked"]+=1
        correctOptions=[self.data["answer"],self.data["answer"]+self.data["units"]]
        if response not in correctOptions:
            self.box = 0
            self.data["wrong"] +=1
            self.wrong +=1
            thisRunData["wrong"]+=1
            self.data["show"] +=1
            print(f"Incorrect! The answer is {self.data["answer"]}{self.data["units"]}.")
            self.data["order"]+='x '
            thisRunData["order"]+='x '
        else:
            print("Correct!")
            self.data["order"]+='√ '
            thisRunData["order"]+='√ '
        asked = self.data["asked"]
        thisRunAsked = thisRunData["asked"]
        wrong = self.data["wrong"]
        thisRunWrong = thisRunData["wrong"]
        self.data["accuracy"] = (asked - wrong)/asked
        self.accuracy = (self.ask-self.wrong)/self.ask
        thisRunData["accuracy"] = (thisRunAsked-thisRunWrong)/(thisRunAsked)
        if self.data["accuracy"] > 0.75:            
            self.oneLessQuestion()
        if self.data["accuracy"] > 0.9:
            self.oneLessQuestion()
    def showStats(self):
        if type(self.data) != dict:
            print(type(self.data))
            return
        for stat in ["question"]:
            if stat not in self.data.keys():
                #print(f"No {stat} stat!")
                #print(dict_to_str(self.data,"|||","<<>>"))
                global questionList
                questionList.__delitem__(indexInList(self,questionList))
                return ''
        statsToShow = f'''{"="*24}
{self.data["question"]}
{self.data["answer"]}{self.data["units"]}

-----Times asked----- 
This run: {self.ask}
Lifetime: {self.data["asked"]}
-----Times correct-----
This run: {self.ask-self.wrong}
Lifetime: {self.data["asked"]-self.data["wrong"]}
-----Times incorrect-----
This run: {self.wrong} 
Lifetime: {self.data["wrong"]}
-----Accuracy----- 
This run: {self.accuracy}
Lifetime: {self.data["accuracy"]}
-----History----- 
{self.data["order"]}
{"="*24}
'''
        return(statsToShow)

user = ask("Username?")
chosenSet = ''
questionSet = ''
possibleSets = ["prices","mines","days","skills","fish","birthdays"]
while not questionSet in ["0","1",'2','3','4','5']:
    chosenSet = ask(f"What question set to use?\n{possibleSets}")
    if chosenSet == 'all':
        if not os.path.isfile(f"{user}.txt"):
            string = ''
            for i in range(len(possibleSets)):
                currentFile = f"{user}{i}.txt"
                if os.path.isfile(f"{currentFile}"):
                    string += open(currentFile,"r").read()
                else:
                    string += open(f"default{i}.txt",'r').read()
        else:
            string = open(f"{user}.txt",'r').read()
        for q in string.split("###"):
            newQuest = quest(str_to_dict(q.replace('\n',''),"|||","<<>>"))
            if "question" in newQuest.data.keys():
                questionList.append(newQuest)
        break        
    if chosenSet in possibleSets:
        questionSet = f"{indexInList(chosenSet,possibleSets)}"
    elif chosenSet in ["0","1",'2','3','4','5']:
        questionSet = chosenSet
        chosenSet = indexInList(int(chosenSet),possibleSets)
    else:
        print('That question set does not exist! Please choose another!')
if chosenSet != 'all':
    fileName = f"{user}{questionSet}.txt"
else:
    fileName = f"{user}.txt"
if 'default' == user:
    forReal = ask("So you'll be adding questions then?")
    if forReal in YesList:
        mode = 'question'
    else:
        mode = 'None'
        print("If you would like to corrupt the question source data, please edit the file directly.")
else:
    mode = ask("run normally, view stats, or add questions?")
if mode == 'normal' or mode == 'normally':
    print("Normal mode selected")
    Tinitial = time.time()
    if os.path.isfile(f"{fileName}") and questionSet != 'all':
        print(f"User file for {user} exists for chosen question set: loading stats")
        source_file = open(f"{fileName}","r").read()
    else:
        print(f"No file found for {user}. Loading default question set")
        if questionSet != 'all':
            source_file = open(f"default{questionSet}.txt","r").read()
    for q in source_file.split("###"):
            newQuest = quest(str_to_dict(q.replace('\n',''),"|||","<<>>"))
            if "question" in newQuest.data.keys():
                questionList.append(newQuest)
    cards = []
    for i in range(len(questionList)): 
        q=questionList[i]
        if type(q.data) != dict:
            #print("there is a bad question - figure it out")
            questionList.__delitem__(i)
        else:
            if "show" not in q.data.keys():
                print("There's a question missing a show stat.")
                for j in range(2):
                    cards.append(i)
            else:
                show = q.data["show"]
                if type(show) == int:
                    #print(f"{q.data["question"]} added to list")
                    for j in range(show):
                        cards.append(i)
                else:
                    if show.isdigit():
                        #print(f"{q.data["question"]} added to list")
                        for j in range(int(show)):
                            cards.append(i)
                    else:
                        print("Something has gone direly wrong")
    #print(cards) 
    deck = shuffle(cards,3)
    #print(deck)
    x = len(deck)
    for i in range(x):
        print(f"\nQuestion {i+1}. (out of {x})")
        chosenCard = deck.pop()
        if r.randint(1,100) <= boxes[questionList[chosenCard].data['box']]:
            questionList[chosenCard].askUser()
    Tfinal = time.time()
    outputFile = open(f"{fileName}","w")
    my_data_string = ''
    thisRunStats = f'''{'='*24}
Stats for {user}'s run of {chosenSet}
{'-'*24}
Time: {makeNiceTime(Tfinal-Tinitial)}
Questions asked: {thisRunData["asked"]}
Correct answers: {thisRunData["asked"]-thisRunData["wrong"]}
Incorrect answers: {thisRunData["wrong"]}
Accuracy: {thisRunData["accuracy"]}
{'='*24}
'''
    for q in questionList:
        print(q.showStats())
        if q.wrong == 0 and q.ask != 0:
            q.data['box'] +=1
        my_data_string += f"{dict_to_str(q.data,"|||","<<>>")}###\n"
    outputFile.write(my_data_string)
    statsFile = f"{user}{questionSet}stats.txt"
    if os.path.isfile(statsFile):
        previousRuns = open(statsFile,'r').read()
    else:
        previousRuns = ''
    open(statsFile,'w').write(f"{previousRuns}\n{thisRunStats}")
    print(thisRunStats)
elif 'stats' in mode:
    source_file = f"{user}{questionSet}stats.txt"
    if os.path.isfile(source_file):
        print(open(source_file,'r').read())
    else:
        print(f"{user} has no saved stats for {chosenSet}.")
elif 'question' in mode:
    addingQuestions = True
    my_data_string = ''
    while addingQuestions:
     data = {}
     for key in ["question","answer","units"]:
        qToAsk = key+":"
        if key == "units":
            qToAsk += '\n(Add a space if there should be a space between the answer and units)'
        data[key] = ask(qToAsk)
     data["accuracy"]=0
     data["show"]=2
     data["asked"]=0
     data["wrong"]=0
     data["order"]=''
     stringVersion = (dict_to_str(data,"|||","<<>>"))
     my_data_string += f"\n{stringVersion}###"
     keepGoing = ask("Keep going?")
     if keepGoing not in YesList:
        addingQuestions = False
        if os.path.isfile(f"{fileName}"):
            existingQuestions = open(f"{fileName}","r").read()
        else:
            existingQuestions = ''
        outputFile = open(f"{fileName}","w")
        outputFile.writelines(existingQuestions+my_data_string)