import pygame as pg
from landing_page import LandingPage
from sys import exit
import game_functions as gf
from time import sleep
from stats import Stats
from scoreboard import Scoreboard
from laser import Lasers
from ship import Ship
from alien import AlienFleet
from settings import Settings
from sound import Sound
from barrier import Barrier
from vector import Vector


class Game:

    RED = (255, 0, 0)
    bg_img = pg.image.load('images/bg.jpg')

    def __init__(self):
        pg.init()

        self.settings = Settings()
        self.stats = Stats(game=self)
        self.screen = pg.display.set_mode((self.settings.screen_width,
                                           self.settings.screen_height))
        self.bg_color = self.settings.bg_color
        self.sound = Sound()
        self.sb = Scoreboard(game=self)
        pg.display.set_caption("Alien Invasion")
        self.ship = Ship(game=self)
        self.alien_fleet = AlienFleet(game=self)
        self.barrier1 = Barrier(game=self, ul=(100, 550), wh=(8, 8))
        self.barrier2 = Barrier(game=self, ul=(550, 550), wh=(8, 8))
        self.barrier3 = Barrier(game=self, ul=(1000, 550), wh=(8, 8))
        self.lasers = Lasers(game=self, owner=self.ship)
        # for ship lasers
        # self.alien_lasers = Lasers(game=self, owner=self.alien_fleet)   # for alien lasers
        self.ship.set_alien_fleet(self.alien_fleet)
        self.ship.set_lasers(self.lasers)

    def restart(self):
        if self.stats.ships_left == 0: 
          self.game_over()
        print("restarting game")
        while self.sound.busy():    # wait for explosion sound to finish
            pass
        self.lasers.empty()
        self.alien_fleet.empty()
        self.alien_fleet.create_fleet()
        self.ship.center_bottom()
        self.ship.reset_timer()
        self.barrier1.barrier_elements.empty()
        self.barrier1.create_barrier()
        self.barrier2.barrier_elements.empty()
        self.barrier2.create_barrier()
        self.barrier3.barrier_elements.empty()
        self.barrier3.create_barrier()
        self.ship.dying = False
        self.update()
        self.draw()
        sleep(0.5)

    def update(self):
        self.ship.update()
        self.alien_fleet.update()
        self.lasers.update()
        self.sb.update()
        self.barrier1.update()
        self.barrier2.update()
        self.barrier3.update()

    def draw(self):
        self.screen.fill(self.bg_color)
        self.screen.blit(Game.bg_img, (0,0))
        self.ship.draw()
        self.alien_fleet.draw()
        self.lasers.draw()
        self.sb.draw()
        self.barrier1.draw()
        self.barrier2.draw()
        self.barrier3.draw()
        pg.display.flip()


    def play(self):
        self.finished = False
        self.sound.play_bg()
        clock = pg.time.Clock()

        while not self.finished:
            self.update()
            self.draw()
            # self.screen.blit(bg_img, [0, 0])
            gf.check_events(game=self)
            clock.tick(144)
            # exits game if QUIT pressed
        self.game_over()

    def game_over(self):
      # self.sound.play_game_over()
      print('\nGAME OVER!\n\n')
      exit()    # can ask to replay here instead of exiting the game

def main():
    g = Game()
    lp = LandingPage(game=g)
    lp.show()
    g.play()


if __name__ == '__main__':
    main()
