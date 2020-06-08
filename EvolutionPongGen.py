'''
Evolutionary Pong
Alex Lange
June 4, 2020 - June 9, 2020
'''
#Import Statements
import pygame
from datetime import datetime
import os
import numpy as np
import pandas as pd
'''Global Variables'''
Black = (0,0,0)
White = (255,255,255)
Red = (255,0,0)
Violet = (75,0,130)
Orange = (255,69,0)

#Initialize Pygame
pygame.init()
#Fonts
nerdheader1 = pygame.font.Font('slkscreb.ttf', 25)
nerdheader2 = pygame.font.Font('slkscreb.ttf', 15)
#Blanks
p1win = nerdheader1.render('', True, Violet)
p2win = nerdheader1.render('', True, Orange)
#Once won, swap text and exit
winner = False
#Set the Size of The screen, and set up the screen.
size = 1200,1000
screen = pygame.display.set_mode(size)
pygame.display.set_caption("EvolutionPong")
#The game is NOT done.
done = False
clock = pygame.time.Clock()
#file for data collection
file_object = 0
#y values for the AI players
y1command=0
y2command=0


'''Definitions for objects in the Game'''
#Player1
def player1(x1, y1, xsize, ysize):
    pygame.draw.rect(screen, Violet, [x1, y1, xsize, ysize])
#Player2
def player2(x2, y2, xsize, ysize):
    pygame.draw.rect(screen, Orange, [x2,y2,xsize,ysize])

#Ball
def ball(ballx, bally):
    pygame.draw.circle(screen, White, [ballx,bally],20)
#Score for P1
def Score1(score1):
    font = pygame.font.Font('slkscr.ttf' ,50)
    text = font.render(str(score1), True, Violet)
    screen.blit(text, [160, 0])
#Score for P2
def Score2(score2):
    font = pygame.font.Font('slkscr.ttf' ,50)
    text = font.render(str(score2), True, Orange)
    screen.blit(text, [510, 0])





''' GENETIC ALGORITHM AND STEPS:
Our genetic algorithm will be a little different than most.
The plan is to create 2 unsupervised neural networks from the data we are collecting
constantly.
One unsupervised network will be player a,
one unsupervised network will be player b.

If either one reaches a score of 10,
the other network will become a copy of the winner,
and they will continue to play as a new "generation"
'''
from sklearn.tree import DecisionTreeClassifier

infile = pd.read_csv("testdata.csv")
feature_names = ['ballx', 'bally', 'y2', 'bouncenum','score1','score2']
x = infile[feature_names]
y = infile['y1']

feature_namesn2 = ['ballx', 'bally', 'y1', 'bouncenum','score1','score2']
xn2 = infile[feature_namesn2]
yn2 = infile['y2']


#Import Train Test Split
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(x,y,random_state=0)
x2_train,x2_test,y2_train,y2_test = train_test_split(xn2,yn2,random_state=0)
#Preprocess the data by scaling
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()

x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)
clf = DecisionTreeClassifier().fit(x_train, y_train)

x2_train = scaler.fit_transform(x2_train)
x2_test = scaler.transform(x2_test)
clf2 = DecisionTreeClassifier().fit(x2_train, y2_train)


#Make a method that gets the current game stats and decides what to do with y1
def getNNmovement1(ballx,bally,y1,y2,score1,score2,bouncenum):
    global y1command
    global y2command
    finalinputs = np.reshape([ballx, bally, y2, bouncenum, score1, score2],(1,-1))
    y1command = clf.predict(finalinputs)
    finalinputs = np.reshape([ballx, bally, y1, bouncenum, score1, score2],(1,-1))
    y2command = clf2.predict(finalinputs)
    print(str(y1command[0])+"   "+str(y2command[0]))
    
#Internal Game Variables
#Player 1 and Paddle Size
x1 = 5
y1 = 175
xsize = 35
ysize = 150
speed1 = 0
#Player 2
x2 = 660
y2 = 175
speed2 = 0
#Ball Params
ballx = 350
bally = 250
speedx = 4
speedy = 4
#Player Scores
score1 = 0
score2 = 0

#Statistics
bouncenum = 0
cumulative = 0
abpp = 0.0

#While the Script isn't over
getNNmovement1(ballx,bally,y1,y2,score1,score2,bouncenum)
while not done:
    
    #Player1 locations
    if y1command < y1:
        speed1 = -10
        print("P1 going up")
    if y1command > y1:
        speed1 = 10
        print("P1 going down")
            #Player2 Location    
    if y2command < y2:
        speed2 = -10
        print("P2 going up")
    if y2command > y2:
        speed2 = 10
        print("P2 going down")
    
    if y2command== y2:
        speed=0
        print("HALT P2")
    if y1command ==y1:
        speed=0
        print("HALT P1")

    #Fill the screen
    screen.fill(Black)
    #Draw lines for where the ball scores.
    pygame.draw.line(screen,Red,(0,500),(0,0),8)
    pygame.draw.line(screen,Red,(698,0),(698,500),9)
    #Draw The Boundary Lines for Clarification.
    pygame.draw.line(screen, White, (705,0),(705,500),5)
    pygame.draw.line(screen, White, (0,502),(707,502),5)
    #Write all of the objects atop the screen.
    player1(x1, y1, xsize, ysize)
    player2(x2, y2, xsize, ysize)
    ball(ballx,bally)
    #Modify stats for next draw
    y1 += speed1
    y2 += speed2
    ballx += speedx
    bally += speedy


    #Boundaries
    if y1 < 0:
        y1 = 0

    if y1 > 350:
        y1 = 350

    if y2 < 0:
        y2 = 0

    if y2 > 350:
        y2 = 350
    
    #Collision Detection
    if ballx+20 > x2 and bally-20 > y2 and bally+20 < y2+ysize and ballx < x2+3:
        #flip ball direction
        speedx = -speedx
        #up the bouncenum stat and speed up ball by one
        bouncenum = bouncenum+1
        if speedx>0 and speedx<20:
            speedx = speedx+1
        else:
            speedx = speedx-1

    if ballx-20 < x1+35 and bally-20 > y1 and bally+20 < y1+ysize and ballx > x1+38:
        #flip ball direction
        speedx = -speedx
        #up the bouncenum and speed up ball by one
        bouncenum=bouncenum+1
        if speedx>0 and speedx<20:
            speedx = speedx+1
        else:
            speedx = speedx-1

    if bally > 477 or bally < 23:
        speedy = -speedy

    if ballx < 13:
        score2 += 1
        ballx = 350
        bally = 250
        #reset speed
        speedx = 4
        #reset bouncebacks and calculate current stats
        cumulative+=bouncenum
        bouncenum = 0
        abpp = cumulative/(score2+score1)

    if ballx > 680:
        score1 += 1
        ballx = 350
        bally = 250
        #reset speed
        speedx = 4
        #reset bouncebacks and calculate current stats
        cumulative+=bouncenum
        bouncenum = 0
        abpp = cumulative/(score2+score1)
       
    '''Check for win'''
    if(score1 == 5):
        p1win = nerdheader1.render('Player 1 Wins!', True, Violet)
        winner = True
    elif(score2 == 5):
        p2win = nerdheader1.render('Player 2 Wins!', True, Orange)
        winner = True
    else:{}
        
    '''
    STATS FOR NERDS
    The following is a bunch of visual blits for all the nerdy
    statistics which will be recorded and thrown into our network.
    '''
    header = nerdheader1.render('Stats For Nerds', True, White)
    stat1 = nerdheader2.render('Number of bouncebacks:',True,White)
    stat1a = nerdheader2.render( str(bouncenum) ,True,White)
    stat2 = nerdheader2.render('Cumulative bouncebacks:',True,White)
    stat2a = nerdheader2.render(str(cumulative),True,White)
    stat3 = nerdheader2.render('Avg bounces per point:',True,White)
    stat3a = nerdheader2.render(str(round(abpp,3)),True,White)
    stat4 = nerdheader2.render('Current Ball Position:',True,White)
    stat4a = nerdheader2.render(str(ballx)+" " +str(bally),True,White)
    stat5 = nerdheader2.render('Player 1 Upper Y-Loc:',True,White)
    stat5a = nerdheader2.render(str(y1),True,Violet)
    stat5b = nerdheader2.render('Player 2 Upper Y-Loc:',True,White)
    stat5c = nerdheader2.render(str(y2),True,Orange)
    screen.blit(header, [800,10])
    screen.blit(stat1, [710,40])
    screen.blit(stat1a, [1020,40])
    screen.blit(stat2,[710,60])
    screen.blit(stat2a,[1020,60])
    screen.blit(stat3,[710,80])
    screen.blit(stat3a,[1020,80])
    screen.blit(stat4,[710,100])
    screen.blit(stat4a,[1020,100])
    screen.blit(stat5, [710,120])
    screen.blit(stat5a, [1020,120])
    screen.blit(stat5b, [710,140])
    screen.blit(stat5c, [1020,140])
    '''
    End Stats for Nerds
    '''
    
    screen.blit(p1win,[150,250])
    screen.blit(p2win,[150,250])
    Score1(score1)
    Score2(score2)
    
    getNNmovement1(ballx,bally,y1,y2,score1,score2,bouncenum)
    
    '''Record Information for the GA'''
    '''Check Fitness in the winner text'''
    if(winner):
        pygame.display.flip()
        pygame.time.delay(2000)
        pygame.quit()
        quit()
    
    
    pygame.display.flip()
    clock.tick(30)
pygame.quit()
