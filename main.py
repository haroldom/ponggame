import pygame, sys


pygame.init()

size = (1058,725)
s_width = 1058
s_height = 725
# Variables globales
margin_left=40
# Para el jugador número uno, coordenadas de su posición, puntaje
margin_top_player1 = s_height/2-(105/2)
player1_speed = 0
score_player1 = 0
text_score_p1 = pygame.font.SysFont('Console', 30, True)

# Para el jugador número uno, coordenadas de su posición, puntaje
margin_top_player2 = s_height/2-(105/2)
player2_speed = 0
score_player2 = 0
text_score_p2 = pygame.font.SysFont('Console', 30, True)


# Para el balón, coordenadas y velocidad:
ball_coord_x = s_width/2
ball_coord_y = s_height/2-5

ball_speed_x = 4
ball_speed_y = 4
# Definimos colores:
BLACK = (0,0,0)
WHITE = (255,255,255)

# Creamos una ventana
screen = pygame.display.set_mode(size)

# Controlar FPS
clock = pygame.time.Clock()

# Ocultar visibilidad de mouse
pygame.mouse.set_visible(0) # 1 = Ver ; 0= Ocultar

def mov_bars(y):
    global margin_top_player1
    speed_y_player1 = y
    margin_top_player1 -= y


def draw_bars(screen):
    pass

def main(screen):
    global margin_top_player1,player1_speed,margin_top_player2,player2_speed, ball_coord_x, ball_coord_y, ball_speed_x, ball_speed_y, score_player1,score_player2
    collision_down = False
    collision_right = False
    collision_left = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player1_speed = -5
                if event.key == pygame.K_s:
                    player1_speed = +5
                if event.key == pygame.K_UP:
                    player2_speed = -5
                if event.key == pygame.K_DOWN:
                    player2_speed = +5
        

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    player1_speed = 0
                if event.key == pygame.K_s:
                    player1_speed = 0  
                if event.key == pygame.K_UP:
                    player2_speed = 0
                if event.key == pygame.K_DOWN:
                    player2_speed = 0

        # --- LOGICA

        # Modificamos las coordenadas, y evitamos que los players se salgan de la ventana.

        margin_top_player1 += player1_speed
        if margin_top_player1 <= 0:
            margin_top_player1 = 0
        if margin_top_player1 >= s_height-105:
            margin_top_player1 = s_height-105

        margin_top_player2 += player2_speed
        if margin_top_player2 <= 0:
            margin_top_player2 = 0
        if margin_top_player2 >= s_height-105:
            margin_top_player2 = s_height-105




        # Detectar colisión con la parte inferior del screen
        if ball_coord_y >= 725-5:
            collision_down = True
        
        if collision_down != True:
            ball_coord_y += ball_speed_y
        elif collision_down == True:
            ball_coord_y -= ball_speed_y

        # Detectar colisión con la parte derecha del screen
        if ball_coord_x >= s_width-5:
            collision_right = True
        if collision_right != True:
            ball_coord_x += ball_speed_x
        elif collision_right == True:
            ball_coord_x = s_width/2
            ball_coord_y = s_height/2-5
            collision_right = False
            score_player1 += 1

        # Detectar colisión con la parte izquierda del screen
        if ball_coord_x <= 5:
            collision_left = True
        if collision_left != True:
            ball_coord_x += ball_speed_x
        elif collision_left == True:
            ball_coord_x = s_width/2
            ball_coord_y = s_height/2-5
            collision_left = False
            score_player2 += 1


        # Detectar colisión con la parte superior del screen
        if ball_coord_y <= 5:
            collision_down = False
        # Detectar colisión con la parte izquierda del screen
        if ball_coord_x <= 5:
            collision_left = True  
    
        # --- LOGICA

        

        # Color fondo
        screen.fill(BLACK)
        ## ----- ZONA DE DIBUJO

        # Player 1:
        player1 = pygame.draw.rect(screen, WHITE, (margin_left,margin_top_player1, 10, 105))
        # Player 2:
        player2 = pygame.draw.rect(screen, WHITE, (s_width-40,margin_top_player2, 10, 105))

        # Dibujar linea central (Cada cuadradito tendrá: 21 = s_height; 6= s_width: Con un margin superior de 4px)
        rect_center_top = 10
        for i in range(18): # 28 cuadraditos
            pygame.draw.rect(screen, WHITE, (s_width/2-(6/2),rect_center_top, 6, 21))
            rect_center_top += 40
        
        # Dibujamos el balón
        ball = pygame.draw.circle(screen, WHITE, (ball_coord_x, ball_coord_y), 10)

        if ball.top <= 0 or ball.bottom >= s_height:
            ball_speed_y *= -1
        
        if ball.colliderect(player2) and ball_speed_x > 0:
            if abs(ball.right - player2.left) < 10:
                ball_speed_x *= -1
            elif abs(ball.top - player2.bottom) < 10 and ball_speed_y < 0:
                ball_speed_y *= -1
            elif abs(ball.bottom - player2.top) < 10 and ball_speed_y > 0:
                ball_speed_y *= -1
        
        if ball.colliderect(player1) and ball_speed_x < 0:
            if abs(ball.left - player1.right) < 10:
                ball_speed_x *= -1
            elif abs(ball.top - player1.bottom) < 10:
                ball_speed_y *= -1
            elif abs(ball.bottom - player1.top) < 10:
                ball_speed_y *= -1


        # Dibujamos el marcador:
        score_p1 = text_score_p1.render(str(score_player1),1,(255,255,255))
        screen.blit(score_p1,(350,10))
        score_p2 = text_score_p1.render(str(score_player2),1,(255,255,255))
        screen.blit(score_p2,(850,10))

        if score_player1 == 3:
            draw_winner("Player 1")
            # text_win_player1 = text_win_p1.render("Win", 1,(255,255,255))
            # screen.blit(text_win_player1,(350, 100))
            # time.sleep(5)
            # break
        elif score_player2 == 3:
            draw_winner("Player 2")

            # text_win_player2 = text_win_p2.render("Win", 1,(255,255,255))
            # screen.blit(text_win_player2,(850,100))
            # time.sleep(5)
            # break
        ## ----- ZONA DE DIBUJO

        #Actualizar pantalla
        pygame.display.flip()
        #Controlamos los FPD
        clock.tick(60)

def draw_winner(winner):
    global score_player1, score_player2, margin_top_player1, margin_top_player2
    screen.fill(BLACK)
    #Dibujar en pantalla el nombre del ganador
    text_win = pygame.font.SysFont('Console', 30, True)
    text_win_screen = text_win.render("Winner: "+str(winner),1,(255,255,255))
    screen.blit(text_win_screen,(s_width/2,100))

    score_player1 = 0
    score_player2 = 0
    margin_top_player1 = s_height/2-(105/2)
    margin_top_player2 = s_height/2-(105/2)


    #Actualizar pantalla
    pygame.display.flip()
    #Controlamos los FPD
    clock.tick(60)
    pygame.time.delay(1500)


def main_menu(screen):
    main(screen)

main_menu(screen)