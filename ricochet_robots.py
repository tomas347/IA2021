# ricochet_robots.py: Template para implementação do 1º projeto de Inteligência Artificial 2020/2021.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 90784 Tomás Leite de Castro
# 00000 Nome2

from search import Problem, Node, astar_search, breadth_first_tree_search, \
    depth_first_tree_search, greedy_search, depth_first_graph_search, breadth_first_graph_search
import sys
import copy
import numpy as np


class RRState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = RRState.state_id
        RRState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id


def new_copy(obj):
    class Empty(obj.__class__):
        def __init__(self): pass
    newcopy = Empty()
    newcopy.__class__ = obj.__class__
    return newcopy

class Board:
    """ Representacao interna de um tabuleiro de Ricochet Robots. """
    def __init__(self, size):
        #Nesta representacao a cor dos robots e representada em numeros em vez de letras. 
        #Robot Y == 1 , G == 2 , B == 3 , R == 4 respetivamente
        self.y_matrix = np.zeros((size + 1, size + 1))
        self.x_matrix = np.zeros((size + 1, size + 1))
        self._compute_restrictions(size)
        self.size = size
        self.goal_x = 0
        self.goal_y = 0
        self.goal_robot = ''
        self.robot_dict = {}

    def __copy__(self):
        newcopy = new_copy(self)
        newcopy.y_matrix = self.y_matrix
        newcopy.x_matrix = self.x_matrix
        newcopy.size = self.size
        newcopy.goal_x = self.goal_x
        newcopy.goal_y = self.goal_y
        newcopy.goal_robot = self.goal_robot
        newcopy.robot_dict = self.robot_dict.copy()
        return newcopy


    def _add_robot(self, robot, x, y):
        self.robot_dict[robot] = (x, y)


    def _move_robot(self, robot, x, y):
        self.robot_dict[robot] = (x, y)


    def _add_goal(self, robot, x ,y):
        self.goal_x = x
        self.goal_y = y
        self.goal_robot = robot
    

    def get_goal_position(self):
        return (self.goal_x, self.goal_y)


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


    def test_action(self, action):
        pos = self.robot_position(action[0], 0)
        if action[1] == 'l':
            return not(self.y_matrix[pos[0]][pos[1]] or pos in self.robot_dict.values())
        if action[1] == 'r':
            return not(self.y_matrix[pos[0]][pos[1] + 1] or pos in self.robot_dict.values())
        if action[1] == 'u':
            return not(self.x_matrix[pos[0]][pos[1]] or pos in self.robot_dict.values())
        if action[1] == 'd':
            return not(self.x_matrix[pos[0] + 1][pos[1]] or pos in self.robot_dict.values())


    def _compute_restrictions(self, size):
        n = size - 1
        for i in range(0,size):
            self._add_restriction(0, i, 'u')
            self._add_restriction(i, 0, 'l')
            self._add_restriction(n, i, 'd')
            self._add_restriction(i, n, 'r')
    
    def get_actions(self, robot):
        pos = self.robot_position(robot, 0)
        actions = []
        if not(self.x_matrix[pos[0]][pos[1]] or (pos[0] - 1, pos[1]) in self.robot_dict.values()):
            actions.append((robot, 'u'))
        if not(self.y_matrix[pos[0]][pos[1]] or (pos[0], pos[1] - 1) in self.robot_dict.values()):
            actions.append((robot, 'l'))
        if not(self.x_matrix[pos[0] + 1][pos[1]] or (pos[0] + 1, pos[1]) in self.robot_dict.values()):
            actions.append((robot, 'd'))
        if not(self.y_matrix[pos[0]][pos[1] + 1] or (pos[0], pos[1] + 1) in self.robot_dict.values()):
            actions.append((robot, 'r'))
        return actions

    def robot_position(self, robot: str, offset = 1):
        """ Devolve a posição atual do robô passado como argumento. """
        if not(offset):
            return self.robot_dict[robot]
        else:
            return (self.robot_dict[robot][0] + 1, self.robot_dict[robot][1] + 1)
    
    def goal_test(self):
        return self.get_goal_position() == self.robot_dict[self.goal_robot]


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
        b._add_robot(parsedLine[0], int(parsedLine[1]) - 1, int(parsedLine[2]) - 1)
    
    parsedLine = lines[5].split()
    b._add_goal(parsedLine[0], int(parsedLine[1]) - 1, int(parsedLine[2]) - 1)

    parsedLine = lines[6].split()
    size = int(parsedLine[0])

    for i in range(0, size):
        parsedLine = lines[i + 7].split()
        b._add_restriction(int(parsedLine[0]) - 1, int(parsedLine[1]) - 1, parsedLine[2])
    return b

class RicochetRobots(Problem):
    def __init__(self, board: Board, state: RRState = None):
        """ O construtor especifica o estado inicial. """
        if state == None:
            self.initial = RRState(board)
        else:
            self.initial = state


    def actions(self, state: RRState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        actions = []
        actions += state.board.get_actions('Y')
        actions += state.board.get_actions('R')
        actions += state.board.get_actions('G')
        actions += state.board.get_actions('B')
        return actions
        

    def result(self, state: RRState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação retornada deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state). """
        # TOGO in if statement below: action in self.actions(state)

        if action in self.actions(state):
            position = state.board.robot_position(action[0], 0)
            if action[1] == 'l':
                # Vamos verificar se existem obstaculos fixos a esquerda percorrendo a lista de obstaculos no eixo Y
                for i in range (position[1], -1, -1):
                    if state.board.y_matrix[position[0]][i]:
                        position_limit = (position[0], i)
                        break
                # Ja temos o nosso limite maximo percorrivel ate batermos num obstaculo no eixo Y
                # Vamos verificar se existe algum robot no caminho previamente encontrado
                for i in state.board.robot_dict.values():
                    if i[0] == position_limit[0] and i[1] >= position_limit[1] and i[1] < position[1]:
                        position_limit = (i[0], i[1] + 1)

                # Nao existe nenhum robot no nosso caminho portanto vamos retornar a posicao obtida no primeiro loop
            
            if action[1] == 'r':
                for i in range (position[1] + 1, state.board.size + 1):
                    if state.board.y_matrix[position[0]][i]:
                        position_limit = (position[0], i - 1)
                        break
                
                for i in state.board.robot_dict.values():
                    if i[0] == position_limit[0] and i[1] <= position_limit[1] and i[1] > position[1]:
                        position_limit = (i[0], i[1] - 1)

            
            if action[1] == 'u':
                for i in range (position[0], -1, -1):
                    if state.board.x_matrix[i][position[1]]:
                        position_limit = (i, position[1])
                        break
                
                for i in state.board.robot_dict.values():
                    if i[1] == position_limit[1] and i[0] >= position_limit[0] and i[0] < position[0]:
                        position_limit = (i[0] + 1, i[1])


            if action[1] == 'd':
                for i in range (position[0] + 1, state.board.size + 1):
                    if state.board.x_matrix[i][position[1]]:
                        position_limit = (i - 1, position[1])
                        break

                for i in state.board.robot_dict.values():
                    if i[1] == position_limit[1] and i[0] <= position_limit[0] and i[0] > position[0]:
                        position_limit = (i[0] - 1, i[1])

            new_state = RRState(copy.copy(state.board))
            new_state.board._move_robot(action[0], position_limit[0], position_limit[1])
            return new_state

        new_state = RRState(copy.copy(state.board))
        return state


        
    def goal_test(self, state: RRState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se o alvo e o robô da
        mesma cor ocupam a mesma célula no tabuleiro. """

        return state.board.goal_test()
        

    def h(self, node: Node):
        robot_pos = node.state.board.robot_position(node.state.board.goal_robot)
        if node.state.board.goal_test():
            return 0
        if node.state.board.goal_x == robot_pos[0] or node.state.board.goal_y == robot_pos[1]:
            return 1
        return 2

if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro de input de sys.argv[1],
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    board = parse_instance(sys.argv[1])
    initial_state = RRState(board)
    problem = RicochetRobots(board, initial_state)
    finish_node = astar_search(problem)
    sol = finish_node.solution()
    print(len(sol))
    for i in sol:
        print(i[0] + ' ' + i[1])
