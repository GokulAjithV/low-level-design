from datetime import datetime
import uuid
from datetime import date
from abc import abstractmethod
from abc import ABC
from typing import Dict
from enum import Enum

"""
1. Core Entities and Enums
"""

class VehicleType(Enum):
    MOTORCYCLE = 1
    CAR = 2
    TRUCK = 3

class SpotType(Enum):
    MOTORCYCLE = 1
    COMPACT = 2
    LARGE = 3
    HANDICAPPED = 4

class Vehicle:
    def __init__(self, license_plate: str, vehicle_type: VehicleType):
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type

"""
2. Parking Spot and Floor Management
"""

class ParkingSpot:
    def __init__(self, spot_id: str, spot_type: SpotType, floor_id: int):
        self.spot_id = spot_id
        self.spot_type = spot_type
        self.floor_id = floor_id
        self.is_free = True
        self.vehicle: Vehicle = None

    def assign_vehicle(self, vehicle: Vehicle):
        self.vehicle = vehicle
        self.is_free = False
    
    def remove_vehicle(self):
        self.vehicle = None
        self.is_free = True

class ParkingFloor:
    def __init__(self, floor_id: int):
        self.floor_id = floor_id 
        self.spots: dict[str, ParkingSpot] = {}

    def add_spots(self, spots: list):
        for spot in spots:
            self.spots[spot.spot_id] = spot

    def get_available_spot(self, spot_type: SpotType):
        for spot in self.spots:
            if spot.is_free and spot.spot_type == spot_type:
                return spot
        print(f"No Available spots in floor {self.floor_id}")

    def get_available_spots(self, spot_type: SpotType) -> list[ParkingSpot]:
        available_spots = []
        for spot in self.spots:
            if spot.is_free and spot.spot_type == spot_type:
                available_spots.append(spot)
        return available_spots

"""
3. Strategy Pattern: ALGO FOR SPOT ALLOCATION (OCP compliant)
"""

class SpotAllocationStrategy(ABC):
    @abstractmethod
    def find_spot(self, floors: list[ParkingFloor], spot_type: SpotType) -> ParkingSpot:
        pass

class NearestSpotAllocationStrategy(SpotAllocationStrategy):
    def find_spot(self, floors: list[ParkingFloor], spot_type: SpotType) -> ParkingSpot:
        
        for floor in sorted(floors, key = lambda f: f.floor_id):
            free_spots = floor.get_available_spots(spot_type)
            if free_spots:
                nearest_spot = free_spots[0]
                for spot in free_spots:
                    if spot.spot_id < nearest_spot.spot_id:
                        nearest_spot = spot
                return nearest_spot


"""
4. Pricing Strategy
"""
class PricingStrategy(ABC):
    def calculate_cost(self, hours: float) -> float:
        pass
    
class CarPricingStrategy(PricingStrategy):
    def calculate_cost(self, hours: float) -> float:
        return max(50.0, 30.0 * hours) # min Rs.50, then Rs.30/hour
 
class MotorcyclePricingStrategy(PricingStrategy):
    def calcualte_cost(self, hours: float) -> float:
        return max(20, 10.0 * hours)

# Factory to dynamically fetch the correct pricing scheme 
class PricingStrategyFactory:
    @staticmethod
    def get_strategy(vehicle_type: VehicleType):
        strategies = {
            VehicleType.MOTORCYCLE: MotorcyclePricingStrategy,
            VehicleType.CAR: CarPricingStrategy
        }
        return strategies.get(vehicle_type, MotorcyclePricingStrategy)

"""
5. Ticketing System
"""

class Ticket:
    def __init__(self, vehicle: Vehicle, spot: ParkingSpot):
        self.ticket_id = str(uuid.uuid4())
        self.vehicle = vehicle
        self.spot = spot
        self.entry_time = datetime.now()
        self.exit_time = None
        self.amount_paid = 0.0

class TicketManager:
    def __init__(self):
        self.active_tickets: dict[str, Ticket] = {}

    def create_ticket(self, vehicle: Vehicle, spot: ParkingSpot) -> Ticket:
        ticket = Ticket(vehicle, spot)
        self.active_tickets[ticket.ticket_id] = ticket
        return ticket

    def close_ticket(self, ticket_id: str):
        if ticket_id not in self.active_tickets:
            raise ValueError("Invalid Ticket ID")
        
        del self.active_tickets[ticket_id]
        print("Ticket Closed")

"""
6. Core Context and Orchestrator (FACADE PATTERN)
"""
class ParkingLot:
    def __init__(self, name: str, spot_allocation_strategy: SpotAllocationStrategy):
        self.name = name
        self.spot_allocation_strategy = spot_allocation_strategy
        self.floors: list[ParkingFloor] = []
        self.ticket_manager = TicketManager()

    def add_floor(self, floor: ParkingFloor):
        self.floors.append(floor)
    
    def remove_floor(self, floor_id: int):
        for i in range(len(self.floors)):
            if self.floors[i].floor_id == floor_id:
                self.floors.pop(i)
                break

    def _map_vehicle_to_spot_type(self, vehicle_type: VehicleType):
        mappings = {
            VehicleType.MOTORCYCLE: SpotType.MOTORCYCLE,
            VehicleType.CAR: SpotType.COMPACT,
            VehicleType.TRUCK: SpotType.LARGE
        }
        return mappings[vehicle_type]

    def park_vehicle(self, vehicle: Vehicle):
        spot_type = self._map_vehicle_to_spot_type(vehicle.vehicle_type)
        spot = SpotAllocationStrategy.find_spot(self.floors, spot_type)

        if not spot:
            print(f"Parking Lot is full for vehicle type: {vehicle.vehicle_type.name}")
            return

        spot.assign_vehicle(vehicle)
        ticket = self.ticket_manager.create_ticket(vehicle, spot)
        print(f"Parking Spot alloted for vehicle - {vehicle.license_plate} | Spot ID - {spot.spot_id} | Floor ID - {spot.floor_id} | Ticket - {ticket.ticket_id}")
        return ticket

    def unpark_vehicle(self, ticket, vehicle):
        pass

