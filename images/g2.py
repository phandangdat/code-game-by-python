import pygame

pygame.init()

size = 600,500
w,h = size

screen = pygame.display.set_mode(size)

red = (255,0,0)
green = (0,255,0)
gray = (128,128,128)

img = pygame.image.load("bird.png")
img.convert()

rect = img.get_rect()
rect.center = w//2,h//2

running = True
moving = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if rect.collidepoint(event.pos):
                moving = True
        elif event.type == pygame.MOUSEBUTTONUP:
            moving = False
        elif event.type == pygame.MOUSEMOTION and moving:
            rect.move_ip(event.rel)
    screen.fill(gray)
    screen.blit(img,rect)
    pygame.draw.rect(screen,red,rect,1)
    pygame.display.update()
pygame.quit()