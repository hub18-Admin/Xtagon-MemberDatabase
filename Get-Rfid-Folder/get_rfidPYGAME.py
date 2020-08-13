#!/usr/bin/python
from time import sleep
import serial
import re
import psycopg2

import pygame, sys
from pygame.locals import *

# set up pygame
pygame.init()

#i
i = 0

# set up the window
windowSurface = pygame.display.set_mode((500, 400), 0, 32)
pygame.display.set_caption('Members')
# set up fonts
basicFont = pygame.font.SysFont(None, 48)


con = psycopg2.connect(database="x_db", user="x_db", password="4icfYGm8e5iwGlXp", host="127.0.0.1", port="5432")

ser = serial.Serial("/dev/ttyACM0",9600)
while True:
    line = ser.readline(16384).decode("utf-8")
    line = line.split(',')
    hexstring = ""
    
    for x in line:
        hexstring+=hex(int(x,2))[2:]
        hexstring+=":"
    hexstring=hexstring[0:-1]

    print('Found tag with id '+hexstring)

    cur = con.cursor()
    cur.execute("SELECT member_id,first_name,last_name,cash FROM members WHERE rfid=%s", [hexstring])
    rows = cur.fetchall()

    windowSurface.fill((255,255,255))
    
    if len(rows)==0:
        print("Member not found")
        text = basicFont.render('Member not found', True, (255,255,255), (0,0,255))
        textRect = text.get_rect()
        textRect.centerx = 200
        textRect.centery = 20
    else:
        print("Found member")
        print("member_id: "+str(rows[0][0]))
        print("fist_name: "+ rows[0][1])
        print("last_name: "+ rows[0][2])
        print("cach: "+ str(rows[0][3]))
        
        text = basicFont.render('Member found '+rows[0][1], True, (255,255,255), (0,0,255))
        textRect = text.get_rect()
        textRect.centerx = 200
        textRect.centery = 20
        windowSurface.fill((255,255,255))
        textRect.centery = 20+i
        windowSurface.blit(text, textRect)
        i+=1
        pygame.display.update()

        
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        

    print("")
# run the game loop

    sleep(1)

con.close()
