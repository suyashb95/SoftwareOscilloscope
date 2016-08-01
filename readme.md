# Software Oscilloscope
An ongoing python project which takes in data from any stream(Serial port, TCP socket or any generic stream) and plot it in real time using matplotlib. The stream must implement open(), close() and readline() methods 
to work with the package.

## Installation
* Requires Python 2
* Clone the repo or download the zip
* Install VC++ for Python from [here](https://www.microsoft.com/en-in/download/details.aspx?id=44266)
* `cd` to the folder
* run `pip -install -r "requirements.txt"`
  
### Dependencies
* matplotlib 
* numpy
* pySerial

### Usage
* The stream has to implement open(), close() and readline() methods
* Data from multiple sources has to be space separated and each reading  must be on a new line</br>
  source1_value1 source2_value1</br>
  source1_value2 source2_value2</br>
  and so on
* X/Y axis limits,  Frame interval, Autoscaling(True by default) and the number of lines(1 by default) to read can be specified via     kwargs.
```python
'''
Uses the SocketPlot-Test example to plot a sine wave.
Run SocketPlot-Test.py on a different console window
'''
>>>from SoftOscilloscope import SocketClientPlot
>>>plot = SocketClientPlot('localhost', 5000)
>>>plot.start()

'''

Example for serial plots
'''
>>>from SoftOscilloscope import SerialPlot
>>>plot = SerialPlot('COM_PORT_NUMBER', BAUD_RATE)
>>>plot.start()

'''
Takes a generic stream and sets custom parameters
'''
>>>from SoftOscilloscope import GenericPlot
>>>plot = GenericPlot(
	myStream, 
	xlim=(-100,100),
	ylim=(-50, 50),
	interval=1, 
	autoscale=False,
	read_size=1)
>>>plot.start()
```

### Demos

Serial                                      |  Socket 
:------------------------------------------:|:-------------------------------------------:
![alt tag](http://i.imgur.com/OWu5wBS.gif)  |![alt tag](http://i.imgur.com/xwUVAz4.gif)
Plotting data from an Ultrasonic sensor     |  Plotting a sine wave from a TCP socket


### Contributions
If you want to add features, improve them, or report issues, feel free to send a pull request!
