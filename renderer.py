#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import curses
from curses import wrapper
from time import sleep
import procedural_generation

import blockdraw

testMap = ["vvvv", "wwww", "wffw", "wffd", "wwww"]
TILE_MAP = {
    "v": " ",
    "w": "#",
    "f": ".",
    "d": "?",
}

SELF_SPRITE = "player.pbm"
SELF_NAME = "You"

TEXTBOX_HEIGHT = 3

BATTLE_WIDTH = 80
BATTLE_HEIGHT = 24

HP_GAUGE = " -=#"
HP_GAUGE_WIDTH = 10

class Renderer(object):
    def __init__(self):
        self.debugfile = open("debugfile", "w")
        self.battle_character = None
        self.battle_character_size = (0, 0)
        self.enemy = None
        self.enemy_size = (0, 0)
        self.enemy_name = ""
        self.self_hp = 0
        self.self_max_hp = 0
        self.enemy_hp = 0
        self.enemy_max_hp = 0
        self.battlemessagebox = None

    def print(self, *parameter_list):
        print(*parameter_list, file=self.debugfile)
    def run(self):
        wrapper(self._run)

    def _run(self, stdscr):
        if curses.LINES < 24 or curses.COLS < 80:
            print("Your terminal is too small for this game. Sorry!")
            exit()
        curses.curs_set(False)
        self.stdscr = stdscr

        self.start_battle("Insect", "insect.pbm", 100, 75, 100, 65)
        self.battle_print("asd1")
        self.battle_print("asd2")
        self.battle_print("3")
        self.battle_print(self.battle_in("? "))
        sleep(1)

        procedural_generation.main(self)

    def draw_map(self, map_, position, enemies):
        self.stdscr.clear()
        self.stdscr.noutrefresh()
        display_x = curses.COLS // 2
        display_y = curses.LINES // 2
        x, y = position
        width, height = len(map_[0]), len(map_)
        mappad = curses.newpad(height, width + 1)
        mappad.addstr('\n'.join(''.join(TILE_MAP[char] for char in line) for line in map_))
        x_offset, y_offset = max(x - display_x, 0), max(y - display_y, 0)
        x_pos, y_pos = max(display_x - x, 0), max(display_y - y, 0)
        x_end = min(curses.COLS, width + x_pos)
        y_end = min(curses.LINES, height + y_pos)
        mappad.noutrefresh(y_offset, x_offset,
                       y_pos, x_pos,
                       y_end - 1, x_end - 1)
        sprite_offset_x, sprite_offset_y = display_x - x, display_y - y
        for sprite_x, sprite_y, char in enemies + [(x, y, '@')]:
            sprite_win = curses.newwin(1, 1, sprite_y + sprite_offset_y, sprite_x + sprite_offset_x)
            try:
                sprite_win.addch(ord(char))
            except curses.error:
                pass #yes.
            sprite_win.noutrefresh()
        curses.doupdate()

    def input(self):
        return self.stdscr.getkey()

    def start_battle(self, enemy_name, enemy_sprite, self_max_hp, self_hp, enemy_max_hp, enemy_hp):
        curses.newwin(BATTLE_HEIGHT, BATTLE_WIDTH, 0, 0).noutrefresh()
        self.battlemessagebox = curses.newwin(TEXTBOX_HEIGHT, BATTLE_WIDTH, BATTLE_HEIGHT - TEXTBOX_HEIGHT, 0)
        self.battlemessagebox.noutrefresh()
        self.battlemessagebox.move(2, 0)
        bc_width, bc_height, battle_character = blockdraw.load_image(SELF_SPRITE)
        self.battle_character = curses.newpad(bc_height, bc_width + 1)
        self.battle_character.addstr(battle_character)
        self.battle_character_size = (bc_width, bc_height)
        enemy_width, enemy_height, enemy = blockdraw.load_image(enemy_sprite)
        self.enemy = curses.newpad(bc_height, bc_width + 1)
        self.enemy.addstr(enemy)
        self.enemy_size = (enemy_width, enemy_height)
        self.enemy_name = enemy_name
        self.self_hp = self_hp
        self.self_max_hp = self_max_hp
        self.enemy_hp = enemy_hp
        self.enemy_max_hp = enemy_max_hp
        self.render_self()
        self.render_enemy()
        curses.doupdate()

    @staticmethod
    def draw_hp_gauge(current, max_):
        to_draw = (current * (len(HP_GAUGE) - 1) *  HP_GAUGE_WIDTH) // max_
        if to_draw == 0 and current != 0:
            return HP_GAUGE[1] + HP_GAUGE[0] * (HP_GAUGE_WIDTH - 1)
        generated = HP_GAUGE[-1] * (to_draw // (len(HP_GAUGE) - 1)) + \
                    HP_GAUGE[to_draw % (len(HP_GAUGE) - 1)] + \
                    HP_GAUGE[0] * HP_GAUGE_WIDTH
        return generated[:HP_GAUGE_WIDTH]

    def render_self(self):
        clearer = curses.newwin(
            BATTLE_HEIGHT - TEXTBOX_HEIGHT - self.battle_character_size[1],
            0,
            self.battle_character_size[1],
            self.battle_character_size[0])
        clearer.noutrefresh()
        self.battle_character.noutrefresh(
            0, 0,
            BATTLE_HEIGHT - TEXTBOX_HEIGHT - self.battle_character_size[1],
            0,
            BATTLE_HEIGHT - TEXTBOX_HEIGHT - 1,
            self.battle_character_size[0] - 1)

        infobox = curses.newwin(
            3, HP_GAUGE_WIDTH,
            BATTLE_HEIGHT - TEXTBOX_HEIGHT - self.battle_character_size[1] + 5,
            self.battle_character_size[0])
 
        info = "{}\n{}{}/{}".format(SELF_NAME, self.draw_hp_gauge(self.self_hp, self.self_max_hp), self.self_hp, self.self_max_hp)
        infobox.addstr(info)

        infobox.noutrefresh()

    def render_enemy(self):
        clearer = curses.newwin(
            self.enemy_size[1],
            self.enemy_size[0],
            0,
            BATTLE_WIDTH - self.enemy_size[0]
            )
        clearer.noutrefresh()
        self.enemy.noutrefresh(
            0, 0,
            0,
            BATTLE_WIDTH - self.enemy_size[0],
            self.enemy_size[1] - 1,
            BATTLE_WIDTH - 1)

        infobox = curses.newwin(
            3, HP_GAUGE_WIDTH,
            5,
            BATTLE_WIDTH - self.enemy_size[0] - HP_GAUGE_WIDTH)

        info = "{}\n{}{}/{}".format(self.enemy_name, self.draw_hp_gauge(self.enemy_hp, self.enemy_max_hp), self.enemy_hp, self.enemy_max_hp)
        infobox.addstr(info)

        infobox.noutrefresh()

    def damage_enemy(self, new_hp):
        self.enemy_hp = new_hp
        self.render_enemy()
        curses.doupdate()

    def damage_self(self, new_hp):
        self.self_hp = new_hp
        self.render_self()
        curses.doupdate()

    def help_enemy(self, new_hp):
        self.enemy_hp = new_hp
        self.render_enemy()
        curses.doupdate()

    def heal_self(self, new_hp):
        self.self_hp = new_hp
        self.render_self()
        curses.doupdate()

    def die_enemy(self, new_hp):
        pass

    def die_self(self, new_hp):
        pass



    def battle_print(self, message):
        self.battlemessagebox.move(0, 0)
        self.battlemessagebox.deleteln()
        self.battlemessagebox.move(2, 0)
        self.battlemessagebox.addstr(message)
        self.battlemessagebox.refresh()

    def battle_in(self, prompt):
        self.battlemessagebox.move(0, 0)
        self.battlemessagebox.deleteln()
        self.battlemessagebox.move(2, 0)
        self.battlemessagebox.addstr(prompt)
        self.battlemessagebox.refresh()
        curses.curs_set(1)
        curses.echo()
        result = self.battlemessagebox.getstr()
        curses.noecho()
        curses.curs_set(0)
        return result

if __name__ == "__main__":
    Renderer().run()
