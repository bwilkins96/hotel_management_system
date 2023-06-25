# SWDV 630 - Object-Oriented Software Architecture
# Driver/test file that adds and retrieves objects from a SQLite database

from datetime import datetime, timedelta
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from base import Base
from room import Room
from stay import Stay
from account import Account
from person import Guest, Employee, Manager
from schedule import Schedule, Shift

def main():
    # Creates a database in the directory called 'test.db'
    #engine = create_engine("sqlite+pysqlite:///test.db", echo=False)
    
    # Creates a transient in-memory database
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=False)
    
    Base.metadata.create_all(engine)

    room = Room(152, 'queen', 100)
    stay = Stay(room, datetime(2023, 8, 1), datetime(2023, 8, 5))

    guest = Guest(stay, 'Joe', 'joe@email.com')
    employee = Employee(20, 'Jeff', 'jeff@email.com')
    manager = Manager(30, 'Jenny', 'jenny@email.com')
    manager.add_employee(employee)

    schedule = employee.get_schedule()
    now = datetime.now()
    schedule.add_shift(Shift(now, now + timedelta(hours=8)))

    data = [room, stay, guest, employee, manager]
    classes = [Room, Stay, Guest, Employee, Manager, Account, Schedule, Shift]

    print()
    with Session(engine) as session:

        # Add objects to database
        for obj in data:
            session.add(obj)
        session.commit()

        # Retrieve objects from database
        for cls in classes:
            print(cls)
            stmt = select(cls)
            result = session.scalars(stmt)
            
            for inst in result.all():
                print(inst)
            print()

if __name__ == '__main__': main()