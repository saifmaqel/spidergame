import pygame
from .constants import LIGHT_WIGHT, WIGHT, ROWS, COLS, CELL_SIZE, HEIGHT, WIDTH, BOARD
import time, random
from queue import PriorityQueue
from collections import deque


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
    # and returns the next step for the spider $$$$$$$$$$$$$$$$$$$$$$$$$$$$ @@@@@@@@ fix
    def breadth_first_search(self, spider, ant):
        start_x, start_y, end_x, end_y = int(spider.body.x), int(spider.body.y), int(ant.pos.x), int(ant.pos.y)
        open_d = deque()
        open_d.appendleft((start_x, start_y))
        closed, visited = [], [(start_x, start_y)]
        node_parent = {(start_x, start_y): None}
        reached_goal = False
        while open_d:
            current_x, current_y = open_d.pop()
            # if (current_x, current_y) == (end_x, end_y):
            #     reached_goal = True
            #     break
            for i in range(8):
                valid_x, valid_y = current_x + self.validRowMoves[i], current_y + self.validColMoves[i]
                closed.append((current_x, current_y))
                if (valid_x, valid_y) in open_d or (valid_x, valid_y) in closed or not self.is_valid(valid_x, valid_y):
                    continue
                visited.append((valid_x, valid_y))
                node_parent[(valid_x, valid_y)] = (current_x, current_y)
                open_d.appendleft((valid_x, valid_y))
                if (valid_x, valid_y) == (end_x, end_y) or reached_goal:
                    reached_goal = True
                    break
        if reached_goal:
            goal_parent = node_parent[end_x, end_y]
            path = [(end_x, end_y)]
            while goal_parent is not None:
                path.append(goal_parent)
                goal_parent = node_parent[goal_parent]
            print(path)
            print(node_parent)
            return path[-2]
        else:
            return -1

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ calculate the shortest path between the spider and the ant
    # and returns the next step for the spider $$$$$$$$$$$$$$$$$$$$$$$$$$$$
    #
    # def dfs(self, spider, ant):
    #     start_x, start_y, end_x, end_y = int(spider.body.x), int(spider.body.y), int(ant.pos.x), int(ant.pos.y)
    #     start = (start_x, start_y)
    #     if (start_x, start_y) == (end_x, end_y):
    #         print(self.parent_node_dfs)
    #         return True
    #     # self.visited_dfs.append(start)
    #     for i in range(8):
    #         valid_x, valid_y = start_x + self.validRowMoves[i], start_y + self.validColMoves[i]
    #         if self.is_valid(valid_x, valid_y):
    #             c_node = (valid_x, valid_y)
    #             self.parent_node_dfs[c_node] = start
    #         if dfs(c_node, ant.pos)

    def depth_first_search(self, spider, ant):
        start_x, start_y, end_x, end_y = int(spider.body.x), int(spider.body.y), int(ant.pos.x), int(ant.pos.y)
        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!$$$$$$$$$$$$$$$$$$$$$$$$$
        open_d, visited = [(start_x, start_y)], [(start_x, start_y)]
        node_parent = {(start_x, start_y): None}
        reached_goal = False
        while open_d:
            current_x, current_y = open_d.pop()
            # closed.append((current_x, current_y))
            if (current_x, current_y) == (end_x, end_y):
                reached_goal = True
                break
            for i in range(8):
                valid_x, valid_y = current_x + self.validRowMoves[i], current_y + self.validColMoves[i]
                # closed.append((current_x, current_y))
                if not self.is_valid(valid_x, valid_y) or (valid_x, valid_y) in visited or (
                valid_x, valid_y) in node_parent:
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
            while goal_parent is not None:
                path.append(goal_parent)
                goal_parent = node_parent[goal_parent]
            print(path)
            print(node_parent)
            if (start_x, start_y) == path[-2]:
                print("loop")
            return path[-2]
        else:
            return -1

    ##################### add every nodes parent to path list ###########################
    # def goal_path(self, prev_graph, a_x, a_y):
    #     path = []
    #     goal_path_x, goal_path_y = prev_graph[a_x][a_y][0], prev_graph[a_x][a_y][1]
    #     goal_index = (a_x, a_y)
    #     path.append(goal_index)
    #     while goal_path_x != -1:
    #         path.append((goal_path_x, goal_path_y))
    #         goal_path_x, goal_path_y = prev_graph[goal_path_x][goal_path_y][0], prev_graph[goal_path_x][goal_path_y][1]
    #     return path

    ##################### check ###########################
    def is_valid(self, x, y):
        if x >= 12 or x < 0 or y >= 12 or y < 0:
            return False
        return True

    def AStare(self, spider, ant):
        G_values = self.get_exact_distance(spider.body, ant.pos)
        H_values = self.get_exact_distance(ant.pos, spider.body)
        F_values = [[0 for i in range(ROWS)] for i in range(COLS)]
        for i in range(ROWS):
            for j in range(COLS):
                F_values[i][j] = G_values[i][j] + H_values[i][j]
        print("%%%%%%  G values")
        for i in G_values:
            print(i)
        print("%%%%%%  H values")
        for i in H_values:
            print(i)
        print("%%%%%%  F values")
        for i in F_values:
            print(i)
        start_node = s_x, s_y = int(spider.body.x), int(spider.body.y)
        goal_node = a_x, a_y = int(ant.pos.x), int(ant.pos.y)
        closed = []
        reached_goal = False
        open_set = PriorityQueue()
        open_set.put((F_values[s_x][s_y], start_node, None))
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
                g, h = G_values[neighbor_x][neighbor_y] + G_values[current_node[1][0]][current_node[1][1]], \
                       H_values[neighbor_x][neighbor_y]
                if neighbor not in explored or (neighbor in explored and g < explored[neighbor]):
                    open_set.put((g + h, neighbor, current_node[1]))
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
                if not self.is_valid(valid_x_g, valid_y_g):
                    continue
                    ############################### visited importan for depth
                if visited_G[valid_x_g][valid_y_g] == 1:
                    continue
                node_distance[valid_x_g][valid_y_g] = node_distance[current_x_g][current_y_g] + 1
                visited_G[valid_x_g][valid_y_g] = 1
                q_G.appendleft((valid_x_g, valid_y_g))
                if (valid_x_g, valid_y_g) == (end_x, end_y):
                    break
        for i in node_distance:
            print(i)
        return node_distance

    ######### first heuristc function that takes tow points and returns the distince based on knight moves  ###########
    def first_heuristc_func(self, start, goal):
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
        elif (abs(a_x - s_x) % 2 == 0 and abs(a_x - s_x) % 2 == 0) or (
                abs(a_x - s_x) % 2 != 0 and abs(a_x - s_x) % 2 != 0):
            cost = 2
        elif (abs(a_x - s_x) % 2 == 0 and abs(a_x - s_x) % 2 != 0) or (
                abs(a_x - s_x) % 2 != 0 and abs(a_x - s_x) % 2 == 0):
            cost = 3
        elif ((abs(a_x - s_x) % 2 == 0 and abs(a_x - s_x) % 2 == 0) or (
                abs(a_x - s_x) % 2 != 0 and abs(a_x - s_x) % 2 != 0)) and abs(a_x - s_x) + abs(a_y - s_y) > 5:
            cost = 4 + (abs(a_x - s_x) + abs(a_y - s_y) / 2)
        elif (abs(a_x - s_x) % 2 == 0 and abs(a_x - s_x) % 2 != 0) or (
                abs(a_x - s_x) % 2 != 0 and abs(a_x - s_x) % 2 == 0) and abs(a_x - s_x) + abs(a_y - s_y) >= 7:
            cost = 5 + (abs(a_x - s_x) + abs(a_y - s_y) / 2)
        # elif (abs(a_x - s_x) % 2 == 0 and abs(a_x - s_x) % 2 == 0) or (
        #         abs(a_x - s_x) % 2 != 0 and abs(a_x - s_x) % 2 != 0):
        #     cost = 2
        # elif (abs(a_x - s_x) % 2 == 0 and abs(a_x - s_x) % 2 != 0) or (
        #         abs(a_x - s_x) % 2 != 0 and abs(a_x - s_x) % 2 == 0):
        #     cost = 3
        # elif ((abs(a_x - s_x) % 2 == 0 and abs(a_x - s_x) % 2 == 0) or (
        #         abs(a_x - s_x) % 2 != 0 and abs(a_x - s_x) % 2 != 0)) and abs(a_x - s_x) + abs(a_y - s_y) > 5:
        #     cost = 4
        # elif (abs(a_x - s_x) % 2 == 0 and abs(a_x - s_x) % 2 != 0) or (
        #         abs(a_x - s_x) % 2 != 0 and abs(a_x - s_x) % 2 == 0) and abs(a_x - s_x) + abs(a_y - s_y) >= 7 :
        #     cost = 5
        else:
            cost = 0
        return cost
    # شوف الفرق بين الجول و النيبور
    def best_first_search(self, spider, ant, heuristic):
        start_node = s_x, s_y = int(spider.body.x), int(spider.body.y)
        goal_node = a_x, a_y = int(ant.pos.x), int(ant.pos.y)
        reached_goal = False
        closed = []
        open_set = PriorityQueue()
        if heuristic == "first":
            h = self.first_heuristc_func(start_node, goal_node)
        else:
            h = self.second_heuristc_func(start_node, goal_node)
        open_set.put((h, start_node, None))
        explored = {start_node: 0.0}
        node_parent = {start_node: None}
        while not open_set.empty():
            current_node = open_set.get()
            closed.append(current_node)
            for i in range(8):
                neighbor_x, neighbor_y = current_node[1][0] + self.validRowMoves[i], current_node[1][1] + \
                                         self.validColMoves[i]
                neighbor = (neighbor_x, neighbor_y)
                if neighbor_x >= 12 or neighbor_x < 0 or neighbor_y >= 12 or neighbor_y < 0 or neighbor in explored or neighbor in closed:
                    continue
                if heuristic == "first":
                    h = self.first_heuristc_func(neighbor, goal_node)
                elif heuristic == "second":
                    h = self.second_heuristc_func(neighbor, goal_node)
                else:
                    h = self.second_heuristc_func(neighbor, goal_node)
                if neighbor not in explored:
                    open_set.put((h, neighbor, current_node[1]))
                    explored[neighbor] = h  # make sure h or g######################33
                    node_parent[neighbor] = current_node[1]
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

    def second_heuristc_func(self, start, goal):
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
            return abs(a_x - s_x) + abs(a_y - s_y) - 2

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
        self.endRow = next_step[0]
        self.endCol = next_step[1]
        self.pieceMoved = self.board[int(self.startRow)][int(self.startCol)]
        self.piececaptured = self.board[int(self.endRow)][int(self.endCol)]




    def AStare(self):
        G_values, H_values = self.get_exact_distance(self.spider.body, self.ant.pos), self.get_exact_distance(
            self.ant.pos, self.spider.body)
        # F_values = [[0 for i in range(ROWS)] for i in range(COLS)]
        # for i in range(ROWS):
        #     for j in range(COLS):
        #         F_values[i][j] = G_values[i][j] + H_values[i][j]
        start_node = s_x, s_y = int(self.spider.body.x), int(self.spider.body.y)
        goal_node = a_x, a_y = int(self.ant.pos.x), int(self.ant.pos.y)
        reached_goal = False
        open_set = PriorityQueue()
        open_set.put((G_values[s_x][s_y] + H_values[s_x][s_y], start_node, None))
        explored, node_parent, closed = {start_node: 0.0}, {start_node: None}, []
        while not open_set.empty() and not reached_goal:
            current_node = open_set.get()
            if current_node == goal_node:
                reached_goal = True
                break
            for i in range(8):
                neighbor_x, neighbor_y = current_node[1][0] + self.validRowMoves[i], current_node[1][1] + \
                                         self.validColMoves[i]
                neighbor = (neighbor_x, neighbor_y)
                if neighbor_x >= 12 or neighbor_x < 0 or neighbor_y >= 12 or neighbor_y < 0 or neighbor in closed:
                    continue
                g, h = G_values[neighbor_x][neighbor_y] + G_values[current_node[1][0]][current_node[1][1]], \
                       H_values[neighbor_x][neighbor_y]
                if neighbor in explored and explored[neighbor] < g:
                    continue
                elif neighbor in closed and explored[neighbor] < g:
                    continue
                else:
                    open_set.put((g + h, neighbor, current_node[1]))
                    explored[neighbor] = g  # make sure h or g######################33
                    node_parent[neighbor] = current_node[1]
                closed.append(neighbor)
                if neighbor == goal_node:
                    reached_goal = True
                    break
        if reached_goal:
            parent, path = node_parent[goal_node], []
            while parent != (s_x, s_y):
                path.append(parent)
                parent = node_parent[parent]
            if path:
                return path[-1]
            else:
                return a_x, a_y
        if not reached_goal:
            return None
