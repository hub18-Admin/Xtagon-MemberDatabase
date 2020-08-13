#!/usr/bin/python
from time import sleep
import serial
import re
import psycopg2
#i
i = 0

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
    
    if len(rows)==0:
        print("Member not found")
    else:
        print("Found member")
        print("member_id: "+str(rows[0][0]))
        print("fist_name: "+ rows[0][1])
        print("last_name: "+ rows[0][2])
        print("cash: "+ str(rows[0][3]))
        print("")
# run the game loop

    sleep(1)

con.close()
