import operator
from pn_entity import Entity

class EntityManager(object):
    """Manages entities, is responsible for calling their methods"""
    def __init__(self, core):
        """ Constructor

        :type core: :class:`PyNARGE.GameCore`"""
        self.entities = []
        self.core = core
        self.deletionList = []
        self.types = {}
        
    def AddEntity(self, ent):
        """Add an entity to the entity manager, initializing the entity

        :param ent: The entity to add
        :type ent: :class:`PyNARGE.Entity`
        :returns: :class:`PyNARGE.Entity` -- The entity that was added, initialized."""
        ent.id = self.core.idDispensor.GetNewID()
        ent.core = self.core
        self.entities.append(ent)
        ent._Init()
        self.types[str(type(ent).__name__)] = type(ent)
        return ent

    def RegisterType(self, typedata):
        self.types[str(typedata.__name__)] = typedata

    def AddForcedEntity(self, typestring, ent_id, position):
        ent = self.types[typestring]()
        ent.id = ent_id
        ent.position = position
        ent.core = self.core
        self.entities.append(ent)
        ent._Init()
        return ent
        

    def RemoveEntity(self, ent):
        """Remove an entity from the entity manager"""
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

    def Clean(self):
        """Removes all entities in the manager"""
        for ent in self.entities:
            self.RemoveEntity(ent)
    
    def RemoveEntityByID(self, the_id):
        """Remove an entity from the entity manager, by searching for a matching ID"""
        self.deletionList.append(the_id)

    def GetEntityWithID(self, the_id):
        """Fetches an entity with the ID supplied, `None` if nonexistant

        :returns: :class:`PyNARGE.Entity` -- The entity"""
        for i in range( len( self.entities ) ):
            if self.entities[i].id == the_id:
                return self.entities[i]

        return None

    def UpdateEntities(self):
        self.entities.sort(key=operator.attrgetter('steplayer'))
        for ent in self.entities:
            ent._Step()
        self.ExecuteEntityDeletions()

    def DrawEntities(self):
        self.entities.sort(key=operator.attrgetter('drawlayer'))
        for ent in self.entities:
            ent._Draw()
