#!/usr/bin/env python

from SoftOscilloscope import SocketClientPlot
plot = SocketClientPlot('localhost', 5000)
plot.start()
