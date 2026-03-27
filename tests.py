#tests
import unittest
from buscaminas import colocar_minas, calcular_numeros, crear_juego, obtener_estado_tablero_visible, marcar_celda, descubrir_celda, verificar_victoria, reiniciar_juego, guardar_estado, cargar_estado
from typing import Any
from os import path
import os
import shutil
import unittest

EstadoJuego = dict[str, Any]
BOMBA = chr(128163)  # simbolo de una mina
BANDERA = chr(127987)  # simbolo de bandera blanca
VACIO = " "

def es_matriz (matriz:list[list[int]]) -> bool:
    if len(matriz) <= 0:
        return False
    columnas:int = len(matriz[0])
    if columnas <= 0:
        return False
    for fila in matriz:
        if len(fila) != columnas:
            return False
    return True



def contar_minas (tablero:list[list[int]]) -> tuple[int,int]:
    res:tuple[int,int] = (0,0)
    for fila in tablero:
        for x in fila:
            if x == -1:
                res = (res[0] + 1, res[1])
            elif x == 0:
                res = (res[0], res[1] + 1)
    return res                


class test_colocar_minas (unittest.TestCase):
    def test_colocar_minas_1(self):
        tablero:list[list[int]] = colocar_minas(5,7,3)
        self.assertTrue(len(tablero) == 5 and len(tablero[0]) == 7)
        self.assertTrue(es_matriz(tablero))
        self.assertEqual(contar_minas(tablero)[0],3)
        self.assertEqual(contar_minas(tablero)[1],32)
    def test_colocar_minas_2(self):
        tablero:list[list[int]] = colocar_minas(4,4,2)
        self.assertTrue(len(tablero) == 4 and len(tablero[0]) == 4)
        self.assertTrue(es_matriz(tablero))
        self.assertEqual(contar_minas(tablero)[0],2)
        self.assertEqual(contar_minas(tablero)[1],14)





class test_calcular_numeros (unittest.TestCase):
    def test_calcular_numeros_1(self):
        tablero:list[list[int]] = [[0,-1],[0,0]]
        tablero_esperado:list[list[int]] = [[1,-1],[1,1]]
        calcular_numeros(tablero)
        self.assertEqual(tablero, tablero_esperado)
    def test_calcular_numeros_2(self):
        tablero:list[list[int]] = [[0,-1],[-1,0]]
        tablero_esperado:list[list[int]] = [[2,-1],[-1,2]]
        calcular_numeros(tablero)
        self.assertEqual(tablero, tablero_esperado)

class test_crear_juego (unittest.TestCase):
    def test_crear_juego_1(self):
        filas: int = 5
        columnas: int = 5
        minas: int = 3
        juego: EstadoJuego = crear_juego(filas,columnas,minas)
        self.assertEqual(juego['minas'],minas)
        self.assertEqual(juego['filas'],filas)
        self.assertEqual(juego['columnas'],columnas)
        self.assertEqual(len(juego['tablero']),filas)
        self.assertEqual(len(juego['tablero_visible']),filas)
        self.assertEqual(len(juego['tablero'][0]),columnas)
        self.assertEqual(len(juego['tablero_visible'][0]),columnas)
        self.assertFalse(juego['juego_terminado'])
        for i in range(filas):
            for j in range(columnas):
                self.assertEqual(juego['tablero_visible'][i][j],VACIO)
        numeros: list[list[int]] = juego['tablero']
        calcular_numeros(numeros)
        self.assertEqual(juego['tablero'],numeros)



    def test_crear_juego_2(self):
        filas: int = 6
        columnas: int = 9
        minas: int = 7
        juego: EstadoJuego = crear_juego(filas,columnas,minas)
        self.assertEqual(juego['minas'],minas)
        self.assertEqual(juego['filas'],filas)
        self.assertEqual(juego['columnas'],columnas)
        self.assertEqual(len(juego['tablero']),filas)
        self.assertEqual(len(juego['tablero_visible']),filas)
        self.assertEqual(len(juego['tablero'][0]),columnas)
        self.assertEqual(len(juego['tablero_visible'][0]),columnas)
        self.assertFalse(juego['juego_terminado'])
        for i in range(filas):
            for j in range(columnas):
                self.assertEqual(juego['tablero_visible'][i][j],VACIO)

        numeros: list[list[int]] = juego['tablero']
        calcular_numeros(numeros)
        self.assertEqual(juego['tablero'],numeros)


class test_obtener_estado_tablero_visible(unittest.TestCase):
    def test_obtener_estado_tablero_visible_1(self):
        tablero: list[list[int]] = [[-1,2,1,0],[2,-1,2,1],[1,2,-1,2],[0,1,2,-1]]
        tablero_visible: list[list[str]] = [[BANDERA,VACIO,VACIO,'0'],['2',VACIO,VACIO,VACIO],[VACIO,VACIO,VACIO,VACIO],['0',VACIO,VACIO,VACIO]]
        estado: EstadoJuego = {
            "filas": 4,
            "columnas": 4,
            "minas": 4,
            "juego_terminado": False,
            "tablero": tablero,
            "tablero_visible": tablero_visible
        }
        estado_tablero_visible: list[list[str]] = obtener_estado_tablero_visible(estado)
        self.assertEqual(tablero_visible,estado_tablero_visible)
    def test_obtener_estado_tablero_visible_2(self):
        tablero: list[list[int]] = [[0,0,0,0,1,-1,2,-1],[1,1,0,0,1,1,2,1],[-1,1,0,1,1,1,0,0],[1,1,1,2,-1,1,0,0],[0,1,3,-1,4,2,0,0],[1,2,-1,-1,-1,1,0,0],[-1,2,2,3,3,2,1,0],[1,1,0,0,1,-1,1,0]]
        tablero_visible: list[list[str]] = [[VACIO,VACIO,VACIO,VACIO,'1',BANDERA,'2',BANDERA],['1','1',VACIO,VACIO,'1','1','2','1'],[BANDERA,'1',VACIO,'1','1','1',VACIO,VACIO],['1','1','1','2',VACIO,'1',VACIO,VACIO],[VACIO,'1','3',VACIO,'4','2',VACIO,VACIO],['1','2',VACIO,BANDERA,VACIO,'1',VACIO,VACIO],[VACIO,'2','2','3','3','2','1',VACIO],['1','1',VACIO,VACIO,'1',BANDERA,'1',VACIO]]
        estado: EstadoJuego = {
            "filas": 8,
            "columnas": 8,
            "minas": 10,
            "juego_terminado": False,
            "tablero": tablero,
            "tablero_visible": tablero_visible
        }
        estado_tablero_visible: list[list[str]] = obtener_estado_tablero_visible(estado)
        self.assertEqual(tablero_visible,estado_tablero_visible)
class test_marcar_celda(unittest.TestCase):
    def test_marcar_celda_1(self):
        tablero: list[list[int]] = [[-1,2,1,0],[2,-1,2,1],[1,2,-1,2],[0,1,2,-1]]
        tablero_visible: list[list[str]] = [[BANDERA,VACIO,VACIO,'0'],['2',VACIO,VACIO,VACIO],[VACIO,VACIO,VACIO,VACIO],['0',VACIO,VACIO,VACIO]]
        tablero_visible_esperado: list[list[str]] = [[VACIO,VACIO,VACIO,'0'],['2',VACIO,VACIO,VACIO],[VACIO,VACIO,VACIO,VACIO],['0',VACIO,VACIO,VACIO]]
        fila: int = 0
        columna: int = 0
        estado: EstadoJuego = {
            "filas": 4,
            "columnas": 4,
            "minas": 4,
            "juego_terminado": False,
            "tablero": tablero,
            "tablero_visible": tablero_visible
        }
        marcar_celda(estado,fila,columna)
        tablero_visible_recibido: list[list[str]] = estado["tablero_visible"]
        self.assertEqual(tablero_visible_recibido,tablero_visible_esperado)
    def test_marcar_celda_2(self):
        tablero: list[list[int]] = [[0,0,0,0,1,-1,2,-1],[1,1,0,0,1,1,2,1],[-1,1,0,1,1,1,0,0],[1,1,1,2,-1,1,0,0],[0,1,3,-1,4,2,0,0],[1,2,-1,-1,-1,1,0,0],[-1,2,2,3,3,2,1,0],[1,1,0,0,1,-1,1,0]]
        tablero_visible: list[list[str]] = [[VACIO,VACIO,VACIO,VACIO,'1',BANDERA,'2',BANDERA],['1','1',VACIO,VACIO,'1','1','2','1'],[BANDERA,'1',VACIO,'1','1','1',VACIO,VACIO],['1','1','1','2',VACIO,'1',VACIO,VACIO],[VACIO,'1','3',VACIO,'4','2',VACIO,VACIO],['1','2',VACIO,BANDERA,VACIO,'1',VACIO,VACIO],[VACIO,'2','2','3','3','2','1',VACIO],['1','1',VACIO,VACIO,'1',BANDERA,'1',VACIO]]
        tablero_visible_esperado: list[list[str]] = [[VACIO,VACIO,VACIO,VACIO,'1',BANDERA,'2',BANDERA],['1','1',VACIO,VACIO,'1','1','2','1'],[BANDERA,'1',VACIO,'1','1','1',VACIO,VACIO],['1','1','1','2',VACIO,'1',VACIO,VACIO],[VACIO,'1','3',VACIO,'4','2',VACIO,VACIO],['1','2',VACIO,BANDERA,VACIO,'1',BANDERA,VACIO],[VACIO,'2','2','3','3','2','1',VACIO],['1','1',VACIO,VACIO,'1',BANDERA,'1',VACIO]]
        fila: int = 5
        columna: int = 6
        estado: EstadoJuego = {
            "filas": 8,
            "columnas": 8,
            "minas": 10,
            "juego_terminado": False,
            "tablero": tablero,
            "tablero_visible": tablero_visible
        }
        marcar_celda(estado,fila,columna)
        tablero_visible_recibido: list[list[str]] = estado["tablero_visible"]
        self.assertEqual(tablero_visible_recibido,tablero_visible_esperado)
    def test_marcar_celda_3(self):
        tablero: list[list[int]] = [[0,0,0,0,1,-1,2,-1],[1,1,0,0,1,1,2,1],[-1,1,0,1,1,1,0,0],[1,1,1,2,-1,1,0,0],[0,1,3,-1,4,2,0,0],[1,2,-1,-1,-1,1,0,0],[-1,2,2,3,3,2,1,0],[1,1,0,0,1,-1,1,0]]
        tablero_visible: list[list[str]] = [[VACIO,VACIO,VACIO,VACIO,'1',VACIO,'2',BANDERA],['1','1','0','0','1','1','2','1'],[BANDERA,'1','0','1','1','1','0','0'],['1','1','1','2',BANDERA,'1','0','0'],['0','1','3',BANDERA,'4','2','0','0'],['1','2',BANDERA,BANDERA,BANDERA,'1','0','0'],[BANDERA,'2','2','3','3','2','1','0'],['1','1','0','0','1',BANDERA,'1','0']]
        tablero_visible_esperado: list[list[str]] = [[VACIO,VACIO,VACIO,VACIO,'1',BANDERA,'2',BANDERA],['1','1','0','0','1','1','2','1'],[BANDERA,'1','0','1','1','1','0','0'],['1','1','1','2',BANDERA,'1','0','0'],['0','1','3',BANDERA,'4','2','0','0'],['1','2',BANDERA,BANDERA,BANDERA,'1','0','0'],[BANDERA,'2','2','3','3','2','1','0'],['1','1','0','0','1',BANDERA,'1','0']]
        fila: int = 0
        columna: int = 5
        estado: EstadoJuego = {
            "filas": 8,
            "columnas": 8,
            "minas": 10,
            "juego_terminado": False,
            "tablero": tablero,
            "tablero_visible": tablero_visible
        }
        marcar_celda(estado,fila,columna)
        tablero_visible_recibido: list[list[str]] = estado["tablero_visible"]
        self.assertEqual(tablero_visible_recibido,tablero_visible_esperado)
class test_descubrir_celda(unittest.TestCase):
    def test_descubrir_celda_1(self):
        tablero: list[list[int]] = [[2,-1,1],[-1,3,1],[-1,2,0]]
        tablero_visible: list[list[str]] = [
            [VACIO,VACIO,VACIO],[VACIO,VACIO,VACIO],[VACIO,VACIO,VACIO]
        ]
        tablero_visible_esperado: list[list[str]] = [[VACIO,BOMBA,VACIO],[BOMBA,VACIO,VACIO],[BOMBA,VACIO,VACIO]]
        fila: int = 0
        columna: int = 1
        
        estado: EstadoJuego = {
            "filas": 3,
            "columnas": 3,
            "minas": 3,
            "juego_terminado": False,
            "tablero": tablero,
            "tablero_visible": tablero_visible
        }
        descubrir_celda(estado,fila,columna)
        self.assertEqual(estado['tablero_visible'],tablero_visible_esperado)
        self.assertTrue(estado['juego_terminado'])
    def test_descubrir_celda_2(self):
        tablero: list[list[int]] = [
                [2, -1, 1],
                [-1, 3,  1],
                [-1, 2,  0]
            ]
        tablero_visible: list[list[str]] = [
                [VACIO, VACIO, VACIO],
                [VACIO,   VACIO, VACIO],
                [VACIO, VACIO, VACIO]
            ]
        estado: EstadoJuego = {
            "filas": 3,
            "columnas": 3,
            "minas": 3,
            "juego_terminado": False,
            "tablero": tablero,
            "tablero_visible": tablero_visible 
        }
        fila: int = 1
        columna: int = 1
        descubrir_celda(estado,fila,columna)
        self.assertEqual(tablero_visible,estado["tablero_visible"])
        self.assertFalse(estado['juego_terminado'])
    def test_descubrir_celda_3(self):
        tablero: list[list[int]] = [
                [2, -1, 1],
                [-1, 3,  1],
                [-1, 2,  0]
            ]
        tablero_visible: list[list[str]] = [
                [VACIO,VACIO,VACIO],
                [VACIO,VACIO,VACIO],
                [VACIO,VACIO,VACIO]
            ]
        tablero_visible_esperado: list[list[str]] = [
                [VACIO,VACIO,VACIO],
                [VACIO,'3','1'],
                [VACIO,'2','0'],
            ]
        estado: EstadoJuego = {
            "filas": 3,
            "columnas": 3,
            "minas": 3,
            "juego_terminado": False,
            "tablero": tablero,
            "tablero_visible": tablero_visible 
        }
        fila: int = 2
        columna: int = 2
        descubrir_celda(estado,fila,columna)
        self.assertEqual(tablero_visible_esperado,estado["tablero_visible"])
        self.assertFalse(estado['juego_terminado'])
    def test_descubrir_celda_4(self):
        tablero: list[list[int]] = [
                [2, -1, 1],
                [-1, 3,  1],
                [-1, 2,  0]
            ]
        tablero_visible: list[list[str]] = [
                ['2',VACIO,'1'],
                [VACIO,VACIO,VACIO],
                [VACIO,VACIO,VACIO]
            ]
        tablero_visible_esperado: list[list[str]] = [
                ['2',VACIO,'1'],
                [VACIO,'3','1'],
                [VACIO,'2','0']
            ]
        estado: EstadoJuego = {
            "filas": 3,
            "columnas": 3,
            "minas": 3,
            "juego_terminado": False,
            "tablero": tablero,
            "tablero_visible": tablero_visible 
        }
        fila: int = 2
        columna: int = 2
        descubrir_celda(estado,fila,columna)
        self.assertEqual(tablero_visible_esperado,estado["tablero_visible"])
        self.assertTrue(estado['juego_terminado'])
class test_verificar_victoria(unittest.TestCase):
    def test_verificar_victoria_victoria(self):
        estado: EstadoJuego = {
            "filas": 2,
            "columnas": 2,
            "minas": 1,
            "juego_terminado": False,
            "tablero": [[1,-1],[1,1]],
            "tablero_visible": [['1',VACIO],['1','1']] 
        }
        self.assertTrue(verificar_victoria(estado))
    def test_verificar_victoria_falso(self):
        estado: EstadoJuego = {
            "filas": 2,
            "columnas": 2,
            "minas": 1,
            "juego_terminado": False,
            "tablero": [[1,-1],[1,1]],
            "tablero_visible": [['1',VACIO],['1',VACIO]] 
        }
        self.assertFalse(verificar_victoria(estado))

class test_reiniciar_juego(unittest.TestCase):
    def test_reiniciar_juego_1(self):
        estado: EstadoJuego = {
            "filas": 2,
            "columnas": 2,
            "minas": 2,
            "juego_terminado": False,
            "tablero": [[1,-1],[1,1]],
            "tablero_visible": [['1',VACIO],['1','1']] 
        }
        filas: int = 2
        columnas: int = 2
        minas: int = 2
        tablero: list[list[int]] = [[1,-1],[1,1]]
        reiniciar_juego(estado)
        distintos: bool = False
        for f in range(2):
            for c in range(2):
                if tablero[f][c] != estado['tablero'][f][c]:
                    distintos = True
        self.assertTrue(distintos)
        self.assertEqual(estado['filas'],filas)
        self.assertEqual(estado['columnas'],columnas)
        self.assertEqual(estado['minas'],minas)
        self.assertFalse(estado['juego_terminado'])
    def test_reiniciar_juego_2(self):
        tablero: list[list[int]] = [
                [2, -1, 1],
                [-1, 3,  1],
                [-1, 2,  0]
            ]
        tablero_visible: list[list[str]] = [
                [VACIO,VACIO,VACIO],
                [VACIO,VACIO,VACIO],
                [VACIO,VACIO,VACIO]
            ]
        estado: EstadoJuego = {
            "filas": 3,
            "columnas": 3,
            "minas": 3,
            "juego_terminado": False,
            "tablero": tablero,
            "tablero_visible": tablero_visible 
        }
        filas: int = 3
        columnas: int = 3
        minas: int = 3
        reiniciar_juego(estado)
        distintos: bool = False
        for f in range(3):
            for c in range(3):
                if tablero[f][c] != estado['tablero'][f][c]:
                    distintos = True
        self.assertTrue(distintos)
        self.assertEqual(estado['filas'],filas)
        self.assertEqual(estado['columnas'],columnas)
        self.assertEqual(estado['minas'],minas)
        self.assertFalse(estado['juego_terminado'])

class test_guardar_estado(unittest.TestCase):
    def test_guardar_estado_1(self):
            tablero: list[list[int]] = [
                    [2, -1, 1],
                    [-1, 3,  1],
                    [-1, 2,  0]
                ]
            tablero_visible: list[list[str]] = [
                    ['2', BANDERA, '1'],
                    [VACIO, VACIO, VACIO],
                    [VACIO, VACIO, VACIO]
                ]
            estado: EstadoJuego = {
                "filas": 3,
                "columnas": 3,
                "minas": 3,
                "juego_terminado": False,
                "tablero": tablero,
                "tablero_visible": tablero_visible 
            }

            ruta_directorio = os.path.join(os.path.dirname(__file__), 'test_guardar_estado')
            if not os.path.exists(ruta_directorio):
                os.makedirs(ruta_directorio)

            guardar_estado(estado, ruta_directorio)

            archivo_tablero = open(os.path.join(ruta_directorio, 'tablero.txt'), 'r', encoding='utf-8')
            archivo_tablero_visible = open(os.path.join(ruta_directorio, 'tablero_visible.txt'), 'r', encoding='utf-8')
            
            lineas_tablero_archivo: list[str] = archivo_tablero.readlines()
            lineas_tablero_visible_archivo: list[str] = archivo_tablero_visible.readlines()
            
            lineas_tablero_esperadas: list[str] = ["2,-1,1\n", "-1,3,1\n", "-1,2,0\n"]
            lineas_tablero_visible_esperadas: list[str] = ["2,*,1\n", "?,?,?\n", "?,?,?\n"]
            
            for i in range(3):
                self.assertEqual(lineas_tablero_archivo[i], lineas_tablero_esperadas[i])
                self.assertEqual(lineas_tablero_visible_archivo[i], lineas_tablero_visible_esperadas[i])
                
            archivo_tablero.close()
            archivo_tablero_visible.close()

class test_cargar_estado(unittest.TestCase):
    
    def setUp(self):
        self.ruta_test = "temp_test_folder"
        if not os.path.exists(self.ruta_test):
            os.makedirs(self.ruta_test)

    def tearDown(self):
        if os.path.exists(self.ruta_test):
            shutil.rmtree(self.ruta_test)

    def test_cargar_estado_1(self):
        tablero = "1,-1\n1,1"
        visible = "?,?\n1,1"
        
        with open(os.path.join(self.ruta_test, "tablero.txt"), "w", encoding="utf-8") as f:
            f.write(tablero)
        with open(os.path.join(self.ruta_test, "tablero_visible.txt"), "w", encoding="utf-8") as f:
            f.write(visible)
            
        estado_inicial = {}
        res = cargar_estado(estado_inicial, self.ruta_test)
        
        self.assertTrue(res)
        self.assertEqual(estado_inicial["filas"], 2)
        self.assertEqual(estado_inicial["minas"], 1)

    def test_cargar_estado_archivo_inexistente(self):
        estado_inicial = {}
        res = cargar_estado(estado_inicial, "ruta_que_no_existe")
        self.assertFalse(res)


if __name__ == "__main__":
    unittest.main(verbosity=2)