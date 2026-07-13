from abc import ABC, abstractmethod

# Strategy Interface
class DiscountStrategy(ABC):
    
    @abstractmethod
    def apply_discount(self, price: float) -> float:
        pass

# Concrete Strategies
class PercentageDiscount(DiscountStrategy):

    def __init__(self, percent):
        self.percent = percent

    def apply_discount(self, price: float) -> float:
        discount_amount = (price * (self.percent / 100))
        return price - discount_amount

class FlatDiscount(DiscountStrategy):

    def __init__(self, amount):
        self.discount_amount = amount

    def apply_discount(self, price: float) -> float:
        return price - self.discount_amount

# Context
class Checkout:
    def __init__(self, discount_strategy: DiscountStrategy):
        self._discount_strategy = discount_strategy

    def set_discount_strategy(self, discount_strategy: DiscountStrategy):
        self._discount_strategy = discount_strategy

    def calculate_total(self, raw_price):
        return self._discount_strategy.apply_discount(raw_price)

# --- Usage ---
if __name__ == "__main__":
    # Start checkout with flat discount
    checkout = Checkout(FlatDiscount(15.0))
    print(f"Total price with flat discount: ${checkout.calculate_total(100.0)}") # $85.0
    
    # Change strategy dynamically at runtime (e.g., customer applies a promo code)
    checkout.set_discount_strategy(PercentageDiscount(0.20)) # 20% off
    print(f"Total price with promo code: ${checkout.calculate_total(100.0)}") # $80.0



