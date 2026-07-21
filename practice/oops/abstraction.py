from abc import ABC, abstractmethod

# 1. Process Abstraction
class PaymentGateway(ABC):

    @abstractmethod
    def pay(self, amount):
        pass

    @abstractmethod
    def refund(self, amount):
        pass

class RazorpayGateway(PaymentGateway):

    def pay(self, amount):
        print(f"Razorpay - Processing Amount: Rs.{amount}")

    def refund(self, amount):
        print(f"Razorpay - Processing Amount: Rs.{amount}")

class PaytmGateway(PaymentGateway):

    def pay(self, amount):
        print(f"Paytm - Processing Amount: Rs.{amount}")

    def refund(self, amount):
        print(f"Paytm - Processing Amount: Rs.{amount}")

gateway = RazorpayGateway()
gateway.pay(500)

# 2. Data Abstraction - It is called Encapsulation (where you wrap data and methods in a class 
# and protect its internal details by controlled access through getters and setters)

class BankAccount:

    def __init__(self):
        self.__balance = 0

    def deposit(self, amount):
        self.__balance += amount

    def withdraw(self, amount):
        if self.__balance >= amount:
            self.__balance -= amount
            print(f"Withdrawn Rs.{amount}. Available Balance: Rs.{self.__balance}")
        else:
            print(f"Insufficient Balance - Rs.{self.__balance}")

    def get_balance(self):
        return self.__balance

acc = BankAccount(10000)
acc.deposit(1000)
acc.withdraw(500)