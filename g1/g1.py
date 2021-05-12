import pygame

pygame.init()

size = 940,600

width,height = size


screen = pygame.display.set_mode(size)
#định nghĩa màu sắc cho background
sandy = (244,164,96)
red = (255,0,0)

#screen.fill(sandy)
#pygame.display.update()

#khởi tạo quả bóng
ball = pygame.image.load("ball.gif")
rect = ball.get_rect()
#khởi tạo biến tốc độ di chuyển của quả bóng
speed = [5,5]

background = sandy

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                background = sandy
            elif event.key == pygame.K_r:
                background = red
        screen.fill(background)
        pygame.display.update()

        rect = rect.move(speed)
        if rect.left < 0 or rect.right > width:
            speed[0] = - speed[0]
        if rect.top < 0 or rect.bottom > height:
            speed[1] = - speed[1]
        pygame.draw.rect(screen,red,rect,1)
    screen.blit(ball,rect)
    pygame.display.update()        
pygame.quit()