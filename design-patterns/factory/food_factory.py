from abc import ABC, abstractmethod

# Product Interface
class Food(ABC):
    @abstractmethod
    def prepare():
        pass 

# Concrete Products
class Pizza(Food):
    def prepare(self):
        print("prepareing Pizza")
    
class Burger(Food):
    def prepare(self):
        print("prepareing Burger")

# Client Code - Tightly Coupled 
class Restaurant:
    @staticmethod
    def order(item):
        
        if item == "pizza":
            food = Pizza()
        elif item == "burger":
            food = Burger()
        else:
            raise ValueError(f"We don't server '{item}'")
            return

        food.prepare()

Restaurant.order("Mutton")
    