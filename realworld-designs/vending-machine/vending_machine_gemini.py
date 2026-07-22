from abc import ABC, abstractmethod
from enum import Enum

# ========================================================
# 1. ENUMS & CORE DATA MODELS
# ========================================================
class ItemType(Enum):
    BEVERAGE = "Beverage"
    SNACK = "Snack"

class Item:
    def __init__(self, item_code: str, name: str, price: float, item_type: ItemType):
        self.item_code = item_code
        self.name = name
        self.price = price
        self.item_type = item_type

class InventorySlot:
    def __init__(self, item: Item, quantity: int):
        self.item = item
        self.quantity = quantity

    def is_available(self) -> bool:
        return self.quantity > 0

    def deduct_quantity(self):
        if self.quantity > 0:
            self.quantity -= 1


# ========================================================
# 2. STATE PATTERN INTERFACE
# ========================================================
class State(ABC):
    @abstractmethod
    def insert_money(self, machine, amount: float): pass

    @abstractmethod
    def select_item(self, machine, item_code: str): pass

    @abstractmethod
    def dispense(self, machine): pass

    @abstractmethod
    def cancel_transaction(self, machine): pass


# ========================================================
# 3. CONCRETE STATES
# ========================================================
class IdleState(State):
    def insert_money(self, machine, amount: float):
        machine.current_balance += amount
        print(f"💰 Inserted: ₹{amount}. Current Balance: ₹{machine.current_balance}")
        machine.set_state(machine.has_money_state)

    def select_item(self, machine, item_code: str):
        print("⚠️ Please insert money before selecting an item!")

    def dispense(self, machine):
        print("⚠️ No transaction in progress.")

    def cancel_transaction(self, machine):
        print("⚠️ No active transaction to cancel.")


class HasMoneyState(State):
    def insert_money(self, machine, amount: float):
        machine.current_balance += amount
        print(f"💰 Added: ₹{amount}. Total Balance: ₹{machine.current_balance}")

    def select_item(self, machine, item_code: str):
        slot = machine.inventory.get(item_code)

        if not slot or not slot.is_available():
            print(f"❌ Item '{item_code}' is out of stock or invalid!")
            return

        if machine.current_balance < slot.item.price:
            needed = slot.item.price - machine.current_balance
            print(f"⚠️ Insufficient funds! '{slot.item.name}' costs ₹{slot.item.price}. Insert ₹{needed} more.")
            return

        print(f"✅ Selected: {slot.item.name} (Price: ₹{slot.item.price})")
        machine.selected_item_code = item_code
        machine.set_state(machine.dispensing_state)

    def dispense(self, machine):
        print("⚠️ Select an item first!")

    def cancel_transaction(self, machine):
        refund = machine.current_balance
        machine.current_balance = 0.0
        print(f"🔄 Transaction cancelled. Refunded: ₹{refund}")
        machine.set_state(machine.idle_state)


class DispensingState(State):
    def insert_money(self, machine, amount: float):
        print("⚠️ Currently dispensing. Please wait!")

    def select_item(self, machine, item_code: str):
        print("⚠️ Currently dispensing. Cannot select new items!")

    def dispense(self, machine):
        slot = machine.inventory[machine.selected_item_code]
        slot.deduct_quantity()
        
        item = slot.item
        change = machine.current_balance - item.price
        
        print(f"🎉 DISPENSED: {item.name}")
        if change > 0:
            print(f"🪙 Returned Change: ₹{change:.2f}")

        # Reset machine state
        machine.current_balance = 0.0
        machine.selected_item_code = None
        machine.set_state(machine.idle_state)

    def cancel_transaction(self, machine):
        print("⚠️ Cannot cancel while dispensing!")


# ========================================================
# 4. VENDING MACHINE CONTEXT
# ========================================================
class VendingMachine:
    def __init__(self):
        # Initialize States
        self.idle_state = IdleState()
        self.has_money_state = HasMoneyState()
        self.dispensing_state = DispensingState()

        # Set default state
        self.current_state = self.idle_state
        
        # Operational variables
        self.inventory: dict[str, InventorySlot] = {}
        self.current_balance = 0.0
        self.selected_item_code = None

    def set_state(self, state: State):
        self.current_state = state

    # Inventory management
    def add_item_to_slot(self, item_code: str, item: Item, quantity: int):
        self.inventory[item_code] = InventorySlot(item, quantity)

    # Delegated user action methods
    def insert_money(self, amount: float):
        self.current_state.insert_money(self, amount)

    def select_item(self, item_code: str):
        self.current_state.select_item(self, item_code)

    def dispense(self):
        self.current_state.dispense(self)

    def cancel(self):
        self.current_state.cancel_transaction(self)


if __name__ == "__main__":
    machine = VendingMachine()

    # 1. Restock machine
    coke = Item("A1", "Coca-Cola", 40.0, ItemType.BEVERAGE)
    chips = Item("B1", "Lays Chips", 20.0, ItemType.SNACK)
    
    machine.add_item_to_slot("A1", coke, quantity=2)
    machine.add_item_to_slot("B1", chips, quantity=5)

    print("--- Case 1: Successful Transaction with Change ---")
    machine.insert_money(50.0)
    machine.select_item("A1")  # Costs ₹40
    machine.dispense()         # Returns ₹10 change

    print("\n--- Case 2: Insufficient Funds ---")
    machine.insert_money(20.0)
    machine.select_item("A1")  # Costs ₹40 -> Warns user

    print("\n--- Case 3: Cancel Transaction & Refund ---")
    machine.cancel()           # Refunds ₹20