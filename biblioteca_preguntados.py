from datos import *
import pygame
import sys
from pygame.locals import *

pygame.init()

config_pantalla = [1280,720]
pygame.display.set_caption("Menu")
pantalla = pygame.display.set_mode(config_pantalla)
fondo = pygame.image.load("preguntados/fondo.png")
fondo_preguntas = pygame.image.load("preguntados/fondo_preguntas.png")
fondo_ranking = pygame.image.load ("preguntados/fondo_ranking.png")
fondo_nombre = pygame.image.load ("preguntados/fondo_nombre.png")
fuente = pygame.font.SysFont("Doppio One",40)

#SONIDOS
musica = pygame.mixer.music.load("preguntados/musica.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)
sonido_correcto =pygame.mixer.Sound("preguntados/correcto.mp3")
sonido_incorrecto = pygame.mixer.Sound("preguntados/incorrecto.mp3")


#BOTONES
tamaño_boton = [400,100]
imagen_boton = pygame.image.load("preguntados/boton.png")
imagen_boton = pygame.transform.scale(imagen_boton,(tamaño_boton))
tamaño_boton_lila = [250,80]
imagen_boton_lila = pygame.image.load("preguntados/boton_lila.png")
imagen_boton_lila = pygame.transform.scale(imagen_boton_lila,(tamaño_boton_lila))
color_violeta = (50, 0, 137)


class Boton():
    def __init__ (self, image, pos_x, pos_y, insertar_texto):
        '''
        Inicializa un objeto Boton con la imagen, posición, texto y pantalla. Se les asignan las variables a los atributos

        Args:
        image: Imagen del botón.
        pos_x (int): Posición horizontal del centro del botón.
        pos_y (int): Posición vertical del centro del botón.
        insertar_texto (str): Texto que se mostrará en el botón.
        '''
        #Se les asignan las variables a los atributos
        self.imagen = image
        self.posicion_x = pos_x
        self.posicion_y = pos_y
        self.rectangulo = self.imagen.get_rect(center=(self.posicion_x, self.posicion_y))
        self.insertar_texto = insertar_texto
        self.texto = fuente.render(self.insertar_texto,True,"white")
        self.texto_rectangulo = self.texto.get_rect (center=(self.posicion_x, self.posicion_y))
        self.pantalla = pantalla
    
    def actualizar(self):
        '''
        Actualiza la representación gráfica del botón en la pantalla.
        '''
        pantalla.blit(self.imagen, self.rectangulo)
        pantalla.blit(self.texto, self.texto_rectangulo)

    def presionar(self, posicion):
        '''
        Verifica si el botón fue presionado.

        Args:
        posicion: Posición del cursor (x, y).

        Returns:
        bool: True si el botón ha sido presionado, False en caso contrario.
        '''

        if posicion[0] in range (self.rectangulo.left,self.rectangulo.right) and posicion[1] in range (self.rectangulo.top, self.rectangulo.bottom):
            return self.rectangulo.collidepoint(posicion)

        
    def cambiar_color(self, posicion):
        '''
        Cambia el color del texto del botón según la posición del cursor.

        Args:
        posicion: Posición del cursor (x, y).
        '''

        if posicion[0] in range (self.rectangulo.left,self.rectangulo.right) and posicion[1] in range (self.rectangulo.top, self.rectangulo.bottom):
            self.texto = fuente.render(self.insertar_texto,True,color_violeta)
        else:
            self.texto = fuente.render(self.insertar_texto,True,"white")


def mostrar_pregunta(indice, intentos, puntaje, estado_respuestas):
    '''
    Dibuja la pregunta actual y las opciones en la pantalla de juego.
    Muestra el número de intentos restantes y el puntaje actual del jugador en la pantalla del juego.

    Args:
    indice: Entero que indica el índice de la pregunta actual en la lista de preguntas.
    intentos: Entero que representa el número actual de intentos disponibles para responder la pregunta.
    puntaje: Entero que indica el puntaje acumulado por el jugador hasta el momento.
    estado_respuestas: Diccionario que indica el estado de cada opción ('correcta', 'incorrecta', 'oculta').
    '''
    pantalla.blit(fondo_preguntas, (0, 0))
    pregunta_actual = lista[indice]
    texto_pregunta = fuente.render(pregunta_actual['pregunta'], True, (230, 216, 255))
    pantalla.blit(texto_pregunta, (50, 200))

    opciones = ['a', 'b', 'c']
    i = 0
    for opcion in opciones:
        texto_opcion = fuente.render(f"{opcion}. {pregunta_actual[opcion]}", True, (230, 216, 255))
        if estado_respuestas[opcion] == 'oculta':
            texto_opcion.set_alpha(0)  # Ajusta la opacidad aquí
        pantalla.blit(texto_opcion, (50, 300 + i * 70))
        i += 1

    texto_intentos = fuente.render(f"Intentos: {intentos}", True, (230, 216, 255))
    pantalla.blit(texto_intentos, (800, 100))
    texto_puntaje = fuente.render(f"Puntaje: {puntaje}", True, (230, 216, 255))
    pantalla.blit(texto_puntaje, (250, 100))

def pedir_nombre():
    '''
    Muestra una interfaz  donde el jugador puede ingresar su nombre al finalizar el juego.
    Muestra un mensaje en pantalla indicando al jugador que ingrese su nombre después de que el juego ha terminado.
    El jugador puede ingresar caracteres usando el teclado. Presionar Enter finaliza la entrada del nombre.

    Returns:
    str: El nombre ingresado por el jugador.
    '''
    pantalla.blit(fondo_nombre, (0, 0))
    texto_ingreso = fuente.render("¡Juego terminado! Ingrese su nombre:", True, (255, 255, 255))
    pantalla.blit(texto_ingreso, (250, 300))
    pygame.display.update()

    nombre = ""
    ingresando_nombre = True
    while ingresando_nombre == True :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                #ENTER
                if event.key == pygame.K_RETURN:
                    ingresando_nombre = False
                #BORRAR
                elif event.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                #OTRA TECLA
                else:
                    nombre += event.unicode

        pantalla.blit(fondo_nombre, (0, 0))
        texto_ingreso = fuente.render("¡Juego terminado! Ingrese su nombre:", True, (255, 255, 255))
        pantalla.blit(texto_ingreso, (250, 250))
        texto_nombre = fuente.render(nombre, True, (255, 255, 255))
        pantalla.blit(texto_nombre, (250, 300))
        pygame.display.update()

    return nombre


def jugar():
    '''
    Maneja la lógica principal del juego, incluyendo la visualización de preguntas, la selección de respuestas y la gestión del puntaje e intentos.
    Cuando el jugador pulse el botón 'Pregunta' va a mostrar las preguntas secuencialmente, permite al jugador seleccionar respuestas y verificar su corrección, actualiza el puntaje y el número de intentos, cuando se agoten los intentos en una pregunta va automáticamente a la siguiente pregunta.
    Al finalizar todas las preguntas, guarda el puntaje del jugador en un archivo y muestra el menú principal.
    '''
    pygame.display.set_caption("Preguntados")
    indice_pregunta = -1
    intentos = 2 #CONTADOR
    puntaje = 0 #ACUMULADOR
    juego_terminado = False

    def estado_respuestas():
        '''
        Inicializa el estado de las respuestas para las opciones 'a', 'b' y 'c'.
        Returns:
        dict: Un diccionario con las claves 'a', 'b' y 'c' inicializadas con cadenas vacías.
        '''
        return { 'a': '', 'b': '', 'c': '' }

    
    estado_respuestas_actual = estado_respuestas()
    boton_pregunta = Boton(imagen_boton, 350, 600, "Pregunta")
    boton_reiniciar = Boton(imagen_boton, 900, 600, "Reiniciar")

    while True:
        pos_mouse = pygame.mouse.get_pos()
        pantalla.blit(fondo_preguntas, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #BOTON PREGUNTA
                if boton_pregunta.presionar(pos_mouse):
                    if not juego_terminado:
                        indice_pregunta += 1
                        if indice_pregunta < len(lista):
                            estado_respuestas_actual = estado_respuestas()
                        mostrar_pregunta(indice_pregunta, intentos, puntaje, estado_respuestas_actual)
                        if indice_pregunta >= len(lista):
                            juego_terminado = True
                #BOTON REINICIAR
                elif boton_reiniciar.presionar(pos_mouse):
                    indice_pregunta = 0
                    intentos = 2
                    puntaje = 0
                    juego_terminado = False
                    estado_respuestas_actual = estado_respuestas()
                #JUEGO
                else:
                    if not juego_terminado and indice_pregunta >= 0:
                        opciones = {0: 'a', 1: 'b', 2: 'c'}
                        # Se va a iterar manualmente sobre las opciones 'a', 'b' y 'c'
                        for i in range(3):
                            opcion_y = 300 + i * 70
                            if 50 <= event.pos[0] <= 450 and opcion_y <= event.pos[1] < opcion_y + 50:
                                opcion_actual = opciones[i]
                                if estado_respuestas_actual[opcion_actual] == 'oculta':
                                    continue
                                #CORRECTO
                                if lista[indice_pregunta]['correcta'] == opcion_actual:
                                    puntaje += 10
                                    sonido_correcto.play()
                                    estado_respuestas_actual = { 'a': 'oculta', 'b': 'oculta', 'c': 'oculta' }
                                    estado_respuestas_actual[opcion_actual] = 'correcta'
                                    mostrar_pregunta(indice_pregunta, intentos, puntaje, estado_respuestas_actual)
                                    indice_pregunta += 1
                                    intentos = 2
                                    if indice_pregunta < len(lista):
                                        estado_respuestas_actual = estado_respuestas()
                                    else:
                                        juego_terminado = True
                                        nombre = pedir_nombre()
                                        with open("preguntados/puntajes.txt", "a") as archivo:
                                            archivo.write(f"{nombre}, {puntaje}\n")
                                        pygame.display.set_caption("Menu")
                                        menu()
                                #INCORRECTO
                                else:
                                    sonido_incorrecto.play()
                                    intentos -= 1
                                    estado_respuestas_actual[opcion_actual] = 'oculta'
                                    mostrar_pregunta(indice_pregunta, intentos, puntaje, estado_respuestas_actual)
                                    if intentos == 0:
                                        indice_pregunta += 1
                                        intentos = 2
                                        if indice_pregunta < len(lista):
                                            estado_respuestas_actual = estado_respuestas()
                                        else:
                                            juego_terminado = True
                                            nombre = pedir_nombre()

                                            with open("preguntados/puntajes.txt", "a") as archivo:
                                                archivo.write(f"{nombre}, {puntaje}\n")
                                            
                                            pygame.display.set_caption("Menu")
                                            menu()
        #MOSTRAR LA PREGUNTA
        if not juego_terminado and indice_pregunta >= 0:
            mostrar_pregunta(indice_pregunta, intentos, puntaje, estado_respuestas_actual)

        boton_pregunta.cambiar_color(pos_mouse)
        boton_reiniciar.cambiar_color(pos_mouse)
        boton_pregunta.actualizar()
        boton_reiniciar.actualizar()
        pygame.display.update()

def ranking():
    '''
    Muestra los puntajes más altos registrados en el juego, ordenados de mayor a menor puntaje.
    Lee los puntajes, los ordena de mayor a menor y muestra los tres puntajes más altos en la pantalla.
    Permite al jugador volver al menú principal para continuar o salir del juego.
    '''
    pygame.display.set_caption("Puntajes")
    pantalla.blit(fondo_ranking, (0, 0))

    #ABRIR
    with open("preguntados/puntajes.txt", "r") as archivo:
        puntajes = []
        for linea in archivo:
            nombre, puntaje = linea.strip().split(",")
            puntajes.append((nombre, int(puntaje)))

    #ORDENAR
    for i in range(len(puntajes)):
        for j in range(i + 1, len(puntajes)):
            if puntajes[i][1] < puntajes[j][1]:
                # SWAP
                aux = puntajes[i]
                puntajes[i] = puntajes[j]
                puntajes[j] = aux

    #CONTAR Y DEVOLVER
    contador = 0
    for i in range(len(puntajes)):
        if contador >= 3:
            break
        nombre = puntajes[i][0]
        puntaje = puntajes[i][1]
        texto_puntaje = fuente.render(f"{nombre}: {puntaje}", True, (233, 252, 255))
        pantalla.blit(texto_puntaje, (760, 160 + contador * 70))
        contador += 1

    boton_volver = Boton(imagen_boton_lila, 1100, 650, "Volver")
    while True:
        pos_mouse = pygame.mouse.get_pos()
        boton_volver.cambiar_color(pos_mouse)
        boton_volver.actualizar()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_volver.presionar(pos_mouse):
                    pygame.display.set_caption("Menu")
                    menu()
        pygame.display.update()


def menu():
        '''
        Esta función muestra el menú principal del juego, donde el jugador puede elegir entre jugar, ver el ranking de puntajes más altos o salir del juego.
        Va a permanecer en el bucle hasta que el jugador decida salir del juego.
        '''
        while True:
            pantalla.blit(fondo, (0,0))
            pos_mouse = pygame.mouse.get_pos()
            boton_juego = Boton(imagen_boton,1000,150,"Jugar")
            boton_ranking = Boton(imagen_boton,1000,350,"Ver puntajes")
            boton_salir = Boton(imagen_boton,1000,550,"Salir")

            for boton in [boton_juego, boton_ranking, boton_salir]:
                boton.cambiar_color(pos_mouse)
                boton.actualizar()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if boton_juego.presionar(pos_mouse):
                        jugar()
                    elif boton_ranking.presionar(pos_mouse):
                        ranking()
                    elif boton_salir.presionar(pos_mouse):
                        pygame.quit()
                        sys.exit()
            
            pygame.display.update()