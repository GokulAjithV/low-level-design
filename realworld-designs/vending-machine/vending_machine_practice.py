from abc import abstractmethod
from enum import Enum

class ItemType(Enum):
    SNACK = 1
    BEVERAGE = 2

class Item:
    def __init__(self, item_code: str, name: str, price: float, item_type: ItemType):
        self.item_code = item_code
        self.name = name
        self.price = price
        self.item_type = item_type

    def change_price(self, price):
        self.price = price

class InventorySlot:
    def __init__(self, slot_id: int, item: Item, quantity: int):
        self.slot_id = slot_id
        self.item = item
        self.quantity = quantity

    def is_item_available(self):
        return self.quantity > 0 

    def add_stock(self, count):
        self.quantity += count

    def reduce_quantity(self, count):
        self.quantity -= count

class State:
    @abstractmethod
    def select_item(self):
        pass

    @abstractmethod
    def insert_money(self):
        pass

    @abstractmethod
    def dispence_item(self):
        pass

    @abstractmethod
    def cancel(self):
        pass

class IdleState:

    def select_item(self, machine, item_code):
        slot_id = machine.item_slot_mappings[item_code]
        slot = machine.slots[slot_id]
        if not slot.is_item_available():
            print(f"The item {slot.item.name} is out of stock!!")
            return
        machine.selected_item = slot.item
        slot.reduce_quantity(1)
        machine.state = ItemSelectedState()

    def insert_money(self, amount):
        print("Select the item first")

    def dispence_item(self):
        print("Select the item first")

    def cancel(self):
        print("No transaction to cancel")

class ItemSelectedState:
    
    def select_item(self, machine, item_code):
        print("Item already selected, complete or cancel the current transaction")
        
    def insert_money(self):
        pass

class VendingMachine:
    def __init__(self):
        self.slots: dict[int, InventorySlot] = {} # {slot_id: InventorySlot}
        self.item_slot_mappings: dict[str, int] = {} # {item_code: slot_id}
        self.selected_item: Item = None
        self.current_balance = 0.0
        self.state = State()

    def select_item(self, item_code, quantity):
        self.state
