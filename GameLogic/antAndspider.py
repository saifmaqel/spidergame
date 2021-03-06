import pygame, random
from pygame.math import Vector2
from .constants import CELL_SIZE, ROWS, COLS


# def name_piece(screen, name, x, y):
#     font = pygame.font.SysFont('freesansbold.ttf', 32)
#     p_name=font.render(name, True, (0,0,0))
#     screen.blit(p_name,(x,y))

class Spider:
    def __init__(self, screen):
        self.screen = screen
        self.body = Vector2(0, 0)

    def draw_spider(self):
        x_pos = int(self.body.x * CELL_SIZE) + 1
        y_pos = int(self.body.y * CELL_SIZE) + 1
        spider_block = pygame.Rect(y_pos, x_pos, CELL_SIZE - 1, CELL_SIZE - 1)
        pygame.draw.rect(self.screen, (30, 100, 160), spider_block)
        # name_piece(screen, "S", x_pos, y_pos)

    def get_pos(self):
        return int(self.body.x), int(self.body.y)


class Ant:
    def __init__(self, screen):
        self.screen = screen
        self.x = random.randint(0, ROWS - 1)
        self.y = random.randint(0, COLS - 1)
        self.pos = Vector2(self.y, self.x)

    def get_pos(self):
        return self.pos

    def draw_ant(self):
        ant_block = pygame.Rect(int(self.pos.y * CELL_SIZE) + 1, int(self.pos.x * CELL_SIZE) + 1, CELL_SIZE - 1,
                                CELL_SIZE - 1)
        pygame.draw.rect(self.screen, (190, 10, 20), ant_block)

    def move_to_left(self):
        self.x = self.x - 1
        self.pos = Vector2(self.y, self.x)
        # D = ['up', 'down', 'left', 'right']
        # d = random.choice(D)
        # if d == "up":
        #     self.y = self.y - 1
        #     self.pos = Vector2(self.x, self.y)
        # elif d == "down":
        #     self.y = self.y + 1
        #     self.pos = Vector2(self.x, self.y)
        # elif d == "right":
        #     self.x = self.x + 1
        #     self.pos = Vector2(self.x, self.y)
        # else:
        #     self.x = self.x - 1
        #     self.pos = Vector2(self.x, self.y)

    def Ant_Died(self):
        self.x = random.randint(0, ROWS - 1)
        self.y = random.randint(0, COLS - 1)
        self.pos = Vector2(self.y, self.x)
        self.draw_ant()

