#from asyncio.subprocess import PIPE
import random
import sys
import pygame
from pygame.locals import *


# Global variables for the game
FPS = 32  # Frame per second
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'python/game/flying.png'
BACKGROUND = 'python/game/background3.jpg'
PIPE = 'python/game/pipe2.png'

# WELCOME SCREEN
# Show welcome image on the screen


def WelcomeScreen():
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT-GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENHEIGHT-GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
        # IF USER CLICKS ON CROSS BUTTON CLOSE THE GAME
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        # if user click space or up key strat the game
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
                SCREEN.blit(GAME_SPRITES['message'],(messagex,messagey))
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0
#create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    #list of upper pipe
    upperPipes = [
        {'x':SCREENHEIGHT+200, 'Y':newPipe1[0]['y']},
        {'x':SCREENHEIGHT+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']},
    ]
    #list of lower pipes
    lowerPipes = [
        {'x':SCREENWIDTH+200, 'Y':newPipe1[1]['y']},
        {'x':SCREENHEIGHT+200+(SCREENWIDTH/2),'Y':newPipe2[1]['y']},
    ]

    pipeVelx = -4

    playerVely = -9
    playerMaxVely = 10
    playerMinVely = -8
    playerAccy = 1

    playerFlapAccv = -8 #velocity while flapping
    playerFlapped = False #true only when bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVely = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['hit'],play()

        crashTest = isCollide(playerx, playery, upperPipes,lowerPipes) #this will eturn true if the player is crashed
        if crashTest:
            return

        #check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score =1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()

        if playerVely < playerMaxVely and not playerFlapped:
            playerVely += playerAccy

        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVely, GROUNDY - playery - playerHeight)

        #move pipes to the left
        for upperPipe,lowerPipe in zip(upperPipes, lowerPipes):
             upperPipe['x'] += pipeVelx
             lowerPipe['x'] += pipeVelx

        #add a neww pipe when the first is abt to cross the leftmost part of thr screen
        if 0 < upperPipes[0]['x'] <5:
            newPipe =getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        #if the pipe i out of the screen, remove it
        if upperPipes[0]['x']<-GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        #lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'],(0,0))
        for upperPipe,lowerPipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperPipes['x'],upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'],lowerPipe['y']))
        
        SCREEN.blit(GAME_SPRITES['base'],(basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))  
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        xoffset = (SCREENHEIGHT-width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digits],(xoffset,SCREENHEIGHT*0.12))
            xoffset += GAME_SPRITES['numbers'][digits].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS) 

def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUNDY- 25 or playery < 0:
        GAME_SOUNDS['hits'].play()
        return True

    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight+pipe['y']and abs(playerx-pipe['x'])<GAME_SPRITES['pipe'][0].get_width()):
            GAME_SPRITES['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height()>pipe['y'])and abs(playerx-pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False


def getRandomPipe():
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0,int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()-1.2*offset))
    pipex = SCREENWIDTH+10
    y1 = pipeHeight - y2 + offset
    pipe = [{'x' : pipex, 'y': -y1},
            {'x' : pipex, 'y': y2}
    ]
    return pipe

if __name__ == "__main__":
    pygame.init()  # initialise all pygame modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by Swana')

    GAME_SPRITES['number'] = (
        pygame.image.load('python/game/o.png').convert_alpha(),
        pygame.image.load('python/game/one.png').convert_alpha(),
        pygame.image.load('python/game/two.png').convert_alpha(),
        pygame.image.load('python/game/three.png').convert_alpha(),
        pygame.image.load('python/game/four.png').convert_alpha(),
        pygame.image.load('python/game/five.png').convert_alpha(),
        pygame.image.load('python/game/six.png').convert_alpha(),
        pygame.image.load('python/game/seven.png').convert_alpha(),
        pygame.image.load('python/game/eight.png').convert_alpha(),
        pygame.image.load('python/game/nine.png').convert_alpha(),
    )

    GAME_SPRITES['message'] = pygame.image.load(
        'python/game/message.jpg').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load(
        'python/game/base2.png').convert_alpha()
    GAME_SPRITES['pipe'] = (pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
                            pygame.image.load(PIPE).convert_alpha()
                            )
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    # GAME SOUND
    GAME_SOUNDS['die'] = pygame.mixer.Sound('python/game/die.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('python/game/point.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('python/game/jump.wav')
    GAME_SOUNDS['jump'] = pygame.mixer.Sound('python/game/jump.wav')
    while True:
        WelcomeScreen()  # shows welcome sreen to the user until he presses the button
        mainGame()
