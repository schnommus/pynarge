import operator
from pn_entity import Entity

class EntityManager(object):
    def __init__(self, core):
        self.entities = []
        self.core = core
        
    def AddEntity(self, ent):
        ent.id = self.core.idDispensor.GetNewID()
        ent.core = self.core
        self.entities.append(ent)
        ent._Init()
        return ent

    def RemoveEntity(self, ent):
        for i in range( len( self.entities ) ):
            if self.entities[i] == ent:
                self.entities[i]._Destroy()
                del self.entities[i]
                break

    def RemoveEntityByID(self, the_id):
        for i in range( len( self.entities ) ):
            if self.entities[i].id == the_id:
                self.entities[i]._Destroy()
                self.core.idDispensor.FreeID(the_id)
                del self.entities[i]
                break

    def GetEntityWithID(self, the_id):
        for i in range( len( self.entities ) ):
            if self.entities[i].id == the_id:
                return self.entities[i]

    def UpdateEntities(self):
        self.entities.sort(key=operator.attrgetter('steplayer'))
        for ent in self.entities:
            ent._Step()

    def DrawEntities(self):
        self.entities.sort(key=operator.attrgetter('drawlayer'))
        for ent in self.entities:
            ent._Draw()
