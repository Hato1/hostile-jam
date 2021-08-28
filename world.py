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

        self.coin_list = []
        self.enemy_list = []
        self.allsprites = pg.sprite.RenderPlain()

        self.world = pg.Surface(self.dims)
        self.world = self.world.convert()
        self.draw_world()
        self.shop = Shop()

        self.money = 100
        self.font_money = pg.font.Font(os.path.join(DATA_DIR, 'Amatic-Bold.ttf'), 12 * 3)
        self.text_money = self.font_money.render(str(self.money), 1, (220, 20, 60))

        sand_sprite_dict = {"DOWN": 'sand'}
        self.experimental_background = Entity(sand_sprite_dict,
                                              (self.world.get_width() / 2, self.world.get_height() / 2))
        self.sprite_dict = {}
        self.create_sprite_dict(player_sprite)
        self.player = Entity(self.sprite_dict, (self.world.get_width() / 2, self.world.get_height() / 2), type='Player',
                             lives=3)
        # self.player = self.entity_list[0]
        self.gen_enemy()

        # spawns 5 coin entities
        for i in range(5):
            self.gen_coin()

        self.update_world()

    def create_sprite_dict(self, player_sprite):
        self.sprite_dict.update({"LEFT": player_sprite + "_left"})
        self.sprite_dict.update({"RIGHT": player_sprite + "_right"})
        self.sprite_dict.update({"UP": player_sprite + "_back"})
        self.sprite_dict.update({"DOWN": player_sprite + "_front"})

    def update_world(self):
        self.world.fill((100, 250, 250))
        self.experimental_background.draw(self.world, self.dims)
        self.player.move()
        for sprite in self.allsprites:
            sprite.move()

        self.allsprites.update()
        for sprite in self.allsprites:
            sprite.draw(self.world, self.dims)

        self.update_gui()
        self.world.blit(self.player.get_sprite(), self.player.get_position())
        pg.display.flip()

    def add_entity(self, sprite_dict, pos, ai=None, name="Entity", speed=5):
        entity = Entity(sprite_dict, pos, ai=ai, type=name, speed=speed)
        self.allsprites.add(entity)
        return entity

    def get_surface(self):
        return self.world

    def draw_world(self):
        self.world.fill((100, 250, 250))

    def update_gui(self):
        self.update_lives()
        self.update_shop()
        self.update_money()

    def update_money(self):
        self.text_money = self.font_money.render(str(self.money), 1, (220, 20, 60))

        textpos_money = self.text_money.get_rect(topright=((self.world.get_width()), 0))

        self.world.blit(self.text_money, textpos_money)

    def update_shop(self):
        self.shop.draw_shop()

        self.world.blit(self.shop.shop_surface, (0, 0))

    def update_lives(self):
        full_heart = LOADED_IMAGES["sprite_heart"][0]
        full_heart = pg.transform.scale(full_heart, (30, 30))
        empty_heart = LOADED_IMAGES["sprite_heart_empty"][0]
        empty_heart = pg.transform.scale(empty_heart, (30, 30))

        heart_positions = [(self.world.get_width() / 3, 0),
                           (self.world.get_width() / 3 + full_heart.get_rect().width, 0),
                           (self.world.get_width() / 3 + full_heart.get_rect().width * 2, 0)]

        counter = 0
        for heart_pos in heart_positions:
            if self.player.lives > counter:
                self.world.blit(full_heart, heart_pos)
            else:
                self.world.blit(empty_heart, heart_pos)
            counter += 1

    def check_alive(self):
        return self.player.is_alive()

    def move(self):
        x = self.dir_dict['LEFT'] - self.dir_dict['RIGHT']
        y = self.dir_dict['UP'] - self.dir_dict['DOWN']
        norm = (x ** 2 + y ** 2) ** 0.5
        if norm == 0:
            return
        x = x / norm
        y = y / norm
        for sprite in self.allsprites:
            # print(x,y)
            sprite.slide([x, y])
            self.player.set_dir([x, y])
        self.experimental_background.slide([x, y])

    def reset_coin(self, coin):
        side = random.randint(0, 3)
        if side == 0:
            coin.set_position((random.randint(1, self.dims[0])), 1)

        elif side == 1:
            coin.set_position((self.dims[0], (random.randint(1, self.dims[1]))))

        elif side == 2:
            coin.set_position(((random.randint(1, self.dims[0])), self.dims[1]))

        else:
            coin.set_position((1, (random.randint(1, self.dims[1]))))

    def gen_coin(self):
        coin_sprite_dict = {"DOWN": "sprite_coin"}
        side = random.randint(0, 3)
        if side == 0:
            coin = self.add_entity(coin_sprite_dict, ((random.randint(1, self.dims[0])), 1), name='Coin')
            self.coin_list.append(coin)
        elif side == 1:
            coin = self.add_entity(coin_sprite_dict, (self.dims[0], (random.randint(1, self.dims[1]))), name='Coin')
            self.coin_list.append(coin)
        elif side == 2:
            coin = self.add_entity(coin_sprite_dict, ((random.randint(1, self.dims[0])), self.dims[1]), name='Coin')
            self.coin_list.append(coin)
        else:
            coin = self.add_entity(coin_sprite_dict, (1, (random.randint(1, self.dims[1]))), name='Coin')
            self.coin_list.append(coin)

    def gen_enemy(self, speed=0.5):
        enemy_sprite_dict = {"DOWN": "sprite_demon_front", "UP": "sprite_demon_back", "LEFT": "sprite_demon_left",
                             "RIGHT": "sprite_demon_right"}
        enemy = self.add_entity(enemy_sprite_dict,
                                ((random.randint(1, self.dims[0])), (random.randint(1, self.dims[0]))), ai='follow',
                                speed=speed, name='Enemy')
        enemy.update_info({'target': self.player, 'me': enemy})
        self.enemy_list.append(enemy)

    def set_dir(self, key, val):
        self.dir_dict[key] = val

    def get_dir(self):
        return self.dir_dict



