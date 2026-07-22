from datetime import datetime
from enum import Enum
from abc import ABC, abstractmethod

# ========================================================
# 1. ENUMS & CORE CONSTANTS
# ========================================================
class SeatStatus(Enum):
    AVAILABLE = 1
    BOOKED = 2
    RESERVED = 3  # For temporary hold during payment

class SeatType(Enum):
    NORMAL = 1
    PREMIUM = 2

# ========================================================
# 2. CORE ENTITIES (Data Layer)
# ========================================================
class Movie:
    def __init__(self, movie_id: str, title: str, duration_mins: int):
        self.movie_id = movie_id
        self.title = title
        self.duration_mins = duration_mins

class Seat:
    def __init__(self, seat_id: str, row: str, number: int, seat_type: SeatType):
        self.seat_id = seat_id
        self.row = row
        self.number = number
        self.seat_type = seat_type
        self.status = SeatStatus.AVAILABLE

    def is_available(self) -> bool:
        return self.status == SeatStatus.AVAILABLE

    def reserve_seat(self):
        self.status = SeatStatus.RESERVED

    def book_seat(self):
        self.status = SeatStatus.BOOKED

class Show:
    def __init__(self, show_id: str, movie: Movie, start_time: datetime, seats: list[Seat]):
        self.show_id = show_id
        self.movie = movie
        self.start_time = start_time
        self.seats = {seat.seat_id: seat for seat in seats}  # Fast O(1) lookup

    def get_available_seats(self) -> list[Seat]:
        return [seat for seat in self.seats.values() if seat.is_available()]

# ========================================================
# 3. FACTORY PATTERN: PRICING ENGINE
# ========================================================
class TicketPricingFactory:
    @staticmethod
    def get_price(seat_type: SeatType) -> float:
        prices = {
            SeatType.NORMAL: 150.0,
            SeatType.PREMIUM: 300.0
        }
        return prices.get(seat_type, 150.0)

# ========================================================
# 4. BOOKING & TICKET MANAGEMENT
# ========================================================
class Booking:
    def __init__(self, booking_id: str, show: Show, seats: list[Seat]):
        self.booking_id = booking_id
        self.show = show
        self.seats = seats
        self.total_amount = sum(TicketPricingFactory.get_price(s.seat_type) for s in seats)
        self.is_confirmed = False

    def confirm_booking(self):
        for seat in self.seats:
            seat.book_seat()
        self.is_confirmed = True


class BookingService:
    def __init__(self):
        self.global_bookings: dict[str, Booking] = {}
        self._booking_counter = 1000

    def create_booking(self, show: Show, seat_ids: list[str]) -> Booking:
        selected_seats = []
        
        # 1. Validate seat availability
        for seat_id in seat_ids:
            seat = show.seats.get(seat_id)
            if not seat or not seat.is_available():
                print(f"❌ Seat {seat_id} is unavailable or invalid!")
                return None
            selected_seats.append(seat)

        # 2. Temporarily Reserve Seats
        for seat in selected_seats:
            seat.reserve_seat()

        # 3. Generate Booking Transaction
        self._booking_counter += 1
        b_id = f"BKG-{self._booking_counter}"
        new_booking = Booking(b_id, show, selected_seats)
        self.global_bookings[b_id] = new_booking
        
        print(f"✅ Booking initiated: {b_id}. Total: ₹{new_booking.total_amount}. Awaiting Payment...")
        return new_booking

    def process_payment(self, booking_id: str, payment_success: bool) -> bool:
        booking = self.global_bookings.get(booking_id)
        if not booking:
            print("❌ Booking record not found!")
            return False

        if payment_success:
            booking.confirm_booking()
            print(f"🎉 Payment successful! Ticket Confirmed for Booking: {booking_id}")
            return True
        else:
            # Release seats back to AVAILABLE state if payment fails
            for seat in booking.seats:
                seat.status = SeatStatus.AVAILABLE
            self.global_bookings.pop(booking_id)
            print(f"⚠️ Payment failed. Booking {booking_id} cancelled and seats released.")
            return False

if __name__ == "__main__":
    # 1. Setup Core Master Data
    interstellar = Movie("M-101", "Interstellar", 169)
    
    # Generate 3 default seats for the screen layout
    layout = [
        Seat("A1", "A", 1, SeatType.NORMAL),
        Seat("A2", "A", 2, SeatType.NORMAL),
        Seat("P1", "P", 1, SeatType.PREMIUM)
    ]
    
    evening_show = Show("S-99", interstellar, datetime(2026, 7, 20, 18, 30), layout)
    engine = BookingService()

    print("--- Simulation Step 1: User Books Available Seats ---")
    my_bkg = engine.create_booking(evening_show, ["A1", "P1"])
    
    print("\n--- Simulation Step 2: Another User Tries Booking Same Seats ---")
    failed_bkg = engine.create_booking(evening_show, ["A1"]) # Should print error
    
    print("\n--- Simulation Step 3: Completing Payment Flow ---")
    if my_bkg:
        engine.process_payment(my_bkg.booking_id, payment_success=True)