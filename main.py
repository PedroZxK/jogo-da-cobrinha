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

# Tamanho do bloco da cobra e velocidade
snake_block = 60
initial_snake_length = 3  # Cabeça + 1 Corpo + Rabo
snake_speed = 10

# Carregamento de imagens
try:
    fundo = pygame.image.load("img/fundo_cobra.png").convert()
    cabeca_cobra = pygame.image.load("img/cabeca_cobra.png").convert_alpha()
    corpo_cobra = pygame.image.load("img/corpo_cobra.png").convert_alpha()
    rabo_cobra = pygame.image.load("img/rabo_cobra.png").convert_alpha()
    curva_cobra = pygame.image.load("img/curva_cobra.png").convert_alpha()
    fruta_img = pygame.image.load("img/fruta.png").convert_alpha()
except pygame.error as e:
    print(f"Erro ao carregar imagens: {e}")
    pygame.quit()
    quit()

# Redimensionamento das imagens
fundo = pygame.transform.scale(fundo, (dis_width, dis_height))
cabeca_cobra = pygame.transform.scale(cabeca_cobra, (snake_block, snake_block))
corpo_cobra = pygame.transform.scale(corpo_cobra, (snake_block, snake_block))
rabo_cobra = pygame.transform.scale(rabo_cobra, (snake_block, snake_block))
curva_cobra = pygame.transform.scale(curva_cobra, (snake_block, snake_block))
fruta_img = pygame.transform.scale(fruta_img, (snake_block, snake_block))

# Função para desenhar a cobra com rotação correta
# Função para desenhar a cobra com rotação correta
# Função para desenhar a cobra com rotação correta
def our_snake(snake_list, direction):
    for i, pos in enumerate(snake_list):
        if i == len(snake_list) - 1:  # Cabeça
            dis.blit(pygame.transform.rotate(cabeca_cobra, direction), pos)
        elif i == 0:  # Rabo
            next_pos = snake_list[i + 1]
            if next_pos[0] > pos[0]:
                angle = 0  # Direção para a direita
            elif next_pos[0] < pos[0]:
                angle = 180  # Direção para a esquerda
            elif next_pos[1] > pos[1]:
                angle = 270  # Direção para baixo
            else:
                angle = 90  # Direção para cima
            dis.blit(pygame.transform.rotate(rabo_cobra, angle), pos)
        else:  # Corpo
            prev_pos = snake_list[i - 1]
            next_pos = snake_list[i + 1]

            # Verifica se o corpo faz uma curva
            if prev_pos[0] != next_pos[0] and prev_pos[1] != next_pos[1]:  # Condição de curva
                # A cobra está fazendo uma curva, usa o sprite da curva
                if  prev_pos[1] < pos[1] and next_pos[1] < pos[1]:  # Curva para a direita e para baixo
                    angle = 0
                elif prev_pos[0] < pos[0] and next_pos[1] > pos[1]:  # Curva para baixo e para a direita
                    angle = 0
                elif prev_pos[1] < pos[1] and next_pos[0] > pos[0]:  # Curva para cima e para a direita
                    angle = 180
                elif prev_pos[0] > pos[0] and next_pos[1] > pos[1]:  # Curva para a esquerda e para baixo
                    angle = 90
                elif prev_pos[1] < pos[1] and next_pos[0] < pos[0]:  # Curva para cima e para a esquerda
                    angle = 270
                elif prev_pos[0] < pos[0] and next_pos[1] < pos[1]:  # Curva para a direita e para cima
                    angle = 270
                elif prev_pos[1] > pos[1] and next_pos[0] < pos[0]:  # Curva para cima e para a esquerda
                    angle = 0
                elif prev_pos[0] > pos[0] and next_pos[1] < pos[1]:  # Curva para a esquerda e para cima
                    angle = 180
                
                dis.blit(pygame.transform.rotate(curva_cobra, angle), pos)
            else:
                # Movimento reto (horizontal ou vertical)
                if prev_pos[0] == next_pos[0]:  # Movimento Vertical
                    if prev_pos[1] < next_pos[1]:
                        angle = 270  # Direção para baixo
                    else:
                        angle = 90  # Direção para cima
                elif prev_pos[1] == next_pos[1]:  # Movimento Horizontal
                    if prev_pos[0] < next_pos[0]:
                        angle = 0  # Direção para a direita
                    else:
                        angle = 180  # Direção para a esquerda

                dis.blit(pygame.transform.rotate(corpo_cobra, angle), pos)



# Função principal do jogo
def gameLoop():
    game_over = False
    game_close = False

    # Posição inicial da cobra
    x1 = dis_width // 2
    y1 = dis_height // 2 + bar_height

    # Direção inicial
    x1_change = snake_block
    y1_change = 0
    direction = 0  # Ângulo da cabeça (0 = Direita, 90 = Cima, 180 = Esquerda, -90 = Baixo)

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

        # Desenha a cobra com rotação
        our_snake(snake_list, direction)

        pygame.display.update()

        # Verifica colisão com a fruta
        if abs(x1 - foodx) < snake_block and abs(y1 - foody) < snake_block:
            foodx = random.randrange(0, dis_width - snake_block, snake_block)
            foody = random.randrange(bar_height, dis_height - snake_block, snake_block)
            length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Inicializa o jogo
gameLoop()
