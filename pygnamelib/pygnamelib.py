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
# Version 0.1
def getname(background=0,namecolor=(0,0,0),helptext="What is your name?",helptextcolor=(0,0,0),maxcharacters=25,fps=20, font=None,surface=0):
    import sys
    import pygame
    import getpass
    clock = pygame.time.Clock()
    pygame.init()
    if not surface:
        print "You need to supply namelib with a surface"
        sys.exit()
    namefont = pygame.font.Font(font, 30)
    helptextfont = pygame.font.Font(font, 30)
    write = 1
    numb = ['1','2','3','4','5','6','7','8','9','0']
    letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    upper = 0
    remove = 0
    Name = getpass.getuser()
    while write:
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LSHIFT]:
            upper = 1
        elif keystate[pygame.K_CAPSLOCK]:
            upper = 1
        else:
            upper = 0
        if keystate[pygame.K_BACKSPACE]:
            if not remove:
                Name = Name[:-1]
            if remove > 10:
                Name = Name[:-1]
            else:
                remove += 2
        else:
            remove = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if str(pygame.key.name(event.key)) in letters + numb:
                    if upper:
                        Name += str(pygame.key.name(event.key)).upper()
                    else:
                        Name += str(pygame.key.name(event.key))
                    if Name.count("") == maxcharacters+1:
                        Name = Name[:-1]
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if Name == "": Name = getpass.getuser()
                write = 0
                pygame.key.set_repeat()
                return Name
        if background:
            surface.blit(background,(0,0))
        else:
            surface.fill((255,255,255))
        nameview = namefont.render(Name, True, namecolor)
        namerequest = helptextfont.render(helptext, True, helptextcolor)
        surface.blit(nameview,(40,150))
        surface.blit(namerequest,(40,120))
        pygame.display.update()
        clock.tick(fps)
