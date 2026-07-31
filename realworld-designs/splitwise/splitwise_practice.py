from abc import ABC, abstractmethod
from collections import defaultdict
import uuid

class User:
    def __init__(self, user_id: str, name: str):
        self.user_id = user_id
        self.name = name

class Split(ABC):
    def __init__(self, user: User):
        self.user = user 
        self.amount_owed  = 0.0

    @abstractmethod
    def calculate_share(self, total_amount, split_value):
        pass

class EqualSplit(Split):
    def calculate_share(self, total_amount, num_participants):
        self.amount_owed = round(total_amount / num_participants, 2)
        return self.amount_owed

class ExactSplit(Split):
    def calculate_share(self, total_amount, exact_amount):
        self.amount_owed = round(exact_amount, 2)
        return self.amount_owed 

class PercentSplit(Split):
    def calculate_share(self, total_amount, percentage):
        self.amount_owed = round(total_amount * (percentage / 100), 2)
        return self.amount_owed

class SplitStrategy:
    @abstractmethod
    def create_splits(self, total_amount, users, values):
        pass

    def validate(self, total_amount, splits):
        total = sum(s.amount_owed for s in splits)
        if abs(total - total_amount) > 0.01:
            raise Exception(f"Split amounts ({total}) do not sum to total ({total_amount})")

class EqualSplitStrategy:
    def create_splits(self, total_amount, users, values=None):
        splits = []
        for user in users:
            split = EqualSplit(user)
            split.calculate_share(total_amount, len(users))
            splits.append(split)
        self._validate(self, splits, total_amount)
        return splits

class ExactSplitStrategy:
    def create_splits(self, total_amount, users, values):
        if (len(users) != len(values)):
            raise Exception("Users and values count mismatch")
        splits = []
        for user, value in zip(users, values):
            split = ExactSplit(user)
            split.calculate_share(total_amount, value)
            splits.append(split)
        self._validate(self, splits, total_amount)
        return splits

class PercentSplitStrategy:
    def create_splits(self, total_amount, users, percentages):
        if len(percentages) != len(users):
            raise Exception("Users and Percentages count mismatch")
        if sum(percentages) != 100:
            raise Exception("Percentages must sum to 100")
        splits = []
        for user, percentage in zip(users, percentages):
            split = PercentSplit(user)
            split.calculate_share(total_amount, percentage)
            splits.append(split)
        self._validate(self, splits, total_amount)
        return splits

class Observer(ABC):
    @abstractmethod
    def notify(self, message: str):
        pass

class EmailNotifier(Observer):
    def notify(self, message: str):
        print(f"Message '{message}' notified via email")

class Expense:
    def __init__(self, expense_id: str, description: str, amount: float, paid_by: User, splits: list[Split]):
        self.expense_id = expense_id
        self.description = description
        self.amount = amount
        self.paid_by = paid_by
        self.splits = splits

class BalanceSheet:
    def __init__(self):
        self.balances = defaultdict(defaultdict(float))

    def update(self, paid_by: User, splits: list[Split]):
        for split in splits:
            if split.user.user_id == paid_by.user_id:
                continue
            self.balances[split.user.user_id][paid_by.user_id] += split.amount_owed
            self.balances[paid_by.user_id][split.user.user_id] -= split.amount_owed

    def show_balance(self, user: User, users: dict[str, User]):
        print(f"---- Balances of user {user.name}")
        for other_id, amount in self.balances[user.user_id]:
            if amount > 0:
                print(f"'{user.name}' owes '{users[other_id]}' Rs.{amount}")
            elif amount < 0:
                print(f"'{users[other_id]}' owes '{user.name}' Rs.{amount}")

    def simplify_debts(self):
        pass

class ExpenseManager:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls.users: dict[str, User] = {}
            cls.expenses: list[Expense] = []
            cls.balance_sheet = BalanceSheet()
            cls.observers: list[Observer] = []
        return cls._instance
        
    def add_user(self, user: User):
        self.users[user.user_id] = user
    
    def add_observer(self, observer: Observer):
        self.observers.append(observer)

    def _notify_all(self, message):
        for observer in self.observers:
            observer.notify(self, message)

    def add_expense(self, description, amount, users, paid_by: User, strategy: SplitStrategy, values=None):
        splits = strategy.create_splits(amount, users, values)
        expense = Expense(str(uuid.uuid4()), description, amount, paid_by, splits)
        self.expenses.append(expense)
        self.balance_sheet.update(paid_by, splits)
        self._notify_all(f"{paid_by.name} added expense '{description}' of Rs.{amount}")
        return expense

