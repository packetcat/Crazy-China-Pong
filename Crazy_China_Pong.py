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

import sys, pygame, random, getpass, os.path
from pygame.locals import *
from string import ascii_letters

#Version Control
version = "1.3.4"
debug = ""

for argument in sys.argv:
    if argument == "--version" or argument == "-v":
        print "Crazy China Pong version "+version
        sys.exit()
    if argument == "--credits":
        print "Crazy China Pong "+version+" Credits:\n\n"+\
            "Original Idea     : SmartViking\n\n"+\
            "Github Account    : Staticsafe\n\n"+\
            "Coding            : SmartViking\n"+" "*20+"Staticsafe\n"+" "*20+"Robert Maehl\n\n"+\
            "Debug             : SmartViking\n"+" "*20+"Staticsafe\n"+" "*20+"Robert Maehl\n\n"+\
            "Credits System    : Robert Maehl\n\n"+\
            "Sys Resource Mgmt : Robert Maehl" and sys.exit()
    if argument == "--debug" or argument == "-d":
	open('.debug', 'w').close()
	debug = " - Debug"
    if argument == "--bug" or argument == "-b":
	if os.path.exists(".debug") == True:
            os.remove('.debug')
	sys.exit()
pygame.init() and pygame.display.set_caption('Crazy China Pong - '+version+debug)

def highscore(player,score):
    #Score output
    with open('.score', 'a') as f:
        f.write(player+","+str(int(score))+"\n")
    f.close()

def main(startup=0):
    #FPS Clock Method used for Main()
    clock = pygame.time.Clock()
    size = width, height = 600,400
    screen = pygame.display.set_mode(size)
    debug = os.path.exists(".debug")

    font = pygame.font.Font("data/FreeMonoBold.ttf", 12)
    endscorefont = pygame.font.Font("data/FreeMonoBold.ttf", 30)
    bonusfont = pygame.font.Font("data/FreeMonoBold.ttf", 17)
    #Start Screen
    if startup == 2:
        write = 1
        Name = getpass.getuser()
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
                    if Name == "": Name = getpass.getuser()
                    write = 0
            screen.fill((255,255,255))
            namename = endscorefont.render(Name, True, (44,44,44))
            namerequest = endscorefont.render("Enter your name...", True, (213, 98, 0))
            screen.blit(namename,(40,150))
            screen.blit(namerequest,(40,120))
            pygame.display.update()
            clock.tick(20)
    else:
        Name = startup                
    score = 0

    #Image Importation
    gun = pygame.image.load("data/gun.png").convert()
    bg = pygame.image.load("data/bg.png").convert()
    guy = pygame.image.load("data/guy.png")
    guy2 = pygame.image.load("data/guy2.png")
    finished = pygame.image.load("data/finished.png")
    bonus = pygame.image.load("data/bonus_score.png")
    badbonus = pygame.image.load("data/bad_score.png")
    bgfreeze = pygame.image.load("data/bgfreeze.png")
    freezeball = pygame.image.load("data/freeze.png")

    #Farmer Image Direction
    farmer = guy2
    #Gun height
    gunh = 125.5
    #Farmer height and width
    guyh = 200
    guyw = 280
    #Farmer Direction Variable
    east = 1

    #+/- Value guyh per loop
    guydirs = 0.2
    if debug == True:
	guyspeed = 0
    else:
        guyspeed = 4
    gunspeed = 5
    #Score
    scorespeed = 0.01

    badbonusw = 650
    bonusw = 650
    bonusactive = 0
    bonuspoints = 0
    badbonusactive = 0
    gamespeed = 90

    balls = 0
    ballw = 0
    ballh = -50
    freeze = 0
    freezecycle = 0
    while 1:
        previousgh = gunh

        score += scorespeed
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit()
        keystate = pygame.key.get_pressed()
        if gunh > 300  or gunh < 0:
            gunh = gunh-((gunspeed-1)*(gunh/abs(gunh)))

        #Controls
	if debug == True:
	    if keystate[115]:
		gunh += gunspeed
	    if keystate[119]:
		gunh -= gunspeed
	    if keystate[pygame.K_UP]:
		guyh = guyh - 4
	    if keystate[pygame.K_DOWN]:
		guyh = guyh + 4
	else:
            if keystate[pygame.K_UP]:
                gunh -= gunspeed
            if keystate[pygame.K_DOWN]:
                gunh += gunspeed
        #Vertical Bounce
            if guyh < -10 or guyh > 370:
                guydirs = guydirs - (guydirs*2)
            guyh = guyh + guydirs

        #Horizontal Bounce
        if east:
            farmer = guy2
            if debug == True:
                if keystate[pygame.K_RIGHT]:
                    if guyw < 560:
		        guyw = guyw + 4
                    else:
			guyw = guyw
			east = 0
            else:
                guyw += guyspeed
            if guyw > 560:
                east = 0
        else:
            farmer = guy
	    if debug == True:
                if keystate[pygame.K_LEFT]:
		    guyw = guyw - 4
		    if guyw < 31 and guyh > gunh-40 and guyh < gunh+100 and guyw > 8:
			east = 1
	    else:
            	guyw -= guyspeed
            if guyw < 31 and guyh > gunh-40 and guyh < gunh+100 and guyw > 8:
                east = 1
                guydirs = guydirs- (gunh-(guyh+20)+50)/50.0
                if previousgh > gunh:
                    guydirs -= 0.8
                elif previousgh < gunh:
                    guydirs += 0.8

        #Pause Screen
        if guyw < 0:
            writefile = 1
            while 1:
                #Pause screen rendering
                screen.blit(bg,(0,0))
                screen.blit(finished,(0,0))
                text = endscorefont.render(" "*4+"Your final score was: "+str(int(score))+" "*40, True, (255, 255, 255), (213, 98, 0))
                screen.blit(farmer,(guyw,guyh))
                screen.blit(gun,(30,gunh))
                screen.blit(text,(0,365))
                pygame.display.update()
                if writefile:
		    if debug == False:
                        highscore(Name,score)
                    writefile = 0
                #FPS and Resource limiting
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
                        f.close

                        screen.fill((255,255,255))
                        stopten= 0
                        heightheight = 80
                        for i in sorted(playerscore.keys(), reverse=True):
                            stopten += 1
                            textplayers = endscorefont.render(playerscore[i], True, (44,44,44))
                            screen.blit(textplayers,(50,heightheight))
                            textscore = endscorefont.render(str(i), True, (44,44,44))
                            r = textscore.get_rect(center=(100,100))
                            r.right = 550
                            r.y = heightheight
                            screen.blit(textscore,r)
                            heightheight += 30
                            if stopten == 10:
                                break
                        leaderboards = endscorefont.render("Highscores:", True, (213,98,0))
                        screen.blit(leaderboards,(200,30))
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


        #Freeze ball
        randomball = random.randint(1,4000)
        if not balls and not freeze and randomball == 399:
            ballw = random.choice(range(100,550,50))
            balls = 1
        #Bonus
        randombonus = random.randint(1,1000)
        if not bonusactive and randombonus == 99:
            bonush = random.choice(range(10,390,10))
            bonusactive = 1
        #Bad bonus
        randombadbonus = random.randint(1,2000)
        if not badbonusactive and randombadbonus == 199:
            badbonush = random.choice(range(5,385,10))
            badbonusactive = 1
        #Rendering
        screen.blit(bg,(0,0))
        text = font.render(" Score:  "+str(int(score))+"   "+"Speed:  "+str(int(guyspeed))+" ", True, (255, 255, 255), (213, 98, 0))
        screen.blit(text, (50,10))


        if balls:
            screen.blit(freezeball,(ballw,ballh))
            ballh += 1
            if ballw < guyw+40 and ballw+40 > guyw and ballh+40 > guyh and ballh < guyh+40:
                ballh = -50
                freeze = 1
                balls = 0
            if ballh > 405:
                ballh = -50
                balls = 0

        #Bonus Calculations
        if bonusactive:
            if bonusw == 650:
                prize = random.randint(100,180)

            bonusamount = bonusfont.render(str(prize), True, (255, 255, 255))
            screen.blit(bonus,(bonusw,bonush))
            screen.blit(bonusamount,(bonusw+4,bonush))

            bonusw -= 2
            if bonusw < 30 and bonush+20 > gunh and bonush < gunh+100 and bonusw > 5:
                score += prize
                bonuspoints += prize
                bonusactive = 0
                bonusw = 650
            if bonusw < -50:
                bonusactive = 0
                bonusw = 650

        if badbonusactive:
            if badbonusw == 650:
                badprize = random.randint(-99,-30)

            badprizeamount = bonusfont.render(str(badprize), True, (255, 255, 255))
            screen.blit(badbonus,(badbonusw+1,badbonush-1))
            screen.blit(badprizeamount,(badbonusw+5,badbonush))

            badbonusw -= 3
            if badbonusw < 30 and badbonush+20 > gunh and badbonush < gunh+100 and badbonusw > 5:
                score += badprize
                bonuspoints += badprize
                badbonusactive = 0
                badbonusw = 650
            if badbonusw < -50:
                badbonusactive = 0
                badbonusw = 650
        screen.blit(farmer,(guyw,guyh))
        screen.blit(gun,(30,gunh))

        if freeze:
            gunspeed = 6
            score += 0.5
            bonuspoints += 0.5
            gamespeed = 60
            screen.blit(bgfreeze,(0,0))
            freezecycle += 1
            if freezecycle > 600:
                freeze = 0
                gamespeed = 90
                freezecycle = 0
                gunspeed = 5
		if debug == False:
                    scorespeed -= 0.03

        #The score algorithm
	if score < 0:
		score = 0
        if (score-bonuspoints) < 5000:
	    if debug == True:
	        guyspeed = 0
		scorespeed = 0.15
            else:
                guyspeed = 2*(score-bonuspoints)/60
                scorespeed = 0.02*(guyspeed/3)
            if 2*(score-bonuspoints)/60 < 4 and 0.02*(guyspeed/3) < 0.04:
	        if debug == True:
	            guyspeed = 0
                else:
                    guyspeed = 4
                scorespeed = 0.04
            if guyspeed >= 22:
                guyspeed = 22
	else:
	    if debug == True:
	        guyspeed = 0
		scorespeed = 0.15
	    else:
		guyspeed = 22
		scorespeed = 0.15  

        #Update Screen
        pygame.display.update()
        clock.tick(gamespeed)

if __name__ == "__main__": main(2)
