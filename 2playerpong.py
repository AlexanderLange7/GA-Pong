import pygame

black = (0,0,0)
white = (255,255,255)

pygame.init()

size = 700,500
screen = pygame.display.set_mode(size)
pygame.display.set_caption("2 player pong")

done = False
clock = pygame.time.Clock()

def player1(x1, y1, xsize, ysize):
    pygame.draw.rect(screen, black, [x1, y1, xsize, ysize])

def player2(x2, y2, xsize, ysize):
    pygame.draw.rect(screen, black, [x2,y2,xsize,ysize])

def ball(ballx, bally):
    pygame.draw.circle(screen, black, [ballx,bally],20)

def Score1(score1):
    font = pygame.font.Font(None ,50)
    text = font.render(str(score1), True, black)
    screen.blit(text, [160, 0])

def Score2(score2):
    font = pygame.font.Font(None ,50)
    text = font.render(str(score2), True, black)
    screen.blit(text, [510, 0])

x1 = 5
y1 = 175
xsize = 35
ysize = 150
speed1 = 0

x2 = 660
y2 = 175
speed2 = 0

ballx = 350
bally = 250
speedx = 5
speedy = 5

score1 = 0
score2 = 0

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                speed1 = -10
            if event.key == pygame.K_s:
                speed1 = 10
            if event.key == pygame.K_UP:
                speed2 = -10
            if event.key == pygame.K_DOWN:
                speed2 = 10

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                speed1 = 0
            if event.key == pygame.K_s:
                speed1 = 0
            if event.key == pygame.K_UP:
                speed2 = 0
            if event.key ==  pygame.K_DOWN:
                speed2 = 0
                

    screen.fill(white)
    player1(x1, y1, xsize, ysize)
    player2(x2, y2, xsize, ysize)
    ball(ballx,bally)
    Score1(score1)
    Score2(score2)

    y1 += speed1
    y2 += speed2
    ballx += speedx
    bally += speedy

    if y1 < 0:
        y1 = 0

    if y1 > 350:
        y1 = 350

    if y2 < 0:
        y2 = 0

    if y2 > 350:
        y2 = 350

    if ballx+20 > x2 and bally-20 > y2 and bally+20 < y2+ysize and ballx < x2+3:
        speedx = -speedx

    if ballx-20 < x1+35 and bally-20 > y1 and bally+20 < y1+ysize and ballx > x1+38:
        speedx = -speedx

    if bally > 477 or bally < 23:
        speedy = -speedy

    if ballx < 13:
        score2 += 1
        ballx = 350
        bally = 250

    if ballx > 680:
        score1 += 1
        ballx = 350
        bally = 250
        

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
