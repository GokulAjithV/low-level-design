from abc import ABC, abstractmethod

# =====================================================================
# CHALLENGE 1: FACTORY METHOD (Logistics System)
# =====================================================================

# 1. Define the Abstract Product
class Transport(ABC):
    @abstractmethod
    def deliver(self, cargo: str) -> str:
        pass


# 2. Implement Concrete Products: Truck and Ship
class Truck(Transport):
    def deliver(self, cargo: str) -> str:
        return f"Delivering {cargo} by land in a box truck."


class Ship(Transport):
    def deliver(self, cargo: str) -> str:
        return f"Delivering {cargo} by sea in a container ship."


# 3. Define the Abstract Creator (Logistics)
class Logistics(ABC):
    @abstractmethod
    def create_transport(self) -> Transport:
        """The Factory Method"""
        pass

    def plan_delivery(self, cargo: str) -> str:
        # The core logic relies on the Factory Method to get the right transport
        transport = self.create_transport()
        return transport.deliver(cargo)


# 4. Implement Concrete Creators: RoadLogistics and SeaLogistics
class RoadLogistics(Logistics):
    def create_transport(self) -> Transport:
        return Truck()


class SeaLogistics(Logistics):
    def create_transport(self) -> Transport:
        return Ship()


# =====================================================================
# CHALLENGE 2: ABSTRACT FACTORY (Cloud Infrastructure Broker)
# =====================================================================

# 1. Abstract Products
class Compute(ABC):
    @abstractmethod
    def start(self) -> str:
        pass

class Storage(ABC):
    @abstractmethod
    def upload(self, file_name: str) -> str:
        pass

class Database(ABC):
    @abstractmethod
    def query(self, sql: str) -> str:
        pass


# 2. Concrete Products for AWS: EC2, S3, RDS
class EC2(Compute):
    def start(self) -> str:
        return "Starting AWS EC2 Instance..."

class S3(Storage):
    def upload(self, file_name: str) -> str:
        return f"Uploading {file_name} to AWS S3 bucket..."

class RDS(Database):
    def query(self, sql: str) -> str:
        return f"Running query '{sql}' on AWS RDS PostgreSQL instance..."


# 3. Concrete Products for GCP: ComputeEngine, CloudStorage, CloudSQL
class ComputeEngine(Compute):
    def start(self) -> str:
        return "Starting GCP Compute Engine VM..."

class CloudStorage(Storage):
    def upload(self, file_name: str) -> str:
        return f"Uploading {file_name} to GCP Cloud Storage bucket..."

class CloudSQL(Database):
    def query(self, sql: str) -> str:
        return f"Running query '{sql}' on GCP Cloud SQL MySQL instance..."


# 4. Abstract Factory
class CloudResourceFactory(ABC):
    @abstractmethod
    def create_compute(self) -> Compute:
        pass

    @abstractmethod
    def create_storage(self) -> Storage:
        pass

    @abstractmethod
    def create_database(self) -> Database:
        pass


# 5. Concrete Factories
class AWSResourceFactory(CloudResourceFactory):
    def create_compute(self) -> Compute:
        return EC2()

    def create_storage(self) -> Storage:
        return S3()

    def create_database(self) -> Database:
        return RDS()


class GCPResourceFactory(CloudResourceFactory):
    def create_compute(self) -> Compute:
        return ComputeEngine()

    def create_storage(self) -> Storage:
        return CloudStorage()

    def create_database(self) -> Database:
        return CloudSQL()


# =====================================================================
# CLIENT / VERIFICATION CODE (Do not modify this part)
# =====================================================================

def verify_challenge_1():
    print("--- Testing Challenge 1 (Factory Method) ---")
    try:
        road_logistics = RoadLogistics()
        sea_logistics = SeaLogistics()
        
        truck_delivery = road_logistics.plan_delivery("Apples")
        ship_delivery = sea_logistics.plan_delivery("Cars")
        
        print(f"Road Delivery Result: {truck_delivery}")
        print(f"Sea Delivery Result: {ship_delivery}")
        
        assert "land" in truck_delivery, "Road delivery should mention 'land'."
        assert "sea" in ship_delivery, "Sea delivery should mention 'sea'."
        print("✅ Challenge 1: Success!")
    except Exception as e:
        print(f"❌ Challenge 1 failed: {e}")


def verify_challenge_2():
    print("\n--- Testing Challenge 2 (Abstract Factory) ---")
    
    def deploy_cluster(factory: CloudResourceFactory) -> list:
        compute = factory.create_compute()
        storage = factory.create_storage()
        database = factory.create_database()
        
        res = [
            compute.start(),
            storage.upload("dashboard.png"),
            database.query("SELECT * FROM users")
        ]
        return res

    try:
        print("Deploying AWS resources...")
        aws_factory = AWSResourceFactory()
        aws_deployment = deploy_cluster(aws_factory)
        for msg in aws_deployment:
            print(f"  > {msg}")
        
        assert "AWS" in aws_deployment[0] and "EC2" in aws_deployment[0], "Compute should be EC2"
        assert "S3" in aws_deployment[1], "Storage should be S3"
        assert "RDS" in aws_deployment[2], "Database should be RDS"
            
        print("Deploying GCP resources...")
        gcp_factory = GCPResourceFactory()
        gcp_deployment = deploy_cluster(gcp_factory)
        for msg in gcp_deployment:
            print(f"  > {msg}")
            
        assert "GCP" in gcp_deployment[0] and "Compute Engine" in gcp_deployment[0], "Compute should be Compute Engine"
        assert "Storage" in gcp_deployment[1], "Storage should be Cloud Storage"
        assert "SQL" in gcp_deployment[2], "Database should be Cloud SQL"
        
        print("✅ Challenge 2: Success!")
    except Exception as e:
        print(f"❌ Challenge 2 failed: {e}")


if __name__ == "__main__":
    verify_challenge_1()
    verify_challenge_2()
