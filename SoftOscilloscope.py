import serial
import socket
import sys
from PyQt5.QtWidgets import QApplication 
from PyQt5 import QtCore
import pyqtgraph as pg
import numpy as np

PY3 = True
if sys.version_info.major == 2:
    PY3 = False


class BasePlot(object):
    def __init__(self, stream, **kwargs):
        self.stream = stream
        try:
            self.app = QApplication([])
        except RuntimeError:
            self.app = QApplication.instance()
        self.view = pg.GraphicsView()
        self.layout = pg.GraphicsLayout(border=(100,100,100))
        self.view.closeEvent = self.handle_close_event
        self.layout.closeEvent = self.handle_close_event
        self.view.setCentralItem(self.layout)
        self.view.show()
        self.view.setWindowTitle('Software Oscilloscope')
        self.view.resize(800,600)
        self.plot_list = []

    def open_stream(self):
        print("Opening Stream")
        self.stream.open()
        
    def close_stream(self):
        if hasattr(self.stream, 'flushInput'):
            self.stream.flushInput()
        if hasattr(self.stream, 'flushOutput'):
            self.stream.flushOutput()
        self.stream.close()
        print("Stream closed")
        
    def handle_close_event(self, event):
        self.close_stream()
        self.app.exit()

    def readline(self):
        global PY3
        if PY3:
            return self.stream.readline().decode('utf8', errors='ignore').rstrip()
        else:
            return self.stream.readline().rstrip()

    def plot_init(self):
        for i in range(20):
            trial_data = self.readline().split(',')
        for i in range(len(trial_data)):
            new_plot = self.layout.addPlot()
            new_plot.plot(np.zeros(250))
            self.plot_list.append(new_plot.listDataItems()[0])
            self.layout.nextRow()
        
    def update(self):
        stream_data = self.readline().split(',')
        for data, line in zip(stream_data, self.plot_list):
            line.informViewBoundsChanged()
            line.xData = np.arange(len(line.yData))
            line.yData = np.roll(line.yData, -1)
            line.yData[-1] = data
            line.xClean = line.yClean = None
            line.xDisp = None
            line.yDisp = None
            line.updateItems()
            line.sigPlotChanged.emit(line)
 
    def start(self):
        self.open_stream()
        self.plot_init()
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(0)   
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            self.app.exec_()   

class SerialPlot(BasePlot):
    def __init__(self, com_port, baud_rate, **kwargs):
        self.serial_port = serial.Serial()
        self.serial_port.baudrate = baud_rate
        self.serial_port.port = com_port
        super(SerialPlot, self).__init__(self.serial_port, **kwargs)

class SocketClientPlot(BasePlot):
    def __init__(self, address, port, **kwargs):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_params = (address, port)
        self.socket.connect((address, port))
        self.stream = self.socket.makefile()  
        super(SocketClientPlot, self).__init__(self.stream, **kwargs)
        
    def open_stream(self):
        pass
        
    def close_stream(self):
        self.socket.close()
        self.stream.close()

class GenericPlot(BasePlot):
    def __init__(self, stream, **kwargs):
        if hasattr(stream, 'open') \
        and hasattr(stream, 'close') \
        and hasattr(stream, 'readline'):
            super(GenericPlot, self).__init__(stream, **kwargs)
        else:
            raise AttributeError("One of the open/close/readline attributes is missing")  
