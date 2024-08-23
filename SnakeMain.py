#Importante instalar estas librerias (usar pip install <Libreria> si estan usando Visual :3)
import pygame,sys, random, time
from pygame.math import Vector2
# Inicializar pygame
pygame.mixer.pre_init(44100, -16, 2, 512) #reprodución la musica cuanod inciia el juego 
pygame.init()
# Colores para el fndo de la pantalla
Verde_claro = (142, 199, 85)  
Verde_oscuro = (168, 220, 92)  
# color para las letras del boton start game
Colores_boton_inicio = (0, 127, 95)  
# Configurar dimensiones de la ventana
Ancho_Pantalla = 700
Alto_Pantalla = 600
#OTROS COLORES
negro=(0,0,0)
blanco=(255,255,255)
size = (Ancho_Pantalla, Alto_Pantalla)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Snake game") # Nombre de la interfaz
sonido_boton = pygame.mixer.Sound("Snake_Kokoa/SonidoBoton.mp3") 
# Cargar la imagen de fondo
imagen_fondo = pygame.image.load("Snake_Kokoa/Imagenes/ImagenFondo.jpg")
# Cargando imagen Manzana
manzana = pygame.transform.scale(pygame.image.load("Snake_Kokoa/Imagenes/manzana.png").convert_alpha(), (40, 35))
# Cargando la imagen de la manzana dorada
manzana_dorada = pygame.transform.scale(pygame.image.load("Snake_Kokoa/Imagenes/ManzanaDorada.png").convert_alpha(), (40, 35))

# Configurar el tamaño del cuadrado del patrón
cell_size = 40
cell_number = 20
# Fuente para los botones (tanto de inicio Start como la pantalla gamee over)
# use la siguiente implementación porque no tengo instlado esta fuenta, la descargue de google font :D
fuente_nueva= "Snake_Kokoa/PressStart2P-Regular.ttf"
tamanio = 25
fuente= pygame.font.Font(fuente_nueva,tamanio)

# Función para dibujar el botón con bordes redondeados
def dibujando_boton(screen, text, rect, color, border_radius, font):
    pygame.draw.rect(screen, color, rect, border_radius=border_radius)
    texto_superficie = font.render(text, True, blanco)
    texto_rect = texto_superficie.get_rect(center=rect.center)
    screen.blit(texto_superficie, texto_rect)

def dibujando_boton2(screen, text, rect, color, border_radius):
    pygame.draw.rect(screen, color, rect, border_radius=border_radius)
    texto_superficie = fuente.render(text, True, negro)
    texto_rect = texto_superficie.get_rect(center=rect.center)
    screen.blit(texto_superficie, texto_rect)

imagen_game_over = pygame.image.load("Snake_Kokoa/Imagenes/game_over.jpg")
imagen_game_over = pygame.transform.scale(imagen_game_over, (450, 180))  

# Función para mostrar la pantalla de game over
def mostrar_pantalla_game_over(screen):
    screen.fill(negro)  # Fondo negro para toda la pantalla

    # Coordenadas centrales del VBox
    vbox_center_x = Ancho_Pantalla // 2
    vbox_start_y = Alto_Pantalla // 4

    # Dibujar la imagen en la parte superior del VBox
    image_rect = imagen_game_over.get_rect(center=(vbox_center_x, vbox_start_y + imagen_game_over.get_height() // 2))
    screen.blit(imagen_game_over, image_rect)

    # Coordenada y del siguiente elemento (botón de reinicio)
    current_y = image_rect.bottom + 30  # 30 píxeles de margen entre elementos

    # Botón para reiniciar
    restart_button_rect = pygame.Rect(vbox_center_x - 100, current_y, 200, 50)
    dibujando_boton2(screen, "Restart", restart_button_rect, (255, 255, 255), border_radius=15)

    # Coordenada y del siguiente elemento (botón de salir)
    current_y = restart_button_rect.bottom + 20  # 20 píxeles de margen entre botones

    # Botón para salir
    boton_salir_react = pygame.Rect(vbox_center_x - 100, current_y, 200, 50)
    dibujando_boton2(screen, "Quit", boton_salir_react, (255, 255, 255), border_radius=15)

    pygame.display.flip()

    return restart_button_rect, boton_salir_react


# Definiendo un Main
class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUTA()
        self.mostrar_mensaje = False
        self.apple_counter = 0  # Contador de manzanas
        self.golden_apple_active = False
        self.golden_apple_start_time = None

    def update(self):
        self.snake.move_snake()
        self.check_fail()
        self.check_collision()
        self.check_golden_apple_timer()

    def draw_elements(self):
        if self.golden_apple_active:
            self.fruit.dibujar_fruta_manza_dorada()
        else:
            self.fruit.dibujar_fruta()
        self.snake.dibujar_serpiente()
        self.contador_manzanas()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            print("Snack")
            self.fruit.randomize_position()
            self.snake.add_block()
            self.apple_counter += 1
            self.mostrar_mensaje = True
            pygame.time.set_timer(pygame.USEREVENT, 2000)
            self.snake.play_crunch_sound()
            if self.apple_counter >= 15 and not self.golden_apple_active:
                self.activate_golden_apple()

    def check_golden_apple_timer(self):
        if self.golden_apple_active and time.time() - self.golden_apple_start_time > 10:
            self.deactivate_golden_apple()

    def activate_golden_apple(self):
        self.golden_apple_active = True
        self.golden_apple_start_time = time.time()
        self.fruit.randomize_position()

    def deactivate_golden_apple(self):
        self.golden_apple_active = False
        self.fruit.randomize_position()
    def check_fail(self):
        # verificamos si chocamos con nuesytro porpio cuerpo
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.snake.game_over()

    def contador_manzanas(self):
        # Dibujar la imagen de la manzana junto al contador
        screen.blit(manzana, (Ancho_Pantalla - 140, 10))
        # Dibujar el contador de manzanas
        counter_surface = fuente.render(str(self.apple_counter), True, negro)
        screen.blit(counter_surface, (Ancho_Pantalla - 80, 15))

# Definiendo una clase para la fruta que come la serpiente
class FRUTA:
    def __init__(self):
        self.randomize_position()

    def dibujar_fruta(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(manzana, fruit_rect)

    def dibujar_fruta_manza_dorada(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(manzana_dorada, fruit_rect)

    def randomize_position(self):
        max_x = Ancho_Pantalla // cell_size - 1
        max_y = Alto_Pantalla // cell_size - 1
        self.x = random.randint(0, max_x)
        self.y = random.randint(0, max_y)
        self.pos = Vector2(self.x, self.y)

def rpedriducir_musica_gameover():
    pygame.mixer.music.pause()
    game_over_sound = pygame.mixer.Sound("Snake_Kokoa/gameovermusic.mp3")  
    game_over_sound.play() 

# Definiendo una clase para crear la estructura de la serpiente 
class SNAKE:

    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(6, 10), Vector2(7, 10)]
        self.direction = Vector2(-1, 0) # asegurarnos de cambiar esta parte para la verificacion de la colision 
        self.new_block = False
        # Cargando imagen para el HEAD serpiente
        self.head_up = pygame.image.load("Snake_Kokoa/Imagenes/head_up.png").convert_alpha()
        self.head_down = pygame.image.load("Snake_Kokoa/Imagenes/head_down.png").convert_alpha()
        self.head_right = pygame.image.load("Snake_Kokoa/Imagenes/head_right.png").convert_alpha()
        self.head_left = pygame.image.load("Snake_Kokoa/Imagenes/head_left.png").convert_alpha()
        # Cargando imagen para el TAIL de la serpiente
        self.tail_up = pygame.image.load("Snake_Kokoa/Imagenes/tail_up.png").convert_alpha()
        self.tail_down = pygame.image.load("Snake_Kokoa/Imagenes/tail_down.png").convert_alpha()
        self.tail_right = pygame.image.load("Snake_Kokoa/Imagenes/tail_right.png").convert_alpha()
        self.tail_left = pygame.image.load("Snake_Kokoa/Imagenes/tail_left.png").convert_alpha()
        # Cargando imagen para el BODY de la serpiente 
        self.body_vertical = pygame.image.load("Snake_Kokoa/Imagenes/body_vertical.png").convert_alpha()
        self.body_horizontal = pygame.image.load("Snake_Kokoa/Imagenes/body_horizontal.png").convert_alpha()
        #Carganndo imagen para el BODY de la serpiente
        self.body_tr = pygame.image.load("Snake_Kokoa/Imagenes/body_topright.png").convert_alpha()
        self.body_tl = pygame.image.load("Snake_Kokoa/Imagenes/body_topleft.png").convert_alpha()
        self.body_br = pygame.image.load("Snake_Kokoa/Imagenes/body_bottomright.png").convert_alpha()
        self.body_bl = pygame.image.load("Snake_Kokoa/Imagenes/body_bottomleft.png").convert_alpha()
        self.crunch_sound = pygame.mixer.Sound("Snake_Kokoa/crunch.mp3")
    # función que se encarga de dar sonido cuando la serpiente coma
    def play_crunch_sound(self):
        self.crunch_sound.play()

    def dibujar_serpiente(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)  # Añadir tamaño del rectángulo
            
            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if (previous_block.x == -1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == -1):
                        screen.blit(self.body_bl, block_rect)
                    elif (previous_block.x == -1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == -1):
                        screen.blit(self.body_tl, block_rect)
                    elif (previous_block.x == 1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == 1):
                        screen.blit(self.body_br, block_rect)
                    elif (previous_block.x == 1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == 1):
                        screen.blit(self.body_tr, block_rect)
  
    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down


    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            new_head = body_copy[0] + self.direction
            body_copy.insert(0, new_head)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            new_head = body_copy[0] + self.direction
            body_copy.insert(0, new_head)
            self.body = body_copy[:]        
        
        # Verificar límites de la ventana en caso de que choque con cualquiera dimension de la ventana 
        if not (0 <= self.body[0].x < Ancho_Pantalla // cell_size) or not (0 <= self.body[0].y < Alto_Pantalla // cell_size):
            self.game_over()

    def add_block(self):
        self.new_block = True
    

    def game_over(self):
        pygame.mixer.music.stop()  # Detener la música actual
        game_over_sound = pygame.mixer.Sound("Snake_Kokoa/gameovermusic.mp3") 
        game_over_sound.play()  # Reproducir la nueva canción

        while True:
            restart_button_rect, quit_button_rect = mostrar_pantalla_game_over(screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button_rect.collidepoint(event.pos):
                        # Reiniciar el juego
                        main_game.__init__()
                        # variable para el tiempo
                        global start_time
                        start_time= time.time
                        return  # Salir del bucle y volver al juego
                    if quit_button_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
            
            pygame.time.Clock().tick(15)


def play(): # funcion para cuando empiece 
    # Creando una instancia de main
    main_game = MAIN()
    # Variables de control
    running = True
    game_started = False
    start_time = 0
    
    # Rectángulo del botón de "empezar" (más grande)
    buoton_ancho = 235
    button_alto = 95
    start_button_rect = pygame.Rect(35, Alto_Pantalla - button_alto - 35, buoton_ancho, button_alto)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    sonido_boton.play()
                    pygame.time.delay(1000)  # Retraso de 1 segundo (1000 milisegundos)
                    game_started = True
                    start_time = time.time()  # Iniciar el cronómetro
                
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if main_game.snake.direction.y != 1:  # Evitar moverse en la dirección opuesta
                        main_game.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_RIGHT:
                    if main_game.snake.direction.x != -1:  # Evitar moverse en la dirección opuesta
                        main_game.snake.direction = Vector2(1, 0)
                if event.key == pygame.K_DOWN:
                    if main_game.snake.direction.y != -1:  # Evitar moverse en la dirección opuesta
                        main_game.snake.direction = Vector2(0, 1)
                if event.key == pygame.K_LEFT:
                    if main_game.snake.direction.x != 1:  # Evitar moverse en la dirección opuesta
                        main_game.snake.direction = Vector2(-1, 0)
            if event.type == pygame.USEREVENT:
                main_game.mostrar_mensaje= False
                pygame.time.set_timer(pygame.USEREVENT, 0)       
        screen.fill((0,0,0))
        if  not game_started:
            screen.blit(imagen_fondo, [0, 0])
            pygame.display.set_caption("Inciio") # cambiar el titulo de la pantalla principal

            dibujando_boton(screen, "Start", start_button_rect, Colores_boton_inicio, border_radius=35, font=fuente)
        else: 
            # Dibujar el patrón
            for x in range(0, Ancho_Pantalla, cell_size):
                for y in range(0, Alto_Pantalla, cell_size):
                    rect = pygame.Rect(x, y, cell_size, cell_size)
                    if (x // cell_size + y // cell_size) % 2 == 0:
                        pygame.draw.rect(screen, Verde_claro, rect)
                    else:
                        pygame.draw.rect(screen, Verde_oscuro, rect)
            main_game.update()
            pygame.display.set_caption("Snake")

            # Calcular el tiempo transcurrido
            elapsed_time = time.time() - start_time
            minutos = int(elapsed_time // 60)
            segundos = int(elapsed_time % 60)

            # Renderizar el cronómetro
            texto_Reloj = fuente.render(f"Time: {minutos:02}:{segundos:02}", True, negro)
            screen.blit(texto_Reloj, (10, 10))

            main_game.draw_elements()
        
        pygame.display.flip() 
        pygame.time.Clock().tick(15)
        

    
play()
pygame.quit()
sys.exit()

