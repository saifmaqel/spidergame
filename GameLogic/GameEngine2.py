from .constants import LIGHT_WIGHT, WIGHT, ROWS, COLS, CELL_SIZE, HEIGHT, WIDTH, BOARD
import time, math
from queue import PriorityQueue
from collections import deque


def is_valid(x, y):
    if x >= ROWS or x < 0 or y >= COLS or y < 0:
        return False
    return True


########## MOVE class that takes start point and next step point and set start point to spider and end point to next step ###########
class Move:
    def __init__(self, spider, next_step):
        self.board = BOARD
        self.startRow = spider.body.x
        self.startCol = spider.body.y
        self.endRow = next_step[0]
        self.endCol = next_step[1]
        self.pieceMoved = self.board[int(self.startRow)][int(self.startCol)]
        self.piececaptured = self.board[int(self.endRow)][int(self.endCol)]


def first_heuristc_func(start, goal):
    s_x, s_y, a_x, a_y = int(start[0]), int(start[1]), int(goal[0]), int(goal[1])
    if (abs(a_x - s_x) == 2 and abs(a_y - s_y) == 1) or (abs(a_x - s_x) == 1 and abs(a_y - s_y) == 2):
        return 1
    elif (abs(a_x - s_x) == 1 and abs(a_y - s_y) == 1) or (abs(a_x - s_x) == 1 and abs(a_y - s_y) == 1):
        return 2
    elif (abs(a_x - s_x) == 0 and abs(a_y - s_y) == 1) or (abs(a_x - s_x) == 1 and abs(a_y - s_y) == 0):
        return 3
    elif abs(a_x - s_x) == 2 and abs(a_y - s_y) == 2:
        return 4
    else:
        return math.sqrt(math.pow(abs(a_x - s_x), 2) + math.pow(abs(a_y - s_y), 2))


def second_heuristc_func(start, goal):
    s_x, s_y, a_x, a_y = int(start[0]), int(start[1]), int(goal[0]), int(goal[1])
    cost = 0
    if (abs(a_x - s_x) == 2 and abs(a_y - s_y) == 1) or (abs(a_x - s_x) == 1 and abs(a_y - s_y) == 2):
        cost = 1
    elif (abs(a_x - s_x) == 1 and abs(a_y - s_y) == 1) or (abs(a_x - s_x) == 1 and abs(a_y - s_y) == 1):
        cost = 2
    elif (abs(a_x - s_x) == 0 and abs(a_y - s_y) == 1) or (abs(a_x - s_x) == 1 and abs(a_y - s_y) == 0):
        cost = 3
    elif abs(a_x - s_x) == 2 and abs(a_y - s_y) == 2:
        cost = 4
    elif (abs(a_x - s_x) % 2 == 0 and abs(a_y - s_y) % 2 == 0) or (
            abs(a_x - s_x) % 2 != 0 and abs(a_y - s_y) % 2 != 0):
        cost = 2 + max(abs(a_x - s_x), abs(a_y - s_y))
    elif (abs(a_x - s_x) % 2 == 0 and abs(a_x - s_x) % 2 != 0) or (
            abs(a_x - s_x) % 2 != 0 and abs(a_x - s_x) % 2 == 0):
        cost = 3 + max(abs(a_x - s_x), abs(a_y - s_y))
    return cost


class GameState:
    def __init__(self, spider, ant):
        self.spider = spider
        self.ant = ant
        self.board = BOARD
        self.spiderMove = True
        self.AntIsDead = False
        self.AntWon = False
        self.validRowMoves = [-2, -1, 1, 2, 2, 1, -1, -2]
        self.validColMoves = [1, 2, 2, 1, -1, -2, -2, -1]
        self.old = (-1, -1)

    ######################################## make spider move on the BOARD and on the GUI takes screen obj MOVE obj
    # spider obj and ant obj##################

    def make_spider_move(self, screen, move):
        if self.spider.body.x >= ROWS or self.spider.body.x < 0 or self.spider.body.y >= COLS or self.spider.body.y < 0:
            self.AntWon = True
            print("ant wins")
        else:
            self.board[int(move.startRow)][int(move.startCol)] = "--"
            self.spider.body.x, self.spider.body.y = move.endRow, move.endCol
            self.board[int(self.spider.body.x)][int(self.spider.body.y)] = "S"
            self.spider.draw_spider()
            if self.spider_won():
                time.sleep(1)
                self.AntIsDead = True
                # self.board[int(self.ant.pos.x)][int(self.ant.pos.y)] = "--"
                # self.ant.draw_ant()
                # self.board[int(self.ant.pos.x)][int(self.ant.pos.y)] = "A"
            else:
                self.spiderMove = not self.spiderMove

    ######################################## make ant move on the BOARD and on the GUI takes screen obj MOVE obj
    # and ant obj##################
    def make_ant_move(self, screen):
        prev_pos = self.ant.pos
        self.ant.move_to_left()
        if self.ant.pos.x > ROWS - 1 or self.ant.pos.x < 0 or self.ant.pos.y > COLS - 1 or self.ant.pos.y < 0:
            self.AntWon = True
        elif self.spider_won():
            self.AntIsDead = True
            print("spider won")
        else:
            self.board[int(prev_pos.x)][int(prev_pos.y)] = "--"
            self.board[int(self.ant.pos.x)][int(self.ant.pos.y)] = "A"
            self.ant.draw_ant()

    ################################################ test if the spider ate the ant ###############################################33
    def spider_won(self):
        if self.spider.body.x == self.ant.pos.x and self.spider.body.y == self.ant.pos.y:
            return True

    def get_next_move(self, node_parent):
        x, y = self.ant.get_pos()
        path, parent = [(x, y)], node_parent[(x, y)]
        while parent != self.spider.get_pos():
            path.append(parent)
            parent = node_parent[(parent[0], parent[1])]
        self.old = path[-1]
        return path[-1]
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ calculate the shortest path between the spider and the ant
    # and returns the next step for the spider $$$$$$$$$$$$$$$$$$$$$$$$$$$$ @@@@@@@@ fix

    def breadth_first_search(self):
        queue, visited, reached_goal, node_parent = [], [], False, {(self.spider.body.x, self.spider.body.y): None}
        body = self.spider.get_pos()
        queue.append((body[0], body[1]))
        while queue:
            current = queue.pop(0)
            visited.append(current)
            if (current[0], current[1]) == (self.ant.get_pos()):
                return node_parent
            for i in range(len(self.validRowMoves)):
                neighbor_x, neighbor_y = current[0] + self.validRowMoves[i], current[1] + self.validColMoves[i]
                if (neighbor_x, neighbor_y) in visited or not is_valid(neighbor_x, neighbor_y):
                    continue
                queue.append((neighbor_x, neighbor_y))
                node_parent[(neighbor_x, neighbor_y)] = current
        return False

    def depth_first_search(self):
        stack, visited, reached_goal, node_parent = [], [], False, {(self.spider.body.x, self.spider.body.y): None}
        body = self.spider.get_pos()
        stack.append((body[0], body[1]))
        while stack:
            current = stack.pop()
            visited.append(current)
            for i in range(len(self.validRowMoves)):
                neighbor_x, neighbor_y = current[0] + self.validRowMoves[i], current[1] + self.validColMoves[i]
                if (neighbor_x, neighbor_y) not in visited and is_valid(neighbor_x, neighbor_y):
                    stack.append((neighbor_x, neighbor_y))
                    node_parent[(neighbor_x, neighbor_y)] = current
                if (neighbor_y, neighbor_x) == (self.ant.get_pos()):
                    return node_parent
        return False

    def AStar(self):
        G_values, H_values = self.get_exact_distance(self.spider.body, self.ant.pos), self.get_exact_distance(
            self.ant.pos, self.spider.body)
        start_node = s_x, s_y = self.spider.get_pos()
        goal_node = a_x, a_y = self.ant.get_pos()
        reached_goal = False
        open_set = PriorityQueue()
        open_set.put((G_values[s_x][s_y] + H_values[s_x][s_y], start_node, None))
        explored, node_parent, closed = {start_node: 0.0}, {start_node: None}, []
        while not open_set.empty():
            current_node = open_set.get()
            closed.append(current_node[1])
            for i in range(8):
                neighbor_x, neighbor_y = current_node[1][0] + self.validRowMoves[i], current_node[1][1] + \
                                         self.validColMoves[i]
                neighbor = (neighbor_x, neighbor_y)
                if not is_valid(neighbor_x, neighbor_y) or neighbor in closed:
                    continue
                g, h = G_values[neighbor_x][neighbor_y] + G_values[current_node[1][0]][current_node[1][1]], \
                       H_values[neighbor_x][neighbor_y]
                f = g + h
                if neighbor in explored and explored[neighbor] < g:
                    continue
                else:
                    open_set.put((g + h, neighbor, current_node[1]))
                    explored[neighbor] = g
                    node_parent[neighbor] = current_node[1]
                if neighbor == goal_node:
                    return node_parent

    def get_exact_distance(self, start, goal):
        start_x, start_y, end_x, end_y = int(start.x), int(start.y), int(goal.x), int(goal.y)
        q_G = deque()
        q_G.appendleft((start_x, start_y))
        node_distance, visited_G = [[0 for _ in range(COLS)] for _ in range(ROWS)], [[-1 for _ in range(COLS)] for _ in
                                                                                     range(ROWS)]
        visited_G[start_x][start_y] = 1
        while q_G:
            current_x_g, current_y_g = q_G.pop()
            for i in range(8):
                valid_x_g, valid_y_g = int(current_x_g) + self.validRowMoves[i], int(current_y_g) + self.validColMoves[
                    i]
                if not is_valid(valid_x_g, valid_y_g) or visited_G[valid_x_g][valid_y_g] == 1:
                    continue
                    ############################### visited importan for depth
                node_distance[valid_x_g][valid_y_g] = node_distance[current_x_g][current_y_g] + 1
                visited_G[valid_x_g][valid_y_g] = 1
                q_G.appendleft((valid_x_g, valid_y_g))
                if (valid_x_g, valid_y_g) == (end_x, end_y):
                    break
        print("s")
        for i in node_distance:
            print(i)
        return node_distance

    def best_first_search(self, heuristic):
        start_node = s_x, s_y = int(self.spider.body.x), int(self.spider.body.y)
        goal_node = a_x, a_y = int(self.ant.pos.x), int(self.ant.pos.y)
        closed, reached_goal = [], False
        open_set = PriorityQueue()
        if heuristic == "first":
            h = first_heuristc_func(start_node, goal_node)
        else:
            h = second_heuristc_func(start_node, goal_node)
        open_set.put((h, start_node, None))
        explored, node_parent = {start_node: 0.0}, {start_node: None}
        while not open_set.empty():
            current_node = open_set.get()
            closed.append(current_node)
            for i in range(8):
                neighbor_x, neighbor_y = current_node[1][0] + self.validRowMoves[i], current_node[1][1] + \
                                         self.validColMoves[i]
                neighbor = (neighbor_x, neighbor_y)
                if not is_valid(neighbor_x, neighbor_y) or neighbor in explored or neighbor in closed:
                    continue
                if heuristic == "first":
                    h = first_heuristc_func(neighbor, goal_node)
                elif heuristic == "second":
                    h = second_heuristc_func(neighbor, goal_node)
                else:
                    h = (first_heuristc_func(neighbor, goal_node) + second_heuristc_func(neighbor, goal_node)) / 2
                if neighbor not in explored:
                    open_set.put((h, neighbor, current_node[1]))
                    explored[neighbor] = h  # make sure h or g######################33
                    node_parent[neighbor] = current_node[1]
                if neighbor == goal_node:
                    return node_parent
        return False
