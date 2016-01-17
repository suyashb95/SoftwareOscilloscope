import serial, multiprocessing
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np

class Oscilloscope(object):
    def __init__(self, com_port, baud_rate):
        self.serial_args = (com_port, baud_rate)
        self.port = None
        self.fig = plt.figure()
        self.fig.canvas.mpl_connect('close_event', self.handle_close)
        self.plot_list = []
        
    def plot_init(self):
        trial_data = self.port.readline().rstrip().split()
        for i in xrange(1, len(trial_data) + 1):
            ax = self.fig.add_subplot(len(trial_data), 1, i)
            ax.set_xlim(0, 50, auto=False)
            ax.set_ylim(0, 100, auto=False)
            ax.grid(True)
            data = np.zeros(50)
            line, = ax.plot([], [], animated=True)
            line.set_data(np.arange(50), data)
            self.plot_list.append([ax, line, data])
        return [x[1] for x in self.plot_list]
        
    def plot_animate(self, fn, read_size=1):
        serial_data = []
        for _ in xrange(read_size):
            serial_data.append(self.port.readline().rstrip().split())
        serial_data = np.array(serial_data).T 
        for data, plot in zip(serial_data, self.plot_list):
            try:
                if(read_size < plot[0].get_ylim()):
                    plot[1]._yorig = np.roll(plot[1]._yorig, -read_size)
                    plot[1]._yorig[-read_size:] = data
                else:
                    plot[1]._yorig = data
                plot[1]._invalidy = True
                #plot[0].relim()
                #plot[0].autoscale()
            except ValueError:
                pass
        return [x[1] for x in self.plot_list]

    def handle_close(self, evt):
        self.close_stream()
     
    def close_stream(self):
        self.port.flushInput()
        self.port.flushOutput()
        self.port.close()
        print "Port closed"
          
    def start(self, read_size=1):
        self.port = serial.Serial(self.serial_args[0], self.serial_args[1])
        animated_plot = animation.FuncAnimation(
            self.fig, 
            self.plot_animate, 
            fargs = (read_size, ),
            init_func=self.plot_init,
            interval=1,
            blit=True)
        try:
            self.fig.show()
        except:
            self.close_stream()