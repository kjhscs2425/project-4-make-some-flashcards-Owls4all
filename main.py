# Write your code here
from utility import *
class quest:
    def __init__(self,string):
        self.data = str_to_dict(string,"|||","<<>>")
        for key in self.data.keys():
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

