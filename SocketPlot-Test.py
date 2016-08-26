import asyncore, socket, time
import numpy as np 
from collections import deque

data = np.linspace(-np.pi, np.pi, 50)

class Server(asyncore.dispatcher):   
    def __init__(self, address):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET,socket.SOCK_STREAM)
        self.bind(address)
        self.listen(5)
        return 
        
    def handle_accept(self):
        global data
        client,addr = self.accept()
        print "Connected to " + str(addr)
        while(1):
            try:
                a = round(50 * np.sin(data[0]), 3)
                b = round(20*data[0], 3)
                client.send(str(a) + "," + str(b) + '\n')
                data = np.roll(data, 1)
                time.sleep(0.05)
            except Exception, message:
                print message
                self.close() 
                break
        
    def handle_close(self):
        self.close()
        print "Closing server."

if __name__ == '__main__':
    address = ('0.0.0.0',5000)
    server = Server(address)
    try:
        print "Server listening on " + str(address) 
        asyncore.loop(0.2,use_poll = True)
    except KeyboardInterrupt:
        print "Closing server."
        server.close()
        