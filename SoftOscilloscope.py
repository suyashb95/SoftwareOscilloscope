import serial, multiprocessing
import matplotlib.pyplot as plt
from matplotlib import animation
from collections import deque
import numpy as np

class Oscilloscope(object):
    def __init__(self, com_port, baud_rate):
        try:
            self.port = serial.Serial(com_port, baud_rate)
        except SerialException, e:
            print e
            return
        self.fig = plt.figure(figsize=(15,15))
        self.plot_list = []
        
    def plot_init(self):
        trial_data = self.port.readline().rstrip().split()
        num_subplots = int(math.ceil(math.sqrt(len(trial_data)))      
        for i in xrange(len(trial_data)):
            ax = self.fig.add_subplot(num_subplots, num_subplots, i)
            line = ax.plot([], [])
            data = deque([0.00]*x_lim, maxlen=x_lim)
            self.plot_list.append((ax, line, data))
        return [x[1] for x in self.plot_list]
        
    def animate(self):
        serial_data = self.port.readline().rstrip().split() 
        for data, plot in zip(serial_data, self.plot_list):
            try:
                plot[2].append(float(data))
                plot[1].set_xdata(np.arange(len(plot[2])))
                plot[1].set_ydata(plot[2])
            except ValueError:
                pass
        return [x[1] for x in self.plot_list]
        
    def start(self):
    
        
    
         
    
        
        
            
            
        
        
        
            
        
                                  
    

