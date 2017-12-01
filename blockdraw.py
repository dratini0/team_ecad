#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import namedtuple
from io import StringIO
from itertools import product
from sys import argv

from PIL import Image

Alphabet = namedtuple("Alphabet", ["width", "height", "letters"])

BRAILLE_ORIGIN = ord("⠀")
BRAILLE_DIMENSIONS = '⠁⠈⠂⠐⠄⠠⡀⢀'
BRAILLE_TO_COMBINE = [(0, ord(dimension) - BRAILLE_ORIGIN) for dimension in BRAILLE_DIMENSIONS]
BRAILLE_INDICES = list(sum(i) + BRAILLE_ORIGIN for i in product(*BRAILLE_TO_COMBINE))
BRAILLE_ALPHABET = "".join(map(chr, BRAILLE_INDICES))

BRAILLE = Alphabet(2, 4, BRAILLE_ALPHABET)

def load_image(filename):

    alphabet = BRAILLE

    image = Image.open(filename)
    image = image.convert("L")
    threshold = 128

    result = StringIO()

    for tileY in range(0, image.height, alphabet.height):
        for tileX in range(0, image.width, alphabet.width):
            index = 0
            for y in range(alphabet.height):
                for x in range(alphabet.width):
                    index <<= 1
                    if tileX + x < image.width and \
                    tileY + y < image.height and \
                    image.getpixel((tileX + x, tileY + y)) <= threshold:
                        index += 1
            result.write(alphabet.letters[index])
        result.write("\n")
    return len(range(0, image.width, alphabet.width)), len(range(0, image.height, alphabet.height)), result.getvalue()[:-1]

if __name__ == "__main__":
    print(load_image(argv[1])[2])
