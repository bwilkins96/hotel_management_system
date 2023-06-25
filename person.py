# SWDV 630 - Object-Oriented Software Architecture
# Person superclass and 3 subclasses for a hotel management system

from datetime import date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from base import Base
from stay import Stay
from account import Account

class Person(Base):
    """Person base class for a hotel management system"""
    
    def __init__(self, name, email, joined=date.today(), end=None):
        """
        Sets up a Person instance with name, start date, and end date parameters.
        Parameters start and end should be date objects.
        """
        self._name = name.title() 
        self._email = email
        self._joined = joined
        self._end = end

    __tablename__ = 'person'

    _id: Mapped[int] = mapped_column(primary_key=True)
    _name: Mapped[str]
    _email: Mapped[str] = mapped_column(unique=True)
    _joined: Mapped[date]
    _end: Mapped[date] = mapped_column(nullable=True)
    _type: Mapped[str]

    # Used to set up a table that keeps track of all instances of the base and subclasses 
    __mapper_args__ = {
        "polymorphic_on": "_type",
        "polymorphic_identity": "person",
    }

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name.title() 
        
    def get_joined(self):
        return self._joined
    
    def set_joined(self, joined):
        self._joined = joined

    def get_end(self):
        return self._end
    
    def set_end(self, end): 
        self._end = end

    def get_type(self):
        return self._type

    def is_current(self):
        """Returns whether the Person instance is currently active"""
        if self.get_end() == None:
            return True
        
        return date.today() <= self.get_end()

    def __repr__(self):
        return f'<Person: {self.get_name()}, {self.get_type().title()}>'

class Guest(Person):
    """Guest subclass for a hotel management system"""

    def __init__(self, stay, *args, **kwargs):
        """Sets up a Guest instance with a stay parameter"""
        self._stay = stay
        self._account = Account()
        super().__init__(*args, **kwargs)

    _stay_id: Mapped[int] = mapped_column(ForeignKey('stay._id'), nullable=True)
    _account_id: Mapped[int] = mapped_column(ForeignKey('account._id'), nullable=True)
    _stay: Mapped[Stay] = relationship()
    _account: Mapped[Account] = relationship(cascade='all, delete')

    __mapper_args__ = {
        "polymorphic_identity": "guest",
    }

    def get_stay(self):
        return self._stay
    
    def set_stay(self, stay):
        self._stay = stay

    def get_account(self):
        return self._account
    
    def is_checked_in(self):
        if self._stay:
            return self._stay.is_checked_in()
        return False

class Employee(Person):
    """Employee subclass for a hotel management system"""

    def __init__(self, pay_rate,  *args, **kwargs):
        """Sets up an Employee instance with a pay_rate parameter"""
        self._pay_rate = float(pay_rate)
        self._unpaid_hours = 0.0
        self._unpaid_overtime = 0.0

        super().__init__(*args, **kwargs)

    _pay_rate: Mapped[float] = mapped_column(nullable=True)
    _unpaid_hours: Mapped[float] = mapped_column(nullable=True)
    _unpaid_overtime: Mapped[float] = mapped_column(nullable=True)
    _manager_id: Mapped[int] = mapped_column(ForeignKey('person._id'), nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "employee",
    }

    def get_pay_rate(self):
        return self._pay_rate
    
    def set_pay_rate(self, pay_rate):
        self._pay_rate = float(pay_rate)

    def add_hours(self, hours, overtime=0):
        """
        Adds hours to unpaid_hours and the optional overtime parameter to unpaid_overtime.
        The overtime parameter defaults to 0.
        """
        self._unpaid_hours += hours
        self._unpaid_overtime += overtime

    def reset_hours(self):
        """Sets unpaid_hours and unpaid_overtime to 0"""
        self._unpaid_hours = 0.0
        self._unpaid_overtime = 0.0

    def get_total_pay(self):
        """Returns the total pay owed to the Employee instance"""
        rate = self.get_pay_rate()
        total = (self._unpaid_hours * rate) + (self._unpaid_overtime * rate * 1.5)
        return total
    
class Manager(Employee):
    """Manager subclass for a hotel management system"""

    def __init__(self, *args, **kwargs):
        """Sets up a Manager instance with an office parameter"""
        self._employees = []
        super().__init__(*args, **kwargs)

    _employees: Mapped[list[Employee]] = relationship()

    __mapper_args__ = {
        "polymorphic_identity": "manager",
    }

    def get_employees(self):
        return self._employees[:]
    
    def add_employee(self, emp):
        """Adds Employee emp to employees list"""
        if type(emp) == Employee:
            self._employees.append(emp)

    def remove_employee(self, emp):
        """Removes Employee emp from employees list"""
        emp_idx = self._employees.index(emp)
        return self._employees.pop(emp_idx)

# Test functions
def test_guest():
    from stay import Stay

    stay = Stay('room 101', date.today(), date.today())
    guest = Guest(stay, 'Joe', date(2023, 5, 20), 'test@email.com')
    print(guest.is_checked_in(), guest.get_joined())     # False, 2023-05-20

    guest.get_stay().check_in()
    print(guest.is_checked_in())        # True

    guest.get_stay().check_out()
    print(guest.is_checked_in())        # False

def test_employee():
    emp = Employee(20, 'Jeff', 'test2@email.com')
    emp.add_hours(40)
    print(emp.get_total_pay())          # 800.0

    emp.add_hours(40, 5)
    print(emp.get_total_pay())          # 1750.0

    emp.reset_hours()
    print(emp.get_total_pay())          # 0.0

    print(emp.is_current())             # True

def test_manager():
    man = Manager(30, 'Jenny', 'test3@email.com')
    print(man.get_employees())          # []

    emp_a = Employee(20, 'Julian', 'test4@email.com')
    emp_b = Employee(20, 'Jennifer', 'test5@email.com')
    man.add_employee(emp_a)
    man.add_employee(emp_b)
    print(man.get_employees())          # [(Person: Julian), (Person: Jennifer)]

    man.remove_employee(emp_a)
    print(man.get_employees())          # [(Person: Jennifer)]

def test():
    test_guest()
    print()
    test_employee()
    print()
    test_manager()

if __name__ == '__main__': test()