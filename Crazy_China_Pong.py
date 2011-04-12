#!/usr/bin/env python
"""
    Copyright (C) 2011  Smart Viking (smartestviking@gmail.com)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys, pygame, random
from pygame.locals import *
from string import ascii_letters

#This is where you edit the version stuff from now on
version = "1.2.1"

for argument in sys.argv:
    if argument == "--version" or argument == "-v":
        print "Crazy China Pong version "+version
        sys.exit()

pygame.init() and pygame.display.set_caption('Crazy China Pong - '+version)

def highscore(player,score):
    # Outputs score to a file
    with open('.score', 'a') as f:
        f.write(player+","+str(int(score))+"\n")
    f.close()


def main(startup=0):
    #clock method to control the frames per second, It's used at the bottom of main()
    clock = pygame.time.Clock()
    size = width, height = 600,400
    screen = pygame.display.set_mode(size)

    font = pygame.font.Font(None, 20)
    endscorefont = pygame.font.Font(None, 40)
    bonusfont = pygame.font.Font(None, 23)
    #This is starting like, the thing where you write your name
    if startup == 2:
        write = 1
        Name = ""
        while write:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                    sys.exit()
                if event.type == KEYDOWN:
                    if str(pygame.key.name(event.key)) in list(ascii_letters):
                        Name += str(pygame.key.name(event.key))
                        if Name.count("") == 16:
                            Name = Name[:-1]
                if event.type == KEYDOWN and event.key == K_BACKSPACE:
                    Name = Name[:-1]
                if event.type == KEYDOWN and event.key == K_RETURN:
                    if Name == "": Name = "unknown"
                    write = 0
            screen.fill((255,255,255))
            namename = endscorefont.render(Name, True, (44,44,44))
            namerequest = endscorefont.render("Write your name...", True, (213, 98, 0))
            screen.blit(namename,(40,150))
            screen.blit(namerequest,(40,120))
            pygame.display.update()
            clock.tick(20)

    else:
        Name = startup                
    score = 0

    #Importing the images, converting those that can be converted because it is more efficient or whatever
    gun = pygame.image.load("data/gun.png").convert()
    bg = pygame.image.load("data/bg.png").convert()
    guy = pygame.image.load("data/guy.png")
    guy2 = pygame.image.load("data/guy2.png")
    finished = pygame.image.load("data/finished.png")
    bonus = pygame.image.load("data/bonus_score.png")
    #Farmer is the variable that decides which way the guy is pointing, it's changed each time it hits the gun and the other side of the window
    farmer = guy2
    #The height of the gun
    gunh = 125.5
    #The height and width of the guy
    guyh = 200
    guyw = 280
    #Variable which decides if the farmer/guy is turning east or west
    east = 1

    #Guydirs basically is the value guyh will change each loop, it changes between positive and negative numbers
    guydirs = 0.2
    guyspeed = 4
    gunspeed = 5
    #How much the score will increase each loop
    scorespeed = 0.01

    bonusw = 650
    bonusactive = 0
    bonuspoints = 0

    while 1:
        score += scorespeed
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit()
        keystate = pygame.key.get_pressed()
        if gunh > 300  or gunh < 0:
            gunh = gunh-(4*(gunh/abs(gunh)))

        #Controls for the gun
        if keystate[pygame.K_UP]:
		gunh -= gunspeed
        if keystate[pygame.K_DOWN]:
		gunh += gunspeed
        #This part makes sure that the guy bounces in the other direction when he hits the top or the bottom
        if guyh < -10 or guyh > 370:
            guydirs = guydirs - (guydirs*2)
        guyh = guyh + guydirs

        #This part makes sure the guy bounces correctly on the east and west side
        if east:
            farmer = guy2
            guyw += guyspeed
            if guyw > 560:
                east = 0
        else:
            farmer = guy
            guyw -= guyspeed
            if guyw < 31 and guyh > gunh-40 and guyh < gunh+100 and guyw > 8:
                east = 1
                guydirs = guydirs- (gunh-(guyh+20)+50)/50.0

        #This is the "game over" pause screen
        if guyw < 0:
            writefile = 1
            while 1:
                #Put things different places for the pause screen
                screen.blit(bg,(0,0))
                screen.blit(finished,(0,0))
                text = endscorefont.render(" "*2+"Your final score was: "+str(int(score))+" (Bonus: "+str(bonuspoints)+")"+" "*40, True, (255, 255, 255), (213, 98, 0))
                screen.blit(farmer,(guyw,guyh))
                screen.blit(gun,(30,gunh))
                screen.blit(text,(0,365))
                pygame.display.update()
                if writefile:
                    highscore(Name,score)
                    writefile = 0
                #Limiting the FPS in the pause screen so it uses minimal resources
                clock.tick(10)
                for event in pygame.event.get():
                    if event.type == KEYDOWN and event.key == K_SPACE:
                        main(Name)
                    if event.type == pygame.QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                        sys.exit()
                    if event.type == KEYDOWN and event.key == K_h:
                        f = open(".score")
                        playerscore = {}
                        for line in f:
                            player,score = line.split(",")
                            playerscore[int(score)] = player
                    

                        screen.fill((255,255,255))
                        stopten= 0
                        heightheight = 80
                        for i in sorted(playerscore.keys(), reverse=True):
                            stopten += 1
                            textplayers = endscorefont.render(playerscore[i], True, (44,44,44))
                            screen.blit(textplayers,(100,heightheight))
                            textscore = endscorefont.render(str(i), True, (44,44,44))
                            screen.blit(textscore,(400,heightheight))
                            heightheight += 30
                            if stopten == 10:
                                break
                        leaderboards = endscorefont.render("Highscore!", True, (213,98,0))
                        screen.blit(leaderboards,(220,30))
                        enterpress = font.render("Press Enter...", True, (44,44,44))
                        screen.blit(enterpress,(250,10))
                        pygame.display.update()
                        brk = 1
                        while brk:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                                    sys.exit()
                                if event.type == KEYDOWN and event.key == K_RETURN or event.type == KEYDOWN and event.key == K_h:
                                    brk = 0

                        
        #The part that decides if there's gona be a bonus and if yes, where to put it
        randombonus = random.randint(1,500)
        if not bonusactive and randombonus == 100:
            bonush = random.choice(range(10,390,10))
            bonusactive = 1

        #Render all the stuff, it matters in what order they are drawed, obviously
        screen.blit(bg,(0,0))
        text = font.render(" Score:  "+str(int(score))+"   "+"Speed:  "+str(int(guyspeed))+" ", True, (255, 255, 255), (213, 98, 0))
        screen.blit(text, (50,10))

        #The part that does the various calculations regarding the bonus
        if bonusactive:
            if bonusw == 650:
                prize = random.randint(60,140)

            prizething = bonusfont.render(str(prize)+"P", True, (255, 255, 255))
            screen.blit(bonus,(bonusw,bonush))
            screen.blit(prizething,(bonusw+3,bonush))

            bonusw -= 2
            if bonusw < 30 and bonush+20 > gunh and bonush < gunh+100 and bonusw > 5:
                score += prize
                bonuspoints += prize
                bonusactive = 0
                bonusw = 650
            if bonusw < -50:
                bonusactive = 0
                bonusw = 650

        screen.blit(farmer,(guyw,guyh))
        screen.blit(gun,(30,gunh))

        #The score algorithm or whatever, the reason "bonuspoints" is there is so the guy will not increase in speed when you get a bonus, because he shouldn't since it's a bonus not a shortcut.
        if (score-bonuspoints) < 1000:
            guyspeed = 2*(score-bonuspoints)/60
            scorespeed = 0.02*(guyspeed/3)
            if 2*(score-bonuspoints)/60 < 4 and 0.02*(guyspeed/3) < 0.04:
                guyspeed = 4
                scorespeed = 0.04
            if guyspeed >= 22:
                guyspeed = 22

        #Update the new images or whatever
        pygame.display.update()
        clock.tick(90)


if __name__ == "__main__": main(2)
