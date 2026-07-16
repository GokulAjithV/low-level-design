from collections import deque
import random

# ========================================================
# 1. CORE ENTITIES (Data Layer)
# ========================================================
class Player:
    def __init__(self, name: str):
        self.name = name
        self.position = 0  # All players start at position 0


class BoardItem:
    """Base class for special board obstacles (LSP compliant)"""
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end


class Snake(BoardItem):
    pass  # start > end (Swallows you down)


class Ladder(BoardItem):
    pass  # start < end (Climbs you up)


# ========================================================
# 2. THE BOARD COMPONENT (Resource Layer)
# ========================================================
class Board:
    def __init__(self, size: int = 100):
        self.size = size
        self.snakes: dict[int, int] = {}
        self.ladders: dict[int, int] = {}

    def add_snake(self, start: int, end: int):
        self.snakes[start] = end

    def add_ladder(self, start: int, end: int):
        self.ladders[start] = end

    def check_new_position(self, current_pos: int) -> int:
        """Continuously resolves position adjustments recursively"""
        if current_pos in self.snakes:
            print(f"🐍 Bitten by a snake! Sliding down from {current_pos} to {self.snakes[current_pos]}")
            return self.check_new_position(self.snakes[current_pos])
        
        if current_pos in self.ladders:
            print(f"🪜 Climbed a ladder! Going up from {current_pos} to {self.ladders[current_pos]}")
            return self.check_new_position(self.ladders[current_pos])
            
        return current_pos


# ========================================================
# 3. GAME ORCHESTRATOR (Engine Layer)
# ========================================================
class GameManager:
    def __init__(self, board: Board, players: list[Player]):
        self.board = board
        # Using a Double-Ended Queue (Deque) to manage turns cleanly
        self.players = deque(players)
        self.winner = None

    def _roll_dice(self) -> int:
        return random.randint(1, 6)

    def play_turn(self) -> bool:
        if self.winner:
            return False

        # 1. Pop the current active player from the front of the queue
        current_player = self.players.popleft()
        dice_value = self._roll_dice()
        
        next_position = current_player.position + dice_value
        print(f"🎲 {current_player.name} rolled a {dice_value}. Moving from {current_player.position} to {next_position}")

        # 2. Rule Validation Boundary
        if next_position <= self.board.size:
            # Resolve if they hit a snake or ladder
            final_position = self.board.check_new_position(next_position)
            current_player.position = final_position
        else:
            print(f"⚠️ {current_player.name} needs exact roll to win. Turn skipped.")

        # 3. Check for Win Condition
        if current_player.position == self.board.size:
            self.winner = current_player
            print(f"🎉🎉 {current_player.name} has won the match! 🎉🎉")
            return True

        # 4. Put the player back to the end of the line if game continues
        self.players.append(current_player)
        return False

if __name__ == "__main__":
    # Setup Board
    game_board = Board(size=100)
    game_board.add_snake(14, 3)
    game_board.add_snake(99, 25)
    game_board.add_ladder(5, 45)
    game_board.add_ladder(40, 89)

    # Setup Players
    p1 = Player("Gokul")
    p2 = Player("Ajith")

    # Start Game Loop
    game = GameManager(game_board, [p1, p2])
    
    # Run turns until someone wins
    has_won = False
    turn_count = 0
    while not has_won and turn_count < 100: # Cap at 20 turns for demo safety
        has_won = game.play_turn()
        turn_count += 1