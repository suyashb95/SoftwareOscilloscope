from SoftOscilloscope import SocketClientPlot

class SocketServer(asyncore.dispatcher):
    def __init__(self, address, num_clients=5, **kwargs):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(address)
        self.listen(num_clients)

    def handle_accept(self):
        client, addr = self.accept()
        print "Connected to " + str(addr)
        SocketClientPlot(socket=client, address=addr).start()
        
    def handle_close(self):
        self.close()
        print "Closing server."
    
def run_server():
    address = ('0.0.0.0',5000)
    server = SocketServer(address)
    try:
        print "Server listening on " + str(address) 
        asyncore.loop(0.2, use_poll = True)
    except KeyboardInterrupt:
        print "Closing server."
        server.close()