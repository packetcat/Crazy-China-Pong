#!/usr/bin/env python
#Coded by FCoFix.org - Robert C. Maehl - fcofix@aol.com
#
#This work is licensed under a Creative Commons Attribution-Commercial-ShareAlike 3.0 Unported License.
#
#Licensed Since 2012
#
import sys, pygame
from pygame.locals import *

pygame.init() and pygame.display.set_caption('Keypress Tool')

def render(screen,bg,output):
    screen.blit(bg,(0,0))
    screen.blit(output,(15,0))
    pygame.display.update()

def main():
    size = width, height = 200,100
    screen = pygame.display.set_mode(size)
    font = pygame.font.Font("data/FreeMonoBold.ttf", 96)
    bg = pygame.image.load("data/kptbg.png").convert()
    output = font.render("---", True, (00,00,00))
    render(screen,bg,output)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if 0 > event.key < 999:
                    output = font.render("Err", True, (00,00,00))
                elif 9 < event.key < 100:
                    output = font.render("0"+str(event.key), True, (00,00,00))
                elif 0 < event.key < 10:
                    output = font.render("00"+str(event.key), True, (00,00,00))
                else:
                    output = font.render(str(event.key), True, (00,00,00))
            else:
                output = font.render("---", True, (00,00,00))
        render(screen,bg,output)

main()
