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
import sys, pygame
from pygame.locals import *
pygame.init()
pygame.display.set_caption('Crazy China Pong')


def main():
    score = 0
    clock = pygame.time.Clock()

    white = 255,255,255
    #the window size
    size = width, height = 600,400
    screen = pygame.display.set_mode(size)

    gun = pygame.image.load("data/gun.png")
    bg = pygame.image.load("data/bg.png")
    guy = pygame.image.load("data/guy.png")
    guy2 = pygame.image.load("data/guy2.png")
    finished = pygame.image.load("data/finished.png")
    farmer = guy2

    gunh = 125.5
    guyh = 200
    guyw = 280

    east = 1

    guydirs = 0.2
    guyspeed = 4
    gunspeed = 4
    scorespeed = 0.01
    while 1:
        score += scorespeed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit()
    
        gunhbackup = gunh
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_UP]:
            gunh -= gunspeed
        if keystate[pygame.K_DOWN]:
            gunh += gunspeed

        if guyh < -10 or guyh > 370:
            guydirs = guydirs - (guydirs*2)
        guyh = guyh + guydirs
        if gunh > 350 or gunh < -50:
            gunh = gunhbackup
    
        if east:
            farmer = guy2
            guyw += guyspeed
            if guyw > 560:
                east = 0
        else:
            farmer = guy
            guyw -= guyspeed
            if guyw < 30 and guyh > gunh-40 and guyh < gunh+100+0 and guyw > 10:
                east = 1
                guydirs = guydirs- (gunh-(guyh+20)+50)/100.0
        if guyw < 0:
            screen.blit(finished,(0,0))
            pygame.display.update()
            print "Your score was: "+str(int(score))
            while 1:
                #print "Your score was: "+str(int(score))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or if event.type == KEYDOWN and event.key == K_ESCAPE:
                        sys.exit()
                    if event.type == KEYDOWN and event.key == K_SPACE:
                        main()
        screen.blit(bg,(0,0))
        screen.blit(farmer,(guyw,guyh))
        screen.blit(gun,(30,gunh))
        
        font = pygame.font.Font(None, 17)

        text = font.render("Score:  "+str(int(score)), True, (255,
255, 255), (159, 182, 205))
        screen.blit(text, (520,10))
        pygame.display.update()
        clock.tick(100)

        if score > 30:
            if guyspeed == 4:
                guyspeed = 6
                scorespeed = 0.04
        if score > 60:
            if guyspeed == 6:
                guyspeed = 10
                scorespeed = 0.08
        if score > 100:
            if guyspeed == 10:
                scorespeed = 0.12
                guyspeed = 14
        if score > 170:
            if guyspeed == 14:
                guyspeed = 18
        if score > 250:
            if guyspeed == 18:
                scorespeed = 0.24
                guyspeed = 24
        if score > 1000:
            if guyspeed == 24:
                scorespeed = 0.5
                guyspeed = 30
main()

