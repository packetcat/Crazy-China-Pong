#!/usr/bin/env python
import sys, pygame
from pygame.locals import *

pygame.init() and pygame.display.set_caption('Keypress Tool')

def main(startup=0):
    size = width, height = 200,100
    screen = pygame.display.set_mode(size)
    font = pygame.font.Font("data/FreeMonoBold.ttf", 96)
    bg = pygame.image.load("data/kptbg.png").convert()
    screen.blit(bg,(0,0))

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                screen.blit(bg,(0,0))
                if 0 > event.key < 999:
                    output = font.render("Err", True, (99,99,99))
                elif 9 < event.key < 100:
                    output = font.render("0"+str(event.key), True, (99,99,99))
                elif 0 < event.key < 10:
                    output = font.render("00"+str(event.key), True, (99,99,99))
                else:
                    output = font.render(str(event.key), True, (99,99,99))
                screen.blit(output,(15,0))
            else:
                screen.blit(bg,(0,0))
                output = font.render("---", True, (99,99,99))
                screen.blit(output,(15,0))
            pygame.display.update()

if __name__ == "__main__": main(2)