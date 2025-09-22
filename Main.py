import pygame
pygame.init()

background_size = pygame.display.set_mode((1366, 760))
pygame.display.set_caption("Stick Clash")

bg = pygame.image.load('Game/bg.jpg')

clock = pygame.time.Clock()

# FOR MOVING
x = 960
y = 540
width = 60
height = 120
speed = 30

# FOR DASH
is_Dash = False
dash_speed = 120
dash_cooldown =  300
last_dash_time = 0

def redraw_game_window():
    global walkcount
    background_size.blit(bg, (0, 0))
    pygame.draw.rect(background_size, (255,255,255),(x, y, width, height))
    pygame.display.update()

# FOR JUMP
is_jump = False
y_velocity = 0
jump_force = -100      # Higher negative = faster jump up
gravity = 10          # Higher = faster fall
ground_y = 540  

run = True
while run:
    redraw_game_window()

    pygame.time.delay(100)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        x -= speed
    if keys[pygame.K_d]:
        x += speed

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3: 
        if current_time - last_dash_time >= dash_cooldown:
            if keys[pygame.K_a]:
                x -= dash_speed
                last_dash_time = current_time
            if keys[pygame.K_d]:
                x += dash_speed
                last_dash_time = current_time
    
    if not is_jump and keys[pygame.K_SPACE]:
        is_jump = True
        y_velocity = jump_force

    if is_jump:
        y_velocity += gravity
        y += y_velocity

        if y >= ground_y:
            y = ground_y
            y_velocity = 0
            is_jump = False

    x = max(0, min(x, 1366 - width))
    y = max(0, min(y, 750 - height))

redraw_game_window()

pygame.quit()
