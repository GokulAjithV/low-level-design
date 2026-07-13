from abc import ABC, abstractmethod

# The Receiver (expert object that does the work)
class CricketMatchScoreCard:
    
    def __init__(self):
        self.total_runs = 0
        self.balls_bowled = 0

    def add_runs(self, count: int):
        self.total_runs += count

    def remove_runs(self, count: int):
        self.total_runs -= count

    def increment_ball(self):
        self.balls_bowled += 1

    def decrement_ball(self):
        self.balls_bowled -= 1

# The Command Interface and Concrete Commands 

class Command(ABC):
    @abstractmethod
    def execute(self): pass

    @abstractmethod
    def undo(self): pass

class ScoreBoundaryCommand(Command):
    def __init__(self, scorecard: CricketMatchScoreCard, runs: int):
        self.scorecard = scorecard
        self.runs = runs

    def execute(self):
        self.scorecard.add_runs(self.runs)
        self.scorecard.increment_ball()

    def undo(self):
        self.scorecard.remove_runs(self.runs)
        self.scorecard.decrement_ball()
    
# The INVOKER (Manages execution context and history stack)

class ScoringHistoryInvoker:
    def __init__(self):
        self._history_stack = []

    def execute_action(self, command: Command):
        command.execute()
        self._history_stack.append(command)

    def undo_last_action(self):
        if not self._history_stack:
            print("no operations left to undo")
            return 

        last_command = self._history_stack.pop()
        last_command.undo()
        print("undo executed!!")


scorecard = CricketMatchScoreCard()
history_manager = ScoringHistoryInvoker()
