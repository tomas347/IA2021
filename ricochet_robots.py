# ricochet_robots.py: Template para implementação do 1º projeto de Inteligência Artificial 2020/2021.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

from search import Problem, Node, astar_search, breadth_first_tree_search, \
    depth_first_tree_search, greedy_search
import sys

import numpy as np


class RRState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = RRState.state_id
        RRState.state_id += 1

    def __lt__(self, other):
    	""" Este método é utilizado em caso de empate na gestão da lista
        de abertos nas procuras informadas. """
        #return self.id < other.id


class Board:
    """ Representacao interna de um tabuleiro de Ricochet Robots. """
    def __init__(self, size):
        self.matrix = np.zeros((size, size))
        self.restrictions = []
        self.compute_restrictions(size)
        self.size = size


    def add_robot(self, robot_number, x, y):
        self.matrix[x][y] = robot_number

    def get_robot_number(self, robot):
        if robot == 'Y':
            return 1
        if robot == 'G':
            return 2
        if robot == 'B':
            return 3
        if robot == 'R':
            return 4

    def add_goal(self, goal_color, x ,y):
        self.matrix[x][y] = goal_color
    
    def add_restriction(self, x, y, barrier):
        self.restrictions.append([x, y, barrier])

    def compute_restrictions(self, size):
        n = size - 1
        for i in range(0,size):
            self.add_restriction(0, i, 'u')
            self.add_restriction(i, 0, 'l')
            self.add_restriction(n, i, 'd')
            self.add_restriction(i, n, 'r')

    def robot_position(self, robot: str):
        """ Devolve a posição atual do robô passado como argumento. """
        if (robot == 'Y'):
            for i in range(0, self.size):
                for j in range(0, self.size):
                    if (self.matrix[i][j] == 1):
                        return (i + 1, j + 1)
        if (robot == 'G'):
            for i in range(0, self.size):
                for j in range(0, self.size):
                    if (self.matrix[i][j] == 2):
                        return (i + 1, j + 1)
        if (robot == 'B'):
            for i in range(0, self.size):
                for j in range(0, self.size):
                    if (self.matrix[i][j] == 3):
                        return (i + 1, j + 1)
        if (robot == 'R'):
            for i in range(0, self.size):
                for j in range(0, self.size):
                    if (self.matrix[i][j] == 4):
                        return (i + 1, j + 1)




def parse_instance(filename: str) -> Board:
    """ Lê o ficheiro cujo caminho é passado como argumento e retorna
    uma instância da classe Board. """
    fp = open(filename, 'r')
    lines = fp.readlines()
    fp.close()
    
    parsedLine = lines[0].split()
    size = int(parsedLine[0])
    b = Board(size)

    for i in range(0, 4):
        parsedLine = lines[i + 1].split()
        b.add_robot(b.get_robot_number(parsedLine[0]), int(parsedLine[1]) - 1, int(parsedLine[2]) - 1)
    
    parsedLine = lines[5].split()
    b.add_goal(b.get_robot_number(parsedLine[0]) + 4, int(parsedLine[1]) - 1, int(parsedLine[2]) - 1)

    parsedLine = lines[6].split()
    size = int(parsedLine[0])

    for i in range(0, size):
        parsedLine = lines[i + 7].split()
        b.add_restriction(int(parsedLine[0]) - 1, int(parsedLine[1]) - 1, parsedLine[2])
    return b



class RicochetRobots(Problem):
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        # TODO: self.initial = ...
        pass

    def actions(self, state: RRState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        # TODO
        pass

    def result(self, state: RRState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação retornada deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state). """
        # TODO
        pass

    def goal_test(self, state: RRState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se o alvo e o robô da
        mesma cor ocupam a mesma célula no tabuleiro. """
        # TODO
        pass

    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        # TODO
        pass


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro de input de sys.argv[1],
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
