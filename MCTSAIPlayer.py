import random
from Player import Player

class MCTSAIPlayer(Player):
    def __init__(self, piece, iterations=1000):
        super().__init__(piece)
        self.iterations = iterations

    def get_move(self, board):
        valid_moves = board.get_valid_moves()
        return random.choice(valid_moves) if valid_moves else None