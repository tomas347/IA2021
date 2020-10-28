# ricochet_robots.py: Template para implementação do 1º projeto de Inteligência Artificial 2020/2021.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 90784 Tomás Leite de Castro
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
        return self.id<other.id


class Board:
    """ Representacao interna de um tabuleiro de Ricochet Robots. """
    def __init__(self, size):
        #Nesta representacao a cor dos robots e representada em numeros em vez de letras. 
        #Robot Y == 1 , G == 2 , B == 3 , R == 4 respetivamente
        self.robot_matrix = np.zeros((size, size))
        self.y_matrix = np.zeros((size + 1, size + 1))
        self.x_matrix = np.zeros((size + 1, size + 1))
        self._compute_restrictions(size)
        self.size = size
        self.goal_x = 0
        self.goal_y = 0
        self.goal_color = 0

    def _add_robot(self, robot_number, x, y):
        self.robot_matrix[x][y] = robot_number

    def _get_robot_number(self, robot):
        if robot == 'Y':
            return 1
        if robot == 'G':
            return 2
        if robot == 'B':
            return 3
        if robot == 'R':
            return 4

    def _add_goal(self, goal_color, x ,y):
        self.goal_x = x
        self.goal_y = y
        self.goal_color = goal_color

    
    def is_goal(self):
        return self.goal_color == self.robot_matrix[self.goal_x][self.goal_y]


    def _add_restriction(self, x, y, barrier):
        if barrier == 'l':
            self.y_matrix[x][y] = 1
            return
        if barrier == 'r':
            self.y_matrix[x][y + 1] = 1
            return
        if barrier == 'u':
            self.x_matrix[x][y] = 1
            return
        if barrier == 'd':
            self.x_matrix[x + 1][y] = 1
            return

    def _compute_restrictions(self, size):
        n = size - 1
        for i in range(0,size):
            self._add_restriction(0, i, 'u')
            self._add_restriction(i, 0, 'l')
            self._add_restriction(n, i, 'd')
            self._add_restriction(i, n, 'r')
    
    def get_nearest_obstacle(self, robot: str, direction: str):
        position = self.robot_position(robot, 0)
        flag = 1
        if direction == 'l':
            # Vamos verificar se existem obstaculos fixos a esquerda percorrendo a lista de obstaculos no eixo Y
            for i in range (position[1], 0, -1):
                if self.y_matrix[position[0]][i]:
                    flag = 0
                    position_limit = (position[0], i)
                    break
            # Ja temos o nosso limite maximo percorrivel ate batermos num obstaculo no eixo Y
            # Vamos verificar se existe algum robot no caminho previamente encontrado
            if flag:
                return position
            for i in range (position[1] - 1, position_limit[1], -1):
                if self.robot_matrix[position[0]][i]:
                    # Encontramos um robot entre a nossa posicao atual e a parede, portanto estas coordenadas sao o nosso limite no eixo Y
                    position_limit = (position[0], i + 1)
                    return position_limit
            # Nao existe nenhum robot no nosso caminho portanto vamos retornar a posicao obtida no primeiro loop
            return position_limit
        
        if direction == 'r':
            for i in range (position[1] + 1, self.size + 1):
                if self.y_matrix[position[0]][i]:
                    flag = 0
                    position_limit = (position[0], i - 1)
                    break
            if flag:
                return position
            for i in range (position[1] + 1, position_limit[1] + 1):
                if self.robot_matrix[position[0]][i]:
                    position_limit = (position[0], i - 1)
                    return position_limit
            return position_limit
        
        if direction == 'u':
            for i in range (position[0], 0, -1):
                if self.x_matrix[i][position[1]]:
                    flag = 0
                    position_limit = (i, position[1])
                    break
            if flag:
                return position
            for i in range (position[0] - 1, position_limit[0], -1):
                if self.robot_matrix[i][position[1]]:
                    position_limit = (i + 1, position[1])
                    return position_limit
            return position_limit

        if direction == 'd':
            for i in range (position[0] + 1, self.size + 1):
                if self.x_matrix[i][position[1]]:
                    flag = 0
                    position_limit = (i - 1, position[1])
                    break
            if flag:
                return position
            for i in range(position[0] + 1, position_limit[0] + 1):
                if self.robot_matrix[i][position[1]]:
                    position_limit = (i - 1, position[1])
                    return position_limit
            return position_limit
            

            


    def robot_position(self, robot: str, offset = 1):
        """ Devolve a posição atual do robô passado como argumento. """
        if (robot == 'Y'):
            for i in range(0, self.size):
                for j in range(0, self.size):
                    if (self.robot_matrix[i][j] == 1):
                        return (i + offset, j + offset)
        if (robot == 'G'):
            for i in range(0, self.size):
                for j in range(0, self.size):
                    if (self.robot_matrix[i][j] == 2):
                        return (i + offset, j + offset)
        if (robot == 'B'):
            for i in range(0, self.size):
                for j in range(0, self.size):
                    if (self.robot_matrix[i][j] == 3):
                        return (i + offset, j + offset)
        if (robot == 'R'):
            for i in range(0, self.size):
                for j in range(0, self.size):
                    if (self.robot_matrix[i][j] == 4):
                        return (i + offset, j + offset)




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
        b._add_robot(b._get_robot_number(parsedLine[0]), int(parsedLine[1]) - 1, int(parsedLine[2]) - 1)
    
    parsedLine = lines[5].split()
    b._add_goal(b._get_robot_number(parsedLine[0]), int(parsedLine[1]) - 1, int(parsedLine[2]) - 1)

    parsedLine = lines[6].split()
    size = int(parsedLine[0])

    for i in range(0, size):
        parsedLine = lines[i + 7].split()
        b._add_restriction(int(parsedLine[0]) - 1, int(parsedLine[1]) - 1, parsedLine[2])
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

        state.board
        pass

    def goal_test(self, state: RRState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se o alvo e o robô da
        mesma cor ocupam a mesma célula no tabuleiro. """
        
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
