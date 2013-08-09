from pn_utils import *
import sfml.network as sf


class Packet(object):
    CLIENT_ALLOCATION = 2

    @classmethod
    def FromString( c, string ):
        attributes = string.split(" ")
        print "Attempting packet creation from attributes: " + str(attributes)
        if attributes[0] == str(Packet.CLIENT_ALLOCATION):
            return ClientAllocationPacket.FromAttributes( attributes )
        

class ClientAllocationPacket(object):
    def __init__(self, assignedid):
        self.packet_type = Packet.CLIENT_ALLOCATION
        self.assignedid = assignedid
        
    def __str__(self):
        return ' '.join([str(self.packet_type), str(self.assignedid)])

    @classmethod
    def FromAttributes( c, attributes ):
        return ClientAllocationPacket( int(attributes[1]) )
