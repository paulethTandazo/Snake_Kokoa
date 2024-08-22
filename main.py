import pygame,sys, random
from pygame.math import Vector2

# Inicializar pygame
pygame.mixer.pre_init(44100, -16, 2, 512) #reprodución la musica
pygame.init() # inicializando el juego

# COLORES A USAR PARA EL FONDO
verde_claro=(142,199,85) 
verde_oscuro=(168,220,92)
# COLORES PARA EL BOTON DE INICIO
color_boton_inicio= (0,127,95)
Blanco= (255,255,255)
Negro= (0,0,0)
# Configurarando dimensiones para la ventana 
Ancho= 700
Alto= 600
size_pantalla = (Ancho,Alto)
screen = pygame.display.set_mode(size_pantalla)
pygame.display.set_caption("Snake Game")
# Sonido de inicio
sonido_boton= pygame.mixer.Sound("Sonido.mp3")
#Cargando el fondo 
imagen_fondo= pygame.image.load("ImagenFondo.jpg")
#Cargando la imagen de la manzana
manzana= pygame.transform.scale(pygame.image.load("manzana.png").convert_alpha(), (40,20))
#FUENTE DEL BOTON DE INICIO Y FUENTE GENERAL
fuente_boton= pygame.font.SysFont("PressStart2P-Regular.ttf",36)
#
# CREANDO BOTON DEL START
def dibujando_boton(screen,text,rect,color,border_Radius,font):
    pygame.draw.rect(screen,color,rect,border_radius=border_Radius)
    text_superficie= font.render(text,True,Blanco)
    texto_rect= text_superficie.get_rect(center=rect.center)
    screen.blit(text_superficie,texto_rect)
# Configurando Rectangulo para el boton empezar
boton_ancho=235
boton_alto= 95
empezar_boton= pygame.Rect(35,Alto - boton_alto -35,boton_ancho, boton_alto)


class FRUTA:
    def __init__(self):
        self.x=random.randint(0,cell_number -1)
        self.y=random.randint(0,cell_number -1)
        self.pos= Vector2(self.x,self.y)
    def dibujando_fruta(self):
        fruit_rect = pygame.Rect(int(self.pos.x *cell_size),int(self.pos.y * cell_size),cell_size, cell_size)
        pygame.draw.rect(screen,(126,166,114), fruit_rect)

cell_size=40 #tamaño de la celda para formar el patron
cell_number=20

fruta= FRUTA()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.QUIT()
            sys.exit()
        for x in range(0, 700, cell_size):
            for y in range(0, 600, cell_size):
                rect = pygame.Rect(x, y, cell_size, cell_size)
                if (x // cell_size + y // cell_size) % 2 == 0:
                    pygame.draw.rect(screen, verde_claro, rect)
                else:
                    pygame.draw.rect(screen, verde_oscuro, rect)
        
        dibujando_boton(screen, "Start",empezar_boton, color_boton_inicio,border_Radius=25, font=fuente_boton)
    screen.fill((175,215,70)) 
    fruta.dibujando_fruta
    pygame.display.flip()
    pygame.time.Clock().tick(15) #Vecloidad de actualización
    
    pygame.quit()
    sys.exit()