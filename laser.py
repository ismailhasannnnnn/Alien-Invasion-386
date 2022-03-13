import pygame as pg

import alien as al
import ship
from vector import Vector
from pygame.sprite import Sprite, Group
from copy import copy
from random import randint
from sound import Sound
from settings import Settings
from timer import Timer
# from alien import Alien
# from stats import Stats


class Lasers:

    fireball_images = [pg.image.load(f'images/Fireball-{n}.png') for n in range(2)]
    fireball_alien_images = [pg.image.load(f'images/Fireball-{n}-Alien.png') for n in range(2)]

    def __init__(self, game, owner):
        self.game = game
        self.stats = game.stats
        self.settings = Settings()
        self.sound = game.sound
        self.owner = owner
        self.alien_fleet = game.alien_fleet
        self.ship = game.ship
        self.lasers = Group()
        self.barrier1 = game.barrier1
        self.barrier2 = game.barrier2
        self.barrier3 = game.barrier3
        # print('owner is ', self.owner, 'type is: ', type(self.owner))
        # print('type is alien.AlienFleet is: ', type(owner) is al.AlienFleet)

    def add(self, laser): self.lasers.add(laser)
    def empty(self): self.lasers.empty()
    def fire(self):
        if type(self.owner) is ship.Ship:
            new_laser = Laser(self.game, user=self.owner, image_list=Lasers.fireball_images)
        if type(self.owner) is al.Alien:
            new_laser = new_laser = Laser(self.game, user=self.owner, image_list=Lasers.fireball_alien_images)
        self.lasers.add(new_laser)
        snd = self.sound
        snd.play_fire_phaser() if type(self.owner) is al.Alien else snd.play_fire_photon()

    def update(self):
        for laser in self.lasers.copy():
            if laser.rect.bottom <= 0: self.lasers.remove(laser)
            if laser.rect.top >= self.settings.screen_height: self.lasers.remove(laser)

        if type(self.owner) is al.Alien:
            ship_collisions = pg.sprite.spritecollide(self.ship, self.lasers, False)
            if not self.ship.is_dying() and len(ship_collisions) > 0:
                self.ship.hit()

            barrier1_collisions = pg.sprite.groupcollide(self.barrier1.barrier_elements, self.lasers, False, True)
            for be in barrier1_collisions:
                be.hit()

            barrier2_collisions = pg.sprite.groupcollide(self.barrier2.barrier_elements, self.lasers, False, True)
            for be in barrier2_collisions:
                be.hit()

            barrier3_collisions = pg.sprite.groupcollide(self.barrier3.barrier_elements, self.lasers, False, True)
            for be in barrier3_collisions:
                be.hit()

        if type(self.owner) is ship.Ship:
            alien_collisions = pg.sprite.groupcollide(self.alien_fleet.fleet, self.lasers, False, True)
            for alien in alien_collisions:
                if not alien.dying: alien.hit()


        if self.alien_fleet.length() == 0:  
            self.stats.level_up()
            self.game.restart()
            
        for laser in self.lasers:
            laser.update()

    def draw(self):
        for laser in self.lasers:
            laser.draw()


class Laser(Sprite):
    def __init__(self, game, user, image_list):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.w, self.h = self.settings.laser_width, self.settings.laser_height
        self.user = user
        self.ship_image = pg.image.load('images/Fireball-1.png')
        self.rect = self.ship_image.get_rect()
        self.alien_image = pg.transform.rotate(pg.image.load('images/Fireball-0.png'), 180)
        self.alien_rect = self.alien_image.get_rect()
        self.image_list = image_list
        self.timer = Timer(image_list=image_list, delay=50, is_loop=True)



        # self.rect = pg.Rect(0, 0, self.w, self.h)
        self.center = Vector(self.user.rect.centerx - 13, self.user.rect.centery - 20)
        if type(self.user) is al.Alien:
            # self.center = Vector(self.user.rect.centerx - 13, self.user.rect.centery - 20)
            pg.transform.flip(self.ship_image, False, True)

        tu = 50, 255
        self.color = randint(*tu), randint(*tu), randint(*tu)
        # self.v = Vector(0, -1) * self.settings.laser_speed_factor
        if type(user) is al.Alien:
            self.v = Vector(0, 1) * self.settings.alien_laser_speed_factor
        if type(user) is ship.Ship:
            self.v = Vector(0, -1) * self.settings.ship_laser_speed_factor


    def update(self):
        self.center += self.v
        self.rect.x, self.rect.y = self.center.x, self.center.y
        # if type(self.user) is alien.AlienFleet:
        #     print(self.center.x)

    def draw(self):
        image = self.timer.image()
        rect = image.get_rect()
        rect.x, rect.y = self.rect.x, self.rect.y
        self.screen.blit(image, rect)
