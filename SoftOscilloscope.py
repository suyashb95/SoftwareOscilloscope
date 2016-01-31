import serial, multiprocessing, socket
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
            
class BasePlot(object):
    def __init__(self, stream, **kwargs):
        self.stream = stream
        self.fig = plt.figure()
        self.fig.canvas.mpl_connect('close_event', self.handle_close_event)
        self.plot_list = []
        self.xlim = kwargs.get('xlim', (0, 500))
        self.ylim = kwargs.get('ylim', (-100, 100))
        self.interval = kwargs.get('interval', 1)
        self.read_size = kwargs.get('read_size', 1)
        self.autoscale = kwargs.get('autoscale', True)

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
            axes = self.fig.add_subplot(len(trial_data), 1, i)
            axes.set_xlim(self.xlim[0], self.xlim[1], auto=self.autoscale)
            axes.set_ylim(self.ylim[0], self.ylim[1], auto=self.autoscale)
            axes.grid(True)
            line_data = np.zeros(self.xlim[1])
            line, = axes.plot([], [], animated=True)
            line.set_data(np.arange(self.xlim[1]), line_data)
            self.plot_list.append([axes, line, line_data])
        return [x[1] for x in self.plot_list]
        
    def plot_animate(self, fn):
        stream_data = []
        for _ in xrange(self.read_size):
            stream_data.append(self.stream.readline().rstrip().split())
        stream_data = np.array(stream_data).T 
        print stream_data
        for data, plot in zip(stream_data, self.plot_list):
            try:
                if(sef.read_size < plot[0].get_ylim()):
                    plot[1]._yorig = np.roll(plot[1]._yorig, -self.read_size)
                    plot[1]._yorig[-self.read_size:] = data
                else:
                    plot[1]._yorig = data
                plot[1]._invalidy = True
            except ValueError:
                pass
            except Exception, message:
                print message
                return [x[1] for x in self.plot_list]
 
    def start(self):
        try:
            self.open_stream()
            animated_plot = animation.FuncAnimation(
                self.fig, 
                self.plot_animate, 
                init_func=self.plot_init,
                interval=1,
                blit=True)
            plt.show()
        except Exception, message:
            print message
            self.close_stream()       

class SerialPlot(BasePlot):
    def __init__(self, com_port, baud_rate):
        self.serial_port = serial.Serial()
        self.serial_port.baud_rate = baud_rate
        self.serial_port.port = com_port
        super(SerialPlot, self).__init__(self.serial_port)
        
           
class SocketPlot(BasePlot):
    def __init__(self, address, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(5)
        self.socket_params = (address, port)
        self.socket.connect((address, port))
        super(SocketPlot, self).__init__(self.socket.makefile())
        
    def open_stream(self):
        try:
            self.socket.connect(self.socket_params)
            self.socket.settimeout(5)
            self.stream = self.socket.makefile()
        except:
            pass
        
class GenericPlot(BasePlot):
    def __init__(self, stream):
        if hasattr(stream, 'open') \
        and hasattr(stream, 'close') \
        and hasattr(stream, 'readline'):
            super(GenericPlot, self).__init__(stream)
        else:
            raise BadAttributeError("One of the open/close/readline attributes is missing")           