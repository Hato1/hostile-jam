import random

import pygame as pg
from pygame.locals import *
import os

from helper import DATA_DIR, load_image, LOADED_IMAGES

from entity import Entity
from shop import Shop


class World:

    def __init__(self, dims, player_sprite):

        self.dims = dims

        # Delete me self.dir_dict = {pg.K_w: 0, pg.K_s: 0, pg.K_a: 0, pg.K_d: 0}
        self.dir_dict = {'UP': 0, 'DOWN': 0, 'LEFT': 0, 'RIGHT': 0}

        self.entity_list = []

        self.world = pg.Surface(self.dims)
        self.world = self.world.convert()
        self.draw_world()
        self.shop = Shop()
        self.money = 100
        self.font_money = pg.font.Font(os.path.join(DATA_DIR, 'Amatic-Bold.ttf'), 36 * 3)
        self.text_money = self.font_money.render(str(self.money), 1, (220, 20, 60))
        # self.add_entity(player_path, (self.world.get_width()/2, self.world.get_height()/2), None, name='Player')
        self.player = Entity(player_sprite, (self.world.get_width()/2, self.world.get_height()/2), type='Player')
        # self.player = self.entity_list[0]

        # spawns 5 coin entities
        for i in range(5):
            self.gen_coin()

        self.gen_enemy()

        self.allsprites = pg.sprite.RenderPlain(self.entity_list)
        self.update_world()

    def update_world(self):
        self.world.fill((100, 250, 250))

        self.update_money()
        self.player.move()
        for entity in self.entity_list:
            entity.move()

        self.allsprites.update()

        for sprite in self.allsprites:
            sprite.draw(self.world, self.dims)
        self.update_shop()
        self.world.blit(self.player.get_sprite(), self.player.get_position())
        pg.display.flip()

    def add_entity(self, sprite, pos, ai=None, name="Entity", speed=5):
        entity = Entity(sprite, pos, ai=ai, type=name, speed=speed)
        self.entity_list.append(entity)
        return entity

    def get_surface(self):
        return self.world

    def draw_world(self):
        self.world.fill((100, 250, 250))

    def update_money(self):
        self.text_money = self.font_money.render(str(self.money), 1, (220, 20, 60))

        textpos_money = self.text_money.get_rect(centerx=self.world.get_width() / 2,
                                                 centery=self.world.get_height() / 4)

        self.world.blit(self.text_money, textpos_money)

    def update_shop(self):
        self.shop.draw_shop()

        self.world.blit(self.shop.shop_surface, (0, 0))

    def check_alive(self):
        return self.player.is_alive()

    def move(self):
        for entity in self.entity_list:
            x = self.dir_dict['LEFT'] - self.dir_dict['RIGHT']
            y = self.dir_dict['UP'] - self.dir_dict['DOWN']
            norm = (x**2 + y**2)**0.5
            if norm == 0:
                return
            x = x / norm
            y = y / norm
            # print(x,y)
            entity.slide([x, y])

    def gen_coin(self):
        coin_path = "sprite_coin"
        side = random.randint(0,3)
        if side == 0:
            self.add_entity(coin_path, ((random.randint(1, self.dims[0])), 1), name='Coin')
        elif side == 1:
            self.add_entity(coin_path, (self.dims[0], (random.randint(1, self.dims[1]))), name='Coin')
        elif side == 2:
            self.add_entity(coin_path, ((random.randint(1, self.dims[0])), self.dims[1]), name='Coin')
        else:
            self.add_entity(coin_path, (1, (random.randint(1, self.dims[1]))), name='Coin')

    def gen_enemy(self):
        enemy = self.add_entity("sprite_coin", ((random.randint(1, self.dims[0])), (random.randint(1, self.dims[0]))), ai='follow', speed=0.5, name='Enemy')
        enemy.update_info({'target': self.player, 'me': enemy})

    def set_dir(self, key, val):
        self.dir_dict[key] = val

    def get_dir(self):
        return self.dir_dict



