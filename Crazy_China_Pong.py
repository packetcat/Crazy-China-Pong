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

import sys, pygame, random, getpass, os.path, time
from pygame.locals import *
from string import ascii_letters

#Developer notes to other developers (Format is: From - To - Message)
#Robert Maehl - Smartviking - Please name your variables better.
#Robert Maehl - Smartviking - We need to make it so the resources get reused instead of drawn with each game.
#Robert Maehl - ALL - I recommend using scite for editing from now on (sudo apt-get install scite)
#Robert Maehl - ALL - You can change scite's spacing and tabs using Ctrl + Shift + I

#Version Control
version = "1.4.2"
debug = ""
skipvid = False

for argument in sys.argv:
    if argument == "--novideo":
        skipvid = True
    if argument == "--version" or argument == "-v":
        print "Crazy China Pong version "+version
        if argument == sys.argv[-1]:
            sys.exit()
        else:
            pass
    if argument == "--credits":
        print "Crazy China Pong "+version+" Credits:\n\n"+\
            "Coding            : SmartViking\n"+" "*20+"Staticsafe\n"+" "*20+"Robert Maehl\n\n"+\
            "Artwork           : SmartViking"
        if argument == sys.argv[-1]:
            sys.exit()
        else:
            pass
    if argument == "--debug" or argument == "-d":
        open('.debug', 'w').close()
        debug = " - Debug"
    if argument == "--bug" or argument == "-b":
        if os.path.exists(".debug") == True:
            os.remove('.debug')
        if argument == sys.argv[-1]:
                sys.exit()
        else:
            pass
pygame.init() and pygame.display.set_caption('Crazy China Pong - '+version+debug)

def highscore(player,score):
    #Score output
    with open('.score', 'a') as f:
        f.write(player+","+str(int(score))+"\n")
    f.close()

def main(startup=0):
    clock = pygame.time.Clock() #FPS Clock Method used for Main()
    size = width, height = 600,400
    screen = pygame.display.set_mode(size)
    debug = os.path.exists(".debug")

    font = pygame.font.Font("data/FreeMonoBold.ttf", 12)
    endscorefont = pygame.font.Font("data/FreeMonoBold.ttf", 30)
    bonusfont = pygame.font.Font("data/FreeMonoBold.ttf", 17)

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
            screen.blit(bg,(0,0))
            namename = endscorefont.render(Name, True, (44,44,44))
            namerequest = endscorefont.render("Enter your name...", True, (213, 98, 0))
            screen.blit(namename,(40,150))
            screen.blit(namerequest,(40,120))
            pygame.display.update()
            clock.tick(20)
    else:
        Name = startup                
    score = 0

    #Intro Video
    if skipvid == False:
        if startup == 2:
            #Intro Video Variables
            vgunh = -100
            video = 1
            videocycle = 0
            vbonusw = 650
            vbbonusw = 650
            goodw = 700
            badw = 700
            vguyw = 650
            vguyh = 450
            vballh = -50
            coldw = 450
            coldh = -40
            vfarmer = guy
            enterh = -20
            enterstay = 0
            skipped = 0
            while video:
                videocycle += 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                        sys.exit()
                    if event.type == KEYDOWN and event.key == K_RETURN or event.type == KEYDOWN and event.key == K_SPACE:
                        video = 0
                screen.blit(bg,(0,0))

                if videocycle > 10 and videocycle < 250:
                    enternoaw = bonusfont.render("Press enter to skip", True, (255, 255, 255))
                    screen.blit(enternoaw,(100,enterh))
                    if enterh < 10 and not skipped:
                        enterh += 2
                    else:
                        skipped = 1
                        enterstay += 1
                        if enterstay > 100:
                            enterh -= 1
                if videocycle < 400:
                    vgunh += 1.2
                if videocycle < 125:
                    vbonusw -= 5
                    vprize = bonusfont.render("113", True, (255, 255, 255))
                    good = endscorefont.render("This is good.", True, (44,44,99))
                    screen.blit(good, (goodw,140))
                    screen.blit(bonus,(vbonusw,100))
                    screen.blit(vprize,(vbonusw+4,100))
                    if videocycle < 80:
                        goodw -= 7
                    elif videocycle > 80:
                        goodw += 10
                    else:
                        time.sleep(1.5)
                if videocycle > 130 and videocycle < 300:
                    vbbonusw -= 6
                    vbadprize = bonusfont.render("-42", True, (255, 255, 255))
                    bad = endscorefont.render("This is bad.", True, (222,54,19))
                    screen.blit(bad, (badw,230))
                    screen.blit(badbonus,(vbbonusw,180))
                    screen.blit(vbadprize,(vbbonusw+4,180))
                    if videocycle < 200:
                        badw -= 8
                    elif videocycle > 200:
                        badw += 10
                    else:
                        time.sleep(1.5)
                    if videocycle > 200 and videocycle < 235:
                        vgunh -= 4
                    if videocycle > 235 and videocycle < 260:
                        vgunh -= 1.2
                if videocycle > 230:
                    if videocycle > 280:
                        vballh += 0.7
                    if videocycle > 230 and videocycle < 360:
                        coldw -= 3
                        coldh += 0.7
                    cold = endscorefont.render("This is very good (and cold).", True, (255,224,219))
                    screen.blit(cold, (coldw,coldh))

                    if videocycle < 585:
                        screen.blit(freezeball, (440,vballh))
                    if videocycle > 600 and videocycle < 650:
                        coldw += 12

                if videocycle > 250:
                    if videocycle < 458:
                        vguyh -= 0.9
                        vguyw -= 3
                    else:
                        if videocycle == 458:
                            vfarmer = guy2
                        vguyh -= 0.7
                        vguyw += 3
                        if videocycle > 580 and vgunh > 125:
                            vgunh -= 1
                            if int(vgunh) <= 125:
                                textloop = 1
                                introtext1 = endscorefont.render("Do not let the Chinese rice", True, (0,50,0))
                                introtext2 = endscorefont.render("farmer escape to the western", True, (0,50,0))
                                introtext3 = endscorefont.render("world.", True, (0,50,0))
                                introtext4 = endscorefont.render("Stop him by controlling", True, (0,50,0))
                                introtext5 = endscorefont.render("the in game paddle", True, (0,50,0))
                                introtext6 = endscorefont.render("with the arrow keys.", True, (0,50,0))
                                introtext7 = endscorefont.render("You win if you have fun.", True, (0,50,0))
                                introtext8 = endscorefont.render("Good luck!", True, (0,50,0))
                                while textloop:
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                                            sys.exit()
                                        if event.type == KEYDOWN and event.key == K_RETURN or event.type == KEYDOWN and event.key == K_SPACE:
                                            video = 0
                                            textloop = 0

                                    screen.blit(bg,(0,0))
                                    screen.blit(introtext1,(70,60))
                                    screen.blit(introtext2,(70,90))
                                    screen.blit(introtext3,(70,120))
                                    screen.blit(introtext4,(70,170))
                                    screen.blit(introtext5,(70,200))
                                    screen.blit(introtext6,(70,230))
                                    screen.blit(introtext7,(70,290))
                                    screen.blit(introtext8,(340,340))
                                    screen.blit(gun,(30,vgunh))
                                    pygame.display.update()
                                    clock.tick(10)
                    screen.blit(vfarmer, (vguyw,vguyh))
                screen.blit(gun,(30,vgunh))
                pygame.display.update()
                clock.tick(50)

    farmer = guy2 #Farmer Image Direction
    gunh = 125 #Gun height
    guyh = 200 #Farmer height
    guyw = 280 #Farmer width
    east = 1 #Farmer Direction Variable

    guydirs = 0.2 #+/- Value guyh per loop
    if debug == True:
        guyspeed = 0
    else:
        guyspeed = 4
    gunspeed = 5
    scorespeed = 0.01 #Score

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
            #Vertical Limiting
            if guyh < -14 or guyh > 374:
                guyh = guyh-(8*(guyh/abs(guyh)))
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
                if guyw < 31 and guyh > gunh-20 and guyh < gunh+85 and guyw > 8:
                    east = 1
            else:
                guyw -= guyspeed
                if guyw < 31 and guyh > gunh-20 and guyh < gunh+85 and guyw > 8:
                    east = 1
                    guydirs = guydirs- (gunh-(guyh+20)+50)/50.0
                    if previousgh > gunh:
                        guydirs -= 0.9
                    elif previousgh < gunh:
                        guydirs += 0.9

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
                screen.blit(text,(0,369))
                pygame.display.update()
                if writefile:
                    highscore(Name,score)
                    writefile = 0
                clock.tick(10) #FPS and Resource limiting
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

                        screen.blit(bg,(0,0))
                        screen.blit(farmer,(guyw,guyh))
                        screen.blit(gun,(30,gunh))
                        stopten= 0
                        heightheight = 60
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
                        leaderboards = endscorefont.render("Highscores", True, (213,98,0))
                        screen.blit(leaderboards,(200,25))
                        enterpress = font.render("Press Enter...", True, (44,44,44))
                        screen.blit(enterpress,(250,10))
                        screen.blit(text,(0,369))

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
        text = font.render(" Score: "+str(int(score))+"  "+"Speed: "+str(int(guyspeed))+" ", True, (255, 255, 255), (213, 98, 0))
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
        if (score-bonuspoints) < 5000 and debug == False and not 2*(score-bonuspoints)/60 < 4 and not 0.02*(guyspeed/3) < 0.04:
            guyspeed = 2*(score-bonuspoints)/60
            scorespeed = 0.02*(guyspeed/3)
        elif debug == False:
            scorespeed = 0.04
            guyspeed = 4
            if guyspeed >= 22:
                guyspeed = 22
        else:
            guyspeed = 0
            scorespeed = 0.15  

        #Update Screen
        pygame.display.update()
        clock.tick(gamespeed)

if __name__ == "__main__": main(2)