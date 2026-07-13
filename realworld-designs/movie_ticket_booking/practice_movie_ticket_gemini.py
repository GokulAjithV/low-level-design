from datetime import datetime
from enum import Enum

"""
1. Enums and Constants
"""

class SeatStatus(Enum):
    AVAILABLE = 1
    RESERVED = 2
    BOOKED = 3

class SeatType(Enum):
    REGULAR = 1
    PREMIUM = 2

"""
2. Core Entities (Data Layer)
"""
class Movie:
    def __init__(self, movie_id: str, title: str, duration_mins: int):
        self.movie_id = movie_id
        self.title = title
        self.duration_mins = duration_mins

class Seat:
    def __init__(self, seat_id: str, row: str, number: str, seat_type: SeatType):
        self.seat_id = seat_id
        self.seat_type = seat_type
        self.row = row
        self.number = number
        self.status = SeatStatus.AVAILABLE

    def is_available(self):
        return self.status == SeatStatus.AVAILABLE

    def reserve_seat(self):
        self.status = SeatStatus.RESERVED

    def book_seat(self):
        self.status = SeatStatus.BOOKED

class Show:
    def __init__(self, show_id: str, movie: Movie, seats: list[Seat], start_time: datetime):
        self.show_id = show_id
        self.movie = movie
        self.seats = seats
        self.start_time = start_time
        
    def get_available_seats(self):
        return [seat for seat in self.seats.values() if seat.is_available()]

"""
3. TicketPricingFactory
"""