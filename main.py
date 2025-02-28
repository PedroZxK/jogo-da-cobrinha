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
red = (255, 0, 0)
dark_green = (0, 128, 0)

# Tamanho do bloco da cobra e velocidade
snake_block = 50
initial_snake_length = 3  # Cabeça + 1 Corpo + Rabo
snake_speed = 7

# Carregamento de imagens
try:
    fundo = pygame.image.load("img/fundo_cobra.png").convert()
    cabeça_cobra = pygame.image.load("img/cabeca_cobra.png").convert_alpha()
    corpo_cobra = pygame.image.load("img/corpo_cobra.png").convert_alpha()
    rabo_cobra = pygame.image.load("img/rabo_cobra.png").convert_alpha()
    corpo_curvado = pygame.image.load("img/curva_cobra.png").convert_alpha()
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
corpo_curvado = pygame.transform.scale(corpo_curvado, (snake_block, snake_block))
fruta_img = pygame.transform.scale(fruta_img, (snake_block, snake_block))

# Função para desenhar a cobra
def our_snake(snake_list, direction):
    for i, pos in enumerate(snake_list):
        if i == len(snake_list) - 1:  # Cabeça
            if i > 0:
                direction = get_segment_direction(snake_list[i - 1], pos)
            else:
                direction = 0  # Padrão
            dis.blit(rotate_image(cabeça_cobra, direction), pos)
        
        elif i == 0:  # Rabo
            next_segment = snake_list[1]
            rabo_dir = get_segment_direction(pos, next_segment)
            dis.blit(rotate_image(rabo_cobra, rabo_dir), pos)
        
        else:  # Corpo
            prev_segment = snake_list[i - 1]
            next_segment = snake_list[i + 1]

            if prev_segment[0] != next_segment[0] and prev_segment[1] != next_segment[1]:
                prev_vector = (prev_segment[0] - pos[0], prev_segment[1] - pos[1])
                current_vector = (pos[0] - next_segment[0], pos[1] - next_segment[1])
                curva_dir = get_curva_direction(prev_vector, current_vector)
                dis.blit(pygame.transform.rotate(corpo_curvado, curva_dir), pos)
            else:
                # Movimento na vertical
                if prev_segment[0] == next_segment[0]:
                    corpo_rotacionado = pygame.transform.rotate(corpo_cobra, 90)
                else:
                    corpo_rotacionado = corpo_cobra
                dis.blit(corpo_rotacionado, pos)


def get_curva_direction(prev_vector, current_vector):
    """Retorna a rotação correta para o sprite da curva com base em vetores."""
    if prev_vector == (1, 0) and current_vector == (0, -1):
        return 0
    elif prev_vector == (0, -1) and current_vector == (-1, 0):
        return 90
    elif prev_vector == (-1, 0) and current_vector == (0, 1):
        return 180
    elif prev_vector == (0, 1) and current_vector == (1, 0):
        return 270
    # Adicione outros casos aqui
    return 0

# Função para determinar a direção do segmento
def get_segment_direction(current, next_segment):
    """ Retorna a direção do movimento baseado em dois segmentos consecutivos """
    if next_segment[0] > current[0]:  # Movendo para a direita
        return 0
    elif next_segment[0] < current[0]:  # Movendo para a esquerda
        return 180
    elif next_segment[1] > current[1]:  # Movendo para baixo
        return 90
    elif next_segment[1] < current[1]:  # Movendo para cima
        return 270
    return 0  # Caso padrão

# Função para rotacionar imagens
def rotate_image(image, direction):
    if direction == 90:
        return pygame.transform.rotate(image, 90)
    elif direction == 270:
        return pygame.transform.rotate(image, -90)
    elif direction == 0:
        return image
    elif direction == 180:
        return pygame.transform.rotate(image, 180)
    return image

# Função principal do jogo
def gameLoop():
    game_over = False
    game_close = False

    # Posição inicial da cobra
    x1 = dis_width // 2
    y1 = dis_height // 2 + bar_height

    # Direção inicial
    direction = "RIGHT"
    x1_change = snake_block
    y1_change = 0

    # Criando a cobra com cabeça, corpo e rabo alinhados
    snake_list = [
        (x1 - snake_block * 2, y1),  # Rabo
        (x1 - snake_block, y1),  # Corpo
        (x1, y1)  # Cabeça
    ]
    length_of_snake = len(snake_list)

    # Posição da fruta
    foodx = random.randrange(0, dis_width - snake_block, snake_block)
    foody = random.randrange(bar_height, dis_height - snake_block, snake_block)

    # Tempo inicial
    start_time = time.time()
    fruits_collected = 0
    clock = pygame.time.Clock()

    while not game_over:

        while game_close:
            dis.fill(black)
            font_style = pygame.font.SysFont('bahnschrift', 35)
            msg = font_style.render("Você perdeu! Pressione C para continuar ou Q para sair", True, red)
            dis.blit(msg, (dis_width // 4, dis_height // 2))
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

        # Verifica se bateu na parede
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < bar_height:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.blit(fundo, (0, 0))

        # Desenha a fruta
        dis.blit(fruta_img, (foodx, foody))

        # Atualiza a posição da cobra
        snake_list.append((x1, y1))
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Verifica colisão da cabeça com o corpo
        if (x1, y1) in snake_list[:-1]:
            game_close = True

        # Desenha a cobra
        our_snake(snake_list, direction)

        pygame.display.update()

        # Verifica colisão com a fruta
        if abs(x1 - foodx) < snake_block and abs(y1 - foody) < snake_block:
            foodx = random.randrange(0, dis_width - snake_block, snake_block)
            foody = random.randrange(bar_height, dis_height - snake_block, snake_block)
            length_of_snake += 1
            fruits_collected += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Inicializa o jogo
gameLoop()
