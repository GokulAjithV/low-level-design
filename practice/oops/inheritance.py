class Payment:
    def __init__(self, amount):
        self.amount = amount

    def process_payment(self):
        print(f"Processing payment of Rs {self.amount}")

class CreditCardPayment(Payment):
    def __init__(self, amount, card_number):
        # super() calls the parent constructor
        super().__init__(amount)
        self.card_number = card_number

    def process_payment(self):
        print(f"Processing Credit Card '{self.card_number}' for amount Rs.{self.amount}")


# cc = CreditCardPayment(5000, "1234-23424-2342")
# cc.process_payment()

class Vehicle:
    def __init__(self, brand):
        self.brand = brand

    def fuel_up(self):
        print("General vehicle fueling...")

class Car(Vehicle):
    def __init__(self, brand, gear_type):
        super().__init__(brand)
        self.gear_type = gear_type

    def fuel_up(self):
        print(f"Fueling {self.brand} with pertrol.")

class EelectricCar(Car):
    def __init__(self, brand, gear_type, battery_kwh):
        super().__init__(brand, gear_type)
        self.battery_kwh = battery_kwh

    def fuel_up(self):
        print(f"Charging up {self.brand} with {self.battery_kwh} kwh")

# ec = EelectricCar("Tesla", "Automatic", 100)
# ec.fuel_up()

class CloudService:
    def __init__(self, region):
        self.region = region

    def deploy(self):
        # The base class defines the general action
        print(f"Deploying resource to {self.region}...")

class ComputeService(CloudService):
    def __init__(self, region, cpu_cores):
        super().__init__(region)
        self.cpu_cores = cpu_cores

    def deploy(self):
        # It calls the parent's deploy logic, then adds its own
        super().deploy()
        print(f"Allocating {self.cpu_cores} CPU cores.")

class StorageService(CloudService):
    def __init__(self, region, ram, rom):
        super().__init__(region)
        self.ram = ram 
        self.rom = rom

    def deploy(self):
        super().deploy()
        print(f"Allocating '{self.ram}GB RAM' and '{self.rom}GB ROM'")

class LambdaFunction(ComputeService):
    def __init__(self, region, cpu_cores, runtime_language):
        super().__init__(region, cpu_cores)
        self.runtime_language = runtime_language

    def deploy(self):
        # The most specific version
        super().deploy()
        print(f"Running code in {self.runtime_language} runtime.")

# Usage
my_func = LambdaFunction("us-east-1", 2, "Python 3.12")
my_func.deploy()