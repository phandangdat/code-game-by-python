import pygame
import random
import time
import math
from dataclasses import dataclass
pygame.init()
width,columns,rows = 300,15,30
distance = width // columns #chiều dài 1 ô
height = distance * rows
grid = [0]*columns*rows #lưới chứa hình tetroromino
speed = 500
#load hình
picture = []
for n in range(8):
    picture.append(pygame.transform.scale(pygame.image.load(f'T_{n}.gif'),(distance,distance)))
screen = pygame.display.set_mode([width,height])
pygame.display.set_caption('Game xếp hình')
#tạo các sự kiện rơi xuống
tetroromino_down = pygame.USEREVENT + 1
pygame.time.set_timer(tetroromino_down,speed)
speedup = pygame.USEREVENT +2
pygame.time.set_timer(speedup,5000)
pygame.key.set_repeat(1,300) #độ nhạy nút

#tetroromino của các chữ cái O,I,J,L,S,Z,T
tetrorominos =[[0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], #O
               [0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0], #I
               [0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 3, 0, 0, 0, 0, 0], #J
               [0, 0, 4, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0], #L
               [0, 5, 5, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #S
               [6, 6, 0, 0, 0, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0], #Z
               [0, 0, 0, 0, 7, 7, 7, 0, 0, 7, 0, 0, 0, 0, 0, 0]] #T
@dataclass
class tetroromino():
    tetro : tetrorominos 
    row : int = 0 #tọa độ rơi xuống lúc đầu
    column : int = 5

    def show(self):
        for n, color in enumerate(self.tetro):
            if color > 0:
                x = (self.column + n % 4) * distance
                y = (self.row + n // 4)* distance
                screen.blit(picture[color],(x,y))
    def check(self,r,c): #hàm kiểm tra để không vượt quá màn hình
        for n,color in enumerate(self.tetro):
            if color > 0:
                ro = r + n//4
                co = c + n%4
                if co < 0 or ro >= rows or co >= columns or grid[ro * columns + co]>0:
                    return False
        return True
    def update(self,r,c):
        if self.check(self.row + r,self.column+c):
            self.row += r
            self.column += c
            return True
        return False
    def turn(self): #hàm xoay
        savetetro = self.tetro.copy()
        for n ,color in enumerate(savetetro):
            self.tetro[(2-(n % 4))*4+(n // 4)] = color
        if not self.check(self.row,self.column):
            self.tetro = savetetro.copy()
character = tetroromino(random.choice(tetrorominos))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == tetroromino_down:
            character.update(1,0)
        if event.type == speedup: #sự kiện time tăng dần
            speed = int(speed * 0.8)
            pygame.time.set_timer(tetroromino_down,speed)
        if event.type == pygame.KEYDOWN: #sự kiện bấm nút
            if event.key == pygame.K_a:
                character.update(0,-1)
            if event.key == pygame.K_d:
                character.update(0,1)
            if event.key == pygame.K_s:
                character.update(1,0)
            if event.key == pygame.K_SPACE:
                character.turn()
    screen.fill((160,160,160))
    character.show()
    for n,color in enumerate(grid):
        if color > 0:
            x= n%column*distance
            y= n//column*distance
            screen.blit(picture[color],(x,y))
    pygame.display.update()
pygame.quit()