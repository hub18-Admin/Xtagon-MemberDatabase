#!/usr/bin/python
from time import sleep
from datetime import datetime
import serial
import re
import psycopg2
 
con = psycopg2.connect(database="x_db", user="x_db", password="4icfYGm8e5iwGlXp", host="127.0.0.1", port="5432")
cur = con.cursor()
ser = serial.Serial("/dev/ttyACM0", 9600)
 
def readRFID():
    return ":".join([hex(int(x, 2))[2:] for x in ser.readline(16384).decode("utf-8").split(",")])
 
def getMemberByRFID(rfid):
    cur.execute("SELECT member_id, first_name, last_name, cash FROM members WHERE rfid=%s", [rfid])
    rows = cur.fetchall()
    if len(rows) == 0:
        return None
    else:
        return rows[0]
 
def getToolByRFID(rfid):
    cur.execute("SELECT tool_id, brand, label, location FROM tools WHERE rfid=%s", [rfid])
    rows = cur.fetchall()
    if len(rows) == 0:
        return None
    else:
        return rows[0]
 
def borrowTool(member_id, tool_id):
    cur.execute("INSERT INTO borrow (member_id, tool_id, date_borrowed) VALUES (%s, %s, %s)", [member_id, tool_id, datetime.now()])
 
while True:
    print("Scan your member rfid tag")
    member_rfid = readRFID()
    print(f"Found tag with id {member_rfid}")
    member = getMemberByRFID(member_rfid)
    if member:
        print(f"Found member\nmember_id: {str(member[0])}\nfist_name: {member[1]}\nlast_name: {member[2]}\ncash: {str(member[3])}\n")
        member_id = member[0]
        input("Press enter to continue")
        print("Scan the tool rfid tag")
        tool_rfid = readRFID()
        print(f"Found tag with id {tool_rfid}")
        tool = getToolByRFID(tool_rfid)
        if tool:
            print(f"Found tool\ntool_id: {str(tool[0])}\nbrand: {tool[1]}\nlabels: {tool[2]}\nlocation: {tool[3]}\n")
            tool_id = tool[0]
            borrowTool(member_id, tool_id)
            print("Member borrowed tool\n")
        else:
            print("Tool not found\n")
    else:
        print("Member not found\n")
    sleep(1)
con.close()