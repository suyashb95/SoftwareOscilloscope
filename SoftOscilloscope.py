import serial, multiprocessing
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np

class Oscilloscope(object):
    def __init__(self, com_port, baud_rate):
        try:
            self.port = serial.Serial(com_port, baud_rate)
        except serial.SerialException, e:
            print e
            return
        self.fig = plt.figure()
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
        
    def plot_animate(self, fn):
        serial_data = self.port.readline().rstrip().split() 
        for data, plot in zip(serial_data, self.plot_list):
            try:
                plot[1]._yorig = np.roll(plot[1]._yorig, -1)
                plot[1]._yorig[-1] = float(data)
                plot[1]._invalidy = True
                #plot[0].relim()
                #plot[0].autoscale()
            except ValueError:
                pass
        return [x[1] for x in self.plot_list]
        
    def start(self):
        animated_plot = animation.FuncAnimation(self.fig, 
                                                self.plot_animate, 
                                                init_func=self.plot_init,
                                                interval=10,
                                                blit=True)
        try:
            plt.show()
        except KeyboardInterrupt or Exception:
            self.port.flushInput()
            self.port.flushOutput()
            self.port.close()