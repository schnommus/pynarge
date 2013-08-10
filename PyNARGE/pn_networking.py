from pn_utils import *
from pn_network_packets import *
import sfml.network as sf

PORT = 50001

class ClientData(object):
    def __init__(self, my_id):
        self.id = my_id
        self.mouse_position = None

class Networking(object):
    """Handles networking - synchronization, events between client and server"""
    def __init__(self, core):
        self.core = core
        self.initialized = False
        self.connected = False
        self.is_server = False
        self.clients = [] #If server, all ClientData. If client, all other clients.

    def InitializeAsServer(self):
        self.server_listener = sf.TcpListener()
        self.server_listener.listen(PORT)
        self.server_listener.blocking = False

        self.id_dispensor = IdDispensor()
        
        self.client_sockets = {}

        print "Initialized networking engine as server"

        self.initialized = True

        self.connected = True

        self.is_server = True

    def InitializeAsClient(self, ip_address):
        ip = sf.IpAddress.from_string(ip_address)

        self.socket_to_server = sf.TcpSocket()
        self.socket_to_server.connect(ip, PORT)
        self.socket_to_server.blocking = False

        self.on_disconnected = None
        
        print "Initialized networking engine as client"

        self.initialized = True

    def UpdateAsClient(self):
        try:
            self.socket_to_server.send( str( MouseUpdatePacket( self.core.input.GetMousePosition()) ) )
            
            p = Packet.FromString( self.socket_to_server.receive(1024) )
            if type(p) == ClientAllocationPacket:
                self.client_id = p.assignedid
                self.connected = True
                print "Connected to server at " + str( self.socket_to_server.remote_address ) + ", my assigned ID is " + str(self.client_id)
                
        except sf.SocketNotReady:
            pass #Waiting for data

        except sf.SocketDisconnected, sf.SocketError:
                print "Disconnected from server!"
                self.initialized = False
                self.connected = False
                if self.on_disconnected:
                    self.on_disconnected( self.core )

    def UpdateAsServer(self):
        try:
            socket = self.server_listener.accept()
            socket.blocking = False
            newid = self.id_dispensor.GetNewID()
            self.client_sockets[newid] = socket
            self.client_sockets[newid].send( str( ClientAllocationPacket( newid ) ) )
            self.clients.append( ClientData(newid) )
            print "Client connected from " + str(self.client_sockets[newid].remote_address) + ", allocated ID will be " + str(newid)
        except (sf.SocketDisconnected, sf.SocketNotReady, sf.SocketError):
            pass #Weren't any new connections to accept

        for clientid in self.client_sockets.keys():
            try:
                p = Packet.FromString( self.client_sockets[clientid].receive(1024) )
                if type(p) == MouseUpdatePacket:
                    for clientdata in self.clients:
                        if clientdata.id == clientid:
                            clientdata.mouseposition = p.mouseposition
                            print clientdata.mouseposition
                            
            except sf.SocketNotReady:
                pass #Waiting for data
            except sf.SocketDisconnected, sf.SocketError:
                print "Client " + str(clientid) + " was disconnected."
                del self.client_sockets[clientid]
                
                for i in range(len(self.clients)):
                    if self.clients[i].id == clientid:
                        del self.clients[i]
                        break
                return

    def Update(self):
        if self.is_server:
            self.UpdateAsServer()
        else:
            self.UpdateAsClient()
        
