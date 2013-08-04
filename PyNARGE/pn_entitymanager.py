import operator
from pn_entity import Entity

class EntityManager(object):
    def __init__(self, core):
        self.entities = []
        self.core = core
        self.deletionList = []
        
    def AddEntity(self, ent):
        ent.id = self.core.idDispensor.GetNewID()
        ent.core = self.core
        self.entities.append(ent)
        ent._Init()
        return ent

    def RemoveEntity(self, ent):
        self.deletionList.append(ent.id)

    def ExecuteEntityDeletions(self):
        deleting = True
        while deleting: #Must do this to avoid array out-of-bounds
            deleting = False
            for i in range( len( self.entities ) ):
                if self.entities[i].id in self.deletionList:
                    self.entities[i]._Destroy()
                    self.core.idDispensor.FreeID(self.entities[i].id)
                    del self.entities[i]
                    deleting = True
                    break
        self.deletionList = []
    
    def RemoveEntityByID(self, the_id):
        self.deletionList.append(the_id)

    def GetEntityWithID(self, the_id):
        for i in range( len( self.entities ) ):
            if self.entities[i].id == the_id:
                return self.entities[i]

    def UpdateEntities(self):
        self.entities.sort(key=operator.attrgetter('steplayer'))
        for ent in self.entities:
            ent._Step()
        self.ExecuteEntityDeletions()

    def DrawEntities(self):
        self.entities.sort(key=operator.attrgetter('drawlayer'))
        for ent in self.entities:
            ent._Draw()
