import pygame, sys
from Checkers.constants import WIDTH, HEIGHT, CELL_SIZE, BOARD
from Checkers.board import Board
from Checkers.antAndspider import Spider, Ant
import Checkers.GameEngine as eng

FPS = 50
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("spider game")


def main():
    running = True
    clock = pygame.time.Clock()  # to make sure that the game runs in consistent time on different computers
    ant = Ant()
    spider = Spider()
    board = Board()
    gs = eng.GameState()
    pygame.display.update()
    eve = ""
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or gs.exitGame:
                running = False  
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    sys.exit()
                elif event.key == pygame.K_b:
                    print("breadth")
                    eve = "breadth"
                elif event.key == pygame.K_d:
                    print("depth")
                    eve = "depth"
                elif event.key == pygame.K_a:
                    print("A*")
                    eve = "A*"
                elif event.key == pygame.K_1:
                    print("first heuristec func")
                    eve = "first"
                elif event.key == pygame.K_2:
                    print("second heuristec func")
                    eve = "second"
                if gs.spiderMove:
                    if event.key == pygame.K_SPACE:
                        if eve == "breadth":
                            # print(gs.breadth_first_search(spider, ant))
                            move = eng.Move(spider, gs.breadth_first_search(spider, ant))
                            gs.make_spider_move(screen, move, spider, ant)
                        elif eve == "depth":
                            # print(gs.depth_first_search(spider, ant))
                            move = eng.Move(spider, gs.depth_first_search(spider, ant))
                            gs.make_spider_move(screen, move, spider, ant)
                        elif eve == "A*":
                            move = eng.Move(spider, gs.AStare(spider, ant))
                            gs.make_spider_move(screen, move, spider, ant)
                        # move = eng.Move(sp id  er)
                        # gs.make_spider_mo ve(screen, move, spider)
            #             (3, 6): (5, 5), (4, 7): (5, 5), (6, 7): (5, 5), (7, 6): (5, 5), (7, 4): (5, 5), (6, 3): (5, 5), (4, 3): (5, 5), (3, 4): (5, 5), (2, 8): (4, 7), (3, 9): (4, 7), (5, 9): (4, 7), (6, 8): (4, 7), (6, 6): (4, 7), (3, 5): (4, 7), (2, 6): (4, 7), (4, 8): (6, 7), (7, 9): (6, 7), (8, 8): (6, 7), (8, 6): (6, 7), (7, 5): (6, 7), (4, 6): (6, 7), (5, 7): (7, 6), (9, 5): (7, 4), (4, 4): (6, 3), (2, 4): (4, 3), (1, 5): (3, 4), (0, 9): (2, 8), (1, 10): (3, 9), (3, 10): (5, 9), (4, 9): (6, 8), (5, 8): (6, 6), (1, 6): (3, 5), (0, 7): (2, 6), (2, 9): (4, 8), (5, 10): (7, 9), (6, 9): (8, 8), (7, 8): (8, 6), (5, 6): (7, 5)}
            if not gs.spiderMove:
                gs.make_ant_move(screen, ant, spider)
                # for i in BOARD:
                #     print(i)
                gs.spiderMove = not gs.spiderMove
            if eve:
                board.draw_grid(screen)
                board.create_spdr_ant_pos(screen, spider, ant)
                gs.spider_won(spider, ant)

        pygame.display.update()
    pygame.quit()


main()
