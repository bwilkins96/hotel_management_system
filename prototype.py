# SWDV 630 - Object-Oriented Software Architecture
# Prototype base class and prototype factory class

from copy import copy, deepcopy

class Prototype:
    """Prototype base class with methods for producing deep and shallow clones"""
    
    def clone(self):
        """Returns a deep clone of self"""
        return deepcopy(self)
    
    def shallow_clone(self):
        """Returns a shallow clone of self"""
        return copy(self)
    
class PrototypeFactory:
    """Prototype factory class that holds a registry of cloneable instances"""

    def __init__(self):
        """Sets up a PrototypeFactory instance with a registry"""
        self._registry = {}

    def register(self, key, obj):
        """Registers a Prototype instance to registry[key]"""
        if isinstance(obj, Prototype):         
            self._registry[key] = obj
            return True
        
        return False

    def get(self, key):
        """Returns a deep clone of the instance at registry[key]"""
        return self._registry[key].clone()
    
    def shallow_get(self, key):
        """Returns a shallow clone of the instance at registry[key]"""
        return self._registry[key].shallow_clone()
    

# -------------------------------------------------------------------------- 
# NOTE: Use make_transient after copying an instance to add it to a database
# -------------------------------------------------------------------------- 
# from sqlalchemy.orm.session import make_transient