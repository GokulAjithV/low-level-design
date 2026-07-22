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
        self.seats = {seat.seat_id: seat for seat in seats}
        self.start_time = start_time
        
    def get_available_seats(self):
        return [seat for seat in self.seats.values() if seat.is_available()]

"""
3. Ticket Pricing Engine (FACTORY PATTERN)
"""

class TicketPricingFactory:
    @staticmethod
    def get_price(seat_type: SeatType) -> float:
        prices = {
            SeatType.REGULAR: 150.0,
            SeatType.PREMIUM: 300.0
        }
        return prices.get(seat_type, 150.0)

"""
4. Booking and Ticket Management
"""

class Booking:
    def __init__(self, booking_id: str, show: Show, seats: Seat):
        self.booking_id = booking_id
        self.show = show 
        self.seats = seats
        self.total_amount = sum(TicketPricingFactory.get_price(seat.seat_type) for seat in seats)
        self.is_confirmed = False

    def confirm_booking(self):
        for seat in self.seats:
            seat.book_seat()
        self.is_confirmed = True

class BookingService:

    def __init__(self):
        self.global_bookings: dict[str, Booking] = {}
        self._booking_counter = 1000
    
    def create_booking(self, show: Show, seat_ids: list[str]):
        selected_seats = []
        
        # 1. Validate seat availability
        for seat_id in seat_ids:
            seat = show.seats.get(seat_id, None)
            if not seat or not seat.is_available():
                print(f"Seat {seat_id} not available or invalid!")
                return 
            selected_seats.append(seat)

        # 2. Reserve seats
        for seat in selected_seats:
            seat.reserve_seat()

        # 3. Generate booking transaction
        self._booking_counter += 1
        booking_id = f"BKG-{self._booking_counter}"
        booking = Booking(booking_id, show, selected_seats)
        self.global_bookings[booking_id] = booking

        print(f"Booking Initiated: {booking_id}. Total Amount: {booking.total_amount} | Awaiting Payment...")
        return booking

    def process_payment(self, booking_id: str, payment_success: bool):
        
        booking = self.global_bookings.get(booking_id, None)

        if not booking:
            print(f"Booking record not found!")
            return False
            
        if payment_success:
            booking.confirm_booking()
            print(f"Payment Successful! Ticket confirmed for booking {booking_id}")
            return True
        else:
            # if payment failed, release all the seats to available state
            for seat in booking.seats:
                seat.status = SeatStatus.AVAILABLE
            self.global_bookings.pop(booking_id)
            print(f"Payment failed. Booking {booking_id} cancelled and seats released")
            return False

if __name__ == "__main__":

    # 1. Setup core master data
    iron_man = Movie("M-101", "Iron Man", 130)

    layout = [
        Seat("A1", "A", "1", SeatType.REGULAR),
        Seat("A2", "A", "2", SeatType.REGULAR),
        Seat("A3", "A", "3", SeatType.REGULAR),
        Seat("A4", "A", "4", SeatType.REGULAR),
        Seat("A5", "A", "5", SeatType.REGULAR),
    ]

    night_show = Show("S-101", iron_man, layout, datetime(2026, 7, 20, 21, 30))
    engine = BookingService()

    print("1. User books available seats")
    user1_booking = engine.create_booking(night_show, ["A1", "A2"])

    print("2. Another user tries to book the same seat")
    user2_booking = engine.create_booking(night_show, ["A1"])

    print("3. Completing payment flow")
    engine.process_payment(user1_booking.booking_id, True)
