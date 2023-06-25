# SWDV 630 - Object-Oriented Software Architecture
# Mock printer class

class Printer():
    def __init__(self, cards, status='ok'):
        self._remaining_cards = int(cards)
        self._status = status

    def get_remaining_cards(self):
        return self._remaining_cards
    
    def get_status(self):
        return self._status
    
    def set_remaining_cards(self, cards):
        self._remaining_cards = int(cards)

    def set_status(self, status):
        self._status = status

    def is_low(self):
        return self.get_remaining_cards() <= 25
    
    def print_keycard(self, room):
        print(f'Printing keycard for room {room.get_room_number()}')
        self._remaining_cards -= 1

def test():
    from room import Room
    
    test_room = Room(101, 'queen', 150)
    printer = Printer(26)

    print(printer.is_low())    # -> False
    printer.print_keycard(test_room)
    print(printer.is_low())    # -> True

if __name__ == '__main__': test()
