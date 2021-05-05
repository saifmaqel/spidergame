import pygame, sys
from GameLogic.constants import WIDTH, HEIGHT, CELL_SIZE, BOARD
from GameLogic.board import Board
from GameLogic.antAndspider import Spider, Ant
import GameLogic.GameEngine2 as eng

FPS = 60
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("spider game")
font = pygame.font.SysFont('None', 28, bold=False, italic=False)
text_Press = font.render(" Press:", True, (200, 200, 200))
text_alg = font.render(" b : BFS,    d : DFS,    a : A*,    1 : H1,    2 : H2,    3 : H3 ", True, (200, 200, 200))

def main():
    running = True
    clock = pygame.time.Clock()  # to make sure that the game runs in consistent time on different computers
    ant = Ant()
    spider = Spider()
    board = Board()
    gs = eng.GameState(spider, ant)
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
                elif event.key == pygame.K_3:
                    print("third heuristec func")
                    eve = "third"
                if gs.spiderMove:
                    if event.key == pygame.K_SPACE:
                        if eve == "breadth" :
                            # print(gs.breadth_first_search())
                            move = eng.Move(spider, gs.breadth_first_search())
                            gs.make_spider_move(screen, move)
                        elif eve == "depth":
                            # print(gs.depth_first_search(spider, ant))
                            move = eng.Move(spider, gs.depth_first_search())
                            gs.make_spider_move(screen, move)
                        elif eve == "A*":
                            # gs.get_exact_distance(spider.body, ant.pos)
                            # gs.AStare()
                            move = eng.Move(spider, gs.AStare())
                            gs.make_spider_move(screen, move)
                        elif eve == "first":
                            #                 # print(gs.best_first_search_firstHeurestic(spider, ant))
                            move = eng.Move(spider, gs.best_first_search(eve))
                            gs.make_spider_move(screen, move)
                        elif eve == "second":
                            #                 # print(gs.second_heuristc_func(spider.body, ant.pos))
                            move = eng.Move(spider, gs.best_first_search(eve))
                            gs.make_spider_move(screen, move)
                        elif eve == "third":
                            #                 # print(gs.second_heuristc_func(spider.body, ant.pos))
                            move = eng.Move(spider, gs.best_first_search(eve))
                            gs.make_spider_move(screen, move)
            if not gs.spiderMove:
                gs.make_ant_move(screen)
                # for i in BOARD:
                #     print(i)
                gs.spiderMove = not gs.spiderMove
                if spider.body == ant.pos:
                    print('spider won')
            if eve:
                gs.spider_won()
                board.draw_grid(screen)
                board.create_spdr_ant_pos(screen, spider, ant)
            else:
                screen.blit(text_Press, (70, HEIGHT//2 - 40))
                screen.blit(text_alg, (70, HEIGHT//2 - 10))


        pygame.display.update()
    pygame.quit()


main()
