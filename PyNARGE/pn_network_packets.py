from pn_utils import *
import sfml.network as sf


class Packet(object):
    CLIENT_ALLOCATION = 2
    CLIENT_UPDATE = 3
    WORLD_UPDATE = 4

    @classmethod
    def FromString( c, string ):
        attributes = string.split(" ")
       # print "Attempting packet creation from attributes: " + str(attributes)
        if attributes[0] == str(Packet.CLIENT_ALLOCATION):
            return ClientAllocationPacket.FromAttributes( attributes )
        if attributes[0] == str(Packet.CLIENT_UPDATE):
            return ClientUpdatePacket.FromAttributes( attributes )
        if attributes[0] == str(Packet.WORLD_UPDATE):
            return WorldUpdatePacket.FromAttributes( attributes )
        

class ClientAllocationPacket(object):
    def __init__(self, assignedid):
        self.packet_type = Packet.CLIENT_ALLOCATION
        self.assignedid = assignedid
        
    def __str__(self):
        return ' '.join([str(self.packet_type), str(self.assignedid)])

    @classmethod
    def FromAttributes( c, attributes ):
        return ClientAllocationPacket( int(attributes[1]) )

class ClientUpdatePacket(object):
    def __init__(self, mouseposition, mousedown):
        self.packet_type = Packet.CLIENT_UPDATE
        self.mouseposition = Vec2(mouseposition)
        self.mousedown = mousedown
        
    def __str__(self):
        return ' '.join([str(self.packet_type), str(self.mouseposition.x), str(self.mouseposition.y), str(self.mousedown)])

    @classmethod
    def FromAttributes( c, attributes ):
        state = attributes[3][0:4]=='True'
        return ClientUpdatePacket( Vec2( float(attributes[1]), float(attributes[2]) ), state )

class NetEntity(object):
    def __init__(self, typestring, the_id, p_x, p_y):
        self.typestring = typestring
        self.id = the_id
        self.position = Vec2(p_x, p_y)

class WorldUpdatePacket(object):
    def __init__(self):
        self.packet_type = Packet.WORLD_UPDATE
        self.entities = []
        self.packet = []

    def Apply(self, core):
        numFields = 8
        for i in range(0, len(self.packet)/numFields):
            typename = self.packet[numFields*i]
            id = int( self.packet[numFields*i+1] )
            position = Vec2( float(self.packet[numFields*i+2]), float(self.packet[numFields*i+3]) )
            angle = float( self.packet[numFields*i+4] )
            linearVelocity = Vec2( float(self.packet[numFields*i+5]), float(self.packet[numFields*i+6]) )
            angularVelocity = float( self.packet[numFields*i+7] )
            if not core.entityManager.GetEntityWithID( id ):
                ent = core.entityManager.AddForcedEntity( typename, id, position )
                ent.spawned_by_server = True
                ent.networked = True
            else:
                ent = core.entityManager.GetEntityWithID( id )
                ent.body.position = core.physicsWorld.GlobalToWorld(position)
                ent.body.angle = angle
                ent.body.linearVelocity = linearVelocity
                ent.body.angularVelocity = angularVelocity

    def Create(self, core):
        self.core = core
        self.packet = []
        for ent in self.core.entityManager.entities:
            if ent.networked:
                self.packet.append( str(type(ent).__name__) )
                self.packet.append( str(ent.id) )
                self.packet.append( str(ent.position.x) )
                self.packet.append( str(ent.position.y) )
                self.packet.append( str(ent.body.angle) )
                self.packet.append( str(ent.body.linearVelocity.x) )
                self.packet.append( str(ent.body.linearVelocity.y) )
                self.packet.append( str(ent.body.angularVelocity) )
    
    def __str__(self):
        return ' '.join([str(self.packet_type)]+self.packet)

    @classmethod
    def FromAttributes( c, attributes ):
        p = WorldUpdatePacket()
        p.packet = attributes[1:]
        return p
