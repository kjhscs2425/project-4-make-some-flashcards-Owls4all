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
        for stat in ["question"]:#if a question has no question stat...
            if stat not in self.data.keys():
                #print(f"No {stat} stat!") #former debugging statement
                #print(dict_to_str(self.data,"|||","<<>>")) #this one too
                global questionList #access the list
                questionList.__delitem__(indexInList(self,questionList))#delete it!
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

user = ask("Username?") #which file to save to
chosenSet = '' #the display name of the set
questionSet = ''#the numerical index of the set (goes into save filename)
possibleSets = ["prices","mines","days","skills","fish","birthdays"] #the names (for display purposes)
while not questionSet in ["0","1",'2','3','4','5']: #when a valid set is chosen, stop asking.
    chosenSet = ask(f"What question set to use?\n{possibleSets}") #get user input - can take either a name or an index.
    if chosenSet == 'all': #secret bonus option
        if not os.path.isfile(f"{user}.txt"): #if there's no file for this mode...
            string = '' #start with an empty string
            for i in range(len(possibleSets)): #for every set,
                currentFile = f"{user}{i}.txt" #
                if os.path.isfile(f"{currentFile}"): #if the user has a file for it
                    string += open(currentFile,"r").read()#add it to the string
                else: #if not,
                    string += open(f"default{i}.txt",'r').read()#add the default to the string
        else: #if they do have a file for 'all' mode
            string = open(f"{user}.txt",'r').read() #read their file for it
        for q in string.split("###"): #convert the string to a list of question-dictionaries
            newQuest = quest(str_to_dict(q.replace('\n',''),"|||","<<>>")) #make the questions
            if "question" in newQuest.data.keys(): #if the new question isn't empty...
                questionList.append(newQuest) #add it to the list
        break        #and stop the choosing loop
    if chosenSet in possibleSets: #if they picked a set by name
        questionSet = f"{indexInList(chosenSet,possibleSets)}" #set the question to the associated number
    elif chosenSet in ["0","1",'2','3','4','5']: #otherwise if they chose a valid number
        questionSet = chosenSet #set the number accordingly
        chosenSet = indexInList(int(chosenSet),possibleSets) #then set the display name based on the number.
    else: #if they gave neither a name nor number...
        print('That question set does not exist! Please choose another!') #tell them to choose again.
if chosenSet != 'all': #if they didn't choose 'all'
    fileName = f"{user}{questionSet}.txt" #choose the save file with the appropriate set index
else:
    fileName = f"{user}.txt" #the user's name with no number for 'all' mode
if 'default' == user: #if they chose 'default' for their name
    forReal = ask("So you'll be adding questions then?") #it's probably me adding questions.
    if forReal in YesList: #if so
        mode = 'question' #set the mode accordingly
    else: #if not...
        mode = 'None' #...be annoying about it
        print("If you would like to corrupt the question source data, please edit the file directly.")
else:#if their name isn't 'default'
    mode = ask("run normally, view stats, or add questions?")#ask what they want to do
if 'normal' in mode: #check if they want to run normally
    print("Normal mode selected") #tell them what was chosen
    Tinitial = time.time() #note the initial time
    if os.path.isfile(f"{fileName}") and questionSet != 'all': #if they have a file...
        print(f"User file for {user} exists for chosen question set: loading stats")#...tell them, then...
        source_file = open(f"{fileName}","r").read()#...open it
    else:#otherwise use the default
        print(f"No file found for {user}. Loading default question set")
        if questionSet != 'all': #if the set is 'all' it will already have made the list.
            source_file = open(f"default{questionSet}.txt","r").read()#since it's not, read the appropriate file.
    for q in source_file.split("###"): #make it into a list of question-dictionaries
            newQuest = quest(str_to_dict(q.replace('\n',''),"|||","<<>>")) #turn them into quests
            if "question" in newQuest.data.keys():
                questionList.append(newQuest) #and, if they're not blank, add them to the list.
    cards = [] #empty list to add to
    for i in range(len(questionList)): #for each question in the list,
        q=questionList[i] #q refers to the question, i is its index in the questionList.
        if type(q.data) != dict: #if q has bad data, it gets deleted. 
            #print("there is a bad question - figure it out") #former debugging statement
            questionList.__delitem__(i) #deletes bad question
        else:
            if "show" not in q.data.keys(): #because if you reference a nonexistent stat it will crash
                print("There's a question missing a show stat.")
                for j in range(2): #assume it's the default and add 2 copies of it.
                    cards.append(i) #add the questionList index to the cards list
            else:
                show = q.data["show"] #get the actual number
                if type(show) == int: #if it's an int, 
                    for j in range(show): #add the question that many times
                        if r.randint(1,100) <= boxes[q.data['box']]: #roll for 5% per box chance to skip
                            cards.append(i) #add to the list
                        else: #if skipped, say so.
                            print(f"{q.data['question']} not shown due to being in box {q.data['box']}")
                else:
                    if show.isdigit(): #if it's a string that can be converted to int
                        for j in range(int(show)): #make it into an int, then add that many instances of the question.
                            if r.randint(1,100) <= boxes[q.data['box']]:#roll for 5% per box chance to skip
                                cards.append(i) #add to list
                            else: #if skipped, say so.
                                print(f"{q.data['question']} not shown due to being in box {q.data['box']}")
                    else: #if it is neither an int nor a string which can be converted to one...
                        print("Something has gone direly wrong") #...then something has gone direly wrong.
    #print(cards) #these were to test list-making
    deck = shuffle(cards,3) #randomize the order of the cards. If it would show the same card twice in a row, re-roll up to 3 times to prevent that.
    #print(deck)#and to test shuffling
    x = len(deck) #set for future reference. (the length changes as we take cards out to ask)
    for i in range(x): #for each card in the deck
        print(f"\nQuestion {i+1}. (out of {x})") #tell the user their progress so far
        chosenCard = deck.pop() #take the top card (this removes it from the list)
        questionList[chosenCard].askUser() #and ask the question
        
    Tfinal = time.time() #after that's all done, save the end time. used to calculate how long it took.
    outputFile = open(f"{fileName}","w")
    my_data_string = '' #empty string to add to later.
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
    for q in questionList: #for each question in the list
        print(q.showStats())#print question-specific stats
        if q.wrong == 0 and q.ask != 0 and q.data['box'] <5: #if it was perfect this run
            q.data['box'] +=1 #move it to a higher box
            q.oneLessQuestion() #and show it one less time (min 1)
        my_data_string += f"{dict_to_str(q.data,"|||","<<>>")}###\n" #make it into a string for saving
    outputFile.write(my_data_string) #after all of them are added to the string, write it to the file.
    statsFile = f"{user}{questionSet}stats.txt" 
    if os.path.isfile(statsFile): #check if there's already a stats file
        previousRuns = open(statsFile,'r').read()
    else:
        previousRuns = ''
    open(statsFile,'w').write(f"{previousRuns}\n{thisRunStats}") #write lifetime stats history to the file.
    print(thisRunStats) #print out the current run stats.
elif 'stats' in mode: #if they want all the stats
    source_file = f"{user}{questionSet}stats.txt" 
    if os.path.isfile(source_file): #if there are stats...
        print(open(source_file,'r').read()) #print all the stats!
    else: #if not,
        print(f"{user} has no saved stats for {chosenSet}.") #tell them there are no stats.
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