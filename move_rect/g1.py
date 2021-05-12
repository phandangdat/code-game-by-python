import pygame

pygame.init()

red = (255,0,0)
blue = (0,0,255)
gray = (128,128,128)

screen = pygame.display.set_mode((600,500))

rect = pygame.Rect(50,60,200,80)
moving = False

running = True

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
    pygame.draw.rect(screen,red,rect)
    if moving:
        pygame.draw.rect(screen,blue,rect,4)
    pygame.display.flip()
pygame.quit()