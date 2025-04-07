
from math import *
import random as r
YesList = ['y','Y','Yes','yes','true','True','yeah'] #used with searchList to check for affirmative inputs
NoList = ['N','n','No','no','false','False','nah'] #used with searchList to check for non-affirmative inputs (im blanking on the word, ok)
def makeDegrees(angle):
    return 180*(angle/pi)
def makeRadians(angle):
    return pi*(angle/180)
def string_angle(angle):
    return f"{angle/pi} pi"
def ask(prompt):
    return(input(prompt+'\n>>> '))
def searchList(query,list): #returns True if query is in list, False otherwise
    for item in list:
        if item == query:
            return True
    return False
def indexInList(query,list): #returns list index if found, -1 if absent
    if searchList(query,list):
        for i in range(len(list)):
            if list[i] == query:
                return i
    else:
        return -1
def make_list(list):
    go = ask('add an item?')
    if searchList(go,YesList):
        list.append(ask("what to add?")) #broken, needs fixing
        make_list(list)
    else:
        print('ok thank you')
def question(list):
    query= ask('what to search for?')
    if (indexInList(query,list)) >= 0:
        print(f'{query} is in position {indexInList(query,list)} in the list')
    else:
        print(f'{query} is not in the list')
    if searchList(ask('look for something else?'),YesList):
        question(list)
def insert(thing,index,list):
    if index >=len(list):
        list.append(thing)
    else:
        for i in range((len(list)-index)+1):
            if i==0:
                list.append(list[-1])
            else:
                list[-i]=list[-i-1]
        list[index]=thing
def swaps(string,listOfpairs):
    if 'TEMP-STRING' in string:
        return string
    else:
        for pair in listOfpairs:
            string = string.replace(pair[0],f' TEMP-STRING{indexInList(pair,listOfpairs)} ')
            string = string.replace(pair[1],f' TEMP-STRING{indexInList(pair,listOfpairs)+len(listOfpairs)} ')
        for pair in listOfpairs:
            string = string.replace(f' TEMP-STRING{indexInList(pair,listOfpairs)} ',pair[1])
            string.replace(f' TEMP-STRING{indexInList(pair,listOfpairs)+len(listOfpairs)} ',pair[0])
    return string
def str_to_dict(string,outer,inner):
    workingDict = {}
    for pair in string.split(outer):
        things =  pair.split(inner)
        if len(things)==2:
            workingDict[things[0]]=things[1]
    return workingDict
def dict_to_str(dictionary,outer,inner):
    workingStr = ''
    for key in dictionary.keys():
        workingStr += f'{key}{inner}{dictionary[key]}{outer}'
    return workingStr
def shuffle(List:list,tries=0):
    attempt = 0
    foo = (len(List))
    newList = []
    for i in range(1,foo+1):
        index = r.randint(0,foo-i)
        if len(newList)==0:
            attempt = 0
            newList.append(List[index])
            List.__delitem__(index)
        elif index >= len(List):
            if len(List)!=0:
                index = index%len(List)
            else:
                pass
                #print("List is length 0!")
        elif newList[-1] != List[index]:
            attempt = 0
            newList.append(List[index])
            List.__delitem__(index)
        while not attempt >tries-1:
            index = r.randint(0,foo-i)
            if index >= len(List):
                if len(List)!=0:
                    index = index%len(List)
                else:
                    #print("List is length 0!")
                    return newList
            elif newList[-1] == List[index]:
                attempt +=1
            else:
                attempt = tries+5
        if len(List) >0:
            newList.append(List[index])
            List.__delitem__(index)
            attempt = 0
        else:
            return newList
        

    return newList
def makeNiceTime(seconds):
    minutes = seconds //60
    seconds = seconds %60
    if minutes >60:
        hours = minutes // 60
        minutes = minutes % 60
        if hours > 24:
            days = hours // 24
            hours = hours % 24
            return f"{days} days, {hours} hours, {minutes} minutes, and {ceil(seconds)} seconds."
        else:
            return f"{hours} hours, {minutes} minutes, and {ceil(seconds)} seconds."
    else:
        return f"{minutes} minutes and {ceil(seconds)} seconds."

def checkDiference(a,b):
    if a == b:
        return 0
    if len(a) >= len(b):
        long = a
        short = b
    else:
        long = b
        short = a
    if short in long:
        diff = len(long) - len(short)
    else:
        if long[0] == short[0]:
            diff = len(long) - len(short)
            for i in range(len(short)):
                if long[i] != short[i]:
                    diff += 1
        elif short[0] in long:
            diff = len(long)-len(short)
            for i in range(len(long)-long.index(short[0])):
                if long[long.index(short[0])+i] != short[i]:
                    diff +=1
        else:
            print('there occured a cornercase I didn\'t come up with an alogorithm for')
        return diff/len(long)