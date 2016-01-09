#Plot one port.

import numpy as np 
from matplotlib import pyplot as plt
from matplotlib import animation
from collections import deque
import serial,time

resolution = 25
Port = serial.Serial('COM27',9600,timeout = None,bytesize = 8,parity = 'N',stopbits = 1,xonxoff = 0,rtscts = 0)
fig = plt.figure()
ax = plt.axes(xlim = (0,resolution),ylim = (0,25))	#Defining limits
line, = ax.plot([],[])
#line2, = ax.plot([],[])
Ydata = deque([0.000]*resolution, maxlen = resolution) 	#Doubly ended queue, initial values are 0. 10 is the max length
#Y2data = deque([0.000]*resolution,maxlen = resolution)
	
def init():
	line.set_data([],[]) #Plot empty line first
	#line2.set_data([],[])
	return line, 
	
def animate(fn,line,Ydata):
	data1 = Port.readline().rstrip()
	if(data1):
		try:
			data1 = float(data1) 
			#data2 = float(data2)
			Ydata.append(data1)	#Append latest reading
			#Y2data.append(data2)
			line.set_xdata(np.arange(len(Ydata))) # Fill X Values with numbers from 0 to 99. Basically the length of Ydata
			line.set_ydata(Ydata)
			#line2.set_xdata(np.arange(len(Y2data)))
			#line2.set_ydata(Y2data)
			animate.count+=1
		except ValueError:
			pass
	if(animate.count>150):	#Flushing serial buffer.
		Port.flushInput()
		animate.count = 0;
		for i in range(5):
			Port.readline().rstrip()
	return line, 

animate.count = 0;		
		
anim = animation.FuncAnimation(fig,animate,fargs = (line,Ydata),init_func = init, interval = 1,blit = True)
try:
	plt.show()
except KeyboardInterrupt or Exception:
	Port.flushInput()
	Port.flushOutput()
	Port.close()
	print "Closed Port."