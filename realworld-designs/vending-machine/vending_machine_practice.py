from abc import ABC, abstractmethod
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
    def __init__(self, slot_id: int):
        self.slot_id = slot_id
        self.item: Item = None
        self.quantity: int = 0

    def is_item_available(self):
        return self.quantity > 0 

    def add_stock(self, count):
        self.quantity += count

    def deduct_quantity(self):
        self.quantity -= 1

    def update_slot_item(self, machine, item, quantity):
        self.item = item
        self.quantity = quantity
        machine.item_slot_mappings[item.item_code] = self.slot_id

class State(ABC):
    @abstractmethod
    def select_item(self, machine, item_code):
        pass

    @abstractmethod
    def insert_money(self, machine, amount):
        pass

    @abstractmethod
    def dispence_item(self, machine):
        pass

    @abstractmethod
    def cancel(self, machine):
        pass

class IdleState:

    def select_item(self, machine, item_code):
        slot_id = machine.item_slot_mappings.get(item_code)
        if not slot_id:
            print("Item not available!")
            return 
        slot = machine.slots[slot_id]
        if not slot.is_item_available():
            print(f"The item {slot.item.name} is out of stock!!")
            return
        machine.selected_item = slot.item
        print(f"Item '{slot.item.name} (Rs.{slot.item.price})' is selected")
        machine.state = ItemSelectedState()

    def insert_money(self, machine, amount):
        print("Select the item first")

    def dispence_item(self, machine):
        print("Select the item first")

    def cancel(self, machine):
        print("No transaction to cancel")

class ItemSelectedState:
    
    def select_item(self, machine, item_code):
        print("Item already selected, complete or cancel the current transaction")
        
    def insert_money(self, machine, amount):
        item_price = machine.selected_item.price
        if amount < item_price:
            print(f"Insufficient amount Rs.{amount}, The item price is Rs.{item_price}")
            print(f"Insert remaining amount Rs.{item_price - amount}")
        else:
            print(f"Payment sufficient")
            if amount > item_price:
                print(f"Remaining amount Rs.{amount - item_price} is refunded!")
            print(f"Ready to dispence the item '{machine.selected_item.name}'")
            machine.state = PaymentAcceptedState()

    def dispence_item(self, machine):
        print("Complete payment to dispence item")
    
    def cancel(self, machine):
        print("Cancelling the current transaction!")
        machine.state = IdleState()
        machine.selected_item = None

class PaymentAcceptedState:

    def selected_item(self, machine, item_code):
        print("Complete the current transaction first, currently dispencing the item")
    
    def insert_payment(self, machine, amount):
        print("Complete the current transaction first, currently dispencing the item")

    def dispence_item(self, machine):
        item_code = machine.selected_item.item_code
        slot_id = machine.item_slot_mappings[item_code]
        slot =  machine.slots[slot_id]
        machine.selected_item = None
        slot.deduct_quantity()
        print(f"Item '{slot.item.name}' dispenced!!")
        machine.state = IdleState()

    def cancel(self, machine):
        print("Cannot cancel the transaction, Item is getting dispenced!")

class VendingMachine:
    def __init__(self):
        self.slots: dict[int, InventorySlot] = {} # {slot_id: InventorySlot}
        self.item_slot_mappings: dict[str, int] = {} # {item_code: slot_id}
        self.selected_item: Item = None
        self.state = IdleState()

    def select_item(self, item_code):
        self.state.select_item(self, item_code)
    
    def insert_money(self, amount):
        self.state.insert_money(self, amount)

    def dispence_item(self):
        self.state.dispence_item(self)

    def cancel(self):
        self.state.cancel(self)

    
if __name__ == "__main__":
    
    vending_machine = VendingMachine()
    for slot_id in range(1, 26):
        vending_machine.slots[slot_id] = InventorySlot(slot_id)
        
    item1 = Item("lays-20", "Lays", 20.0, ItemType.SNACK)
    item2 = Item("coke-40", "Coke", 40.0, ItemType.BEVERAGE)
    item3 = Item("sprite-40", "Sprite", 40.0, ItemType.BEVERAGE)
    items = [item1, item2, item3]

    for i, item in enumerate(items):
        slot_id = i+1
        vending_machine.slots[slot_id].update_slot_item(vending_machine, item, 5)
        vending_machine.item_slot_mappings[item.item_code] = slot_id

    vending_machine.select_item("lays-20")
    vending_machine.insert_money(40.0)
    vending_machine.dispence_item()
    
        


