# Write your code here
from utility import *
questionList = []
class quest:
    def __init__(self,dataDict:dict):
        self.data = dataDict
        for key in ["times wrong","times asked","times to show","accuracy"]:
            if key in ["times wrong","times asked","times to show"]:
                self.data[key] = int(self.data[key])
            elif key == 'accuracy':
                self.data[key] = float(self.data[key])
    def stringify(self):
        return dict_to_str(self.data,"|||","<<>>")
    def oneLessQuestion(self):
        if self.data["times to show"] >=2:
            self.data["times to show"] -=1
    def askUser(self):
        response = ask(self.data["question"])
        self.data["times asked"] +=1
        if response != self.data["answer"]:
            self.data["times wrong"] +=1
            self.data["times to show"] +=1
        asked = self.data["times asked"]
        wrong = self.data["times wrong"]
        self.data["accuracy"] = (asked - wrong)/asked
        if self.data["accuracy"] > 0.75:            
            self.oneLessQuestion()
        if self.data["accuracy"] > 0.9:
            self.oneLessQuestion()
    def showStats(self):
        statsToShow = f'''{"="*24}
{self.data["question"]}
{self.data["answer"]}

Times asked: {self.data["times asked"]}
Times correct: {self.data["times asked"]-self.data["times wrong"]}
Times incorrect: {self.data["times wrong"]}
Accuracy: {self.data["accuracy"]}
{"="*24}
'''
        print(statsToShow)
user = ask("User name?")
#'''
if False: #[check for user file]
    source_file = open(f"{user}.txt","r").read()
else:
    source_file = open("default.txt","r").read()
    for q in source_file.split("###"):
        questionList.append[quest(str_to_dict(q,"|||","<<>>"))]
cards = []
for q in questionList:
    foo = q.data["times to show"]
    for i in range(foo):
        cards.append(indexInList(q,questionList))



for card in shuffle(cards):
    chosenCard = cards.pop()
    questionList[chosenCard].askUser()
outputFile = open(f"{user}.txt","w")
my_data_string = ''
for q in questionList:
    print(q.showStats())
    my_data_string += f"{dict_to_str(q.data,"|||","<<>>")}###\n"
outputFile.write(my_data_string)
#'''

'''    
addingQuestions = True
my_data_string = ''
while addingQuestions:
    data = {}
    for key in ["question","answer","accuracy","times to show","times asked","times wrong"]:
        data[key] = ask(key)
    stringVersion = (dict_to_str(data,"|||","<<>>"))
    my_data_string += f"{stringVersion}###\n"
    keepGoing = ask("Keep going?")
    if keepGoing not in YesList:
        addingQuestions = False
        outputFile = open("default.txt","w")
        outputFile.writelines(my_data_string)
        
'''