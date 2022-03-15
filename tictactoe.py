#Tic-Tac-Toe
import random

#Initial state of board
row0=["-", "-", "-"]
row1=["-", "-", "-"]
row2=["-", "-", "-"]

def settoinitial():
    row0[0]="-"
    row0[1]="-"
    row0[2]="-"
    row1[0]="-"
    row1[1]="-"
    row1[2]="-"
    row2[0]="-"
    row2[1]="-"
    row2[2]="-"
    
    userchoices.clear()
    return None
    

def createandprintboard(x,y,usorcomp):
    if usorcomp == True:
        if x == 0:
            if y == 0:
                row0[0] = 1
            elif y==1:
                row0[1]=1
            elif y ==2:
                row0[2]=1
    
        elif x == 1:
           if y == 0:
               row1[0] = 1
           elif y==1:
               row1[1]=1
           elif y ==2:
               row1[2]=1
        
        elif x == 2:
           if y == 0:
               row2[0] = 1
           elif y==1:
               row2[1]=1
           elif y ==2:
               row2[2]=1
        
    if usorcomp == False:
        if x == 0:
            if y == 0:
                row0[0] = 0
            elif y==1:
                row0[1]=0
            elif y ==2:
                row0[2]=0
        
        elif x == 1:
           if y == 0:
               row1[0] = 0
           elif y==1:
               row1[1]=0
           elif y ==2:
               row1[2]=0
        
        elif x == 2:
           if y == 0:
               row2[0] = 0
           elif y==1:
               row2[1]=0
           elif y ==2:
               row2[2]=0
    return True
    
        
                
def checkifnumok(x,y):
    if x <0 or x>2:
        return(False)
    if x <0 or x>2:
        return(False)
    else:
        return(True)

def playerschoices():
    while True:
        x = int(input("Please specify which row you want to place your cross"))
        y = int(input("Please specify which column you want to place your cross"))
        if checkifnumok(x, y) == False:
            print("entered number out of range, please re-enter")
        else: 
            if [x,y] not in userchoices:
                userchoices.append([x,y])
                break
            else:
                print("entered row was already selected, please re-enter")
    return [x,y]   

def computerschoice():
    while True:
        #understand where are free spaces
        x = random.randint(0,2)
        y = random.randint(0,2)
        if [x,y] not in userchoices:
            userchoices.append([x,y])
            break
        else:
            pass
    return [x,y]
    
def checkwinnerdraw():
    #check for player
    if row0[0] ==1 and row1[0] ==1 and row2[0] == 1:
        return 1
    elif row0[1] ==1 and row1[1] ==1 and row2[1] == 1:
        return 1
    elif row0[2] ==1 and row1[2] ==1 and row2[2] == 1:
        return 1
    elif row0[0] ==1 and row0[1] ==1 and row0[2] == 1:
        return 1
    elif row1[0] ==1 and row1[1] ==1 and row1[2] == 1:
        return 1
    elif row2[0] ==1 and row2[1] ==1 and row2[2] == 1:
        return 1
    elif row0[0] ==1 and row1[1] ==1 and row2[2] == 1:
        return 1
    elif row0[2] ==1 and row1[1] ==1 and row2[0] == 1:
        return 1
    #check for computer
    if row0[0] ==0 and row1[0] ==0 and row2[0] == 0:
        return 0
    elif row0[1] ==0 and row1[1] ==0 and row2[1] ==0:
        return 0
    elif row0[2] ==0 and row1[2] ==0 and row2[2] == 0:
        return 0
    elif row0[0] ==0 and row0[1] ==0 and row0[2] == 0:
        return 0
    elif row1[0] ==0 and row1[1] ==0 and row1[2] == 0:
        return 0
    elif row2[0] ==0 and row2[1] ==0 and row2[2] == 0:
        return 0
    elif row0[0] ==0 and row1[1] ==0 and row2[2] == 0:
        return 0
    elif row0[2] ==0 and row1[1] ==0 and row2[0] == 0:
        return 0
    #check for draw
    if "-" not in row0 and "-" not in row1 and  "-" not in row2:
        return 3
    
    
userchoices= []
count = 1


#Game
print("Welcome to the game")
print(row0[0],"|",row0[1],"|",row0[2])
print("-","-","-","-","-")
print(row1[0],"|",row1[1],"|",row1[2])
print("-","-","-","-","-")
print(row2[0],"|",row2[1],"|",row2[2])

while True:
    
    print("Round ", count)
    
    y = playerschoices()
    print("you have chosen: ", y)
    createandprintboard(y[0],y[1], True)
    print(row0[0],"|",row0[1],"|",row0[2])
    print("-","-","-","-","-")
    print(row1[0],"|",row1[1],"|",row1[2])
    print("-","-","-","-","-")
    print(row2[0],"|",row2[1],"|",row2[2])
    
    
    
    y = computerschoice()
    print("Computer has chosen", y)
    createandprintboard(y[0],y[1], False)
    print(row0[0],"|",row0[1],"|",row0[2])
    print("-","-","-","-","-")
    print(row1[0],"|",row1[1],"|",row1[2])
    print("-","-","-","-","-")
    print(row2[0],"|",row2[1],"|",row2[2])
    
    count = count+1
    
    if checkwinnerdraw() == 1:
        print("User wins, congrats. Game over")
        x = input("want to play again? [y/n]")
        if x == "y":
            settoinitial()
            pass
        else:
            break
    elif checkwinnerdraw() ==2:
        print("Computer wins, maybe next time")
        x = input("want to play again? [y/n]")
        if x == "y":
            settoinitial()
            pass
        else:
            break
    elif checkwinnerdraw() ==3:
        print("Draw")
        x = input("want to play again? [y/n]")
        if x == "y":
            settoinitial()
            pass
        else:
            break
    else:
        print("continue")
        pass   
    
    
     
