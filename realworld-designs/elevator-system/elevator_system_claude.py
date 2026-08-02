
from abc import ABC, abstractmethod
from enum import Enum
import heapq


class Direction(Enum):
    UP = 1
    DOWN = -1
    IDLE = 0


class ElevatorState(ABC):
    @abstractmethod
    def request_floor(self, elevator, floor):
        pass

    @abstractmethod
    def open_doors(self, elevator):
        pass

    @abstractmethod
    def close_doors(self, elevator):
        pass

    @abstractmethod
    def move(self, elevator):
        pass


class IdleState(ElevatorState):
    def request_floor(self, elevator, floor):
        elevator.add_request(floor)
        if floor != elevator.current_floor:
            elevator.set_state(MovingState())
        else:
            elevator.set_state(DoorsOpenState())
            elevator.state.open_doors(elevator)

    def open_doors(self, elevator):
        print("Elevator idle, no doors to open")

    def close_doors(self, elevator):
        print("Elevator idle, no doors to close")

    def move(self, elevator):
        print("No requests, staying idle")


class MovingState(ElevatorState):
    def request_floor(self, elevator, floor):
        elevator.add_request(floor)
        print(f"Queued floor {floor} request while moving")

    def open_doors(self, elevator):
        print("Cannot open doors while moving")

    def close_doors(self, elevator):
        print("Doors already closed while moving")

    def move(self, elevator):
        next_floor = elevator.get_next_floor()
        if next_floor is None:
            elevator.set_state(IdleState())
            return
        direction = Direction.UP if next_floor > elevator.current_floor else Direction.DOWN
        elevator.direction = direction
        print(f"Moving {direction.name} from {elevator.current_floor} to {next_floor}")
        elevator.current_floor = next_floor
        elevator.remove_request(next_floor)
        elevator.set_state(DoorsOpenState())
        elevator.state.open_doors(elevator)


class DoorsOpenState(ElevatorState):
    def request_floor(self, elevator, floor):
        elevator.add_request(floor)
        print(f"Queued floor {floor} request while doors open")

    def open_doors(self, elevator):
        print(f"Doors opened at floor {elevator.current_floor}")

    def close_doors(self, elevator):
        print(f"Doors closed at floor {elevator.current_floor}")
        if elevator.has_pending_requests():
            elevator.set_state(MovingState())
        else:
            elevator.direction = Direction.IDLE
            elevator.set_state(IdleState())

    def move(self, elevator):
        print("Cannot move, doors are open")


class SchedulingStrategy(ABC):
    @abstractmethod
    def get_next_floor(self, current_floor, direction, up_requests, down_requests):
        pass


class ScanSchedulingStrategy(SchedulingStrategy):
    def get_next_floor(self, current_floor, direction, up_requests, down_requests):
        if direction != Direction.DOWN:
            higher = [f for f in up_requests if f >= current_floor]
            if higher:
                return min(higher)
            if down_requests:
                return max(down_requests)
            lower = [f for f in up_requests if f < current_floor]
            if lower:
                return max(lower)
        else:
            lower = [f for f in down_requests if f <= current_floor]
            if lower:
                return max(lower)
            if up_requests:
                return min(up_requests)
            higher = [f for f in down_requests if f > current_floor]
            if higher:
                return min(higher)
        return None


class Elevator:
    def __init__(self, elevator_id, scheduling_strategy: SchedulingStrategy):
        self.elevator_id = elevator_id
        self.current_floor = 0
        self.direction = Direction.IDLE
        self.state = IdleState()
        self.scheduling_strategy = scheduling_strategy
        self.up_requests = set()
        self.down_requests = set()

    def set_state(self, state: ElevatorState):
        self.state = state

    def add_request(self, floor):
        if floor > self.current_floor:
            self.up_requests.add(floor)
        elif floor < self.current_floor:
            self.down_requests.add(floor)

    def remove_request(self, floor):
        self.up_requests.discard(floor)
        self.down_requests.discard(floor)

    def has_pending_requests(self):
        return bool(self.up_requests or self.down_requests)

    def get_next_floor(self):
        return self.scheduling_strategy.get_next_floor(
            self.current_floor, self.direction, self.up_requests, self.down_requests
        )

    def request_floor(self, floor):
        self.state.request_floor(self, floor)

    def close_doors(self):
        self.state.close_doors(self)

    def step(self):
        self.state.move(self)


class ElevatorController:
    def __init__(self):
        self.elevators = []

    def add_elevator(self, elevator: Elevator):
        self.elevators.append(elevator)

    def find_best_elevator(self, floor):
        return min(self.elevators, key=lambda e: abs(e.current_floor - floor))

    def request_elevator(self, floor):
        elevator = self.find_best_elevator(floor)
        print(f"Assigning elevator {elevator.elevator_id} for floor {floor}")
        elevator.request_floor(floor)
        return elevator


if __name__ == "__main__":
    controller = ElevatorController()
    controller.add_elevator(Elevator("E1", ScanSchedulingStrategy()))
    controller.add_elevator(Elevator("E2", ScanSchedulingStrategy()))

    e1 = controller.request_elevator(5)
    e1.close_doors()
    e1.step()
    e1.close_doors()

    e1.request_floor(8)
    e1.step()
    e1.close_doors()
