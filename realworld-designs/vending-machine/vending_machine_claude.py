
from abc import ABC, abstractmethod
from enum import Enum


class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> float:
        pass


class CoinPayment(PaymentStrategy):
    def pay(self, amount: float) -> float:
        print(f"Paid Rs.{amount} using coins")
        return amount


class CardPayment(PaymentStrategy):
    def pay(self, amount: float) -> float:
        print(f"Paid Rs.{amount} using card")
        return amount


class UpiPayment(PaymentStrategy):
    def pay(self, amount: float) -> float:
        print(f"Paid Rs.{amount} using UPI")
        return amount


class Product:
    def __init__(self, code: str, name: str, price: float, quantity: int):
        self.code = code
        self.name = name
        self.price = price
        self.quantity = quantity

    def is_available(self):
        return self.quantity > 0

    def reduce_stock(self):
        if self.quantity <= 0:
            raise Exception("Out of stock")
        self.quantity -= 1


class Inventory:
    def __init__(self):
        self.products = {}

    def add_product(self, product: Product):
        self.products[product.code] = product

    def get_product(self, code: str) -> Product:
        product = self.products.get(code)
        if not product:
            raise Exception("Invalid product code")
        return product

    def restock(self, code: str, quantity: int):
        product = self.get_product(code)
        product.quantity += quantity

    def update_price(self, code: str, price: float):
        product = self.get_product(code)
        product.price = price


class VendingMachineState(ABC):
    @abstractmethod
    def select_product(self, machine, code):
        pass

    @abstractmethod
    def insert_payment(self, machine, amount, strategy: PaymentStrategy):
        pass

    @abstractmethod
    def dispense(self, machine):
        pass

    @abstractmethod
    def cancel(self, machine):
        pass


class IdleState(VendingMachineState):
    def select_product(self, machine, code):
        product = machine.inventory.get_product(code)
        if not product.is_available():
            print(f"{product.name} is out of stock")
            return
        machine.selected_product = product
        print(f"Selected {product.name}, price Rs.{product.price}")
        machine.set_state(ProductSelectedState())

    def insert_payment(self, machine, amount, strategy):
        print("Select a product first")

    def dispense(self, machine):
        print("Select a product first")

    def cancel(self, machine):
        print("Nothing to cancel")


class ProductSelectedState(VendingMachineState):
    def select_product(self, machine, code):
        print("Product already selected, complete or cancel current transaction")

    def insert_payment(self, machine, amount, strategy: PaymentStrategy):
        paid = strategy.pay(amount)
        machine.balance += paid
        if machine.balance >= machine.selected_product.price:
            machine.set_state(PaymentAcceptedState())
            print("Payment sufficient, ready to dispense")
        else:
            remaining = machine.selected_product.price - machine.balance
            print(f"Insufficient payment, remaining: Rs.{remaining}")

    def dispense(self, machine):
        print("Insert payment first")

    def cancel(self, machine):
        print(f"Transaction cancelled, refunding Rs.{machine.balance}")
        machine.reset()


class PaymentAcceptedState(VendingMachineState):
    def select_product(self, machine, code):
        print("Complete current transaction first")

    def insert_payment(self, machine, amount, strategy):
        print("Payment already sufficient")

    def dispense(self, machine):
        product = machine.selected_product
        product.reduce_stock()
        change = machine.balance - product.price
        print(f"Dispensing {product.name}")
        if change > 0:
            print(f"Returning change: Rs.{change}")
        machine.reset()

    def cancel(self, machine):
        print(f"Transaction cancelled, refunding Rs.{machine.balance}")
        machine.reset()


class VendingMachine:
    _instance = None

    def __init__(self):
        if VendingMachine._instance is not None:
            raise Exception("Use get_instance()")
        self.inventory = Inventory()
        self.state = IdleState()
        self.selected_product = None
        self.balance = 0.0

    @staticmethod
    def get_instance():
        if VendingMachine._instance is None:
            VendingMachine._instance = VendingMachine()
        return VendingMachine._instance

    def set_state(self, state: VendingMachineState):
        self.state = state

    def reset(self):
        self.selected_product = None
        self.balance = 0.0
        self.state = IdleState()

    def select_product(self, code):
        self.state.select_product(self, code)

    def insert_payment(self, amount, strategy: PaymentStrategy):
        self.state.insert_payment(self, amount, strategy)

    def dispense(self):
        self.state.dispense(self)

    def cancel(self):
        self.state.cancel(self)


if __name__ == "__main__":
    machine = VendingMachine.get_instance()
    machine.inventory.add_product(Product("A1", "Coke", 40, 5))
    machine.inventory.add_product(Product("A2", "Chips", 30, 0))

    machine.select_product("A1")
    machine.insert_payment(20, CoinPayment())
    machine.insert_payment(30, UpiPayment())
    machine.dispense()

    print("---")
    machine.select_product("A2")
