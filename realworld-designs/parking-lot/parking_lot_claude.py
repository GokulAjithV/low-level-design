from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
import uuid


class VehicleType(Enum):
    MOTORCYCLE = 1
    CAR = 2
    TRUCK = 3


class Vehicle:
    def __init__(self, license_plate: str, vehicle_type: VehicleType):
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type


class SpotType(Enum):
    MOTORCYCLE = 1
    COMPACT = 2
    LARGE = 3


VEHICLE_TO_SPOT = {
    VehicleType.MOTORCYCLE: [SpotType.MOTORCYCLE, SpotType.COMPACT, SpotType.LARGE],
    VehicleType.CAR: [SpotType.COMPACT, SpotType.LARGE],
    VehicleType.TRUCK: [SpotType.LARGE],
}


class ParkingSpot:
    def __init__(self, spot_id: str, spot_type: SpotType):
        self.spot_id = spot_id
        self.spot_type = spot_type
        self.vehicle = None

    def is_free(self):
        return self.vehicle is None

    def can_fit(self, vehicle: Vehicle):
        return self.spot_type in VEHICLE_TO_SPOT[vehicle.vehicle_type]

    def park(self, vehicle: Vehicle):
        if not self.is_free() or not self.can_fit(vehicle):
            raise Exception("Cannot park here")
        self.vehicle = vehicle

    def unpark(self):
        self.vehicle = None


class Ticket:
    def __init__(self, vehicle: Vehicle, spot: ParkingSpot):
        self.ticket_id = str(uuid.uuid4())
        self.vehicle = vehicle
        self.spot = spot
        self.entry_time = datetime.now()
        self.exit_time = None


class PricingStrategy(ABC):
    @abstractmethod
    def calculate_fee(self, ticket: Ticket) -> float:
        pass


class HourlyPricingStrategy(PricingStrategy):
    RATE_PER_HOUR = {
        SpotType.MOTORCYCLE: 10,
        SpotType.COMPACT: 20,
        SpotType.LARGE: 30,
    }

    def calculate_fee(self, ticket: Ticket) -> float:
        duration = (ticket.exit_time - ticket.entry_time).total_seconds() / 3600
        duration = max(duration, 1)
        rate = self.RATE_PER_HOUR[ticket.spot.spot_type]
        return round(duration * rate, 2)


class ParkingFloor:
    def __init__(self, floor_id: str, spots: list):
        self.floor_id = floor_id
        self.spots = spots

    def find_free_spot(self, vehicle: Vehicle):
        for spot in self.spots:
            if spot.is_free() and spot.can_fit(vehicle):
                return spot
        return None


class ParkingLot:
    _instance = None

    def __init__(self, pricing_strategy: PricingStrategy):
        if ParkingLot._instance is not None:
            raise Exception("Use get_instance()")
        self.floors = []
        self.active_tickets = {}
        self.pricing_strategy = pricing_strategy

    @staticmethod
    def get_instance(pricing_strategy: PricingStrategy = None):
        if ParkingLot._instance is None:
            ParkingLot._instance = ParkingLot(pricing_strategy)
        return ParkingLot._instance

    def add_floor(self, floor: ParkingFloor):
        self.floors.append(floor)

    def park_vehicle(self, vehicle: Vehicle) -> Ticket:
        for floor in self.floors:
            spot = floor.find_free_spot(vehicle)
            if spot:
                spot.park(vehicle)
                ticket = Ticket(vehicle, spot)
                self.active_tickets[ticket.ticket_id] = ticket
                return ticket
        raise Exception("Parking lot full")

    def unpark_vehicle(self, ticket_id: str) -> float:
        ticket = self.active_tickets.get(ticket_id)
        if not ticket:
            raise Exception("Invalid ticket")
        ticket.exit_time = datetime.now()
        fee = self.pricing_strategy.calculate_fee(ticket)
        ticket.spot.unpark()
        del self.active_tickets[ticket_id]
        return fee


if __name__ == "__main__":
    spots_f1 = [
        ParkingSpot("F1-M1", SpotType.MOTORCYCLE),
        ParkingSpot("F1-C1", SpotType.COMPACT),
        ParkingSpot("F1-L1", SpotType.LARGE),
    ]
    floor1 = ParkingFloor("F1", spots_f1)

    lot = ParkingLot.get_instance(HourlyPricingStrategy())
    lot.add_floor(floor1)

    car = Vehicle("KA-01-1234", VehicleType.CAR)
    ticket = lot.park_vehicle(car)
    print(f"Parked at {ticket.spot.spot_id}, ticket: {ticket.ticket_id}")

    fee = lot.unpark_vehicle(ticket.ticket_id)
    print(f"Fee: {fee}")
