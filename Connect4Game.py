import pygame
from MinimaxAIPlayer import MinimaxAIPlayer
from MCTSAIPlayer import MCTSAIPlayer

from Connect4Board import Connect4Board
from Connect4Gui import Connect4Gui
from HumanPlayer import HumanPlayer
from RandomPlayer import RandomAIPlayer


# =========================
# GAME LOOP
# =========================

class Connect4Game:

    def __init__(self):
        pass

    def run_game(self, player1, player2, headless = False, rows = 6, cols = 7, n_connect = 4 ):

        board = Connect4Board(rows, cols, n_connect)

        gui = Connect4Gui(board,rows,cols)
        if (not headless):
            gui.init(board)

        players = [player1, player2]
        turn = 0
        game_over = False

        while not game_over:
            current_player = players[turn]
            if (not headless):
                gui.deal_with_events(board, current_player)

            move = current_player.get_move(board)

            if move is not None and move in board.get_valid_moves():
                row, col = board.drop_piece(move, current_player.piece)

                if board.check_winner(current_player.piece):
                    if(not headless):
                       gui.update_winner(current_player)
                    else:
                        print(f"Player {current_player.piece} wins!")

                    game_over = True

                elif board.is_board_full():
                    if (not headless):
                        gui.draw_game()
                    print("Draw!!!!")
                    game_over = True

                if(not headless):
                    gui.draw_board(board)
                turn = (turn + 1) % 2

            # AI delay (optional for visibility)
            if not headless and not isinstance(current_player, HumanPlayer):
                pygame.time.wait(300)

            if game_over and not headless:
                gui.game_over() 


# =========================
# AUTOMATED TESTS FUNCTION
# =========================

def run_tests(test_name, p1, p2, num_games=10):
    print(f"\nA correr testes para: {test_name} ({num_games} games)...")
    
    pygame.init() 
    
    victories_p1 = 0
    victories_p2 = 0
    draws = 0
    game_durations = []

    for i in range(num_games):
        board = Connect4Board(6, 7, 4)
        players = [p1, p2]
        turn = 0
        
        # Mede o tempo inicial em milissegundos usando o pygame
        tempo_inicio = pygame.time.get_ticks()
        
        while True:
            current_player = players[turn]
            move = current_player.get_move(board)
            
            if move is not None and move in board.get_valid_moves():
                board.drop_piece(move, current_player.piece)
                
                if board.check_winner(current_player.piece):
                    if current_player.piece == p1.piece:
                        victories_p1 += 1  # CORRIGIDO AQUI
                    else:
                        victories_p2 += 1  # CORRIGIDO AQUI
                    break
                elif board.is_board_full():
                    draws += 1             # CORRIGIDO AQUI
                    break
                    
                turn = (turn + 1) % 2
            else:
                draws += 1                 # CORRIGIDO AQUI
                break

        # Mede o tempo final e calcula a duração em segundos
        tempo_fim = pygame.time.get_ticks()
        duracao_segundos = (tempo_fim - tempo_inicio) / 1000.0
        game_durations.append(duracao_segundos)
        
        print(f"   Jogo {i+1}/{num_games} concluído.")

     #Calculos
    victory_rate_p1 = (victories_p1 / num_games) * 100
    victory_rate_p2 = (victories_p2 / num_games) * 100
    avg_duration = sum(game_durations) / len(game_durations)
    max_duration = max(game_durations)
    min_duration = min(game_durations)

    print("\n" + "="*50)
    print(f"Nº de Jogos:                      {num_games}")
    print(f"Vitórias Jogador 1:               {victories_p1}")
    print(f"Vitórias Jogador 2:               {victories_p2}")
    print(f"Empates:                          {draws}")
    print(f"Taxa de Vitórias Jogador 1 (%):   {victory_rate_p1:.2f}%")
    print(f"Taxa de Vitórias Jogador 2 (%):   {victory_rate_p2:.2f}%")
    print(f"Duração Média do Jogo (s):        {avg_duration:.4f}")
    print(f"Duração Máxima (s):               {max_duration:.4f}")
    print(f"Duração Mínima (s):               {min_duration:.4f}")
    print("="*50 + "\n")


# =========================
# RUN CONFIGURATION
# =========================
#if __name__ == "__main__":
#    game = Connect4Game()
#    
    # Exemplo: Humano vs Minimax (profundidade 4)
#    p1 = HumanPlayer(piece=1)
#    p2 = MinimaxAIPlayer(piece=2, depth=4)
    
#    game.run_game(p1, p2, headless=False)
if __name__ == "__main__":
    total_games = 50
    print("A INICIAR TESTES (50 JOGOS CADA)...\n")

    # 1. Minimax vs Aleatório
    p1 = MinimaxAIPlayer(piece=1, depth=3) 
    p2 = RandomAIPlayer(piece=2)
    run_tests("MiniMax vs Aleatório", p1, p2, total_games)
    
    # 2. MCTS vs Aleatório
    p1_mcts = MCTSAIPlayer(piece=1, iterations=1000)
    p2_rand = RandomAIPlayer(piece=2)
    run_tests("MCTS vs Aleatório", p1_mcts, p2_rand, total_games)

    # 3. 1º comb MiniMax vs MCTS (Jogadas Rápidas)
    p1_comb1 = MinimaxAIPlayer(piece=1, depth=2)
    p2_comb1 = MCTSAIPlayer(piece=2, iterations=150)
    run_tests("1º comb MiniMax vs MCTS", p1_comb1, p2_comb1, total_games)

    # 4. 2º comb MiniMax vs MCTS (Jogadas Médias)
    p1_comb2 = MinimaxAIPlayer(piece=1, depth=3)
    p2_comb2 = MCTSAIPlayer(piece=2, iterations=1500)
    run_tests("2º comb MiniMax vs MCTS", p1_comb2, p2_comb2, total_games)

    # 5. 3º comb MiniMax vs MCTS (Jogadas Lentas / Pesadas)
    p1_comb3 = MinimaxAIPlayer(piece=1, depth=4)
    p2_comb3 = MCTSAIPlayer(piece=2, iterations=8000)
    run_tests("3º comb MiniMax vs MCTS", p1_comb3, p2_comb3, total_games)

    print("TODOS OS TESTES FORAM CONCLUÍDOS COM SUCESSO! Podes preencher o Excel.")