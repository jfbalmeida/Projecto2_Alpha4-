# Projeto 2: Alpha4' - Agentes Inteligentes para Connect N

**Unidade Curricular:** Inteligência Artificial 2025/2026
**Instituição:** ISCTE - Instituto Universitário de Lisboa
**Autores:**
- João Almeida - 129862
- Henrique Fernandes - 129844

---

## Sobre o Projeto

Este projeto consiste na implementação de agentes de Inteligência Artificial para jogar Connect N (uma generalização do clássico 4 em Linha, em que o tamanho do tabuleiro e o número de peças para alinhar são configuráveis).

O objetivo principal é a aplicação e comparação de duas técnicas de procura em jogos:
1. Procura Adversarial: Algoritmo Minimax com Poda Alfa-Beta e uma função de avaliação heurística do tabuleiro.
2. Procura Baseada em Simulação: Algoritmo MCTS (Monte Carlo Tree Search).

O projeto inclui um motor de jogo base, uma interface gráfica em Pygame e um sistema de testes automatizado construído para extrair métricas de desempenho (tempo de execução e taxa de vitórias) das várias IAs.

---

## Estrutura de Ficheiros

- Connect4Board.py: Lógica central do jogo e representação do estado do tabuleiro.
- Connect4Game.py: Motor do jogo que controla o ciclo de turnos e as condições de vitória. Inclui também o script principal de testes automatizados (headless).
- Connect4Gui.py: Interface gráfica desenvolvida em Pygame para visualização e interação humana com o jogo.
- Player.py: Classe base genérica para a criação de jogadores.
- HumanPlayer.py: Permite que um utilizador humano jogue utilizando o rato.
- RandomPlayer.py: Agente que joga através de escolhas puramente aleatórias (usado como baseline de controlo).
- MinimaxAIPlayer.py: Implementação do agente Minimax com Poda Alfa-Beta.
- MCTSAIPlayer.py: Implementação do agente MCTS (Monte Carlo Tree Search).
- resultados.xlsx: Folha de cálculo contendo os resultados e a análise das métricas extraídas dos testes automatizados.

---

## Pré-requisitos e Instalação

Para executar o projeto, é necessário ter o Python 3 instalado. As seguintes bibliotecas externas são necessárias para o motor do jogo e para a interface gráfica:

pip install numpy pygame-ce

---

## Como Executar

### 1. Bateria de Testes Automatizados

O ficheiro Connect4Game.py está configurado para executar as simulações exigidas no enunciado em modo invisível (headless), de modo a extrair os tempos médios e taxas de vitória.

Para correr os testes e ver os resultados no terminal, executar:

python Connect4Game.py

Como o MCTS realiza milhares de simulações iterativas, o processo completo de testes poderá demorar alguns minutos.

### 2. Jogar na Interface Gráfica

Para jogar diretamente contra uma das IAs ou visualizar duas IAs a jogar com interface gráfica, é necessário editar o bloco if __name__ == "__main__": no final do ficheiro Connect4Game.py e substituir o código de testes pela chamada normal do jogo:

if __name__ == "__main__":
    game = Connect4Game()
    
    # Exemplo: Humano vs Minimax (profundidade 4)
    p1 = HumanPlayer(piece=1)
    p2 = MinimaxAIPlayer(piece=2, depth=4)
    
    game.run_game(p1, p2, headless=False)

Em seguida, executar o ficheiro:

python Connect4Game.py

---

## Algoritmos e Implementação

### Minimax (Poda Alfa-Beta)

A IA Minimax explora a árvore de jogo até uma profundidade (depth) configurável. Para avaliar nós folha não-terminais, utiliza uma função de avaliação heurística que analisa as janelas (linhas, colunas e diagonais) ativas no tabuleiro e atribui pontuações baseadas em:
- Peças seguidas a favor (com prioridade máxima para a vitória imediata).
- Ameaças iminentes do adversário (para efeitos de classificação de bloqueio defensivo).

### MCTS (Monte Carlo Tree Search)

A IA MCTS toma as suas decisões através da simulação do jogo até ao fim, iterando num processo contínuo de Seleção, Expansão, Simulação e Retropropagação. O tempo de raciocínio do MCTS pode ser ajustado modificando o número de iterações na sua instanciação.