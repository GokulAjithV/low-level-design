import random
from collections import deque

"""
1. Core Entities (Data Layer)
"""

class Player:
    def __init__(self, name):
        self.name = name
        self.position = 0 # all players start from position 0

class BoardItem:
    """Base class for board items (LSP Compliant)"""
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

class Snake(BoardItem):
    pass

class Ladder(BoardItem):
    pass

"""
2. Board Component (Resource Layer)
"""

class Board:
    def __init__(self, size: int = 100):
        self.size = size
        self.snakes: dict[int, int] = {}
        self.ladder: dict[int, int] = {}

    def add_snake(self, start: int, end: int):
        if start <= end:
            print("Start should be greater than end to add snake")
            return
        self.snakes[start] = end

    def add_ladder(self, start: int, end: int):
        if start >= end:
            print("Start should be smaller than end to add ladder")
            return
        self.ladder[start] = end

    def new_position_if_snake_or_ladder(self, current_position: int):
        """Continuously resolves position adjustments recursively"""
        if current_position in self.snakes:
            print(f"🐍 Bitten by the snake! Sliding down from {current_position} to {self.snakes[current_position]}")
            return self.new_position_if_snake_or_ladder(self.snakes[current_position])

        if current_position in self.ladder:
            print(f"🪜 Climbed a ladder! Going to top from {current_position} to {self.ladder[current_position]}")
            return self.new_position_if_snake_or_ladder(self.ladder[current_position])

        return current_position 


"""
3. Core Orchestrater (Engine Layer)
"""

class GameManager:
    def __init__(self, board, players: list[Player]):
        self.board = board
        self.players = deque(players)
        self.winner = None

    def _roll_dice(self):
        return random.randint(1, 6)

    def play_turn(self):

        current_player = self.players.popleft()
        dice_value = self._roll_dice()
        current_position = current_player.position + dice_value
        
        if current_position <= self.board.size:
            print(f"Player {current_player.name} rolled {dice_value} and moving from position {current_player.position} to {current_position}")
            final_position = self.board.new_position_if_snake_or_ladder(current_position)
            current_player.position = final_position
        else:
            print(f"Player {current_player.name} rolled {dice_value}!")
            print(f"Turn Skipped! Player {current_player.name} exactly needs dice value {self.board.size - current_player.position} to win!")

        if current_position == self.board.size:
            print(f"Player {current_player.name} won!!")
            self.winner = current_player
            return True

        self.players.append(current_player)
        return False
        

if __name__ == "__main__":
    
    game_board = Board(size=100)
    game_board.add_snake(50, 25)
    game_board.add_snake(90, 30)
    game_board.add_snake(79, 11)
    game_board.add_snake(10, 20)
    game_board.add_ladder(28, 45)
    game_board.add_ladder(40, 80)
    game_board.add_ladder(31, 57)
    game_board.add_ladder(90, 80)


    player1 = Player("Gokul Ajith")
    player2 = Player("Sanjay")
    player3 = Player("Senthil")
    player4 = Player("Karthi")
    players = [player1, player2, player3, player4]

    game_engine = GameManager(game_board, players)

    turn_count = 0
    has_won = False
    while not has_won and turn_count <= 100:
        has_won = game_engine.play_turn()
        turn_count += 1