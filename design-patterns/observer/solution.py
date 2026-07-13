from abc import ABC, abstractmethod
from typing import List

# =====================================================================
# CHALLENGE: Stock Market Notification Engine (Solution)
# =====================================================================

# 1. Define the Observer Interface
class StockObserver(ABC):
    @abstractmethod
    def update(self, symbol: str, price: float) -> None:
        pass


# 2. Define the Subject Interface
class StockSubject(ABC):
    def __init__(self):
        self._observers: List[StockObserver] = []

    def attach(self, observer: StockObserver) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: StockObserver) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, symbol: str, price: float) -> None:
        for observer in self._observers:
            observer.update(symbol, price)


# 3. Implement Concrete Subject (Stock)
class Stock(StockSubject):
    def __init__(self, symbol: str, price: float):
        super().__init__()
        self.symbol = symbol
        self.price = price

    def set_price(self, new_price: float) -> None:
        self.price = new_price
        self.notify(self.symbol, self.price)


# 4. Implement Concrete Observers
class PriceLogger(StockObserver):
    def __init__(self):
        self.log = []

    def update(self, symbol: str, price: float) -> None:
        self.log.append(f"{symbol}: {price}")
        print(f"PriceLogger: {symbol} is now ${price}")


class StockAlertSystem(StockObserver):
    def __init__(self, threshold: float):
        self.threshold = threshold
        self.alerts_triggered = 0

    def update(self, symbol: str, price: float) -> None:
        if price < self.threshold:
            self.alerts_triggered += 1
            print(f"ALERT: {symbol} has dropped below threshold! Current price: ${price}")


# =====================================================================
# CLIENT / VERIFICATION CODE (Do not modify this part)
# =====================================================================

def verify_observer():
    print("--- Testing Observer (Stock Market Engine) ---")
    
    # Instantiate stock
    apple_stock = Stock("AAPL", 150.00)
    
    # Instantiate observers
    logger = PriceLogger()
    alert_system = StockAlertSystem(threshold=140.00)
    
    # Attach observers
    apple_stock.attach(logger)
    apple_stock.attach(alert_system)
    
    # 1. Price drops slightly (no alert)
    print("Setting price to $145.00...")
    apple_stock.set_price(145.00)
    
    # 2. Price drops below threshold (should alert)
    print("\nSetting price to $138.00...")
    apple_stock.set_price(138.00)
    
    # 3. Detach logger, change price again
    print("\nDetaching logger and changing price to $135.00...")
    apple_stock.detach(logger)
    apple_stock.set_price(135.00)
    
    # Verification checks
    try:
        assert len(logger.log) == 2, f"❌ Failed: Logger should have logged exactly 2 updates. Logged: {logger.log}"
        assert logger.log[0] == "AAPL: 145.0", f"❌ Failed: First logged price incorrect. Got {logger.log[0]}"
        assert logger.log[1] == "AAPL: 138.0", f"❌ Failed: Second logged price incorrect. Got {logger.log[1]}"
        
        # Verify alert system ran 2 alerts (since price went to 138.0 and 135.0, both below 140.0)
        assert alert_system.alerts_triggered == 2, f"❌ Failed: Alert system should have triggered twice. Got: {alert_system.alerts_triggered}"
        
        print("\n✅ Observer Challenge: Success!")
    except AssertionError as e:
        print(f"\n❌ Assertion Failed: {e}")
    except Exception as e:
        print(f"\n❌ Failed with unexpected error: {e}")


if __name__ == "__main__":
    verify_observer()
