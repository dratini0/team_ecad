#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image
from sys import argv, exit
from collections import namedtuple
from itertools import product

image = Image.open(argv[1])

Alphabet = namedtuple("Alphabet", ["width", "height", "letters"])

braille_origin = ord("⠀")
braille_dimensions = '⠁⠈⠂⠐⠄⠠⡀⢀'
braille_to_combine = [(0, ord(dimension) - braille_origin) for dimension in braille_dimensions]
braille_indices = list(sum(i) + braille_origin for i in product(*braille_to_combine))
braille_alphabet = "".join(map(chr, braille_indices))

braille = Alphabet(2, 4, braille_alphabet)

blockdraw_alphabet = " ▗▖▄▝▐▞▟▘▚▌▙▀▜▛█"
blockdraw = Alphabet(2, 2, blockdraw_alphabet)

half_blockdraw_alphabet = " ▄▀█"
half_blockdraw = Alphabet(1, 2, half_blockdraw_alphabet)

alphabet = braille

image = image.convert("L")
threshold = 128

for tileY in range(0, image.height, alphabet.height):
    for tileX in range(0, image.width, alphabet.width):
        index = 0
        for y in range(alphabet.height):
            for x in range(alphabet.width):
                index <<= 1
                if tileX + x < image.width and \
                   tileY + y < image.height and \
                   image.getpixel((tileX + x, tileY + y)) > threshold:
                    index += 1
        print(alphabet.letters[index], end="")
    print()

