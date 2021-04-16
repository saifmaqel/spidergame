import pygame, random
from pygame.math import Vector2
from .constants import CELL_SIZE, ROWS, COLS


# def name_piece(screen, name, x, y):
#     font = pygame.font.SysFont('freesansbold.ttf', 32)
#     p_name=font.render(name, True, (0,0,0))
#     screen.blit(p_name,(x,y))

class Spider:
    def __init__(self):
        self.body = Vector2(5, 5)

    def draw_spider(self, screen):
        x_pos = int(self.body.x * CELL_SIZE) + 1
        y_pos = int(self.body.y * CELL_SIZE) + 1
        spider_block = pygame.Rect(y_pos, x_pos, CELL_SIZE - 1, CELL_SIZE - 1)
        pygame.draw.rect(screen, (30, 100, 160), spider_block)
        # name_piece(screen, "S", x_pos, y_pos)

    def move_diraction(self, x, y,search_type):
        validRowMoves1 = [-2, -1, 1, 2, 2, 1, -1, -2]
        validColMoves2 = [1, 2, 2, 1, -1, -2, -2, -1]

        # random_spider_move = random.randint(0, len(validRowMoves1)-1)
        # # print(random_spider_move)
        # xx = self.body.x + validRowMoves1[random_spider_move]
        # yy = self.body.y + validColMoves2[random_spider_move]
        # self.body = Vector2(xx, yy)
        # if direction == "3":
        #     new_x_move = self.body.x + validRowMoves1[0]
        #     new_y_move = self.body.y + validColMoves2[0]
        #     self.body = Vector2(new_x_move, new_y_move)
        # elif direction == "down":
        #     new_x_move = self.body.x + 1
        #     self.body = Vector2(new_x_move, self.body.y)
        # elif direction == "right":
        #     new_y_move = self.body.y + 1
        #     self.body = Vector2(self.body.x, new_y_move)
        # else:
        #     new_y_move = self.body.y - 1
        #     self.body = Vector2(self.body.x, new_y_move)


class Ant:
    def __init__(self):
        self.x = random.randint(0, ROWS - 1)
        self.y = random.randint(0, COLS - 1)
        self.pos = Vector2(self.x, self.y)

    def draw_ant(self, screen):
        ant_block = pygame.Rect(int(self.pos.y * CELL_SIZE) + 1, int(self.pos.x * CELL_SIZE) + 1, CELL_SIZE - 1, CELL_SIZE - 1)
        pygame.draw.rect(screen, (190, 10, 20), ant_block)

    def get_random_pos(self):
        D = ['up', 'down', 'left', 'right']
        d = random.choice(D)
        if d == "up":
            self.y = self.y - 1
            self.pos = Vector2(self.x, self.y)
        elif d == "down":
            self.y = self.y + 1
            self.pos = Vector2(self.x, self.y)
        elif d == "right":
            self.x = self.x + 1
            self.pos = Vector2(self.x, self.y)
        else:
            self.x = self.x - 1
            self.pos = Vector2(self.x, self.y)


 # path=[]
 #        goal = node_parent[(a_x, a_y)]
 #        while goal.get("cell") != 'S':
 #            goal_parent = goal.get("key")
 #            path.append(goal_parent)
 #            goal = node_parent[(goal_parent[0], goal_parent[1])]