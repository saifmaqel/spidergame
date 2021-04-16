import pygame
from .constants import LIGHT_WIGHT, WIGHT, ROWS, COLS, CELL_SIZE, HEIGHT, WIDTH, BOARD
import time
from queue import PriorityQueue


class GameState:
    def __init__(self):
        self.board = BOARD
        self.spiderMove = True
        self.exitGame = False
        self.validRowMoves = [-2, -1, 1, 2, 2, 1, -1, -2]
        self.validColMoves = [1, 2, 2, 1, -1, -2, -2, -1]

    ######################################## make spider move on the BOARD and on the GUI takes screen obj MOVE obj
    # spider obj and ant obj##################

    def make_spider_move(self, screen, move, spider, ant):
        if spider.body.x >= 12 or spider.body.x < 0 or spider.body.y >= 12 or spider.body.y < 0:
            self.exitGame = True
            print("ant wins")
        else:
            self.board[int(move.startRow)][int(move.startCol)] = "--"
            spider.body.x = move.endRow
            spider.body.y = move.endCol
            self.board[int(spider.body.x)][int(spider.body.y)] = "S"
            spider.draw_spider(screen)
            if self.spider_won(spider, ant):
                print("spider won")
                time.sleep(1)
                self.exitGame = True
            else:
                self.spiderMove = not self.spiderMove

    ################################################ test if the spider ate the ant ###############################################33
    def spider_won(self, spider, ant):
        if spider.body.x == ant.pos.x and spider.body.y == ant.pos.y:
            return True

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ calculate the shortest path between the spider and the ant
    # and returns the next step for the spider $$$$$$$$$$$$$$$$$$$$$$$$$$$$
    def breadth_first_search(self, spider, ant):
        start_x, start_y, end_x, end_y = int(spider.body.x), int(spider.body.y), int(ant.pos.x), int(ant.pos.y)
        open_d, closed, visited = [(start_x, start_y)], [], [(start_x, start_y)]
        node_parent = {(start_x, start_y): None}
        reached_goal = False
        while open_d:
            current_x, current_y = open_d.pop(0)
            if (current_x, current_y) == (end_x, end_y) :
                reached_goal = True
                break
            for i in range(8):
                valid_x, valid_y = current_x + self.validRowMoves[i], current_y + self.validColMoves[i]
                closed.append((current_x, current_y))
                if (valid_x, valid_y) in open_d or (valid_x, valid_y) in closed or not self.is_valid(valid_x, valid_y):
                    continue
                visited.append((valid_x, valid_y))
                node_parent[(valid_x, valid_y)] = (current_x, current_y)
                open_d.append((valid_x, valid_y))
                if (valid_x, valid_y) == (end_x, end_y) or reached_goal:
                    reached_goal = True
                    break
        if reached_goal:
            goal_parent = node_parent[end_x, end_y]
            path = [(end_x, end_y)]
            while goal_parent is not None :
                path.append(goal_parent)
                goal_parent = node_parent[goal_parent]
            print(path)
            print(node_parent)
            return path[-2]
        else:
            return -1

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ calculate the shortest path between the spider and the ant
    # and returns the next step for the spider $$$$$$$$$$$$$$$$$$$$$$$$$$$$

    def depth_first_search(self, spider, ant):
        start_x, start_y, end_x, end_y = int(spider.body.x), int(spider.body.y), int(ant.pos.x), int(ant.pos.y)
        open_d, closed, visited = [(start_x, start_y)], [], [(start_x, start_y)]
        node_parent = {(start_x, start_y): None}
        reached_goal = False
        while open_d:
            current_x, current_y = open_d.pop()
            if (current_x, current_y) == (end_x, end_y) :
                reached_goal = True
                break
            for i in range(8):
                valid_x, valid_y = current_x + self.validRowMoves[i], current_y + self.validColMoves[i]
                closed.append((current_x, current_y))
                if (valid_x, valid_y) in open_d or (valid_x, valid_y) in closed or not self.is_valid(valid_x, valid_y):
                    continue
                visited.append((valid_x, valid_y))
                node_parent[(valid_x, valid_y)] = (current_x, current_y)
                open_d.insert(1, (valid_x, valid_y))
                if (valid_x, valid_y) == (end_x, end_y) or reached_goal:
                    reached_goal = True
                    break
                #     c_node = (3, 4)
                # open = [ (5,5), (3,6), (4,7), (6,7), (7, 6), (7, 4), (6, 3), (4, 3), (3, 4)  ]
                # node_parent={ (5,5): None, (3,6): (5,5), (4,7): (5,5), (6,7): (5,5), (7, 6): (5,5), (7, 4): (5, 5), (6, 3): (5, 5), (4, 3): (5, 5),
                #               (3, 4): (5, 5),
        if reached_goal:
            goal_parent = node_parent[end_x, end_y]
            path = [(end_x, end_y)]
            while goal_parent is not None :
                path.append(goal_parent)
                # print((spider.body.x, spider.body.y), node_parent[(ant.pos.x, ant.pos.y)])
                # print(node_parent)
                goal_parent = node_parent[goal_parent]
            print(path)
            print(node_parent)
            return path[-2]
        else:
            return -1

    ##################### add every nodes parent to path list ###########################
    def goal_path(self, prev_graph, a_x, a_y):
        path = []
        goal_path_x, goal_path_y = prev_graph[a_x][a_y][0], prev_graph[a_x][a_y][1]
        goal_index = (a_x, a_y)
        path.append(goal_index)
        while goal_path_x != -1:
            path.append((goal_path_x, goal_path_y))
            goal_path_x, goal_path_y = prev_graph[goal_path_x][goal_path_y][0], prev_graph[goal_path_x][goal_path_y][1]
        return path

    ##################### check ###########################
    def is_valid(self, x, y):
        if x >= 12 or x < 0 or y >= 12 or y < 0:
            return False
        return True

    def AStare(self, spider, ant):
        start_node = s_x, s_y = spider.body.x, spider.body.y
        goal_node = a_x, a_y = ant.pos.x, ant.pos.y
        reached_goal = False
        closed = []
        open_set = PriorityQueue()
        open_set.put((
            self.first_heuristc_func(start_node, start_node) + self.first_heuristc_func(start_node, goal_node),
            start_node, None))
        explored = {start_node: 0.0}
        node_parent = {start_node: None}
        while not open_set.empty() and not reached_goal:
            current_node = open_set.get()
            closed.append(current_node)
            for i in range(8):
                neighbor_x, neighbor_y = current_node[1][0] + self.validRowMoves[i], current_node[1][1] + \
                                         self.validColMoves[i]
                neighbor = (neighbor_x, neighbor_y)
                if neighbor_x >= 12 or neighbor_x < 0 or neighbor_y >= 12 or neighbor_y < 0 or neighbor in explored or neighbor in closed:
                    continue
                # make sure
                g, h = self.first_heuristc_func(start_node, neighbor) + self.first_heuristc_func(start_node,
                                                                                                 current_node[1]) \
                    , self.first_heuristc_func(neighbor, goal_node)
                f = g + h
                if neighbor not in explored or (neighbor in explored and g < explored[neighbor]):
                    open_set.put((f, neighbor, current_node[1]))
                    explored[neighbor] = g  # make sure h or g######################33
                    node_parent[neighbor] = current_node[1]
                elif neighbor in explored and g > explored[neighbor]:
                    continue
                if neighbor == goal_node:
                    reached_goal = True
                    break
            if reached_goal:
                break
        if reached_goal:
            parent = node_parent[goal_node]
            path = []
            while parent != (s_x, s_y):
                path.append(parent)
                parent = node_parent[parent]
            if path:
                return path[-1]
            else:
                return a_x, a_y
        if not reached_goal:
            return None

    ######### first heuristc function that takes tow points and returns the distince based on knight moves  ###########
    def first_heuristc_func(self, spider, ant):
        s_x, s_y, a_x, a_y = int(spider[0]), int(spider[1]), int(ant[0]), int(ant[1])
        if (abs(a_x - s_x) == 2 and abs(a_y - s_y) == 1) or (abs(a_x - s_x) == 1 and abs(a_y - s_y) == 2):
            return 1
        elif (abs(a_x - s_x) == 1 and abs(a_y - s_y) == 1) or (abs(a_x - s_x) == 1 and abs(a_y - s_y) == 1):
            return 2
        elif (abs(a_x - s_x) == 0 and abs(a_y - s_y) == 1) or (abs(a_x - s_x) == 1 and abs(a_y - s_y) == 0):
            return 3
        elif abs(a_x - s_x) == 2 and abs(a_y - s_y) == 2:
            return 4
        elif (abs(a_x - s_x) % 2 == 0 and abs(a_x - s_x) % 2 == 0) or (
                abs(a_x - s_x) % 2 != 0 and abs(a_x - s_x) % 2 != 0):
            return 2
        elif (abs(a_x - s_x) % 2 == 0 and abs(a_x - s_x) % 2 != 0) or (
                abs(a_x - s_x) % 2 != 0 and abs(a_x - s_x) % 2 == 0):
            return 3
        elif ((abs(a_x - s_x) % 2 == 0 and abs(a_x - s_x) % 2 == 0) or (
                abs(a_x - s_x) % 2 != 0 and abs(a_x - s_x) % 2 != 0)) and abs(a_x - s_x) + abs(a_y - s_y) > 5:
            return 4
        elif (abs(a_x - s_x) % 2 == 0 and abs(a_x - s_x) % 2 != 0) or (
                abs(a_x - s_x) % 2 != 0 and abs(a_x - s_x) % 2 == 0) and abs(a_x - s_x) + abs(a_y - s_y) >= 11:
            return 5
        else:
            return 0

    ######################################## make ant move on the BOARD and on the GUI takes screen obj MOVE obj
    # and ant obj##################
    def make_ant_move(self, screen, ant, spider):
        prev_pos = ant.pos
        ant.get_random_pos()
        if ant.pos.x > ROWS - 1 or ant.pos.x < 0 or ant.pos.y > COLS - 1 or ant.pos.y < 0:
            self.exitGame = True
        elif ant.pos.x == spider.body.x and ant.pos.y == spider.body.y:
            print("spider won")
        else:
            self.board[int(prev_pos.x)][int(prev_pos.y)] = "--"
            self.board[int(ant.pos.x)][int(ant.pos.y)] = "A"
            ant.draw_ant(screen)


########## MOVE class that takes start point and next step point and set start point to spider and end point to next step ###########
class Move:
    def __init__(self, spider, next_step):
        self.board = BOARD
        self.startRow = spider.body.x
        self.startCol = spider.body.y
        # spider.move_diraction(next_step)
        self.endRow = next_step[0]
        self.endCol = next_step[1]
        self.pieceMoved = self.board[int(self.startRow)][int(self.startCol)]
        self.piececaptured = self.board[int(self.endRow)][int(self.endCol)]
