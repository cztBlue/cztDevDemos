import global_res.gvar as gvar
from global_res.gfunc import init_game,getch
from game import Game

if __name__ == "__main__":
    init = init_game()
    gvar.gGame = Game(gvar.gWorld, gvar.gPlayer)
    gvar.gGame.start()