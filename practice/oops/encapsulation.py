class BankAccount:

    def __init__(self, owner, bank, balance):
        self.owner = owner
        self._bank = bank
        self.__balance = balance 

    def get_balance(self):
        print("Available Balance: Rs.", self.__balance)
        return self.__balance

    def deposit(self, amount):
        if amount <= 0:
            print("Amount can't zero or negative")
            return
        self.__balance += amount
        print(f"Deposited Rs.{amount}, New Balance: Rs.{self.__balance}")
            

    def withdraw(self, amount):
        if amount > self.__balance:
            print("Insufficient Balance.")
            return    
        self.__balance -= amount
        print(f"Withdrawn Rs.{amount}, Available Balance: Rs.{self.__balance}")

# acc = BankAccount("Gokul", "SBI", 10000)
# acc.get_balance()
# acc.deposit(1000)
# acc.withdraw(500)

# Using @property — The Pythonic Way
# Instead of get_balance() / set_balance(), Python has a cleaner approach:

class Employee:

    def __init__(self, name, salary):
        self.name = name
        self.__salary = salary

    @property
    def salary(self):
        print(f"Salary of the employee {self.name} is Rs.{self.__salary}")
        return self.__salary

    @salary.setter
    def salary(self, value):
        if value <= 0:
            print("Salary can't be zero or negative")
            return
        self.__salary = value

emp = Employee("Gokul", 200000)
emp.salary
emp.salary = 250000
emp.salary 
emp.salary = -250000