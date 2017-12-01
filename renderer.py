#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import curses
from curses import wrapper
from time import sleep
import procedural_generation

testMap = ["vvvv", "wwww", "wffw", "wffd", "wwww"]
TILE_MAP = {
    "v": "v",
    "w": "#",
    "f": ".",
    "d": "?",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
}

class Renderer(object):
    def __init__(self):
        self.debugfile = open("debugfile", "w")

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

if __name__ == "__main__":
    Renderer().run()
