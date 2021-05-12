import pygame
from pygame.locals import *

pygame.init()

size = 600,500
w,h = size

screen = pygame.display.set_mode(size)

red = (255,0,0)
green = (0,255,0)
gray = (128,128,128)

img0 = pygame.image.load("bird.png")
img0.convert()

rect0 = img0.get_rect()
pygame.draw.rect(img0,green,rect0,1)

center = w//2,h//2
img = img0
rect = img.get_rect()
rect.center = center

angle = 0
scale = 1

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                img = pygame.transform.flip(img,True, False)
            if event.key == pygame.K_v:
                img = pygame.transform.flip(img,False, True)
    rect = img.get_rect()
    rect.center = center
    screen.fill(gray)
    screen.blit(img,rect)
    pygame.draw.rect(screen,red,rect,1)
    pygame.display.update()
pygame.quit()