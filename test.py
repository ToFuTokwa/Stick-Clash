import pygame
pygame.init()

background_size = pygame.display.set_mode((1920,1097))
pygame.display.set_caption("Stick Clash")

bg = pygame.image.load('Game/bg1.jpg')
idle = pygame.image.load('Game/standing.png')
walkright = [pygame.image.load(f'Game/R{i}E.png') for i in range(1, 10)]
walkleft = [pygame.image.load(f'Game/L{i}E.png') for i in range(1, 10)]

clock = pygame.time.Clock()

# FOR MOVING
x = 200
y = 850
width = 64
height = 64
speed = 16

# 🔧 FIXED: Added missing state variables
left = False  # 🔧 FIXED
right = False  # 🔧 FIXED
walkcount = 0  # 🔧 FIXED

# FOR DASH
dash_speed = 32
dash_cooldown = 300
last_dash_time = 0

# FOR JUMP
is_jump = False
y_velocity = 0
jump_force = -32      # Higher negative = faster jump up
gravity = 3          # Higher = faster fall
ground_y = 850

def redraw_game_window():
    global walkcount
    background_size.blit(bg, (0, 0))

    if walkcount + 1 >= 27:
        walkcount = 0

    if left:
        background_size.blit(walkleft[walkcount // 3], (x, y))
        walkcount += 1
    elif right:
        background_size.blit(walkright[walkcount // 3], (x, y))  # 🔧 FIXED: Was using walkleft
        walkcount += 1
    else:
        background_size.blit(idle, (x, y))

    pygame.display.update()

run = True
while run:

    redraw_game_window()
    clock.tick(27)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # 🔧 FIXED: Moved MOUSEBUTTONDOWN check inside event loop
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            if current_time - last_dash_time >= dash_cooldown:
                if keys[pygame.K_a]:
                    x -= dash_speed
                elif keys[pygame.K_d]:
                    x += dash_speed
                last_dash_time = current_time
                right = False
                left = False
                walkcount = 0

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        x -= speed
        left = True
        right = False
    elif keys[pygame.K_d]:  # 🔧 FIXED: use elif so you don’t set both to True
        x += speed
        right = True
        left = False
    else:
        right = False  # 🔧 FIXED: reset if no key pressed
        left = False

    if not is_jump and keys[pygame.K_SPACE]:
        is_jump = True
        y_velocity = jump_force
        right = False
        left = False
        walkcount = 0

    if is_jump:
        y_velocity += gravity
        y += y_velocity

        if y >= ground_y:
            y = ground_y
            y_velocity = 0
            is_jump = False

    # Keep within screen bounds
    x = max(0, min(x, 1920 - width))
    y = max(0, min(y, 10997 - height))

# 🔧 FIXED: Removed unnecessary redraw after quitting
pygame.quit()
