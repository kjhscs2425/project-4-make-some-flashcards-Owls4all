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
        correctOptions=[self.data["answer"],self.data["answer"]+self.data["units"]]
        if response not in correctOptions:
            self.data["wrong"] +=1
            self.data["show"] +=1
            print(f"Incorrect! The answer is {self.data["answer"]}{self.data["units"]}.")
        else:
            print("Correct!")
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

Times asked: {self.data["asked"]}
Times correct: {self.data["asked"]-self.data["wrong"]}
Times incorrect: {self.data["wrong"]}
Accuracy: {self.data["accuracy"]}
{"="*24}
'''
        return(statsToShow)

user = ask("Username?")
if 'default' in user:
    forReal = ask("So you'll be adding questions then?")
    if forReal in YesList:
        mode = 'question'
    else:
        mode = 'None'
        print("If you would like to corrupt the question source data, please edit the file directly.")
else:
    mode = ask("run normally or add questions?")
if mode == 'normal' or mode == 'normally':
    print("Normal mode selected")
    if os.path.isfile(f"{user}.txt"):
        print(f"User file for {user} exists: loading stats")
        source_file = open(f"{user}.txt","r").read()
    else:
        print(f"No file found for {user}.")
        choice = ask("Which default file to open?")
        if choice == '0' or choice not in ["0","1"]:
            choice = ''
        source_file = open(f"default{choice}.txt","r").read()
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
        print(f"\nQuestion {i}. (out of {x})")
        chosenCard = deck.pop()
        questionList[chosenCard].askUser()
    outputFile = open(f"{user}.txt","w")
    my_data_string = ''
    for q in questionList:
        print(q.showStats())
        my_data_string += f"{dict_to_str(q.data,"|||","<<>>")}###\n"
    outputFile.write(my_data_string)

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
     stringVersion = (dict_to_str(data,"|||","<<>>"))
     my_data_string += f"\n{stringVersion}###"
     keepGoing = ask("Keep going?")
     if keepGoing not in YesList:
        addingQuestions = False
        if os.path.isfile(f"{user}.txt"):
            existingQuestions = open(f"{user}.txt","r").read()
        else:
            existingQuestions = ''
        outputFile = open(f"{user}.txt","w")
        outputFile.writelines(existingQuestions+my_data_string)