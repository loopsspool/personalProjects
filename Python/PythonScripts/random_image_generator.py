#! python3

import copy
import random

def random_image():
    print('How big would you like your image? It is a square, so the value will be the width and height')
    dimension = int(input())
    columns = []
    rows = []
    symbols = ['|','_']
    for i in range(dimension):
        columns.append('')
    for i in range(dimension):
        rows.append(copy.copy(columns))

    for r in range(dimension):
        for c in range(dimension):
            rows[r][c] = random.choice(symbols)
    for r in range(dimension):
        for c in range(dimension):
            print(rows[r][c], end='  ')
        print('\n', end='')

random_image()