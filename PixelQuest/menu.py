from settings import *
from entities.button import Button
from game import Game


def get_font(size):
    return pg.font.Font("assets/fonts/font.ttf", size)


class Menu:
    def __init__(self):
        pg.display.set_caption("Menu")
        
        self.play_button = Button(image=None, pos=(640, 250),
                                  text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

    def setup(self):
        pass

    def loop(self):
        run = True
        while run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    run = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.play_button.check_for_input(pg.mouse.get_pos()):
                        game = Game()
                        game.loop()

        SCREEN.fill(pg.Color('gray35'))

        self.play_button.change_color(pg.mouse.get_pos())
        self.play_button.update(SCREEN)

        pg.display.update()

