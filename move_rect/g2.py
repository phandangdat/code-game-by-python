import pygame

pygame.init()

red = (255,0,0)
blue = (0,0,255)
gray = (128,128,128)

size = 600,500
width, height = size

screen = pygame.display.set_mode(size)

rect = pygame.Rect(50,60,80,80)
v = [2,2]

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    rect.move_ip(v)

    if rect.left < 0 or rect.right > width:
        v[0] *= -1
    elif rect.top < 0 or rect.bottom > height:
        v[1] *= -1

    screen.fill(gray)
    pygame.draw.rect(screen, red, rect)
    pygame.display.flip()
pygame.quit()