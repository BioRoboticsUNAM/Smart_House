#!/usr/bin/env python
import rospy

import serial
import time
import math
import os

from pyrobotics import BB
from pyrobotics.messages import Response, Command

from Tkinter import *



s=" "
mov_time1 = 0
mov_time2 = 0
magnet_time1 = 0
magnet_time2 = 0
MagEntryTime = ""
MovEntryTime = ""
MagEntry = ""
MovEntry = ""

def cmd_one(c):
    time.sleep(1)
    return Response.FromCommandObject(c, True, 'cmd_one response')

def cmd_two(c):
    time.sleep(5)
    return Response.FromCommandObject(c, True, 'cmd_two response')


fmap = {
        'cmd_one' : cmd_one,
        'cmd_two' : (cmd_two, True)
        }



def fA1_on():
	global s
	s="a1on"
	BB.WriteSharedVar(BB.SharedVarTypes.STRING, 'smarthause', s)

def fA1_off():
	global s
	s="a1off"
	BB.WriteSharedVar(BB.SharedVarTypes.STRING, 'smarthause', s)

def fA2_on():
	global s
	s="a2on"
	BB.WriteSharedVar(BB.SharedVarTypes.STRING, 'smarthause', s)

def fA2_off():
	global s
	s="a2off"
	BB.WriteSharedVar(BB.SharedVarTypes.STRING, 'smarthause', s)
def fA3_on():
	global s
	s="a3on"
	BB.WriteSharedVar(BB.SharedVarTypes.STRING, 'smarthause', s)

def fA3_off():
	global s
	s="a3off"
	BB.WriteSharedVar(BB.SharedVarTypes.STRING, 'smarthause', s)



def f_st():
	global s
	s="st"
	BB.WriteSharedVar(BB.SharedVarTypes.STRING, 'smarthause', s)
	



def InterfaceHandler(sv):
	global MagEntryTime
	global MovEntryTime	
	global MagEntry
	global MovEntry
		
	print sv.data
	linea = sv.data.split()
	
	MagEntryTime.delete ( 0, END )
	MovEntryTime.delete ( 0, END )
	
	z= "LAST: " + linea[1]
	MagEntryTime.insert ( 5, z )
	z= "LAST: " + linea[0]
	MovEntryTime.insert ( 5, z )
	
	t_st = linea[2]
	t_mov = linea[1].split(":")
	t_mag = linea[0].split(":")
	mov_time1 = int(t_mov[0])
	mov_time2 = int(t_mov[1])
	magnet_time1 = int(t_mag[0])
	magnet_time2 = int(t_mag[1])	

	print magnet_time1
	if t_st == "Contact_alert_":
			MovEntryTime['bg']= 'red'	
			MagEntry.delete ( 0, END )
			MagEntry.insert ( 0, 'OPEN!!' )
			MagEntry['bg'] = 'red'
	else:
			MovEntryTime['bg']= 'green'
			MagEntry['bg'] = 'green'
			MagEntry.delete ( 0, END )
			MagEntry.insert ( 0, 'CLOSE' )


	if mov_time1 == 0:
		if mov_time2 < 20:
			print "ALERTA"
			MagEntryTime['bg']= 'red'			
			MovEntry.delete ( 0, END )
			MovEntry.insert ( 0, 'MOTION!!!' )
			MovEntry['bg'] = 'red'

	else:
			MagEntryTime['bg']= 'green'
			MovEntry['bg'] = 'green'
			MovEntry.delete ( 0, END )
			MovEntry.insert ( 0, 'NO MOTION' )
			

#Initialize Blackboard			
def Initialize():
    	BB.Initialize(2020, fmap)
    	BB.Start()
    	BB.CreateSharedVar(BB.SharedVarTypes.STRING, 'interface')
    	BB.CreateSharedVar(BB.SharedVarTypes.STRING, 'smarthause')
    	BB.SubscribeToSharedVar('interface',InterfaceHandler, subscriptionType='writeothers', reportType='content')
	BB.SetReady()


def main():
	
	global MagEntryTime
	global MovEntryTime
	global MagEntry
	global MovEntry	
	Initialize()
	while True:
		
		BB.WriteSharedVar(BB.SharedVarTypes.STRING, 'smarthause', s)
		ventana = Tk()
		ventana.wm_title('Smart Hause')
		
		OnA1Button = Button(ventana, width = 20, text = 'ON', bg = 'blue', activebackground = 'blue', command = fA1_on)
		OffA1Button = Button(ventana, width = 20, text = 'OFF', bg = 'blue', activebackground = 'blue', command = fA1_off)
		OnA2Button = Button(ventana, width = 20, text = 'ON', bg = 'blue', activebackground = 'blue', command = fA2_on)
		OffA2Button = Button(ventana, width = 20, text = 'OFF', bg = 'blue', activebackground = 'blue', command = fA2_off)
		OnA3Button = Button(ventana, width = 20, text = 'ON', bg = 'blue', activebackground = 'blue', command = fA3_on)
		OffA3Button = Button(ventana, width = 20, text = 'OFF', bg = 'blue', activebackground = 'blue', command = fA3_off)
				

		StLabel = Label(ventana, width = 20, bg = 'yellow', text =  'STATUS' )
		MagLabel = Label(ventana, width = 20, bg = 'blue', text =  'MAGNET' )
		MovLabel = Label(ventana, width = 20, bg = 'blue', text =  'MOTION DETECTOR' )
		LampLabelA1 = Label(ventana, width = 20, bg = 'yellow', text = 'LAMP A1')		
		LampLabelA2 = Label(ventana, width = 20, bg = 'yellow', text = 'LAMP A2')		
		LampLabelA3 = Label(ventana, width = 20, bg = 'yellow', text = 'LAMP A3')		
		LampLabel = Label(ventana, width = 20, bg = 'yellow', text = 'LAMPS	')		
		

		MovEntry = Entry(ventana, width = 20, foreground='black',background='green')
		MovEntry.insert ( 0, 'NORMAL' )
		MagEntry = Entry(ventana, width = 20, foreground='black',background='green')
		MagEntry.insert ( 0, 'NORMAL' )
		MagEntryTime = Entry(ventana, width = 20, foreground='black',background='green')
		MagEntryTime.insert ( 5, 'LAST: ' )
		MovEntryTime = Entry(ventana, width = 20, foreground='black',background='green')
		MovEntryTime.insert ( 5, 'LAST: ' )
		
		LampLabel.grid({'row':0, 'column':0 })
		LampLabelA1.grid({'row':1, 'column':0 })
		LampLabelA2.grid({'row':2, 'column':0 })
		LampLabelA3.grid({'row':3, 'column':0 })

		OnA1Button.grid({'row':1, 'column': 1})
		OffA1Button.grid({'row':1, 'column': 2})
		OnA2Button.grid({'row':2, 'column': 1})
		OffA2Button.grid({'row':2, 'column': 2})
		OnA3Button.grid({'row':3, 'column': 1})
		OffA3Button.grid({'row':3, 'column': 2})
				

		StLabel.grid({'row':4, 'column': 0})
		MagLabel.grid({'row':5, 'column': 0})
		MovLabel.grid({'row':5, 'column': 1})
		MovEntryTime.grid({'row':7, 'column': 0})
		MovEntry.grid({'row':6, 'column': 1})
		MagEntry.grid({'row':6, 'column': 0})
		MagEntryTime.grid({'row':7, 'column': 1})

		ventana.mainloop()
		

if __name__ == "__main__":

    main()
