import math
import random
from Player import Player

class MinimaxAIPlayer(Player):
    def __init__(self, piece, depth=4):
        super().__init__(piece)
        self.depth = depth
        self.opponent_piece = 1 if piece == 2 else 2

    def is_terminal_node(self, board):
        """Verifica se o jogo acabou (alguém ganhou ou empate)"""
        return board.check_winner(self.piece) or board.check_winner(self.opponent_piece) or board.is_board_full()

    def evaluate_window(self, window, piece):
        """Avalia uma única janela de 4 posições consecutivas."""
        score = 0
        opp_piece = self.opponent_piece

        count_piece = window.count(piece)
        count_opp = window.count(opp_piece)
        count_empty = window.count(0)

        # Lógica ofensiva
        if count_piece == 4:
            score += 1000
        elif count_piece == 3 and count_empty == 1:
            score += 5
        elif count_piece == 2 and count_empty == 2:
            score += 2

        # Lógica defensiva (bloqueio imediato)
        if count_opp == 3 and count_empty == 1:
            score -= 4 

        return score

    def score_position(self, board, piece):
        """Avalia o estado completo do tabuleiro."""
        score = 0

        # 1. Bónus pela Coluna Central
        center_col = board.cols // 2
        center_array = [int(board.grid[r][center_col]) for r in range(board.rows)]
        center_count = center_array.count(piece)
        score += center_count * 3

        # 2. Linhas Horizontais
        for r in range(board.rows):
            row_array = [int(board.grid[r][c]) for c in range(board.cols)]
            for c in range(board.cols - 3):
                window = row_array[c:c+4]
                score += self.evaluate_window(window, piece)

        # 3. Linhas Verticais
        for c in range(board.cols):
            col_array = [int(board.grid[r][c]) for r in range(board.rows)]
            for r in range(board.rows - 3):
                window = col_array[r:r+4]
                score += self.evaluate_window(window, piece)

        # 4. Diagonais Positivas (/)
        for r in range(board.rows - 3):
            for c in range(board.cols - 3):
                window = [int(board.grid[r+i][c+i]) for i in range(4)]
                score += self.evaluate_window(window, piece)

        # 5. Diagonais Negativas (\)
        for r in range(3, board.rows):
            for c in range(board.cols - 3):
                window = [int(board.grid[r-i][c+i]) for i in range(4)]
                score += self.evaluate_window(window, piece)

        return score

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        valid_moves = board.get_valid_moves()
        is_terminal = self.is_terminal_node(board)
        
        if depth == 0 or is_terminal:
            if is_terminal:
                if board.check_winner(self.piece):
                    return (None, 1000000000000)
                elif board.check_winner(self.opponent_piece):
                    return (None, -1000000000000)
                else:
                    return (None, 0)
            else:
                return (None, self.score_position(board, self.piece))
                
        if maximizingPlayer:
            value = -math.inf
            column = random.choice(valid_moves)
            for col in valid_moves:
                b_copy = board.copy() # Não modificamos o tabuleiro original!
                b_copy.drop_piece(col, self.piece)
                new_score = self.minimax(b_copy, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break # Poda Alpha-Beta
            return column, value
            
        else: # Turno do oponente (Minimizador)
            value = math.inf
            column = random.choice(valid_moves)
            for col in valid_moves:
                b_copy = board.copy()
                b_copy.drop_piece(col, self.opponent_piece)
                new_score = self.minimax(b_copy, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break # Poda Alpha-Beta
            return column, value

    def get_move(self, board):
        col, minimax_score = self.minimax(board, self.depth, -math.inf, math.inf, True)
        
        # Fallback de segurança
        if col is None:
            valid_moves = board.get_valid_moves()
            return random.choice(valid_moves) if valid_moves else None
            
        return col