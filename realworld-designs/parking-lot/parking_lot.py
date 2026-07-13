import threading
import time
import uuid
from datetime import datetime, timedelta
from enum import Enum
from abc import ABC, abstractmethod
from typing import List, Optional, Dict

# =====================================================================
# 1. ENUMS & DATA STRUCTURES
# =====================================================================

class VehicleType(Enum):
    MOTORCYCLE = 1
    CAR = 2
    VAN = 3
    TRUCK = 4

class ParkingSpotType(Enum):
    MOTORCYCLE = 1
    COMPACT = 2
    LARGE = 3
    HANDICAPPED = 4

# =====================================================================
# 2. VEHICLES
# =====================================================================

class Vehicle(ABC):
    def __init__(self, license_plate: str, vehicle_type: VehicleType, is_handicapped: bool = False):
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type
        self.is_handicapped = is_handicapped

class Car(Vehicle):
    def __init__(self, license_plate: str, is_handicapped: bool = False):
        super().__init__(license_plate, VehicleType.CAR, is_handicapped)

class Motorcycle(Vehicle):
    def __init__(self, license_plate: str, is_handicapped: bool = False):
        super().__init__(license_plate, VehicleType.MOTORCYCLE, is_handicapped)

class Truck(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.TRUCK, False)

class Van(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.VAN, False)

# =====================================================================
# 3. PARKING SPOT & DISPLAY BOARD
# =====================================================================

class DisplayBoard:
    def __init__(self, floor_number: int):
        self.floor_number = floor_number
        self.free_spots: Dict[ParkingSpotType, int] = {
            ParkingSpotType.MOTORCYCLE: 0,
            ParkingSpotType.COMPACT: 0,
            ParkingSpotType.LARGE: 0,
            ParkingSpotType.HANDICAPPED: 0
        }

    def update(self, spot_type: ParkingSpotType, delta: int) -> None:
        self.free_spots[spot_type] += delta

    def show_status(self) -> None:
        status_str = ", ".join([f"{k.name}: {v}" for k, v in self.free_spots.items()])
        print(f"[Floor {self.floor_number} Display] Free Spots -> {status_str}")


class ParkingSpot:
    def __init__(self, spot_id: str, spot_type: ParkingSpotType, floor_number: int):
        self.spot_id = spot_id
        self.spot_type = spot_type
        self.floor_number = floor_number
        self.is_free = True
        self.vehicle: Optional[Vehicle] = None

    def assign_vehicle(self, vehicle: Vehicle) -> None:
        self.is_free = False
        self.vehicle = vehicle

    def remove_vehicle(self) -> None:
        self.is_free = True
        self.vehicle = None

    def is_compatible(self, vehicle: Vehicle) -> bool:
        # Handicapped vehicles check
        if vehicle.is_handicapped:
            return self.spot_type == ParkingSpotType.HANDICAPPED
        
        # Spot size compatibility mapping
        if vehicle.vehicle_type == VehicleType.MOTORCYCLE:
            # Motorcycle can park in any spot size
            return self.spot_type in [ParkingSpotType.MOTORCYCLE, ParkingSpotType.COMPACT, ParkingSpotType.LARGE]
        elif vehicle.vehicle_type == VehicleType.CAR:
            # Cars can park in compact or large spots
            return self.spot_type in [ParkingSpotType.COMPACT, ParkingSpotType.LARGE]
        elif vehicle.vehicle_type in [VehicleType.VAN, VehicleType.TRUCK]:
            # Large vehicles can only park in large spots
            return self.spot_type == ParkingSpotType.LARGE
        return False

# =====================================================================
# 4. PARKING FLOOR (Thread-safe Operations)
# =====================================================================

class ParkingFloor:
    def __init__(self, floor_number: int):
        self.floor_number = floor_number
        self.spots: List[ParkingSpot] = []
        self.display_board = DisplayBoard(floor_number)
        self._lock = threading.Lock()

    def add_spot(self, spot: ParkingSpot) -> None:
        self.spots.append(spot)
        self.display_board.update(spot.spot_type, 1)

    def get_free_spot(self, vehicle: Vehicle) -> Optional[ParkingSpot]:
        # Lock to ensure thread safety during spot scanning and booking
        with self._lock:
            for spot in self.spots:
                if spot.is_free and spot.is_compatible(vehicle):
                    return spot
            return None

    def occupy_spot(self, spot: ParkingSpot, vehicle: Vehicle) -> None:
        with self._lock:
            spot.assign_vehicle(vehicle)
            self.display_board.update(spot.spot_type, -1)

    def release_spot(self, spot: ParkingSpot) -> None:
        with self._lock:
            spot.remove_vehicle()
            self.display_board.update(spot.spot_type, 1)

# =====================================================================
# 5. PRICING & BILLING STRATEGY
# =====================================================================

class PaymentStrategy(ABC):
    @abstractmethod
    def calculate_fee(self, duration_hours: float, vehicle_type: VehicleType) -> float:
        pass

class HourlyRateStrategy(PaymentStrategy):
    def __init__(self):
        # Base hourly rates for each vehicle type
        self.rates = {
            VehicleType.MOTORCYCLE: 1.0,
            VehicleType.CAR: 2.0,
            VehicleType.VAN: 3.5,
            VehicleType.TRUCK: 5.0
        }

    def calculate_fee(self, duration_hours: float, vehicle_type: VehicleType) -> float:
        # Hourly rate, rounding up partial hours
        hours = max(1, int(duration_hours + 0.99))
        return float(hours * self.rates.get(vehicle_type, 2.0))

# =====================================================================
# 6. TICKETS & GATES
# =====================================================================

class ParkingTicket:
    def __init__(self, vehicle: Vehicle, spot: ParkingSpot):
        self.ticket_id = str(uuid.uuid4())[:8]
        self.vehicle = vehicle
        self.spot = spot
        self.entry_time = datetime.now()
        self.exit_time: Optional[datetime] = None
        self.fee = 0.0
        self.is_paid = False


class EntranceGate:
    def __init__(self, gate_id: str, parking_lot):
        self.gate_id = gate_id
        self.parking_lot = parking_lot

    def enter_vehicle(self, vehicle: Vehicle) -> Optional[ParkingTicket]:
        print(f"[Entrance {self.gate_id}] Vehicle {vehicle.license_plate} is requesting entry...")
        
        # Request a compatible spot from the parking lot
        spot = self.parking_lot.find_and_occupy_spot(vehicle)
        if not spot:
            print(f"[Entrance {self.gate_id}] ❌ Entry Denied: No compatible spots available for {vehicle.license_plate}")
            return None
        
        ticket = ParkingTicket(vehicle, spot)
        print(f"[Entrance {self.gate_id}] ✅ Entry Granted: Spot {spot.spot_id} on Floor {spot.floor_number}. Ticket ID: {ticket.ticket_id}")
        return ticket


class ExitGate:
    def __init__(self, gate_id: str, parking_lot):
        self.gate_id = gate_id
        self.parking_lot = parking_lot
        self.pricing_strategy = HourlyRateStrategy()

    def exit_vehicle(self, ticket: ParkingTicket) -> None:
        print(f"[Exit {self.gate_id}] Processing exit for Vehicle {ticket.vehicle.license_plate}...")
        
        # Simulate elapsed time (e.g., ticket generated 3 hours ago)
        ticket.exit_time = datetime.now()
        duration_hours = 3.5  # Fixed simulation duration for demonstration
        
        ticket.fee = self.pricing_strategy.calculate_fee(duration_hours, ticket.vehicle.vehicle_type)
        ticket.is_paid = True
        
        print(f"[Exit {self.gate_id}] Fee for {duration_hours} hours: ${ticket.fee:.2f}. Payment received.")
        
        # Release the spot back to the parking lot
        self.parking_lot.release_spot(ticket.spot)
        print(f"[Exit {self.gate_id}] ✅ Goodbye! Spot {ticket.spot.spot_id} has been cleared.")

# =====================================================================
# 7. PARKING LOT (Singleton Thread-safe facade)
# =====================================================================

class ParkingLot:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        # Thread-safe singleton instantiation
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, name: str = "Central Plaza Parking"):
        if hasattr(self, '_initialized'):
            return
        self.name = name
        self.floors: List[ParkingFloor] = []
        self.entrance_gates: Dict[str, EntranceGate] = {}
        self.exit_gates: Dict[str, ExitGate] = {}
        self._global_lock = threading.Lock()
        self._initialized = True

    def add_floor(self, floor: ParkingFloor) -> None:
        self.floors.append(floor)

    def add_entrance_gate(self, gate_id: str) -> None:
        self.entrance_gates[gate_id] = EntranceGate(gate_id, self)

    def add_exit_gate(self, gate_id: str) -> None:
        self.exit_gates[gate_id] = ExitGate(gate_id, self)

    def find_and_occupy_spot(self, vehicle: Vehicle) -> Optional[ParkingSpot]:
        with self._global_lock:
            for floor in self.floors:
                spot = floor.get_free_spot(vehicle)
                if spot:
                    floor.occupy_spot(spot, vehicle)
                    return spot
            return None

    def release_spot(self, spot: ParkingSpot) -> None:
        with self._global_lock:
            for floor in self.floors:
                if floor.floor_number == spot.floor_number:
                    floor.release_spot(spot)
                    return

    def display_status(self) -> None:
        print(f"\n--- {self.name} Current Status ---")
        for floor in self.floors:
            floor.display_board.show_status()
        print("--------------------------------------\n")

# =====================================================================
# 8. CONCURRENCY SIMULATION RUNNER
# =====================================================================

def simulate_user_actions(parking_lot: ParkingLot, vehicle: Vehicle, ent_gate_id: str, ext_gate_id: str):
    # Simulate a delay before entering
    time.sleep(0.1)
    entrance = parking_lot.entrance_gates[ent_gate_id]
    exit_gate = parking_lot.exit_gates[ext_gate_id]
    
    ticket = entrance.enter_vehicle(vehicle)
    if ticket:
        # Simulate parking duration
        time.sleep(1.0)
        exit_gate.exit_vehicle(ticket)

def run_simulation():
    # 1. Initialize the Parking Lot Singleton
    lot = ParkingLot("City Core Automated Parking")
    
    # 2. Construct 2 Floors
    floor0 = ParkingFloor(0)
    floor0.add_spot(ParkingSpot("P0-101", ParkingSpotType.HANDICAPPED, 0))
    floor0.add_spot(ParkingSpot("P0-102", ParkingSpotType.MOTORCYCLE, 0))
    floor0.add_spot(ParkingSpot("P0-103", ParkingSpotType.COMPACT, 0))
    floor0.add_spot(ParkingSpot("P0-104", ParkingSpotType.LARGE, 0))

    floor1 = ParkingFloor(1)
    floor1.add_spot(ParkingSpot("P1-201", ParkingSpotType.MOTORCYCLE, 1))
    floor1.add_spot(ParkingSpot("P1-202", ParkingSpotType.COMPACT, 1))
    floor1.add_spot(ParkingSpot("P1-203", ParkingSpotType.COMPACT, 1))
    floor1.add_spot(ParkingSpot("P1-204", ParkingSpotType.LARGE, 1))
    
    lot.add_floor(floor0)
    lot.add_floor(floor1)
    
    # 3. Add Gates
    lot.add_entrance_gate("Ent-A")
    lot.add_entrance_gate("Ent-B")
    lot.add_exit_gate("Exit-X")
    lot.add_exit_gate("Exit-Y")
    
    # Show initial empty status
    lot.display_status()
    
    # 4. Spin up concurrent threads to simulate multiple vehicles arriving at the same time
    test_vehicles = [
        (Car("CAR-777", is_handicapped=False), "Ent-A", "Exit-X"),
        (Motorcycle("BIKE-123", is_handicapped=False), "Ent-B", "Exit-Y"),
        (Car("VIP-001", is_handicapped=True), "Ent-A", "Exit-X"),
        (Truck("TRK-999"), "Ent-B", "Exit-Y"),
        (Car("CAR-888"), "Ent-A", "Exit-X"), # Competes for compact slots
    ]
    
    threads = []
    for vehicle, ent, ext in test_vehicles:
        t = threading.Thread(target=simulate_user_actions, args=(lot, vehicle, ent, ext))
        threads.append(t)
        t.start()
        
    # Wait for all parking events to complete
    for t in threads:
        t.join()
        
    # Show final empty status (since all exited)
    lot.display_status()

if __name__ == "__main__":
    run_simulation()
