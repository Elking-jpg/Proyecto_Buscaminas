import random
from typing import Any
import os
from queue import Queue as Cola
 
# Constantes para dibujar
BOMBA = chr(128163)  # simbolo de una mina
BANDERA = chr(127987)  # simbolo de bandera blanca
VACIO = " "  # simbolo vacio inicial
 
# Tipo de alias para el estado del juego
EstadoJuego = dict[str, Any]
 
def existe_archivo(ruta_directorio: str, nombre_archivo:str) -> bool:
    """Chequea si existe el archivo en la ruta dada"""
    return os.path.exists(os.path.join(ruta_directorio, nombre_archivo))



"""
FUNCION split
RECIBE: una linea de texto de tipo string
DEVUELVE: una lista de strings extraída de la linea original, pero tomando los caracteres ',' como delimitador
"""
def split(linea: str) -> list[str]:
    res: list[str] = []
    actual: str = ""
    i: int = 0
    while i < len(linea):
        if linea[i] == ',' or linea[i] == '\n':
            res.append(actual)
            actual = ""
        else:
            actual = actual + linea[i]
        i += 1
    if actual != "":
        res.append(actual)
    return res


"""
FUNCION join
RECIBE: una lista de strings
DEVUELVE: una linea de texto de tipo string que corresponde a unir los elementos de la lista separados cada uno por un caracter ','
"""
def join(lista: list[str]) -> str:
    res: str = ""
    i: int = 0
    while i < len(lista):
        res = res + lista[i]
        if i < len(lista) - 1:
            res = res + ","
        i += 1
    return res
 

#------------------------------------------------------------------------
#--------------------- ejercicio 1) colocar_minas() ---------------------
#------------------------------------------------------------------------

"""
FUNCION colocar_minas
RECIBE: tres enteros; el número de filas, el número de columnas, y el número de minas que se utilizarán en el juego
DEVUELVE: una matriz de caracteres de dimensión filas x columnas que contiene una cantidad filas*columnas-minas caracteres '0' y una cantidad minas de caracteres '*',
donde los caracteres de tipo '*' han sido colocados de forma aleatoria en la matriz. Esta matriz en nuestro contexto representa el estado primitivo del tablero del juego.
"""
def colocar_minas(filas:int, columnas: int, minas:int) -> list[list[int]]:
    posiciones_validas: list[tuple[int,int]] = []
    tablero: list[list[int]] = []
    for i in range(filas):
        fila_ceros: list[int] = []
        for j in range(columnas):
            fila_ceros.append(0)
            pos: tuple[int,int] = (i,j)
            posiciones_validas.append(pos)
        tablero.append(fila_ceros)
 
    posiciones_minas: list[tuple[int,int]] = random.sample(posiciones_validas, minas)
    for pos in posiciones_minas:
        i, j = pos
        tablero[i][j] = -1
 
    return tablero
 
#-------------------------------------------------------------------------
#-------------------- ejercicio 2) calcular_numeros() --------------------
#-------------------------------------------------------------------------


"""
FUNCION colocar_minas
RECIBE: una matriz de caracteres de dimensión filas x columnas que contiene caracteres de tipo '0' y caracteres de tipo '*' donde los caracteres de tipo '0' representan un espacio vacío
y los caracteres de tipo '*' representan una mina
MODIFICA: la matriz original en la cual se ven reemplazados los valores de tipo '0' por la cantidad de valores tipo '*' adyacentes, donde adyacente significa que está en alguna de las casillas
entre (x-1,y-1) y (x+1,y+1)
NO DEVUELVE NADA
"""
def calcular_numeros(tablero: list[list[int]]) -> None:
    filas: int = len(tablero)
    columnas: int = len(tablero[0])
    adyacentes: list[tuple[int,int]] = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    for i in range(filas):
        for j in range(columnas):
            if tablero[i][j] == -1:
                for dx,dy in adyacentes:
                    x: int = i+dx
                    y: int = j+dy
                    if (0 <= x < filas and 0 <= y < columnas):
                        if tablero[x][y] != -1:
                            tablero[x][y] = tablero[x][y]+1
    return
 
#-------------------------------------------------------------------------
#---------------------- ejercicio  3) crear_juego() ----------------------
#-------------------------------------------------------------------------

"""
FUNCION crear_juego
RECIBE: tres enteros, filas, columas y minas
DEVUELVE: un valor de tipo EstadoJuego que es en sí un diccionario que describe el actual estado del juego recién creado.
"""
def crear_juego(filas:int, columnas:int, minas:int) -> EstadoJuego:
    tablero : list[list[int]] = colocar_minas(filas, columnas, minas)
    calcular_numeros(tablero)
    tablero_visible: list[list[str]] = []
    for _ in range(filas):
        fila_aux: list[str] = []
        for _ in range(columnas):
            fila_aux.append(VACIO)
        tablero_visible.append(fila_aux)
 
    res: EstadoJuego = {
        "filas": filas,
        "columnas": columnas,
        "minas": minas,
        "juego_terminado": False,
        "tablero": tablero,
        "tablero_visible": tablero_visible
    }
    return res


"""
FUNCION todas_celdas_seguras_descubiertas
RECIBE una matriz de enteros que representa al tablero y una matriz de strings que representa al tablero visible
DEVUELVE:
    · True si todas las celdas en tablero que contengan un valor entre 0 y 9 tienen el mismo valor pero de tipo string en la posición correspondiente en el tablero_visible
    · False si al menos una celda en tablero que contenga un valor entre 0 y 9 no cumple la condición anterior
"""
def todas_celdas_seguras_descubiertas(tablero: list[list[int]], tablero_visible: list[list[str]]) -> bool:
    for i in range(len(tablero)):
        for j in range(len(tablero[0])):
            if tablero[i][j] != -1 and tablero_visible[i][j] != str(tablero[i][j]):
                return False
    return True
 
#------------------------------------------------------------------------
#---------------- ejercicio  4) obtener_estado_tablero_visible() --------
#------------------------------------------------------------------------

"""
FUNCION copiar_tablero_visible
RECIBE: una matriz de strings que representa el tablero visible
DEVUELVE: una nueva matriz con los mismos valores que la matriz que entró, pero sin referencia a ella
"""
def copiar_tablero_visible(tablero_visible: list[list[str]]) -> list[list[str]]:
    copia: list[list[str]] = []
    for fila in tablero_visible:
        fila_nueva: list[str] = []
        for valor in fila:
            fila_nueva.append(valor)
        copia.append(fila_nueva)
    return copia

"""
FUNCION obtener_estado_tablero_visible
RECIBE: un valor de tipo EstadoJuego que representa el estado actual del juego
DEVUELVE: una matriz de strings que contiene por valor al tablero visible guardado en el parámetro recibido
"""
def obtener_estado_tablero_visible(estado: EstadoJuego) -> list[list[str]]:
    return copiar_tablero_visible(estado["tablero_visible"])
 
#------------------------------------------------------------------------
#--------------------- ejercicio  5) marcar_celda() ---------------------
#------------------------------------------------------------------------
 
"""
FUNCION marcar_celda
RECIBE: un valor de tipo EstadoJuego que representa el estado actual del juego; dos valores de tipo entero que representan una fila y una columna
MODIFICA: modifica el valor "tablero_visible" del primer parámetro recibido, de forma tal que si en su valor anterior contenía un caracter BANDERA,
será reemplazado por un caracter VACIO; y si en su valor anterior contenía un caracter VACIO, será reemplazado por un caracter BANDERA.
NO DEVUELVE NADA
"""
def marcar_celda(estado_juego: EstadoJuego, fila: int, columna: int) -> None:
    if not estado_juego["juego_terminado"]:
        actual: str = estado_juego["tablero_visible"][fila][columna]
        # Si es vacio que lo cambie por una bandera 
        if actual == VACIO:
            estado_juego["tablero_visible"][fila][columna] = BANDERA
        # Si es una bandera que lo cambie por  vacio 
        elif actual== BANDERA:
            estado_juego["tablero_visible"][fila][columna] = VACIO
        # Si no es ni vacio ni bandera que no haga nada (ya que significaria que el usuario intenta poner bandera sobre una ya descubierta)   
    return
 
#------------------------------------------------------------------------
#--------------------- ejercicio  6) descubrir_celda() ---------------------
#------------------------------------------------------------------------
"""
FUNCION copiar_tablero
RECIBE: una matriz de enteros que representa el tablero
DEVUELVE: una nueva matriz con los mismos valores que la matriz que entró, pero sin referencia a ella

def copiar_tablero(tablero: list[list[int]]) -> list[list[int]]:
    copia: list[list[int]] = []
    for fila in tablero:
        fila_nueva: list[int] = []
        for valor in fila:
            fila_nueva.append(valor)
        copia.append(fila_nueva)
    return copia
"""
"""
FUNCION descubrir_celda
RECIBE un estado de juego estado, que representa la configuración actual del buscaminas, incluyendo el tablero oculto con las minas (tablero), el tablero visible por el jugador (tablero visible), y la información sobre si el juego terminó, entre otros datos. También recibe una fila fila y una columna columna, que representan la celda que el jugador intenta descubrir.

MODIFICA el estado del juego de la siguiente manera:
· Si el juego ya estaba terminado antes de descubrir la celda, no hace nada: el tablero visible queda igual.
· Si la celda descubierta contiene una bomba (es decir, en tablero[fila][columna] == -1), el juego se termina. Todas las bombas se muestran en el tablero visible, y las celdas que no eran bombas quedan igual a como estaban antes.
· Si la celda descubierta no es una bomba:
    - Se revela el contenido de la celda (un número o un 0).
    - Si la celda contiene un 0, también se descubren automáticamente todas las celdas conectadas a ella que también contengan 0, y las celdas adyacentes a estos ceros, siempre que no estén marcadas con una bandera.
    - El tablero visible se actualiza para reflejar esos descubrimientos: cada celda se reemplaza por el número correspondiente del tablero original, salvo que estuviera marcada con una bandera.
    - El juego termina solo si al descubrir esa celda se revelan todas las celdas seguras (es decir, todas las que no contienen bomba).
"""
def descubrir_celda(estado_juego: EstadoJuego, fila: int, columna: int) -> None:
    if estado_juego["juego_terminado"]:
        return
    if estado_juego["tablero"][fila][columna] == -1:
        estado_juego["tablero_visible"][fila][columna] = BOMBA
        estado_juego["juego_terminado"] = True
        tablero_visible: list[list[int]] = estado_juego["tablero_visible"]
        filas: int = estado_juego["filas"]
        columnas: int = estado_juego["columnas"]
        for i in range(filas):
            for j in range(columnas):
                if estado_juego["tablero"][i][j] == -1:
                    tablero_visible[i][j] = BOMBA
        return
    celdas_a_descubrir: Cola[tuple[int,int]] = Cola()
    celdas_a_descubrir.put((fila,columna))
    visitado: list[tuple[int,int]] = []
    while not celdas_a_descubrir.empty():
        celda: tuple[int,int] = celdas_a_descubrir.get()
        
        
        
        if not celda in visitado:
            visitado.append(celda)
            i,j = celda
            valor: int = estado_juego["tablero"][i][j]
            estado_juego["tablero_visible"][i][j] = str(valor)
            if valor == 0:
                for df in [-1,0,1]:
                    for dc in [-1,0,1]:
                        nf: int = i + df
                        nc: int = j + dc
                        if 0 <= nf < estado_juego["filas"] and 0 <= nc < estado_juego["columnas"]:
                            if estado_juego["tablero_visible"][nf][nc] == VACIO and estado_juego["tablero"][nf][nc] >= 0:
                                celdas_a_descubrir.put((nf, nc))
        
    if todas_celdas_seguras_descubiertas(estado_juego["tablero"],estado_juego["tablero_visible"]):
        estado_juego["juego_terminado"] = True
    
 
 
 
 
 
#------------------------------------------------------------------------
#------------------ ejercicio  7) verificar_victoria() ------------------
#------------------------------------------------------------------------
"""
FUNCION verificar_victoria
RECIBE: un valor de tipo EstadoJuego que representa el estado actual del juego
DEVUELVE:
    · True si todas las celdas que no contienen un -1 en la matriz tablero del estado del juego, tampoco contienen VACIO en la matriz tablero visible
    · False de no cumplirse la condición anterior
"""
def verificar_victoria(estado: EstadoJuego) -> bool:
    tablero: list[list[int]] = estado["tablero"]
    tablero_visible: list[list[str]] = estado["tablero_visible"]
    return todas_celdas_seguras_descubiertas(tablero,tablero_visible)
 
 
#------------------------------------------------------------------------
#-------------------- ejercicio  8)reiniciar_juego() --------------------
#------------------------------------------------------------------------

"""
FUNCION reiniciar_juego
RECIBE: un valor de tipo EstadoJuego que representa el estado actual del juego
MODIFICA: el estado del juego creando un nuevo juego, con la misma cantidad de filas, columnas y minas, pero con un tablero visible vacío y un nuevo tablero aleatorio
"""
def reiniciar_juego(estado: EstadoJuego) -> None:
    filas: int = estado['filas']
    columnas: int = estado['columnas']
    minas: int = estado['minas']
    nuevo: EstadoJuego = crear_juego(filas, columnas, minas)
    distintos: bool = False
    for fila in range(filas):
        for columna in range(columnas):
            if nuevo['tablero'][fila][columna] != estado['tablero'][fila][columna]:
                distintos = True
    if not distintos:
        reiniciar_juego(estado)
    estado['filas'] = nuevo['filas']
    estado['columnas'] = nuevo['columnas']
    estado['minas'] = nuevo['minas']
    estado['juego_terminado'] = nuevo['juego_terminado']
    estado['tablero'] = nuevo['tablero']
    estado['tablero_visible'] = nuevo['tablero_visible']
 
#------------------------------------------------------------------------
#-------------------- ejercicio  9) guardar_estado() --------------------
#------------------------------------------------------------------------

"""
FUNCION guardar_estado
RECIBE: un valor de tipo EstadoJuego con el estado actual del juego; un valor de tipo string que representa la ruta de archivo donde se desea guardar el juego
REALIZA: crea o sobreescribe los archivos "tablero.txt" y "tablero_visible.txt" ubicados en la ruta pasada como parámetro de la siguiente forma:
    · el archivo "tablero.txt" contiene en cada línea una fila del tablero en la cual se encuentran separados por ',' los valores de esa fila de la matriz tablero
    · el archivo "tablero_visible.txt" contiene en cada línea una fila del tablero en la cual se encuentran separados por ',' los valores de esa fila de la matriz tablero_visible,
        pero reemplazando el caracter BANDERA por el caracter '*' y el caracter VACIO por el caracter '?'
"""
def guardar_estado(estado: EstadoJuego, ruta_directorio: str) -> None:
    archivo_tablero = open(os.path.join(ruta_directorio, "tablero.txt"), 'w', encoding='utf-8')
    archivo_tablero_visible = open(os.path.join(ruta_directorio, 'tablero_visible.txt'), 'w', encoding='utf-8')
    tablero: list[list[int]] = estado["tablero"]
    for fila in tablero:
        str_fila: list[str] = []
        for x in fila:
            str_fila.append(str(x))
        archivo_tablero.write(join(str_fila) + '\n')
    archivo_tablero.close()
    tablero_visible: list[list[str]] = estado["tablero_visible"]
    for fila in tablero_visible:
        linea: list[str] = []
        for c in fila:
            if c == BANDERA:
                linea.append("*")
            elif c == VACIO:
                linea.append("?")
            else:
                linea.append(c)
        archivo_tablero_visible.write(join(linea) + '\n')
    archivo_tablero_visible.close()
 
#------------------------------------------------------------------------
#-------------------- ejercicio  10) cargar_estado() --------------------
#------------------------------------------------------------------------

"""
FUNCION quitar_lineas_vacias
RECIBE: una lista de lineas de texto (strings)
DEVUELVE: otra lista de lineas de texto donde se han eliminado las líneas vacías
"""
def quitar_lineas_vacias(lineas: list[str]) -> list[str]:
    lineas_sin_vacias: list[str] = []
    for linea in lineas:
        if not (linea == "" or linea == "\n"):
            lineas_sin_vacias.append(linea)
    return lineas_sin_vacias


"""
RECIBE:  un estado, que representa el estado actual del juego Buscaminas, y una ruta_directorio, 
que es la ubicación donde se encuentran los archivos "tablero.txt" y "tablero_visible.txt". Estos archivos contienen el tablero real y el tablero visible del juego, 
respectivamente, en formato de texto.

MODIFICA el contenido del estado en caso de que los archivos sean válidos y consistentes entre sí. En ese caso, se actualizan las siguientes claves del estado:
· 'filas': cantidad de filas del tablero,
· 'columnas': cantidad de columnas del tablero,
· 'minas': cantidad total de minas (valor -1) en el tablero,
· 'juego_terminado': siempre se establece en False,
· 'tablero': el contenido de "tablero.txt" convertido a enteros,
· 'tablero_visible': el contenido de "tablero_visible.txt" adaptado a los valores del juego (BANDERA donde había un caracter '*', VACIO donde había un caracter '?', o número en string).

NO MODIFICA el estado si:
· Alguno de los archivos no existe.
· El número de filas en los dos tableros no coincide.
· El número de columnas en alguna fila no coincide con el resto.
· En el tablero visible no hay al menos un ? (VACIO) que tenga una mina o número real (entre 1 y 9) en el mismo lugar en el tablero oculto.

Devuelve:
· True si el estado fue cargado exitosamente
· False en caso contrario.
"""

def cargar_estado(estado: EstadoJuego, ruta_directorio: str) -> bool:
    if not (existe_archivo(ruta_directorio, "tablero.txt") and existe_archivo(ruta_directorio, "tablero_visible.txt")):
        return False
    archivo_tablero = open(os.path.join(ruta_directorio,"tablero.txt"), "r",encoding="utf-8")
    archivo_tablero_visible = open(os.path.join(ruta_directorio,"tablero_visible.txt"), "r",encoding="utf-8")
    lineas_tablero: list[str] = archivo_tablero.readlines()
    lineas_tablero_visible: list[str] = archivo_tablero_visible.readlines()
    lineas_tablero = quitar_lineas_vacias(lineas_tablero)
    lineas_tablero_visible = quitar_lineas_vacias(lineas_tablero_visible)
    archivo_tablero_visible.close()
    archivo_tablero.close()
    lineas_del_tablero: list[list[str]] = []
    cumple_ultima_condicion: bool = False
    for linea in lineas_tablero:
        if len(linea) > 0:
            lineas_del_tablero.append(split(linea))
    
    lineas_del_tablero_visible: list[list[str]] = []
 
    for linea in lineas_tablero_visible:
        if len(linea) > 0:
            lineas_del_tablero_visible.append(split(linea))
    
    if len(lineas_del_tablero) != len(lineas_del_tablero_visible):
        return False
    
    cantidad_lineas: int = len(lineas_del_tablero)
    cantidad_columnas: int = len(lineas_del_tablero[0])
    for i in range(cantidad_lineas):
        if len(lineas_del_tablero[i]) != cantidad_columnas or len(lineas_del_tablero_visible[i]) != cantidad_columnas:
            return False
    
    tablero: list[list[int]] = []
    for fila in lineas_del_tablero:
        fila_enteros: list[int] = []
        for x in fila:
            if ('0' <= x <= '9' or x == '-1'):
                fila_enteros.append(int(x))
            else:
                return
        tablero.append(fila_enteros)

    tablero_visible: list[list[str]] = []
    for i in range(len(lineas_del_tablero_visible)):
        fila: list[str] = lineas_del_tablero_visible[i]
        fila_modificada: list[str] = []
        for j in range(len(fila)):
            x: str = fila[j]
            if x == '*':
                fila_modificada.append(BANDERA)
            elif x == '?':
                if (1<=tablero[i][j]<=9):
                    cumple_ultima_condicion = True
                fila_modificada.append(VACIO)
            elif '0' <= x <= '9':
                fila_modificada.append(x)
            else:
                return
        tablero_visible.append(fila_modificada)
    
    minas: int = 0
    for fila in tablero:
        for x in fila:
            if x == -1:
                minas = minas + 1
    
    if not cumple_ultima_condicion:
        return False

    estado['filas'] = cantidad_lineas
    estado['columnas'] = cantidad_columnas
    estado['minas'] = minas
    estado['juego_terminado'] = False
    estado['tablero'] = tablero
    estado['tablero_visible'] = tablero_visible
    return True