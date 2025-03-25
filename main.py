# Write your code here
import os
from utility import *
questionList = []
class quest:
    def __init__(self,dataDict:dict):
        self.data = dataDict
        if type(self.data)==dict:
            for key in self.data.keys():
                if key in ["wrong","asked","show"]:
                    self.data[key] = int(self.data[key])
                elif key == 'accuracy':
                    self.data[key] = float(self.data[key])
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
        response = ask(self.data["question"])
        self.data["asked"] +=1
        if response != self.data["answer"]:
            self.data["wrong"] +=1
            self.data["show"] +=1
        asked = self.data["asked"]
        wrong = self.data["wrong"]
        self.data["accuracy"] = (asked - wrong)/asked
        if self.data["accuracy"] > 0.75:            
            self.oneLessQuestion()
        if self.data["accuracy"] > 0.9:
            self.oneLessQuestion()
    def showStats(self):
        if type(self.data) != dict:
            print(type(self.data))
            return
        statsToShow = f'''{"="*24}
{self.data["question"]}
{self.data["answer"]}

Times asked: {self.data["asked"]}
Times correct: {self.data["asked"]-self.data["wrong"]}
Times incorrect: {self.data["wrong"]}
Accuracy: {self.data["accuracy"]}
{"="*24}
'''
        print(statsToShow)

user = ask("User name?")
mode = ask("run normally or add questions?")
if mode == 'normal':

    if os.path.isfile("data.json"):
        source_file = open(f"{user}.txt","r").read()
    else:
        source_file = open("default.txt","r").read()
        for q in source_file.split("###"):
            newQuest = quest(str_to_dict(q.replace('\n',''),"|||","<<>>"))
            questionList.append(newQuest)
    cards = []
    for q in questionList:
        if "show" not in q.data.keys():
            q.data["show"]=3
        elif type(q.data["show"]) != int:
            q.data["show"]=int(q.data["show"])
        foo = q.data["show"]
        for i in range(foo):
            cards.append(indexInList(q,questionList))
    
    deck = shuffle(cards)
    for card in deck:
        chosenCard = deck.pop()
        questionList[chosenCard].askUser()
    outputFile = open(f"{user}.txt","w")
    my_data_string = ''
    for q in questionList:
        print(q.showStats())
        my_data_string += f"{dict_to_str(q.data,"|||","<<>>")}###\n"
    outputFile.write(my_data_string)

elif mode == 'questions':
    addingQuestions = True
    my_data_string = ''
    while addingQuestions:
     data = {}
     for key in ["question","answer"]:
        data[key] = ask(key)
     data["accuracy"]=0
     data["show"]=3
     data["asked"]=0
     data["wrong"]=0
     stringVersion = (dict_to_str(data,"|||","<<>>"))
     my_data_string += f"\n{stringVersion}###"
     keepGoing = ask("Keep going?")
     if keepGoing not in YesList:
        addingQuestions = False
        existingQuestions = open("default.txt","r").read()
        outputFile = open("default.txt","w")
        outputFile.writelines(existingQuestions+my_data_string)
        
