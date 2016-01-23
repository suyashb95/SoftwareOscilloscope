import serial, multiprocessing, socket
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np

class Oscilloscope(object):
    def __init__(self, stream=None):
        self.stream = None
        self.stream_type = None
        self.fig = plt.figure()
        self.fig.canvas.mpl_connect('close_event', self.handle_close)
        self.plot_list = []
        self.stream_is_open = False
        self.stream_args = None
            
    def init_serial(self, com_port, baud_rate):
        try:
            self.stream = serial.Serial()
            self.stream.port = com_port
            self.stream.baud_rate = baud_rate
            self.stream_type = 'serial'
            self.stream_args = (com_port, baud_rate)
        except SerialException, message:
            print message
            return
            
    def init_socket(self, address, port):
        try:
            self.stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.stream.connect((address, port))
            self.settimeout(5)
            self.stream = self.stream.makefile()
            self.stream_is_open = True
            self.stream_type = 'socket'
            self.stream_args = (address, port)
        except SocketException, message:
            print message
            return
            
    def init_stream(self, stream):
        if hasattr(stream, 'readline'):
            if hasattr(stream, 'open') or hasattr(stream, 'connect'):
                self.stream = stream
                self.stream_type = 'generic'                  
            else:
                return
        else:
            return
            
    def open_stream(self):
        if self.stream is None:
            print "Stream not initialized."
            return
        if not self.stream_is_open
            try:
                if self.stream_type == 'serial':
                    self.stream.open()
                elif self.stream_type == 'socket':
                    self.init_socket()
                elif self.stream_type == 'generic':
                    if hasattr(self.stream, 'open'):
                        self.stream.open()
                    elif hasattr(self.stream, 'connect'):
                        self.stream.connect()
                    else
                        return
                 else:
                    return
                 self.stream_is_open = True
            except error, message:
                print message
                return
        else:
            return
            
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
        return [x[1] for x in self.plot_list]

    def handle_close(self, evt):
        self.close_stream()
     
    def close_stream(self):
        if hasattr(self.stream, 'flushInput'):
            self.stream.flushInput()
        if hasattr(self.stream, 'flushOutput'):
            self.stream.flushOutput()
        if hasattr(self.stream, 'close'):
            self.stream.close()
            print "stream closed"
          
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