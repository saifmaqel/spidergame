from .constants import LIGHT_WIGHT, WIGHT, ROWS, COLS, CELL_SIZE, HEIGHT, WIDTH, BOARD
import time, random
from queue import PriorityQueue
from collections import deque


def is_valid(x, y):
    if x >= 12 or x < 0 or y >= 12 or y < 0:
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


class GameState:
    def __init__(self, spider, ant):
        self.spider = spider
        self.ant = ant
        self.board = BOARD
        self.spiderMove = True
        self.exitGame = False
        self.validRowMoves = [-2, -1, 1, 2, 2, 1, -1, -2]
        self.validColMoves = [1, 2, 2, 1, -1, -2, -2, -1]

    ######################################## make spider move on the BOARD and on the GUI takes screen obj MOVE obj
    # spider obj and ant obj##################

    def make_spider_move(self, screen, move):

        if self.spider.body.x >= 12 or self.spider.body.x < 0 or self.spider.body.y >= 12 or self.spider.body.y < 0:
            self.exitGame = True
            print("ant wins")
        else:
            self.board[int(move.startRow)][int(move.startCol)] = "--"
            self.spider.body.x = move.endRow
            self.spider.body.y = move.endCol
            self.board[int(self.spider.body.x)][int(self.spider.body.y)] = "S"
            self.spider.draw_spider(screen)
            if self.spider_won():
                print("spider won")
                time.sleep(1)
                self.exitGame = True
            else:
                self.spiderMove = not self.spiderMove

    ######################################## make ant move on the BOARD and on the GUI takes screen obj MOVE obj
    # and ant obj##################
    def make_ant_move(self, screen):
        prev_pos = self.ant.pos
        self.ant.get_random_pos()
        if self.ant.pos.x > ROWS - 1 or self.ant.pos.x < 0 or self.ant.pos.y > COLS - 1 or self.ant.pos.y < 0:
            self.exitGame = True
        elif self.ant.pos.x == self.spider.body.x and self.ant.pos.y == self.spider.body.y:
            print("spider won")
        else:
            self.board[int(prev_pos.x)][int(prev_pos.y)] = "--"
            self.board[int(self.ant.pos.x)][int(self.ant.pos.y)] = "A"
            self.ant.draw_ant(screen)

    ################################################ test if the spider ate the ant ###############################################33
    def spider_won(self):
        if self.spider.body.x == self.ant.pos.x and self.spider.body.y == self.ant.pos.y:
            return True

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ calculate the shortest path between the spider and the ant
    # and returns the next step for the spider $$$$$$$$$$$$$$$$$$$$$$$$$$$$ @@@@@@@@ fix
    def breadth_first_search(self):
        start_x, start_y, end_x, end_y = int(self.spider.body.x), int(self.spider.body.y), int(self.ant.pos.x), int(
            self.ant.pos.y)
        open_d = deque()
        open_d.appendleft((start_x, start_y))
        visited, node_parent, reached_goal = [(start_x, start_y)], [[(-1, -1) for _ in range(COLS)] for _ in range(ROWS)], False
        while open_d:
            current_x, current_y = current_node = open_d.pop()
            if (current_x, current_y) == (end_x, end_y):
                reached_goal = True
                break
            for i in range(8):
                valid_x, valid_y = current_x + self.validRowMoves[i], current_y + self.validColMoves[i]
                if (valid_x, valid_y) in open_d or (valid_x, valid_y) in visited or not is_valid(valid_x, valid_y):
                    continue
                visited.append((valid_x, valid_y))
                node_parent[valid_x][valid_y] = (current_x, current_y)
                open_d.appendleft((valid_x, valid_y))
        if reached_goal:
            goal_parent, path = node_parent[end_x][end_y], [(end_x, end_y)]
            while goal_parent != (-1, -1):
                path.append(goal_parent)
                goal_parent = node_parent[goal_parent[0]][goal_parent[1]]
            print(path)
            for i in node_parent:
                print(i)
            return path[-2]
        else:
            return -1
