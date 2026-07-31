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
        self.amount_owed = 0.0

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
        self.amount_owed = round(total_amount * percentage / 100, 2)
        return self.amount_owed


class SplitStrategy(ABC):
    @abstractmethod
    def create_splits(self, total_amount, users, values):
        pass

    def _validate(self, splits, total_amount):
        total = sum(s.amount_owed for s in splits)
        if abs(total - total_amount) > 0.01:
            raise Exception(f"Split amounts ({total}) do not sum to total ({total_amount})")


class EqualSplitStrategy(SplitStrategy):
    def create_splits(self, total_amount, users, values=None):
        splits = []
        for user in users:
            split = EqualSplit(user)
            split.calculate_share(total_amount, len(users))
            splits.append(split)
        self._validate(splits, total_amount)
        return splits


class ExactSplitStrategy(SplitStrategy):
    def create_splits(self, total_amount, users, values):
        if len(users) != len(values):
            raise Exception("Users and amounts count mismatch")
        splits = []
        for user, amount in zip(users, values):
            split = ExactSplit(user)
            split.calculate_share(total_amount, amount)
            splits.append(split)
        self._validate(splits, total_amount)
        return splits


class PercentSplitStrategy(SplitStrategy):
    def create_splits(self, total_amount, users, values):
        if len(users) != len(values):
            raise Exception("Users and percentages count mismatch")
        if sum(values) != 100:
            raise Exception("Percentages must sum to 100")
        splits = []
        for user, percent in zip(users, values):
            split = PercentSplit(user)
            split.calculate_share(total_amount, percent)
            splits.append(split)
        self._validate(splits, total_amount)
        return splits


class Observer(ABC):
    @abstractmethod
    def notify(self, message: str):
        pass


class EmailNotifier(Observer):
    def notify(self, message: str):
        print(f"[EMAIL] {message}")


class Expense:
    def __init__(self, expense_id, description, amount, paid_by: User, splits):
        self.expense_id = expense_id
        self.description = description
        self.amount = amount
        self.paid_by = paid_by
        self.splits = splits


class BalanceSheet:
    def __init__(self):
        self.balances = defaultdict(lambda: defaultdict(float))

    def update(self, paid_by: User, splits):
        for split in splits:
            if split.user.user_id == paid_by.user_id:
                continue
            self.balances[split.user.user_id][paid_by.user_id] += split.amount_owed
            self.balances[paid_by.user_id][split.user.user_id] -= split.amount_owed

    def show_balances(self, user: User):
        print(f"--- Balances for {user.name} ---")
        for other_id, amount in self.balances[user.user_id].items():
            if amount > 0:
                print(f"{user.name} owes {other_id}: Rs.{round(amount,2)}")
            elif amount < 0:
                print(f"{other_id} owes {user.name}: Rs.{round(-amount,2)}")

    def simplify_debts(self):
        net = defaultdict(float)
        for debtor, creditors in self.balances.items():
            for creditor, amount in creditors.items():
                net[debtor] -= amount
                net[creditor] += amount
        return net


class ExpenseManager:
    _instance = None

    def __init__(self):
        if ExpenseManager._instance is not None:
            raise Exception("Use get_instance()")
        self.users = {}
        self.expenses = []
        self.balance_sheet = BalanceSheet()
        self.observers = []

    @staticmethod
    def get_instance():
        if ExpenseManager._instance is None:
            ExpenseManager._instance = ExpenseManager()
        return ExpenseManager._instance

    def add_user(self, user: User):
        self.users[user.user_id] = user

    def add_observer(self, observer: Observer):
        self.observers.append(observer)

    def _notify_all(self, message):
        for obs in self.observers:
            obs.notify(message)

    def add_expense(self, description, amount, paid_by: User, users, strategy: SplitStrategy, values=None):
        splits = strategy.create_splits(amount, users, values)
        expense = Expense(str(uuid.uuid4()), description, amount, paid_by, splits)
        self.expenses.append(expense)
        self.balance_sheet.update(paid_by, splits)
        self._notify_all(f"{paid_by.name} added expense '{description}' of Rs.{amount}")
        return expense


if __name__ == "__main__":
    manager = ExpenseManager.get_instance()
    manager.add_observer(EmailNotifier())

    alice = User("u1", "Alice")
    bob = User("u2", "Bob")
    charlie = User("u3", "Charlie")

    for u in [alice, bob, charlie]:
        manager.add_user(u)

    manager.add_expense(
        "Dinner", 300, alice, [alice, bob, charlie], EqualSplitStrategy()
    )

    manager.add_expense(
        "Groceries", 500, bob, [alice, bob, charlie],
        ExactSplitStrategy(), values=[200, 200, 100]
    )

    manager.add_expense(
        "Rent", 1000, charlie, [alice, bob, charlie],
        PercentSplitStrategy(), values=[40, 30, 30]
    )

    for u in [alice, bob, charlie]:
        manager.balance_sheet.show_balances(u)
