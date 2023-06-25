# SWDV 630 - Object-Oriented Software Architecture
# Factory for producing Person instances

from person import Guest, Employee, Manager

class PersonFactory:
    """Factory class for producing Person instances"""

    @staticmethod
    def create(type, *args, **kwargs):
        """
        Returns a Person subclass instance based on the type parameter
        i.e. PersonFactory.create('guest', room, name, start, end) 
        """
        type = type.strip().lower()

        if type == 'guest':
            return Guest(*args, **kwargs)
        elif type == 'employee':
            return Employee(*args, **kwargs)
        elif type == 'manager':
            return Manager(*args, **kwargs)

def test():
    guest = PersonFactory.create('guest', 101, 'Brandon')
    employee = PersonFactory.create('employee', 20, 'Hannah') 
    manager = PersonFactory.create('manager', 110, 25, 'Bridgett')

    for person in [guest, employee, manager]:
        print(type(person))

if __name__ == '__main__': test()