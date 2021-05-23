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
speed,score,level,temp = 400,0,1,0
#load hình
picture = []
for n in range(8):
    picture.append(pygame.transform.scale(pygame.image.load(f'T_{n}.gif'),(distance,distance)))
screen = pygame.display.set_mode([width,height])
pygame.display.set_caption('Game xếp hình')
#tạo các sự kiện
tetroromino_down = pygame.USEREVENT + 1
pygame.time.set_timer(tetroromino_down,speed)
#gameover = pygame.USEREVENT +3
#textfinish = pygame.font.SysFont("comicsansms", 40).render("Game Over!",True,(255, 255, 255))
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
    def gameover():
	    for column in range(columns):			
		    if (grid[column]) > 0:
			    screen.fill((0,0,0))		
			    screen.blit(textfinish,(width//2 - text.get_width()//2,80))    
def ObjectOnGridline():
    for n, color in enumerate(character.tetro):
        if color > 0:
            grid[(character.row + n // 4)*columns+(character.column + n % 4)] = color
def deleteRow():
    fullrows = 0
    for row in range(rows):
        for column in range(columns):
            if grid[row*columns+column] == 0: # in ra một cột có 30 số 0 ???#kiểm tra nếu dòng nào có ô rỗng thì bỏ qua
                break
        else:
            del grid[row*columns:row*columns+columns]
            grid[0:0] = [0]*columns  # trả về []
            fullrows += 1
    return fullrows**2*100 #xóa 1 dòng đc 100đ,xóa n dòng cùng lúc đc n^2*100đ
character = tetroromino(random.choice(tetrorominos))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == tetroromino_down:
            if not character.update(1,0):
                ObjectOnGridline()
                score += deleteRow()
                if score>0 and score//500 >= level and temp != score:
                    speed = int(speed * 0.5)
                    pygame.time.set_timer(tetroromino_down,speed)
                    level = score//500 +1
                    temp = score 
                character = tetroromino(random.choice(tetrorominos))
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
    text = pygame.font.SysFont('Time new roman',40).render(f'{score:,}',False,(255, 255, 255)) #in ra màn hình điểm
    screen.blit(text,(width//2- text.get_width()//2,5)) #vị trí của điểm
    text = pygame.font.SysFont('Time new roman',40).render(f'Level:{level:,}',False,(255, 255, 255)) #Level
    screen.blit(text,(width//2- text.get_width()//2,40)) #vị trí level
    
    for n,color in enumerate(grid): #duyệt từ ô trong lưới nếu có màu thì tính tọa độ
        if color > 0:
            x= n%columns*distance
            y= n//columns*distance
            screen.blit(picture[color],(x,y))
    pygame.display.update()
pygame.quit()