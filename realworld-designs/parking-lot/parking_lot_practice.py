from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Optional, Dict

"""
1. Enums and Data Structures
"""

class VehicleType(Enum):
    MOTORCYLE = 1
    CAR = 2
    TRUCK = 3
    VAN = 4

class ParkingSpotType(Enum):
    MOTORCYCLE = 1
    COMPACT = 2
    LARGE = 3
    HANDICAPPED = 4

"""
2. Vehicles
"""

class Vehicle(ABC):
    def __init__(self, license_plate: str, vehicle_type: VehicleType, is_handicapped: bool = False):
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type
        self.is_handicapped = is_handicapped

class Motorcycle(Vehicle):
    def __init__(self, license_plate: str, is_handicapped: bool):
        super().__init__(self, license_plate, VehicleType.MOTORCYLE, is_handicapped)

class Car(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(self, license_plate, VehicleType.CAR)

class Truck(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(self, license_plate, VehicleType.TRUCK)

class Van(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(self, license_plate, VehicleType.VAN)


"""
3. Parking Spot and Display Board
"""

class DisplayBoard():
    def __init__(self, floor_number: int):
        self.floor_number = floor_number
        self.free_spots: Dict[ParkingSpotType, int] = {
            ParkingSpotType.MOTORCYCLE: 0,
            ParkingSpotType.COMPACT: 0, 
            ParkingSpotType.LARGE: 0, 
            ParkingSpotType.HANDICAPPED: 0
        }

    def update(self, spot_type: ParkingSpotType, delta: int):
        self.free_spots[spot_type] += delta

    def show_status(self) -> None:
        status_str = ", ".join([f"{k.name}: {v}" for k, v in self.free_spots.items()])
        print(f"[Floor {self.floor_number} Display] Free Spots -> {status_str}")

class ParkingSpot():
    def __init__(self, spot_id: int, spot_type: ParkingSpotType, floor_number: int):
        self.spot_id = spot_id
        self.spot_type = spot_type
        self.floor_number = floor_number
        self.is_free = True
        self.vehicle: Optional[Vehicle] = None

    def assign_vehicle(self, vehicle: Vehicle):
        self.is_free = False
        self.vehicle = vehicle

    def remove_vehicle(self):
        self.is_free = True
        self.vehicle = None


