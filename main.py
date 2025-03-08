import pygame
import time
import random

pygame.init()

infoObject = pygame.display.Info()
dis_width = infoObject.current_w
dis_height = infoObject.current_h
bar_height = 80

dis = pygame.display.set_mode((dis_width, dis_height), pygame.FULLSCREEN)
pygame.display.set_caption('Snake Game - Remastered')

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
dark_green = (0, 150, 0)
gold = (255, 215, 0)
light_blue = (173, 216, 230)
dark_blue = (0, 0, 139)
gray = (128, 128, 128)
dark_gray = (80, 80, 80)
orange = (255, 165, 0)
purple = (128, 0, 128)
button_color = (60, 60, 60)
score_color = (70, 70, 70)

snake_block = 60
initial_snake_length = 3
snake_speed = 10
snake_speed_increment = 0.2
max_snake_speed = 30

try:
    fundo = pygame.image.load("img/fundo_cobra.png").convert()
    cabeca_cobra = pygame.image.load("img/cabeca_cobra.png").convert_alpha()
    corpo_cobra = pygame.image.load("img/corpo_cobra.png").convert_alpha()
    rabo_cobra = pygame.image.load("img/rabo_cobra.png").convert_alpha()
    curva_cobra = pygame.image.load("img/curva_cobra.png").convert_alpha()
    fruta_img = pygame.image.load("img/fruta_normal.png").convert_alpha()
    rare_fruit_img = pygame.image.load("img/fruta_dourada.png").convert_alpha()
    menu_background = pygame.image.load("img/menu_background.jpg").convert()
    gameover_background = pygame.image.load("img/menu_background.jpg").convert()
    original_button_image = pygame.image.load("img/espaco.jpg").convert_alpha()
    particle_image = pygame.image.load("img/particle.png").convert_alpha()
    menu_logo = pygame.image.load("img/logo.png").convert_alpha()
    speed_powerup_img = pygame.image.load("img/dash.png").convert_alpha()
    invincible_powerup_img = pygame.image.load("img/invencibilidade.png").convert_alpha()
    obstacle_img = pygame.image.load("img/asteroide.png").convert_alpha()
    rotten_apple = pygame.image.load("img/veneno.png").convert_alpha()
    game_over_img = pygame.image.load("img/game_over.png").convert_alpha() # Carrega a imagem de Game Over


except pygame.error as e:
    print(f"Erro ao carregar imagens: {e}")
    pygame.quit()
    quit()

def round_image(image, radius):
    corner_mask = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(corner_mask, (0, 0, 0, 0), (radius, radius), radius, radius)
    rect = image.get_rect()
    rounded_image = image.copy()
    rounded_image.blit(corner_mask, (0, 0))
    rounded_image.blit(corner_mask, (rect.width - radius * 2, 0))
    rounded_image.blit(corner_mask, (0, rect.height - radius * 2))
    rounded_image.blit(corner_mask, (rect.width - radius * 2, rect.height - radius * 2))
    return rounded_image

fundo = pygame.transform.scale(fundo, (dis_width, dis_height))
cabeca_cobra = pygame.transform.scale(cabeca_cobra, (snake_block, snake_block))
corpo_cobra = pygame.transform.scale(corpo_cobra, (snake_block, snake_block))
rabo_cobra = pygame.transform.scale(rabo_cobra, (snake_block, snake_block))
curva_cobra = pygame.transform.scale(curva_cobra, (snake_block, snake_block))
fruta_img = pygame.transform.scale(fruta_img, (snake_block, snake_block))
rare_fruit_img = pygame.transform.scale(rare_fruit_img, (snake_block, snake_block))
menu_background = pygame.transform.scale(menu_background, (dis_width, dis_height))
gameover_background = pygame.transform.scale(gameover_background, (dis_width, dis_height))
original_button_image = pygame.transform.scale(original_button_image, (200, 70))
button_image = round_image(original_button_image, 15)
particle_image = pygame.transform.scale(particle_image, (10, 10))

logo_height = dis_height // 4
logo_width = int(menu_logo.get_width() * (logo_height / menu_logo.get_height()))
menu_logo = pygame.transform.scale(menu_logo, (logo_width, logo_height))

speed_powerup_img = pygame.transform.scale(speed_powerup_img, (snake_block, snake_block))
invincible_powerup_img = pygame.transform.scale(invincible_powerup_img, (snake_block, snake_block))
obstacle_img = pygame.transform.scale(obstacle_img, (snake_block, snake_block))
rotten_apple = pygame.transform.scale(rotten_apple, (snake_block, snake_block))
game_over_img = pygame.transform.scale(game_over_img, (dis_width // 2, dis_height // 5))  # Escala a imagem do game over

def our_snake(snake_list, direction):
    for i, pos in enumerate(snake_list):
        if i == len(snake_list) - 1:
            dis.blit(pygame.transform.rotate(cabeca_cobra, direction), pos)
        elif i == 0:
            next_pos = snake_list[i + 1]
            if next_pos[0] > pos[0]:
                angle = 0
            elif next_pos[0] < pos[0]:
                angle = 180
            elif next_pos[1] > pos[1]:
                angle = 270
            else:
                angle = 90
            dis.blit(pygame.transform.rotate(rabo_cobra, angle), pos)
        else:
            prev_pos = snake_list[i - 1]
            next_pos = snake_list[i + 1]

            if prev_pos[0] != next_pos[0] and prev_pos[1] != next_pos[1]:
                if prev_pos[1] < pos[1] and next_pos[1] < pos[1]:
                    angle = 0
                elif prev_pos[0] < pos[0] and next_pos[1] > pos[1]:
                    angle = 0
                elif prev_pos[1] < pos[1] and next_pos[0] > pos[0]:
                    angle = 180
                elif prev_pos[0] > pos[0] and next_pos[1] > pos[1]:
                    angle = 90
                elif prev_pos[1] < pos[1] and next_pos[0] < pos[0]:
                    angle = 270
                elif prev_pos[0] < pos[0] and next_pos[1] < pos[1]:
                    angle = 270
                elif prev_pos[1] > pos[1] and next_pos[0] < pos[0]:
                    angle = 0
                elif prev_pos[0] > pos[0] and next_pos[1] < pos[1]:
                    angle = 180

                dis.blit(pygame.transform.rotate(curva_cobra, angle), pos)
            else:
                if prev_pos[0] == next_pos[0]:
                    if prev_pos[1] < next_pos[1]:
                        angle = 270
                    else:
                        angle = 90
                elif prev_pos[1] == next_pos[1]:
                    if prev_pos[0] < next_pos[0]:
                        angle = 0
                    else:
                        angle = 180

                dis.blit(pygame.transform.rotate(corpo_cobra, angle), pos)

pygame.mixer.init()

pygame.mixer.music.load("gameplay_musica.mp3")
death_sound = pygame.mixer.Sound("glitch_7.mp3")
point_sound = pygame.mixer.Sound("pontos.mp3")
menu_music = pygame.mixer.Sound("ambiente-menu.mp3")
menu_button_sound = pygame.mixer.Sound("menu-botoes.mp3")
eat_sound = pygame.mixer.Sound("pop.mp3")
powerup_sound = pygame.mixer.Sound("powerup.mp3")
obstacle_hit_sound = pygame.mixer.Sound("obstacle_hit.mp3")

pygame.mixer.music.set_volume(0.5)
death_sound.set_volume(0.7)
point_sound.set_volume(0.7)
menu_music = pygame.mixer.Sound("ambiente-menu.mp3")
menu_button_sound = pygame.mixer.Sound("menu-botoes.mp3")
eat_sound = pygame.mixer.Sound("pop.mp3")
powerup_sound = pygame.mixer.Sound("powerup.mp3")
obstacle_hit_sound = pygame.mixer.Sound("obstacle_hit.mp3")

pygame.mixer.music.set_volume(0.5)
death_sound.set_volume(0.7)
point_sound.set_volume(0.7)
menu_music.set_volume(0.5)
menu_button_sound.set_volume(0.7)
eat_sound.set_volume(0.7)
powerup_sound.set_volume(0.7)
obstacle_hit_sound.set_volume(0.7)

def generate_food(snake_list, powerups, obstacles, rotten_apples, rare_fruits):
    while True:
        foodx = random.randrange(0, dis_width - snake_block, snake_block)
        foody = random.randrange(bar_height, dis_height - snake_block, snake_block)
        if (foodx, foody) not in snake_list and (foodx, foody) not in powerups and (foodx, foody) not in obstacles and (foodx,foody) not in rotten_apples and (foodx, foody) not in rare_fruits:
            return foodx, foody

def message(msg, color, x, y, font_size=35, font='bahnschrift'):
    font_style = pygame.font.SysFont(font, font_size)
    msg_surface = font_style.render(msg, True, color)
    msg_rect = msg_surface.get_rect(center=(x, y))
    dis.blit(msg_surface, msg_rect)

def button(msg, x, y, w, h, action=None, parameter=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, w, h)

    if rect.collidepoint(mouse):
        darkened_button = button_image.copy()
        darkened_button.fill((0, 0, 0, 50), special_flags=pygame.BLEND_RGBA_SUB)
        dis.blit(darkened_button, (x, y))
        pygame.draw.rect(dis, gold, rect, 3, border_radius=15)
        if click[0] == 1 and action is not None:
            menu_button_sound.play()
            if parameter is not None:
                action(parameter)
            else:
                action()
    else:
        dis.blit(button_image, (x, y))

    message(msg, white, x + w / 2, y + h / 2, 25)

def create_particles(x, y, color, num_particles):
    particles = []
    for _ in range(num_particles):
        particle = {
            'x': x,
            'y': y,
            'size': random.randint(4, 8),
            'color': color,
            'speed_x': random.uniform(-1, 1),
            'speed_y': random.uniform(-1, 1),
            'life': random.randint(20, 40)
        }
        particles.append(particle)
    return particles

def draw_particles(particles):
    for particle in particles:
        pygame.draw.circle(dis, particle['color'], (int(particle['x']), int(particle['y'])), particle['size'])

def update_particles(particles):
    for particle in particles[:]:
        particle['x'] += particle['speed_x']
        particle['y'] += particle['speed_y']
        particle['life'] -= 1
        if particle['life'] <= 0:
            particles.remove(particle)

def draw_top_bar(score, speed, invincible_timer, level, speed_timer, selected_level):
    pygame.draw.rect(dis, score_color, (0, 0, dis_width, bar_height))
    pygame.draw.rect(dis, black, (0, 0, dis_width, bar_height), 2)
    message(f"Pontuação: {score}", white, dis_width / 6, bar_height / 2, 25)
    message(f"Velocidade: {round(speed, 2)}", white, 2 * dis_width / 6, bar_height / 2, 25)
    message(f"Fase: {selected_level}", white, 3 * dis_width / 6, bar_height / 2, 25)
    if invincible_timer > 0:
        message(f"Invencível: {round(invincible_timer, 1)}", light_blue, 5 * dis_width / 6, bar_height / 2, 25)
    if speed_timer > 0:
        message(f"Velocidade Acelerada: {round(speed_timer, 1)}", orange, 4 * dis_width / 6, bar_height / 2, 25)

def screen_shake(duration=0.1, magnitude=5):
    shake_surface = pygame.Surface((dis_width, dis_height), pygame.SRCALPHA)
    shake_surface.blit(dis, (0, 0))

    start_time = time.time()
    while time.time() - start_time < duration:
        x_offset = random.randint(-magnitude, magnitude)
        y_offset = random.randint(-magnitude, magnitude)

        dis.blit(fundo, (0, 0))

        dis.blit(shake_surface, (x_offset, y_offset))

        pygame.time.delay(5)
        pygame.display.update()

def animate_item(scale, scale_change, min_scale, max_scale):
    scale += scale_change
    if scale > max_scale or scale < min_scale:
        scale_change *= -1
    return scale, scale_change

def create_new_obstacle(snake_list, powerups, obstacles, rotten_apples, rare_fruits):
    while True:
        obsx = random.randrange(0, dis_width - snake_block, snake_block)
        obsy = random.randrange(bar_height, dis_height - snake_block, snake_block)
        if (obsx, obsy) not in snake_list and (obsx, obsy) not in powerups and (obsx, obsy) not in obstacles and (obsx, obsy) not in rotten_apples and (obsx, obsy) not in rare_fruits:
            obstacles.append((obsx, obsy))
            break

def gameLoop(selected_level):
    game_over = False
    game_close = False

    pygame.mixer.music.play(-1)
    menu_music.stop()

    x1 = dis_width // 2
    y1 = dis_height // 2 + bar_height

    x1_change = snake_block
    y1_change = 0
    direction = 0

    snake_list = [
        (x1 - snake_block * 2, y1),
        (x1 - snake_block, y1),
        (x1, y1)
    ]
    length_of_snake = len(snake_list)

    enable_powerups = selected_level > 1
    enable_obstacles = selected_level > 2

    foodx, foody = generate_food(snake_list, [], [], [], [])

    clock = pygame.time.Clock()

    fruit_scale = 1.0
    fruit_scale_change = 0.01
    rare_fruit_scale = 1.0
    rare_fruit_scale_change = 0.01
    powerup_scale = 1.0
    powerup_scale_change = 0.01
    rotten_scale = 1.0
    rotten_scale_change = 0.01
    obstacle_scale = 1.0
    obstacle_scale_change = 0.01

    item_max_scale = 1.1
    item_min_scale = 0.9

    particles = []

    current_snake_speed = snake_speed
    original_snake_speed = snake_speed

    powerups = []
    powerup_spawn_rate = 5
    invincible = False
    invincible_timer = 0
    invincible_duration = 5
    speed_boost = False
    speed_timer = 0
    speed_duration = 3
    speed_powerup_amount = 5

    obstacles = []
    obstacle_count = 3
    obstacle_speed = 2
    obstacle_spawn_rate = 7
    last_obstacle_spawn = pygame.time.get_ticks()
    obstacle_spawn_interval = 3000

    rotten_apples = []
    rotten_apple_spawn_rate = 6

    rare_fruits = []
    rare_fruit_spawn_rate = 12

    if enable_obstacles:
        for _ in range(obstacle_count):
            create_new_obstacle(snake_list, powerups, obstacles, rotten_apples, rare_fruits)

    score = 0
    game_time = 0
    level = 1

    last_frame_time = time.time()

    def increase_difficulty():
        nonlocal level, current_snake_speed, obstacle_count, original_snake_speed
        level += 1
        original_snake_speed = min(original_snake_speed + 0.5, max_snake_speed)
        current_snake_speed = original_snake_speed
        if enable_obstacles:
            obstacle_count += 1

    while not game_over:

        current_time = time.time()
        delta_time = current_time - last_frame_time
        last_frame_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                    direction = 180
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                    direction = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                    direction = 90
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0
                    direction = -90

        if (
            x1 >= dis_width
            or x1 < 0
            or y1 >= dis_height
            or y1 < bar_height
            or (x1, y1) in snake_list[:-1]
        ):
            if not invincible:
                pygame.mixer.music.stop()
                death_sound.play()
                game_over = True
                game_close = True
                gameOver(score)
                break
            else:
                screen_shake(duration = 0.3, magnitude = 7)
                obstacles = []
                x1 = dis_width // 2
                y1 = dis_height // 2 + bar_height
                snake_list = [
                    (x1 - snake_block * 2, y1),
                    (x1 - snake_block, y1),
                    (x1, y1)
                ]
                length_of_snake = len(snake_list)
                pass

        if enable_obstacles:
            for obsx, obsy in obstacles:
                if abs(x1 - obsx) < snake_block and abs(y1 - obsy) < snake_block:
                    if not invincible:
                        pygame.mixer.music.stop()
                        death_sound.play()
                        game_close = True
                        game_over = True
                        gameOver(score)
                        break
                    else:
                        obstacle_hit_sound.play()
                        obstacles.remove((obsx, obsy))
                        particles.extend(create_particles(obsx + snake_block // 2, obsy + snake_block // 2, gray, 20))
                        screen_shake(duration = 0.2, magnitude = 5)
                        score += 5
                        for _ in range(2):
                            create_new_obstacle(snake_list, powerups, obstacles, rotten_apples, rare_fruits)

        if game_close:
            gameOver(score)

        x1 += x1_change
        y1 += y1_change
        dis.blit(fundo, (0, 0))

        fruit_scale, fruit_scale_change = animate_item(fruit_scale, fruit_scale_change, item_min_scale, item_max_scale)
        scaled_fruta = pygame.transform.scale(fruta_img, (int(snake_block * fruit_scale), int(snake_block * fruit_scale)))
        fruta_rect = scaled_fruta.get_rect(center=(foodx + snake_block // 2, foody + snake_block // 2))
        dis.blit(scaled_fruta, fruta_rect)

        snake_list.append((x1, y1))
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        our_snake(snake_list, direction)

        draw_particles(particles)
        update_particles(particles)

        if enable_powerups:
            for i, (powerupx, powerupy, powerup_type) in enumerate(powerups):
                powerup_scale, powerup_scale_change = animate_item(powerup_scale, powerup_scale_change, item_min_scale, item_max_scale)

                if powerup_type == "speed":
                   scaled_powerup = pygame.transform.scale(speed_powerup_img, (int(snake_block * powerup_scale), int(snake_block * powerup_scale)))
                   powerup_rect = scaled_powerup.get_rect(center=(powerupx + snake_block // 2, powerupy + snake_block // 2))
                   dis.blit(scaled_powerup, powerup_rect)

                elif powerup_type == "invincible":
                   scaled_powerup = pygame.transform.scale(invincible_powerup_img, (int(snake_block * powerup_scale), int(snake_block * powerup_scale)))
                   powerup_rect = scaled_powerup.get_rect(center=(powerupx + snake_block // 2, powerupy + snake_block // 2))
                   dis.blit(scaled_powerup, powerup_rect)

                if abs(x1 - powerupx) < snake_block and abs(y1 - powerupy) < snake_block:
                    powerup_sound.play()
                    powerups.pop(i)

                    if powerup_type == "speed":
                        speed_boost = True
                        speed_timer = speed_duration
                    elif powerup_type == "invincible":
                        invincible = True
                        invincible_timer = invincible_duration

        if enable_obstacles:
            for i, (obsx, obsy) in enumerate(obstacles):
                obstacle_scale, obstacle_scale_change = animate_item(obstacle_scale, obstacle_scale_change, item_min_scale, item_max_scale)
                scaled_obstacle = pygame.transform.scale(obstacle_img, (int(snake_block * obstacle_scale), int(snake_block * obstacle_scale)))
                obstacle_rect = scaled_obstacle.get_rect(center=(obsx + snake_block // 2, obsy + snake_block // 2))
                dis.blit(scaled_obstacle, obstacle_rect)

        for i, (rottenx, rotteny) in enumerate(rotten_apples):
            rotten_scale, rotten_scale_change = animate_item(rotten_scale, rotten_scale_change, item_min_scale, item_max_scale)
            scaled_rotten = pygame.transform.scale(rotten_apple, (int(snake_block * rotten_scale), int(snake_block * rotten_scale)))
            rotten_rect = scaled_rotten.get_rect(center=(rottenx + snake_block // 2, rotteny + snake_block // 2))
            dis.blit(scaled_rotten, rotten_rect)

            if abs(x1 - rottenx) < snake_block and abs(y1 - rotteny) < snake_block:
                rotten_apples.pop(i)
                score = max(0, score - 1) 
                particles.extend(create_particles(x1, y1, dark_green, 20))
                screen_shake(duration = 0.1, magnitude = 4)
                if length_of_snake > initial_snake_length:
                    length_of_snake -= 1

        for i, (rarex, rarey) in enumerate(rare_fruits):
            rare_fruit_scale, rare_fruit_scale_change = animate_item(rare_fruit_scale, rare_fruit_scale_change, item_min_scale, item_max_scale)
            scaled_rare = pygame.transform.scale(rare_fruit_img, (int(snake_block * rare_fruit_scale), int(snake_block * rare_fruit_scale)))
            rare_rect = scaled_rare.get_rect(center=(rarex + snake_block // 2, rarey + snake_block // 2))
            dis.blit(scaled_rare, rare_rect)

            if abs(x1 - rarex) < snake_block and abs(y1 - rarey) < snake_block:
                rare_fruits.pop(i)
                length_of_snake += 2
                score += 5
                particles.extend(create_particles(rarex + snake_block // 2, rarey + snake_block // 2, gold, 30))
                screen_shake(duration=0.1, magnitude=4)

        draw_top_bar(score, current_snake_speed, invincible_timer, level, speed_timer, selected_level)

        pygame.display.update()

        if abs(x1 - foodx) < snake_block and abs(y1 - foody) < snake_block:
            foodx, foody = generate_food(snake_list, powerups, obstacles, rotten_apples, rare_fruits)
            length_of_snake += 1
            score += 1
            eat_sound.play()
            particles.extend(create_particles(foodx + snake_block // 2, foody + snake_block // 2, orange, 20))
            original_snake_speed = min(original_snake_speed + snake_speed_increment, max_snake_speed)
            current_snake_speed = original_snake_speed

            screen_shake(duration=0.05, magnitude=3)

            if enable_powerups and random.randint(1, 3) == 1:
                powerupx = random.randrange(0, dis_width - snake_block, snake_block)
                powerupy = random.randrange(bar_height, dis_height - snake_block, snake_block)
                powerup_type = random.choice(["speed", "invincible"])
                powerups.append((powerupx, powerupy, powerup_type))

            if random.randint(1, rotten_apple_spawn_rate) == 1:
                rottenx = random.randrange(0, dis_width - snake_block, snake_block)
                rotteny = random.randrange(bar_height, dis_height - snake_block, snake_block)
                rotten_apples.append((rottenx, rotteny))

            if random.randint(1, rare_fruit_spawn_rate) == 1:
                rarex = random.randrange(0, dis_width - snake_block, snake_block)
                rarey = random.randrange(bar_height, dis_height - snake_block, snake_block)
                rare_fruits.append((rarex, rarey))

        if enable_obstacles:
            for i, (obsx, obsy) in enumerate(obstacles):
                obsx += obstacle_speed
                if obsx > dis_width:
                    obsx = 0 - snake_block
                obstacles[i] = (obsx, obsy)

            now = pygame.time.get_ticks()
            if enable_obstacles and now - last_obstacle_spawn > obstacle_spawn_interval and random.randint(1, obstacle_spawn_rate) == 1:
                create_new_obstacle(snake_list, powerups, obstacles, rotten_apples, rare_fruits)
                last_obstacle_spawn = now

        if invincible_timer > 0:
            invincible_timer -= delta_time
            if invincible_timer <= 0:
                invincible = False

        if speed_boost:
            current_snake_speed = original_snake_speed + speed_powerup_amount
            if speed_timer > 0:
                speed_timer -= delta_time
            else:
                speed_boost = False
                current_snake_speed = original_snake_speed

        clock.tick(current_snake_speed)


def gameOver(score):
    game_over = True
    start_fade = False
    alpha = 255

    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_fade = True

        dis.blit(gameover_background, (0, 0))

        # Use a imagem game_over_img em vez da mensagem de texto
        game_over_rect = game_over_img.get_rect(center=(dis_width / 2, dis_height / 4))  # Posiciona a imagem
        dis.blit(game_over_img, game_over_rect)

        message(f"Sua Pontuação: {score}", gold, dis_width / 2, dis_height / 3, font_size=30)

        button("Reiniciar", dis_width / 4 - 100, dis_height / 2, 200, 70, lambda: gameLoop(level_selected))
        button("Menu", dis_width / 2 - 100, dis_height / 2, 200, 70, gameMenu)
        button("Sair", 3 * dis_width / 4 - 100, dis_height / 2, 200, 70, pygame.quit)

        pygame.display.update()


def gameMenu():
    menu = True
    menu_music.play(-1)
    pygame.mixer.music.stop()

    logo_y = -menu_logo.get_height()
    logo_speed = 2

    button1_x = -200
    button2_x = dis_width + 200
    button_speed = 5
    buttons_animated = False

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        dis.blit(menu_background, (0, 0))

        if logo_y < dis_height / 4 - menu_logo.get_height() / 2:
            logo_y += logo_speed
        else:
            logo_y = dis_height / 4 - menu_logo.get_height() / 2

            if not buttons_animated:
                button1_x = dis_width / 2 - 100
                button2_x = dis_width / 2 - 100
                buttons_animated = True

        dis.blit(menu_logo, (dis_width / 2 - menu_logo.get_width() / 2, logo_y))

        level1_description = "Cobra Clássica: Apenas frutas e a cobra."
        level2_description = "Poderes Ativados: Power-ups e frutas raras."
        level3_description = "Desafio Completo: Tudo + obstáculos!"

        desc_x = dis_width / 2
        level_button_y_start = dis_height / 3 + 50
        desc_y_offset = 90

        if buttons_animated:
            level1_button = button("Nível 1", dis_width / 2 - 100, level_button_y_start, 200, 70, lambda: set_level(1))
            message(level1_description, white, desc_x, level_button_y_start + desc_y_offset, 20, font='comicsansms')

            level2_y = level_button_y_start + 180
            level2_button = button("Nível 2", dis_width / 2 - 100, level2_y, 200, 70, lambda: set_level(2))
            message(level2_description, white, desc_x, level2_y + desc_y_offset, 20, font='comicsansms')

            level3_y = level2_y + 180
            level3_button = button("Nível 3", dis_width / 2 - 100, level3_y, 200, 70, lambda: set_level(3))
            message(level3_description, white, desc_x, level3_y + desc_y_offset, 20, font='comicsansms')

            sair_y = level3_y + 180
            sair_button = button("Sair", dis_width / 2 - 100, sair_y, 200, 70, pygame.quit)

        pygame.display.update()

level_selected = 1

def set_level(level):
    global level_selected
    level_selected = level
    gameLoop(level_selected)

gameMenu()