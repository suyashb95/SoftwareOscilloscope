# Software Oscilloscope
An ongoing python project which takes in data from any stream(Serial port, TCP socket or any generic stream)
and plot it in real time using matplotlib. The stream must implement open(), close() and readline() methods 
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

Serial                                      |  Socket 
:------------------------------------------:|:-------------------------------------------:
![alt tag](http://i.imgur.com/OWu5wBS.gif)  |![alt tag](http://i.imgur.com/xwUVAz4.gif)
Plotting data from an Ultrasonic sensor     |  Plotting a sine wave from a TCP socket


### Contributions
If you want to add features, improve them, or report issues, feel free to send a pull request!
