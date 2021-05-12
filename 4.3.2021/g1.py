import pygame
pygame.init()

screen = pygame.display.set_mode(500,600)

start = (0, 0)
size = (0, 0)
drawing = False
rect_list = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elifevent.type == MOUSEBUTTONUP:
            end = event.pos
            size = end[0]-start[0], end[1]-start[1]
            rect = pygame.Rect(start, size)
            rect_list.append(rect)
            drawing =False
    pygame.display.update()