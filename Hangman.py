# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 10:52:57 2021

@author: haefe
"""
import random

rows = [[" ","|-------"],["( )     ","|"],
        ["-|-    "," |"],["/\   ",'|--|--\''],
        ["    ","|------\""]]
count= 4

def hangman(x):
    if x == -1:
        for i in range(len(rows)):
            print(" ".join(map(str, rows[i])))
    #for every number below 4, print whole line starting from top
       
    else:
        y = 4-x
        for i in range(len(rows)):
                if i in range(y):
                    print(" ".join(map(str,rows[i])))
                else:
                    pass   
    
    
    
listofnames= ['alexander',"mike","raphael",
              "justin","joel","laura","lorena",
              'michelle','christine']
namelist = []
chosenname = random.choice(listofnames)
for i in chosenname:
    namelist.append(i)

    
#print(chosenname)
userguesses =[]

for i in range(len(chosenname)):
    userguesses.append("-")
print(" ".join(map(str, userguesses)))
hangman(-1)
print("you have ", count, " left")
      
while True:
    
    x = input("please enter a letter: ")
    if x not in namelist:
        print("letter not in name - please try again")
        count = count -1
        hangman(count)
        print("you have ", count, " guesses left")
    for i in range(len(namelist)):
        if namelist[i] == x:
            userguesses[i] = x
            print(" ".join(map(str, userguesses))) 
            hangman(count)
            print("you have ", count, " guesses left")
    if userguesses == namelist:
        print("You have guessed the right word! Congrats!")
        print("The name was:", chosenname)
        break
    elif count == 0:
        print("You loose")
        print("The name was:", chosenname)
        break
    else: pass
            