import pygame
import time
import random

# Inicialização do Pygame
pygame.init()

# Configurações da tela
infoObject = pygame.display.Info()
dis_width = infoObject.current_w
dis_height = infoObject.current_h
bar_height = 60  # Altura da barra superior

dis = pygame.display.set_mode((dis_width, dis_height), pygame.FULLSCREEN)
pygame.display.set_caption('Snake Game - Remastered')

# Cores
white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
dark_green = (0, 128, 0)  # Definida no escopo global

# Tamanho do bloco da cobra e velocidade
snake_block = 40
snake_speed = 7

# Carregamento de imagens
try:
    fundo = pygame.image.load("img/fundo_cobra.png").convert()
    cabeça_cobra = pygame.image.load("img/cabeça_cobra.png").convert_alpha()
    corpo_cobra = pygame.image.load("img/corpo_cobra.png").convert_alpha()
    rabo_cobra = pygame.image.load("img/rabo_cobra.png").convert_alpha()
    fruta_img = pygame.image.load("img/fruta.png").convert_alpha()
except pygame.error as e:
    print(f"Erro ao carregar imagens: {e}")
    pygame.quit()
    quit()

# Redimensionamento das imagens
fundo = pygame.transform.scale(fundo, (dis_width, dis_height))
cabeça_cobra = pygame.transform.scale(cabeça_cobra, (snake_block, snake_block))
corpo_cobra = pygame.transform.scale(corpo_cobra, (snake_block, snake_block))
rabo_cobra = pygame.transform.scale(rabo_cobra, (snake_block, snake_block))
fruta_img = pygame.transform.scale(fruta_img, (snake_block, snake_block))

# Fontes
font_style = pygame.font.SysFont('bahnschrift', 25)
score_font = pygame.font.SysFont('comicsansms', 35)

# Função para exibir a pontuação
def your_score(score):
    value = score_font.render("Your Score: " + str(score), True, white)
    dis.blit(value, [0, 0])

# Função para desenhar a cobra
def our_snake(snake_block, snake_list, direction):
    for i, x in enumerate(snake_list):
        if i == len(snake_list) - 1:  # Cabeça
            rotated_head = rotate_image(cabeça_cobra, direction)
            dis.blit(rotated_head, [x[0], x[1]])
        elif i == 0 and len(snake_list) > 1:  # Rabo
            # Determina a direção do rabo com base na posição do próximo segmento
            next_segment = snake_list[1]
            if x[0] < next_segment[0]:  # Rabo à esquerda
                rabo_dir = "RIGHT"
            elif x[0] > next_segment[0]:  # Rabo à direita
                rabo_dir = "LEFT"
            elif x[1] < next_segment[1]:  # Rabo para cima
                rabo_dir = "DOWN"
            else:  # Rabo para baixo
                rabo_dir = "UP"
            rotated_tail = rotate_image(rabo_cobra, rabo_dir)
            dis.blit(rotated_tail, [x[0], x[1]])
        else:  # Corpo
            dis.blit(corpo_cobra, [x[0], x[1]])

# Função para exibir mensagens na tela
def message(msg, color, y_displacement=0):
    mesg = font_style.render(msg, True, color)
    text_rect = mesg.get_rect(center=(dis_width / 2, dis_height / 2 + y_displacement))
    dis.blit(mesg, text_rect)

# Função para rotacionar imagens
def rotate_image(image, direction):
    if direction == "UP":
        return pygame.transform.rotate(image, 90)
    elif direction == "DOWN":
        return pygame.transform.rotate(image, -90)
    elif direction == "RIGHT":
        return pygame.transform.rotate(image, 0)
    elif direction == "LEFT":
        return pygame.transform.rotate(image, 180)
    return image

# Função para desenhar a barra de status
def draw_status_bar(score, start_time, fruits):
    pygame.draw.rect(dis, dark_green, [0, 0, dis_width, bar_height])
    elapsed_time = round(time.time() - start_time, 2)

    score_text = font_style.render(f"Placar: {score}", True, white)
    time_text = font_style.render(f"Tempo: {elapsed_time}s", True, white)
    fruit_text = font_style.render(f"Frutas: {fruits}", True, white)

    dis.blit(score_text, (10, 10))
    dis.blit(time_text, (dis_width // 2 - 50, 10))
    dis.blit(fruit_text, (dis_width - 150, 10))

# Loop principal do jogo
def gameLoop():
    game_over = False
    game_close = False

    # Posição inicial da cobra
    x1 = dis_width / 2
    y1 = dis_height / 2 + bar_height

    # Velocidade inicial
    x1_change = snake_block  # Começa movendo para a direita
    y1_change = 0

    # Lista da cobra
    snake_List = []
    Length_of_snake = 1
    fruits_collected = 0

    # Posição da comida
    foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(bar_height, dis_height - snake_block) / snake_block) * snake_block

    # Direção inicial da cobra
    direction = "RIGHT"

    # Tempo inicial
    start_time = time.time()
    snake_speed = 7

    while not game_over:

        while game_close == True:
            dis.fill(black)
            message("You Lost! Press C-Play Again or Q-Quit", red, y_displacement=-50)
            message("Your Score: " + str(Length_of_snake - 1), white, y_displacement=50)
            your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != "RIGHT":
                    x1_change = -snake_block
                    y1_change = 0
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    x1_change = snake_block
                    y1_change = 0
                    direction = "RIGHT"
                elif event.key == pygame.K_UP and direction != "DOWN":
                    y1_change = -snake_block
                    x1_change = 0
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    y1_change = snake_block
                    x1_change = 0
                    direction = "DOWN"

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < bar_height:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.blit(fundo, (0, 0))

        # Desenha a comida usando a imagem
        dis.blit(fruta_img, [foodx, foody])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List, direction)
        draw_status_bar(Length_of_snake - 1, start_time, fruits_collected)

        pygame.display.update()

        # Verifica se a cabeça da cobra colidiu com a fruta
        if x1 < foodx + snake_block and x1 + snake_block > foodx and y1 < foody + snake_block and y1 + snake_block > foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(bar_height, dis_height - snake_block) / snake_block) * snake_block
            Length_of_snake += 1
            fruits_collected += 1
            snake_speed += 0.2

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Inicializa o jogo
clock = pygame.time.Clock()
gameLoop()