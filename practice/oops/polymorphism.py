# Polymorphism allows you to write a single function that can deploy any service (execute any behaviour) without knowing what it is. 
# And it only knows each object has a method with common name

# 1. Compile-Time Polymorphism (Static Binding)

# This occurs when the method to be called is determined at the time of compilation.

# Method Overloading: Defining multiple methods with the same name but different parameters (e.g., add(int, int) vs add(double, double)).

# The Python Catch: Python does not support traditional method overloading. If you define two methods with the same name, the last one defined wins.

# Python Workaround: We achieve this using default arguments or variable-length arguments (*args, kwargs).



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

class LambdaFunction(ComputeService):
    def __init__(self, region, cpu_cores, runtime_language):
        super().__init__(region, cpu_cores)
        self.runtime_language = runtime_language

    def deploy(self):
        # The most specific version
        super().deploy()
        print(f"Running code in {self.runtime_language} runtime.")

class StorageService(CloudService):
    def __init__(self, region, ram, rom):
        super().__init__(region)
        self.ram = ram 
        self.rom = rom

    def deploy(self):
        super().deploy()
        print(f"Allocating '{self.ram}GB RAM' and '{self.rom}GB ROM'")


# A single function that handles ANY cloud service

def start_deployment(service):
    print("--- Starting System Check ---")
    service.deploy()
    print("--- Deployment Complete ---")

services = [
    LambdaFunction("us-east-1", 3, "Python 3.11.1"),
    StorageService("us-east-1", 8, 120)
]

for service in services:
    start_deployment(service)

