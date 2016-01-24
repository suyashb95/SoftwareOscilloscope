import serial, multiprocessing, socket
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
            
class BasePlot(object):
    def __init__(self, stream):
        self.stream = stream
        self.fig = plt.figure()
        self.fig.canvas.mpl_connect('close_event', self.handle_close)
        self.plot_list = []
                
    def open_stream(self):
        self.stream.open()
        
    def close_stream(self):
        if hasattr(self.stream, 'flushInput'):
            self.stream.flushInput()
        if hasattr(self.stream, 'flushOutput'):
            self.stream.flushOutput()
        self.stream.close()
        print "stream closed"
        
    def handle_close_event(self, event):
        self.close_stream()

    def plot_init(self):
        trial_data = self.stream.readline().rstrip().split()
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
        stream_data = []
        for _ in xrange(read_size):
            stream_data.append(self.stream.readline().rstrip().split())
        stream_data = np.array(stream_data).T 
        for data, plot in zip(stream_data, self.plot_list):
            try:
                if(read_size < plot[0].get_ylim()):
                    plot[1]._yorig = np.roll(plot[1]._yorig, -read_size)
                    plot[1]._yorig[-read_size:] = data
                else:
                    plot[1]._yorig = data
                plot[1]._invalidy = True
            except ValueError:
                pass
            except error, message:
                print message
                return
        return [x[1] for x in self.plot_list]
 
    def start(self, read_size=1):
        self.open_stream()
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

class SerialPlot(BasePlot):
    def __init__(self, com_port, baud_rate):
        self.serial_port = serial.Serial()
        self.serial_port.baud_rate = baud_rate
        self.serial_port.com_port = com_port
        super(SerialPlot, self).__init__(self.serial_port)
        
           
class SocketPlot(BasePlot):
    def __init__(self, address, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(5)
        self.socket.connect((address, port))
        super(SocketPlot, self).__init__(self.socket.makefile())
        
    def open_stream(self):
        self.socket.connect((address, port))
        self.socket.settimeout(5)
        self.stream = self.socket.makefile()
        
class GenericStreamPlot(BasePlot):
    def __init__(self, stream):
        if hasattr(stream, 'open') \
        and hasattr(stream, 'close') \
        and hasattr(stream, 'readline'):
            super(GenericStreamPlot, self).__init__(stream)
        else:
            raise BadAttributeError("One of the open/close/readline attributes is missing")           