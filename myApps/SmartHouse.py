import serial
import time
import math
import os

#Blackboard
from pyrobotics import BB
from pyrobotics.messages import Response, Command
import subprocess

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

ban_ejec=0
s=" "

def LamparaHandler(sv):
	global ban_ejec
	global s	
	print sv.data
	if sv.data == "a1on":
		os.system('echo "rf a1 on" | nc localhost 1099')
	elif sv.data == "a1off":	
		os.system('echo "rf a1 off" | nc localhost 1099')
	elif sv.data == "a2on":
		os.system('echo "rf a2 on" | nc localhost 1099')
	elif sv.data == "a2off":	
		os.system('echo "rf a2 off" | nc localhost 1099')
	elif sv.data == "a3on":
		os.system('echo "rf a3 on" | nc localhost 1099')
	elif sv.data == "a3off":	
		os.system('echo "rf a3 off" | nc localhost 1099')

	ban_ejec=1
	


def Initialize():
    	BB.Initialize(2030, fmap)
    	BB.Start()
    	BB.CreateSharedVar(BB.SharedVarTypes.STRING, 'interface')
    	BB.CreateSharedVar(BB.SharedVarTypes.STRING, 'smarthause')
    	BB.SubscribeToSharedVar('smarthause',LamparaHandler, subscriptionType='writeothers', reportType='content')
	BB.SetReady()


def main():

	global ban_ejec
	global s
	magnetTime=" "
	movTime=" "
	magnetStatus= " "
	Initialize()
	while True:
		if ban_ejec==1:
			ban_ejec=0
			BB.WriteSharedVar(BB.SharedVarTypes.STRING, 'interface', s)
		os.system('echo "st" | nc localhost 1099')
		os.system('echo "st" | nc localhost 1099')
		os.system('echo "st" | nc localhost 1099')
		
		s= os.popen('echo "st" | nc localhost 1099').read(500)
		i = 0
		b_fin=0
		while b_fin==0:
			if s != "":
				i=i+1
				if s[i] == "7":
					i=i+1
					if s[i] == "7":
						i=i+1
						if s[i] == "E":
							i=i+1
							if s[i] == "D":
								i=i+1
								if s[i] == "0":
									i=i+1
									if s[i] == "0":	
										magnetTime= s[i+8] + s[i+9] + s[i+10] + s[i+11] + s[i+12]
										print magnetTime
										magnetStatus= s[i+14] + s[i+15] + s[i+16] + s[i+17] + s[i+18] + s[i+19] + s[i+20] + s[i+21] + s[i+22] + s[i+23] + s[i+24] + s[i+25] + s[i+26] + s[i+27] 
				 
				elif s[i] == "8":
					i=i+1
					if s[i] == "8":
						i=i+1
						if s[i] == "0":
							i=i+1
							if s[i] == "2":
								i=i+1
								if s[i] == "8":
									i=i+1
									if s[i] == "0":	
										movTime= s[i+8] + s[i+9] + s[i+10] + s[i+11] + s[i+12]
										print movTime
				elif s[i]=="E":
					i=i+1
					if s[i]=="n":
						i=i+1
						if s[i]=="d":
							b_fin=1
		s = magnetTime + " " + movTime + " " + magnetStatus
		BB.WriteSharedVar(BB.SharedVarTypes.STRING, 'interface', s)				
		time.sleep(.5)


if __name__ == "__main__":

    main()

