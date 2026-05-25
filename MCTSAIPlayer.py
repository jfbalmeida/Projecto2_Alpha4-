import math
from platform import node
import random
from Player import Player


class Node:
    def __init__(self, board, parent=None, move=None, current_piece=1):
        self.board = board
        self.parent = parent
        self.move = move
        self.current_piece = current_piece
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = board.get_valid_moves()

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def is_terminal(self):
    # O jogo termina se o tabuleiro encher OU se o jogador 1 ou 2 vencerem
        return (len(self.board.get_valid_moves()) == 0 or 
            self.board.check_winner(1) or 
            self.board.check_winner(2))

    def ucb(self, c=math.sqrt(2)):
        if self.visits == 0:
            return float('inf')
        return (self.wins / self.visits) + c * math.sqrt(math.log(self.parent.visits) / self.visits)

    def best_child(self, c=math.sqrt(2)):
        return max(self.children, key=lambda child: child.ucb(c))


class MCTSAIPlayer(Player):
    def __init__(self, piece, iterations=1000):
        super().__init__(piece)
        self.iterations = iterations
        self.opponent_piece = 2 if piece == 1 else 1

    def get_move(self, board):
        valid_moves = board.get_valid_moves()
        if not valid_moves:
            return None
        if len(valid_moves) == 1:
            return valid_moves[0]

        root = Node(board.copy(), current_piece=self.piece)

        for _ in range(self.iterations):
            node = self._select(root)
            result = self._simulate(node)
            self._backpropagate(node, result)

        best = root.best_child(c=0)
        return best.move

    def _select(self, node):
        while not node.is_terminal():
            if not node.is_fully_expanded():
                return self._expand(node)
            else:
                node = node.best_child()
        return node

    def _expand(self, node):
        move = random.choice(node.untried_moves)
        node.untried_moves.remove(move)

        new_board = node.board.copy()
        new_board.drop_piece(move, node.current_piece)

        next_piece = self.opponent_piece if node.current_piece == self.piece else self.piece

        child = Node(new_board, parent=node, move=move, current_piece=next_piece)
        node.children.append(child)
        return child

    def _simulate(self, node):
        sim_board = node.board.copy()
        current_piece = node.current_piece

        while True:
            # Verifica se o jogador anterior ganhou com a última jogada colocada
            prev_piece = self.opponent_piece if current_piece == self.piece else self.piece
            if sim_board.check_winner(prev_piece):
                return prev_piece # Devolve 1 ou 2

            moves = sim_board.get_valid_moves()
            if not moves:
                return 0.5 # Empate

            sim_board.drop_piece(random.choice(moves), current_piece)
            current_piece = self.opponent_piece if current_piece == self.piece else self.piece
    def _backpropagate(self, node, winner):
        while node is not None:
            node.visits += 1
            if winner == 0.5:
                node.wins += 0.5
            else:
                if node.parent and node.parent.current_piece == winner:
                    node.wins += 1
            node = node.parent