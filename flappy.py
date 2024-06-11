import pygame
import random
import sys

#prueba github
#prueba rama luis 2
# Inicializar Pygame
pygame.init()

# Configuraciones generales
infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
pajaro_WIDTH, pajaro_HEIGHT = 40, 30
tuberia_WIDTH, tuberia_HEIGHT = 70, 400
espacio_tuberia = 300
gravedad = 0.25
salto = -6
colorFondo = (135, 206, 250)
color_pajaro = (255, 0, 100)
color_tuberia = (0, 128, 0)
pajaro_img = pygame.image.load("src/flappy.png")
pajaro_img = pygame.transform.scale(pajaro_img, (60, 40))

# Variables globales para el puntaje y la velocidad de las tuberías
puntaje = 0
velocidad_tuberia = 3
FPS = 80  # Definir FPS globalmente

# Función para crear tuberías cercanas al pájaro
def crearTuberiaCercana(pajaro_y):
    margen = 50  # Margen de seguridad para evitar que el agujero esté demasiado cerca del borde de la pantalla
    random_height = random.randint(max(100, pajaro_y - 200), min(pajaro_y + 200, HEIGHT - espacio_tuberia - margen))
    tuberia_superior = pygame.Rect(WIDTH, 0, tuberia_WIDTH, random_height)
    tuberia_inferior = pygame.Rect(WIDTH, random_height + espacio_tuberia, tuberia_WIDTH, HEIGHT - random_height - espacio_tuberia)
    return tuberia_superior, tuberia_inferior

# Función para mostrar el menú de inicio
def mostrarMenuInicio(pantalla):
    font = pygame.font.Font(None, 36)
    texto_titulo = font.render("Pajaro Volador", True, (255, 255, 255))
    texto_inicio = font.render("Haga click o presione espacio para empezar", True, (255, 255, 255))
    pantalla.blit(texto_titulo, (WIDTH//2 - texto_titulo.get_width()//2, HEIGHT//2 - 50))
    pantalla.blit(texto_inicio, (WIDTH//2 - texto_inicio.get_width()//2, HEIGHT//2 + 50))
    pygame.display.flip()
    contador = True
    while contador:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                contador = False

# Función para mostrar el menú de reinicio
def mostrarMenuReinicio(pantalla, puntaje):
    font = pygame.font.Font(None, 36)
    texto_perdiste = font.render("¡Perdiste!", True, (255, 255, 255))
    texto_reiniciar = font.render("Presiona R para reiniciar o ESCAPE para salir", True, (255, 255, 255))
    texto_puntaje = font.render(f"Puntaje: {int(puntaje)}", True, (255, 255, 255))
    pantalla.blit(texto_perdiste, (WIDTH//2 - texto_perdiste.get_width()//2, HEIGHT//2 - 50))
    pantalla.blit(texto_reiniciar, (WIDTH//2 - texto_reiniciar.get_width()//2, HEIGHT//2 + 50))
    pantalla.blit(texto_puntaje, (WIDTH//2 - texto_puntaje.get_width()//2, HEIGHT//2 + 100))
    pygame.display.flip()
    contador = True
    while contador:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# Función principal del juego
def main():
    global puntaje, velocidad_tuberia, espacio_tuberia, FPS  # Asegurarse de que FPS sea global

    puntaje = 0
    espacio_tuberia = 150
    velocidad_tuberia = 3  # Velocidad inicial de las tuberías

    pantalla = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    tiempo = pygame.time.Clock()
    pajaro = pygame.Rect(100, HEIGHT // 2, pajaro_WIDTH, pajaro_HEIGHT)
    tuberias = []
    pajaro_movimiento = 0

    # Variables para controlar la velocidad de aparición de tuberías
    contador_tuberia = 0
    frecuencia_tuberia = 1500  # Ajusta esto para cambiar la frecuencia de aparición de tuberías
    incremento_aplicado = False  # Bandera para controlar el incremento de velocidad de tuberías y espacio_tuberia

    # Mostrar menú de inicio
    mostrarMenuInicio(pantalla)

    while True:
        tiempo.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pajaro_movimiento = salto
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pajaro_movimiento = salto

        # Movimiento del pájaro
        pajaro_movimiento += gravedad
        pajaro.y += pajaro_movimiento

        # Verificar si el pájaro ha muerto
        if pajaro.top <= 0 or pajaro.bottom >= HEIGHT:
            if mostrarMenuReinicio(pantalla, puntaje):
                return main()

              # Generar tuberías cercanas al pájaro
        contador_tuberia += tiempo.get_time()
        if contador_tuberia > frecuencia_tuberia:
            tuberia_superior, tuberia_inferior = crearTuberiaCercana(pajaro.y)
            tuberias.append(tuberia_superior)
            tuberias.append(tuberia_inferior)
            contador_tuberia = 0


        # Aumentar la velocidad del juego y el espacio de las tuberías cada 7 puntos
        if int(puntaje) % 7 == 0 and int(puntaje) != 0:
            if not incremento_aplicado:
                if velocidad_tuberia <= 10:
                    velocidad_tuberia += 1
                espacio_tuberia +=5
                incremento_aplicado = True
        else:
            incremento_aplicado = False

        # Mover tuberías
        nuevas_tuberias = []
        for tuberia in tuberias:
            tuberia.x -= velocidad_tuberia
            if tuberia.x + tuberia_WIDTH > 0:
                nuevas_tuberias.append(tuberia)
            else:
                puntaje += 0.5

        tuberias = nuevas_tuberias

        # Dibujar elementos
        pantalla.fill(colorFondo)
        for tuberia in tuberias:
            pygame.draw.rect(pantalla, color_tuberia, tuberia)
        pantalla.blit(pajaro_img, (pajaro.x, pajaro.y))

        # Colisiones
        for tuberia in tuberias:
            if pajaro.colliderect(tuberia):
                if mostrarMenuReinicio(pantalla, puntaje):
                    return main()

        # Mostrar puntaje
        font = pygame.font.Font(None, 36)
        texto_puntaje = font.render(f"Puntaje: {int(puntaje)}", True, (255, 255, 255))
        pantalla.blit(texto_puntaje, (10, 10))

        pygame.display.flip()

# Iniciar el juego
if __name__ == "__main__":
    main()
