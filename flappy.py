import pygame
import random
import sys

# Inicializar Pygame
pygame.init()


# Inicializar el mezclador de sonido
pygame.mixer.init()

# Configuraciones generales
infoObject = pygame.display.Info()
ANCHO, ALTURA = infoObject.current_w, infoObject.current_h
ancho_pajaro, altura_pajaro = 40, 30
ancho_tuberia, altura_tuberia = 70, 400
espacio_tuberia = 300
gravedad = 0.25
salto = -6
color_fondo = (135, 206, 250)
color_pajaro = (255, 0, 100)
color_tuberia = (0, 128, 0)
imagen_pajaro = pygame.image.load("C:/Users/Usuario/OneDrive/Documentos/python1/final/Flappy/src/flappy.png")
imagen_pajaro = pygame.transform.scale(imagen_pajaro, (60, 40))

sonido_punto = pygame.mixer.Sound('C:/Users/Usuario/OneDrive/Documentos/python1/final/Flappy/src/pajaro_sonido2.wav') 

# Variables globales para el puntaje y la velocidad de las tuberías
puntaje = 0
velocidad_tuberia = 3
FPS = 80  # Definir FPS globalmente

# Función para crear tuberías cercanas al pájaro
def crearTuberiaCercana(pajaro_y):
    margen = 50  # Margen de seguridad para evitar que el agujero esté demasiado cerca del borde de la pantalla
    random_height = random.randint(max(50, pajaro_y - 150), min(pajaro_y + 150, ALTURA - espacio_tuberia - margen))
    tuberia_superior = pygame.Rect(ANCHO, 0, ancho_tuberia, random_height)
    tuberia_inferior = pygame.Rect(ANCHO, random_height + espacio_tuberia, ancho_tuberia, ALTURA - random_height - espacio_tuberia)
    return tuberia_superior, tuberia_inferior



# Función para mostrar el menú de inicio
def mostrarMenuInicio(pantalla):
    font = pygame.font.Font(None, 36)
    texto_titulo = font.render("Pajaro Volador", True, (255, 255, 255))
    texto_inicio = font.render("Haga click o presione espacio para empezar", True, (255, 255, 255))
    pantalla.blit(texto_titulo, (ANCHO // 2 - texto_titulo.get_width() // 2, ALTURA // 2 - 50))
    pantalla.blit(texto_inicio, (ANCHO // 2 - texto_inicio.get_width() // 2, ALTURA // 2 + 50))
    pygame.display.flip()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE):
                return

# Función para mostrar el menú de reinicio
def mostrarMenuReinicio(pantalla, puntaje):
    font = pygame.font.Font(None, 36)
    texto_perdiste = font.render("¡Perdiste!", True, (255, 255, 255))
    texto_reiniciar = font.render("Presiona R para reiniciar o ESCAPE para salir", True, (255, 255, 255))
    texto_puntaje = font.render(f"Puntaje: {int(puntaje)}", True, (255, 255, 255))
    pantalla.blit(texto_perdiste, (ANCHO // 2 - texto_perdiste.get_width() // 2, ALTURA // 2 - 50))
    pantalla.blit(texto_reiniciar, (ANCHO // 2 - texto_reiniciar.get_width() // 2, ALTURA // 2 + 50))
    pantalla.blit(texto_puntaje, (ANCHO // 2 - texto_puntaje.get_width() // 2, ALTURA // 2 + 100))
    pygame.display.flip()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    return True
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# Función para mostrar el menú de pausa
def mostrarMenuPausa(pantalla, pausa):
    font = pygame.font.Font(None, 36)
    texto_pausa = font.render("Juego Pausado", True, (255, 255, 255))
    if pausa:
        texto_continuar = font.render("Presiona P para continuar o S para salir", True, (255, 255, 255))
    else:
        texto_continuar = font.render("Presiona P para pausar o S para salir", True, (255, 255, 255))
    pantalla.blit(texto_pausa, (ANCHO // 2 - texto_pausa.get_width() // 2, ALTURA // 2 - 50))
    pantalla.blit(texto_continuar, (ANCHO // 2 - texto_continuar.get_width() // 2, ALTURA // 2 + 50))
    pygame.display.flip()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p:
                    return False  # Continuar o pausar el juego
                elif evento.key == pygame.K_s:
                    pygame.quit()
                    sys.exit()


# Función principal del juego
def main():
    global puntaje, velocidad_tuberia, espacio_tuberia, FPS  # Asegurarse de que FPS sea global

    puntaje = 0
    espacio_tuberia = 150
    velocidad_tuberia = 3  # Velocidad inicial de las tuberías

    pantalla = pygame.display.set_mode((ANCHO, ALTURA), pygame.FULLSCREEN)
    tiempo = pygame.time.Clock()
    pajaro = pygame.Rect(100, ALTURA // 2, ancho_pajaro, altura_pajaro)
    tuberias = []
    movimiento_pajaro = 0

    # Variables para controlar la velocidad de aparición de tuberías
    contador_tuberia = 0
    frecuencia_tuberia = 1500  # Ajusta esto para cambiar la frecuencia de aparición de tuberías
    incremento_aplicado = False  # Bandera para controlar el incremento de velocidad de tuberías y espacio_tuberia

    # Mostrar menú de inicio
    mostrarMenuInicio(pantalla)

    while True:
        tiempo.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    movimiento_pajaro = salto
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    movimiento_pajaro = salto
                elif evento.key == pygame.K_p:
                    if mostrarMenuPausa(pantalla, True):
                        return main()  # Reiniciar el juego si se selecciona salir desde el menú de pausa

        # Movimiento del pájaro
        movimiento_pajaro += gravedad
        pajaro.y += movimiento_pajaro

        # Verificar si el pájaro ha muerto
        if pajaro.top <= 0 or pajaro.bottom >= ALTURA:
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
                espacio_tuberia -= 5  # Reducir el espacio entre tuberías
                incremento_aplicado = True
        else:
            incremento_aplicado = False

        # Mover tuberías
        nuevas_tuberias = []
        for tuberia in tuberias:
            tuberia.x -= velocidad_tuberia
            if tuberia.x + ancho_tuberia > 0:
                nuevas_tuberias.append(tuberia)
                # Verificar si el pájaro pasa entre las tuberías y aumentar el puntaje
                if tuberia.x + ancho_tuberia < pajaro.x <= tuberia.x + ancho_tuberia + velocidad_tuberia:
                    if puntaje > 0:
                        sonido_punto.play()
                    if tuberia.y == 0:  # Solo contar la tubería superior para el puntaje
                        puntaje += 1
            else:
                # Cuando la tubería sale de la pantalla, eliminarla de la lista
                del tuberia
        tuberias = nuevas_tuberias

        # Dibujar elementos
        pantalla.fill(color_fondo)
        for i in range(0, len(tuberias), 2):
            pygame.draw.rect(pantalla, color_tuberia, tuberias[i])
            pygame.draw.rect(pantalla, color_tuberia, tuberias[i+1])
        pantalla.blit(imagen_pajaro, (pajaro.x, pajaro.y))

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

if __name__ == "__main__":
    main()