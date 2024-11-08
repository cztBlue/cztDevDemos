import gvar
from gfunc import init_game
from Game import Game

if __name__ == "__main__":
    init = init_game()
    gvar.gGame = Game(init[0], init[1])
    gvar.gGame.start()