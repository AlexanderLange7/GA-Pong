'''
Evolutionary Pong
Alex Lange
June 4, 2020 - June 9, 2020
'''

#Import Statement
import pygame


#Global Variables
#Colors Used in the Game
#The Violet and Orange are complementary colors to distinguish players
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

'''
GENETIC ALGORITHM AND STEPS

There are 4 different moves for each AI:
Hold down W/UP
Hold down S/DOWN
Release W/UP
Release S/DOWN

The Network should be aware of the following things:
ball's xy coords
ball's speed
y values of the paddles
y1
y2
(score?)


Fitness function is based on the score, being 10.
Generation will only ever have a pop. size of 2, so hopefully it picks
up on params fast.






'''




    


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
while not done:
    #Grab the Keystrokes
    for event in pygame.event.get():
        #If Pygame Quits
        if event.type == pygame.QUIT:
            #End the loop
            done = True
        #If a Key is being Held Down 
        if event.type == pygame.KEYDOWN:
            #Set Player1 Location
            if event.key == pygame.K_w:
                speed1 = -10
            if event.key == pygame.K_s:
                speed1 = 10
            #Set Player2 Location    
            if event.key == pygame.K_UP:
                speed2 = -10
            if event.key == pygame.K_DOWN:
                speed2 = 10

        #On a Key Release
        if event.type == pygame.KEYUP:
            #For All Params, S T O P
            if event.key == pygame.K_w:
                speed1 = 0
            if event.key == pygame.K_s:
                speed1 = 0
            if event.key == pygame.K_UP:
                speed2 = 0
            if event.key ==  pygame.K_DOWN:
                speed2 = 0
                
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
        if speedx>0:
            speedx = speedx+1
        else:
            speedx = speedx-1

    if ballx-20 < x1+35 and bally-20 > y1 and bally+20 < y1+ysize and ballx > x1+38:
        #flip ball direction
        speedx = -speedx
        #up the bouncenum and speed up ball by one
        bouncenum=bouncenum+1
        if speedx>0:
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
        
    if(score1 == 10):
        p1win = nerdheader1.render('Player 1 Wins!', True, Violet)
        winner = True
    elif(score2 == 10):
        p2win = nerdheader1.render('Player 2 Wins!', True, Orange)
        winner = True
    else:{}
        
    '''
    Stats for Nerds
    '''

    header = nerdheader1.render('Stats For Nerds', True, White)
    stat1 = nerdheader2.render('Number of bouncebacks:',True,White)
    stat1a = nerdheader2.render( str(bouncenum) ,True,White)
    stat2 = nerdheader2.render('Cumulative bouncebacks:',True,White)
    stat2a = nerdheader2.render(str(cumulative),True,White)
    stat3 = nerdheader2.render('Avg bounces per point:',True,White)
    stat3a = nerdheader2.render(str(round(abpp,3)),True,White)
    screen.blit(header, [800,10])
    screen.blit(stat1, [710,40])
    screen.blit(stat1a, [1020,40])
    screen.blit(stat2,[710,60])
    screen.blit(stat2a,[1020,60])
    screen.blit(stat3,[710,80])
    screen.blit(stat3a,[1020,80])
    '''
    End Stats for Nerds
    '''
    
    screen.blit(p1win,[150,250])
    screen.blit(p2win,[150,250])
    Score1(score1)
    Score2(score2)
    
    
    
    '''Record Information for the GA'''
    '''Check Fitness in the winner text'''
    if(winner):
        pygame.display.flip()
        pygame.time.delay(2000)
        pygame.quit()
        quit()
    
    
    pygame.display.flip()
    clock.tick(60)
pygame.quit()






'''
TO-DO for SATURDAY
    Make the Collision Detection Less Buggy
    Ramp up the Statistics for Nerds Space
    Make the Pong Ball a Square, and Smaller
    Make the Ball Start Slower, and Speed up based on # of Collisions
    Record Data into a CSV
'''