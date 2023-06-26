# SWDV 630 - Object-Oriented Software Architecture

from datetime import datetime, date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from base import Base

def calculate_hours(time1, time2):
    diff = time2 - time1
    hours = diff.seconds / 60 / 60
    return hours

class Shift(Base):
    def __init__(self, start, end):
        self._start = start
        self._end = end
        self._start_actual = None
        self._end_actual = None
        self._clocked_in = False

    __tablename__ = 'shift'

    _id: Mapped[int] = mapped_column(primary_key=True)
    _start: Mapped[datetime]
    _end: Mapped[datetime]
    _start_actual: Mapped[datetime] = mapped_column(nullable=True)
    _end_actual: Mapped[datetime] = mapped_column(nullable=True)
    _clocked_in: Mapped[bool]
    _schedule_id: Mapped[int] = mapped_column(ForeignKey('schedule._id'), nullable=True)

    def is_clocked_in(self):
        return self._clocked_in
    
    def get_start(self):
        return self._start
    
    def get_end(self):
        return self._end
    
    def get_real_start(self):
        return self._start_actual
    
    def get_real_end(self):
        return self._end_actual
    
    def set_start(self, start):
        self._start = start

    def set_end(self, end):
        self._end = end

    def set_real_start(self, start):
        self._start_actual = start

    def set_real_end(self, end):
        self._end_actual = end

    def clock_in(self):
        if not self.is_clocked_in(): 
            self._clocked_in = True
            self.set_real_start(datetime.now())
            return True
        
        return False
    
    def clock_out(self):
        if self.is_clocked_in():
            self._clocked_in = False
            self.set_real_end(datetime.now())
            return True
        
        return False

    def hours_scheduled(self):
        return calculate_hours(self.get_start(), self.get_end())
    
    def hours_worked(self):
        return calculate_hours(self.get_real_start(), self.get_real_end())
    
    def __repr__(self):
        shift_date = self.get_start().date()
        start_time = self.get_start().strftime('%H:%M:%S')
        end_time = self.get_end().strftime('%H:%M:%S')
        return f'<Shift: {shift_date} ({start_time} to {end_time})>'
    
class Schedule(Base):
    _week_days = ('m', 't', 'w', 'th', 'f', 's', 'su')
    
    def __init__(self, week_start='m'):
        self._shifts = []
        
        week_start = week_start.strip().lower()
        if week_start in self._week_days:
            self._week_start = week_start
        else:
            self._week_start = 'm'

    __tablename__ = 'schedule'

    _id: Mapped[int] = mapped_column(primary_key=True)
    _shifts: Mapped[list[Shift]] = relationship()
    _week_start: Mapped[str]

    def get_shifts(self):
        return self._shifts[:]
    
    def get_current_shift(self):
        for shift in self._shifts:
            if shift.get_start().date() == date.today():
                return shift
    
    def add_shift(self, shift):
        if type(shift) == Shift:
            self._shifts.append(shift)

    def remove_shift(self, shift):
        shift_idx = self._shifts.index(shift)
        self._shifts.pop(shift_idx)

    def hours_scheduled(self):
        total = 0.0
        for shift in self._shifts:
            total += shift.hours_scheduled()

        return total
    
    def hours_worked(self):
        total = 0.0
        for shift in self._shifts:
            total += shift.hours_worked()

        return total
    
    def is_clocked_in(self):
        for shift in self._shifts:
            if shift.is_clocked_in():
                return True
            
        return False
    
    def reset(self):
        self._shifts = []

    def __repr__(self):
        return f'<Schedule: {len(self._shifts)} Shifts>'