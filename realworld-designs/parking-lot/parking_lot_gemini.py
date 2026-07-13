from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
import uuid

# ========================================================
# 1. ENUMS & CORE ENTITIES
# ========================================================
class VehicleType(Enum):
    MOTORBIKE = 1
    CAR = 2
    TRUCK = 3

class SpotType(Enum):
    MOTORBIKE = 1
    COMPACT = 2
    LARGE = 3
    HANDICAPPED = 4

class Vehicle:
    def __init__(self, license_plate: str, vehicle_type: VehicleType):
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type

# ========================================================
# 2. PARKING SPOT & FLOOR MANAGEMENT
# ========================================================
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

    def add_spot(self, spot: ParkingSpot):
        self.spots[spot.spot_id] = spot

    def get_free_spots(self, spot_type: SpotType) -> list[ParkingSpot]:
        return [spot for spot in self.spots.values() if spot.is_free and spot.spot_type == spot_type]

# ========================================================
# 3. STRATEGY PATTERN: ALGO FOR SPOT ALLOCATION (OCP compliant)
# ========================================================
class SpotAllocationStrategy(ABC):
    @abstractmethod
    def find_spot(self, floors: list[ParkingFloor], spot_type: SpotType) -> ParkingSpot:
        pass

class NearestFirstAllocationStrategy(SpotAllocationStrategy):
    def find_spot(self, floors: list[ParkingFloor], spot_type: SpotType) -> ParkingSpot:
        # Sort floors chronologically to get the lowest/nearest floor first
        for floor in sorted(floors, key=lambda f: f.floor_id):
            free_spots = floor.get_free_spots(spot_type)
            if free_spots:
                return sorted(free_spots, key=lambda s: s.spot_id)[0]
        return None

# ========================================================
# 4. STRATEGY PATTERN: PRICING ENGINE
# ========================================================
class PricingStrategy(ABC):
    @abstractmethod
    def calculate_cost(self, hours: float) -> float:
        pass

class CarPricingStrategy(PricingStrategy):
    def calculate_cost(self, hours: float) -> float:
        return max(50.0, hours * 30.0)  # Min ₹50, then ₹30/hour

class MotorbikePricingStrategy(PricingStrategy):
    def calculate_cost(self, hours: float) -> float:
        return max(20.0, hours * 10.0)

# Factory to dynamically fetch the correct pricing scheme
class PricingStrategyFactory:
    @staticmethod
    def get_strategy(vehicle_type: VehicleType) -> PricingStrategy:
        strategies = {
            VehicleType.CAR: CarPricingStrategy,
            VehicleType.MOTORBIKE: MotorbikePricingStrategy
        }
        return strategies.get(vehicle_type, CarPricingStrategy)()

# ========================================================
# 5. TICKETING SYSTEM
# ========================================================
class ParkingTicket:
    def __init__(self, vehicle: Vehicle, spot: ParkingSpot):
        self.ticket_id = str(uuid.uuid4())[:8]
        self.vehicle = vehicle
        self.spot = spot
        self.entry_time = datetime.now()
        self.exit_time = None
        self.amount_paid = 0.0

class TicketManager:
    def __init__(self):
        self.active_tickets: dict[str, ParkingTicket] = {}

    def create_ticket(self, vehicle: Vehicle, spot: ParkingSpot) -> ParkingTicket:
        ticket = ParkingTicket(vehicle, spot)
        self.active_tickets[ticket.ticket_id] = ticket
        return ticket

    def close_ticket(self, ticket_id: str, hours_spent: float) -> float:
        ticket = self.active_tickets.get(ticket_id)
        if not ticket:
            raise ValueError("Invalid Ticket ID")
        
        pricing_algo = PricingStrategyFactory.get_strategy(ticket.vehicle.vehicle_type)
        ticket.amount_paid = pricing_algo.calculate_cost(hours_spent)
        ticket.exit_time = datetime.now()
        
        del self.active_tickets[ticket_id]
        return ticket.amount_paid

# ========================================================
# 6. THE CORE CONTEXT / ORCHESTRATOR (FACADE PATTERN)
# ========================================================
class ParkingLot:
    def __init__(self, name: str, allocation_strategy: SpotAllocationStrategy):
        self.name = name
        self.floors: list[ParkingFloor] = []
        self.allocation_strategy = allocation_strategy
        self.ticket_manager = TicketManager()

    def add_floor(self, floor: ParkingFloor):
        self.floors.append(floor)

    def _map_vehicle_to_spot_type(self, vehicle_type: VehicleType) -> SpotType:
        mapping = {
            VehicleType.MOTORBIKE: SpotType.MOTORBIKE,
            VehicleType.CAR: SpotType.COMPACT,
            VehicleType.TRUCK: SpotType.LARGE
        }
        return mapping.get(vehicle_type, SpotType.COMPACT)

    def park_vehicle(self, vehicle: Vehicle) -> ParkingTicket:
        target_type = self._map_vehicle_to_spot_type(vehicle.vehicle_type)
        spot = self.allocation_strategy.find_spot(self.floors, target_type)
        
        if not spot:
            print(f"❌ Parking Full for vehicle type: {vehicle.vehicle_type.name}")
            return None
        
        spot.assign_vehicle(vehicle)
        ticket = self.ticket_manager.create_ticket(vehicle, spot)
        print(f"✅ Parked {vehicle.license_plate} at Spot {spot.spot_id} (Floor {spot.floor_id}). Ticket: {ticket.ticket_id}")
        return ticket

    def unpark_vehicle(self, ticket_id: str, hours_spent: float):
        ticket = self.ticket_manager.active_tickets.get(ticket_id)
        if not ticket:
            print("❌ Ticket not found!")
            return
        
        spot = ticket.spot
        spot.remove_vehicle()
        cost = self.ticket_manager.close_ticket(ticket_id, hours_spent)
        print(f"🚗 Vehicle left Spot {spot.spot_id}. Duration: {hours_spent} hours. Total Charges: ₹{cost}")

    
if __name__ == "__main__":
    # 1. Initialize System with an allocation strategy
    parking_lot = ParkingLot("Alpha Tech Park Station", NearestFirstAllocationStrategy())

    # 2. Setup Infrastructure (Floor 0 containing spots)
    floor_0 = ParkingFloor(floor_id=0)
    floor_0.add_spot(ParkingSpot("S-101", SpotType.COMPACT, floor_id=0))
    floor_0.add_spot(ParkingSpot("S-102", SpotType.COMPACT, floor_id=0))
    floor_0.add_spot(ParkingSpot("M-201", SpotType.MOTORBIKE, floor_id=0))
    parking_lot.add_floor(floor_0)

    print(f"--- Welcome to {parking_lot.name} ---")
    
    # 3. Vehicles Arrive
    car_1 = Vehicle("TN-21-AX-1234", VehicleType.CAR)
    bike_1 = Vehicle("KA-03-MM-9999", VehicleType.MOTORBIKE)
    car_2 = Vehicle("DL-01-C-5678", VehicleType.CAR)
    car_3 = Vehicle("MH-12-G-0001", VehicleType.CAR) # Should trigger parking full

    ticket_1 = parking_lot.park_vehicle(car_1)
    ticket_2 = parking_lot.park_vehicle(bike_1)
    ticket_3 = parking_lot.park_vehicle(car_2)
    ticket_fail = parking_lot.park_vehicle(car_3) # No spot left

    print("\n--- Processing Exit ---")
    # 4. Vehicles Exit after hours spent
    parking_lot.unpark_vehicle(ticket_1.ticket_id, hours_spent=3.5)