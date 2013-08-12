from pn_utils import *
from pn_network_packets import *
import sfml.network as sf

PORT = 50001

class ClientData(object):
    def __init__(self, my_id):
        self.id = my_id
        self.mouse_position = Vec2(0, 0)
        self.mouse_down = False
        self.time_out = 0.0

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

        self.world_packet_timer = 0.0

    def InitializeAsClient(self, ip_address):
        ip = sf.IpAddress.from_string(ip_address)

        self.socket_to_server = sf.TcpSocket()
        self.socket_to_server.connect(ip, PORT)
        self.socket_to_server.blocking = False

        self.on_disconnected = None
        
        print "Initialized networking engine as client"

        self.initialized = True

    def DestroyNonServerEntities(self):
        for ent in self.core.entityManager.entities:
            if ent.networked and not ent.spawned_by_server:
                self.core.entityManager.RemoveEntity(ent)

    def ProcessClientPackets(self, data):
        p = Packet.FromString( data )
        if type(p) == ClientAllocationPacket:
            self.client_id = p.assignedid
            self.connected = True
            print "Connected to server at " + str( self.socket_to_server.remote_address ) + ", my assigned ID is " + str(self.client_id)
        elif type(p) == WorldUpdatePacket:
            p.Apply(self.core)
        if p.rest:
            print "PROCESSING " + ' '.join(p.rest[0:10])
            self.ProcessClientPackets(' '.join(p.rest))
    
    def UpdateAsClient(self):
        self.DestroyNonServerEntities()
        
        try:
            mouse = self.core.input.mouse
            self.socket_to_server.send( str( ClientUpdatePacket( self.core.input.GetMousePosition(), mouse.is_button_pressed( mouse.LEFT ) ) ).encode("zlib") )
        except (sf.SocketError, sf.SocketDisconnected):
            pass #Maybe socket wasn't ready

        getting_packets = True
        while getting_packets:
            try:
                data = self.socket_to_server.receive(20000).decode("zlib")
                self.ProcessClientPackets(data)
            except sf.SocketNotReady:
                getting_packets = False #Waiting for data

            except sf.SocketDisconnected, sf.SocketError:
                print "Disconnected from server!"
                self.initialized = False
                self.connected = False
                if self.on_disconnected:
                    self.on_disconnected( self.core )
                getting_packets = False

    def UpdateAsServer(self):
        try:
            socket = self.server_listener.accept()
            socket.blocking = False
            newid = self.id_dispensor.GetNewID()
            self.client_sockets[newid] = socket
            self.client_sockets[newid].send( str( ClientAllocationPacket( newid ) ).encode("zlib") )
            self.clients.append( ClientData(newid) )
            print "Client connected from " + str(self.client_sockets[newid].remote_address) + ", allocated ID will be " + str(newid)
        except (sf.SocketDisconnected, sf.SocketNotReady, sf.SocketError):
            pass #Weren't any new connections to accept

        self.world_packet_timer += self.core.time.GetDelta()
        #Do world updates
        if( self.world_packet_timer >= 0.25 ):
            outpacket = WorldUpdatePacket()
            outpacket.Create(self.core)
            encoded = str(outpacket).encode('zlib')
            print "Outgoing WP @ " + str((100*len(encoded))/(len(str(outpacket)))) + "% compression to " + "{0:.2f}".format(float(len(encoded))/1024.0) + "Kb"
            for clientid in self.client_sockets.keys():
                try:
                    self.client_sockets[clientid].send( encoded )
                except (sf.SocketDisconnected, sf.SocketNotReady, sf.SocketError):
                    pass #Weren't any new connections to accept
            self.world_packet_timer = 0.0
        
        for clientid in self.client_sockets.keys():
            getting_packets = True
            while getting_packets:
                try:
                    p = Packet.FromString( self.client_sockets[clientid].receive(1024).decode("zlib") )
                    if type(p) == ClientUpdatePacket:
                        for clientdata in self.clients:
                            if clientdata.id == clientid:
                                clientdata.mouse_position = p.mouseposition
                                clientdata.mouse_down = p.mousedown
                                
                except sf.SocketNotReady:
                    getting_packets = False #Waiting for data
                except sf.SocketDisconnected, sf.SocketError:
                    print "Client " + str(clientid) + " was disconnected."
                    del self.client_sockets[clientid]
                    getting_packets = False
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
        
