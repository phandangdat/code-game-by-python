import pygame
import random
import time
import math
from dataclasses import dataclass
pygame.init()
width, columns, rows = 300, 15, 30
distance = width // columns
height = distance * rows
grid = [0] * columns * rows
picture = [] # 
for n in range(8):
    picture.append(pygame.transform.scale(pygame.image.load(f'T_{n}.gif'), (distance, distance)))
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption('Tetris Game')
tetrorominos = [[0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], #O
               [0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0], #I
               [0, 0, 3, 0, 0, 0, 3, 0, 0, 3, 3, 0, 0, 0, 0, 0], #J
               [0, 4, 0, 0, 0, 4, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0], #L
               [0, 5, 5, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #S
               [6, 6, 0, 0, 0, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0], #Z
               [0, 0, 0, 0, 7, 7, 7, 0, 0, 7, 0, 0, 0, 0, 0, 0]] #T

#tạo lớp và định nghĩa các hàm
@dataclass
class tetroromino():
    tetro: list
    row: int = 0 # vị trí xuất hiện đầu tiên
    column: int = 5

    def show(self):
        for n, color in enumerate(self.tetro): # enumerate tạo list dạng liệt kê
            if color > 0:
                x = (self.column + n % 4) * distance
                y = (self.row + n // 4) * distance
                screen.blit(picture[color], (x, y))
    def update(self, r, c):
        self.row += r
        self.column += c
character = tetroromino(random.choice(tetrorominos))
running = True
#clock = pg.time.Clock()
while running:
    #clock.tick(80)
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    character.update(1,0)
    screen.fill((128,128,128))
    character.show()
    for n, color in enumerate(grid):
        if color > 0:
            x = n % columns * distance
            y = n // columns * distance
            screen.blit(picture[color], (x, y))
  
    pygame.display.flip()

pygame.quit()
        
            
