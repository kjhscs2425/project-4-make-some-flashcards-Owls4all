
from math import *
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