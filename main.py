# Write your code here
import os #for checking if files exist
import time #for timing runs
from utility import * #primarily for 'ask', but also for 'YesList' and some other stuff 
questionList = [] #make an empty list - we append questions as we read from the file
source_file = '' 
thisRunData = { #dictionary of current stats for the run
    "asked":0,
    "wrong":0, #right can be calculated 'asked - wrong' and thus need not be tracked separately
    "accuracy":'---',
    "order":'' #show history of right/wrong answers chronologically with '√' or 'x'
}
boxes = [100,95,90,85,80] # % chance to show question (per instance)
class quest: 
    def __init__(self,dataDict:dict):  #establish a question with a dictionary of stats.
        #the stats, in order, are:
        '''
        question - Text prompt shown to the user.
        answer - expected response from the user.
        units - Optional 2nd part of response, such as specifying 'stone' or 'g' when asked how much something costs.
        accuracy - what fraction of this question's answers have been correct
        show - how many times to show the question. Does not account for high box skipping questions. 
            (default 2. Perfect runs decrease it by 1. mistakes increase it by 1)
        asked - the number of times the question has ever been asked
        wrong - the number of times the question has been gotten wrong
        order - the question's lifetime history of right/wrong answers, represented with 'x' or '√' accordingly
        box - leitner system box. Higher-boxed questions have a 5*box % chance to not be shown
        '''
        self.data = dataDict
        self.ask = 0 #single-run stat
        self.wrong = 0 #single-run stat
        self.accuracy = '---' #single-run stat
        if type(self.data)==dict: #in past versions it wasn't. this is to prevent TypeErrors
            for key in self.data.keys(): #the way the dictionary is read from the file, all stats start as strings.
                if key in ["wrong","asked","show",'box']: #checking stats one at a time
                    self.data[key] = int(self.data[key]) #those which should be integers are converted here
                elif key == 'accuracy': 
                    self.data[key] = float(self.data[key])#that which should be a float is converted here
            if 'box' not in self.data.keys():#Some of the older save files did not have a 'box' stat.
                self.data["box"] = 0 #This adds the stat with the default value in that case
        else:
            print(f"self.data is a {type(self.data)}") #error message printed rather than causing a crash
    def stringify(self): #data is stored in a file as a string with dividers between key-value pairs
        return dict_to_str(self.data,"|||","<<>>") #converts the data to a string, with '<<>>' between a key and its value, and '|||' between pairs, so it can be interpreted again later.
    def oneLessQuestion(self): #lowers show stat, but not less than 1.
        if self.data["show"] >=2:
            self.data["show"] -=1
    def askUser(self): 
        if type(self.data) != dict: #primarily to prevent errors which have been patched out. Kept primarily out of laziness, but also the remote chance that a similar error be introduced again later.
            print(f"self.data is a {type(self.data)}")
            return
        if "question" not in self.data.keys(): #skip questions with no actual question
            return
        response = ask(self.data["question"]).lower() #get user input
        self.data["asked"] +=1 #increment stats as is appropriate
        self.ask +=1
        thisRunData["asked"]+=1
        correctOptions=[self.data["answer"],self.data["answer"]+self.data["units"]] #acceptable answers
        if response not in correctOptions: #if the user is wrong...
            self.box = 0 #put the question back into the first box. (no skipping it)
            self.data["wrong"] +=1 #increment stats as is appropriate
            self.wrong +=1
            thisRunData["wrong"]+=1
            self.data["show"] +=1
            print(f"Incorrect! The answer is {self.data["answer"]}{self.data["units"]}.")#tell the user they got it wrong. (and what they should have said!)
            self.data["order"]+='x ' #make a note in the question history of the wrong answer
            thisRunData["order"]+='x '#and in the run history
        else: #if they didn't get it wrong...
            print("Correct!") #tell them they got it right!
            self.data["order"]+='√ '#record it in the question's history
            thisRunData["order"]+='√ '#and in the run history
        asked = self.data["asked"]#shortcut
        thisRunAsked = thisRunData["asked"]#shortcut
        wrong = self.data["wrong"]#shortcut
        thisRunWrong = thisRunData["wrong"]#shortcut
        self.data["accuracy"] = (asked - wrong)/asked#recalculate question's accuracy
        self.accuracy = (self.ask-self.wrong)/self.ask#calculate run-specific question accuracy
        thisRunData["accuracy"] = (thisRunAsked-thisRunWrong)/(thisRunAsked)#recalculate overall run accuracy
    def showStats(self):
        if type(self.data) != dict:
            print(type(self.data))
            return
        for stat in ["question"]:
            if stat not in self.data.keys():
                #print(f"No {stat} stat!") #former debugging statement
                #print(dict_to_str(self.data,"|||","<<>>")) #this one too
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
                        if r.randint(1,100) <= boxes[q.data['box']]:
                            cards.append(i)
                        else:
                            print(f"{q.data['question']} not shown due to being in box {q.data['box']}")
                else:
                    if show.isdigit():
                        #print(f"{q.data["question"]} added to list")
                        for j in range(int(show)):
                            if r.randint(1,100) <= boxes[q.data['box']]:
                                cards.append(i)
                            else:
                                print(f"{q.data['question']} not shown due to being in box {q.data['box']}")
                    else:
                        print("Something has gone direly wrong")
    #print(cards) 
    deck = shuffle(cards,3)
    #print(deck)
    x = len(deck)
    for i in range(x):
        print(f"\nQuestion {i+1}. (out of {x})")
        chosenCard = deck.pop()
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
        if q.wrong == 0 and q.ask != 0 and q.data['box'] <5:
            q.data['box'] +=1
            q.data['show'] -=1
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
     data["accuracy"]='---'
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