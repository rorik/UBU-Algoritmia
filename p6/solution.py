import unittest
import math


def divide_y_venceras_recursivo(inferior, superior=None, divisiones=2):
    """
    Dados los índices inferior y superior, genera la secuencia de índices
    correspondiente a las llamadas recursivas que se realizan al dividir en
    tantos subproblemas como el número de divisiones indicado.
    Los subproblemas son de aproximadamente el mismo tamaño.
    Si el número de elementos entre inferior y superior es menor que el número
    de divisiones, se planteará un subproblema para cada elemento.
    Los subproblemas se plantearán en orden ascendente: el primer problema
    contendrá inferior, el último contendrá superior.
    Si el número de elementos no es múltiplo del número de divisiones, los
    primeros subproblemas tendrán un elemento más que los últimos.
    Si superior es None, el primer argumento recibido será superior e inferior
    será 0.
    """

    if superior is None:
        superior = inferior
        inferior = 0

    resultado = [(inferior, superior)]
    if inferior != superior:
        diff = superior - inferior + 1
        if diff <= divisiones:
            for i in range(diff):
                inf = inferior + i
                resultado.append((inf, inf))
        else:
            gap = math.floor(diff / divisiones)
            remainder = diff - gap * divisiones
            next_inf = inferior
            for i in range(divisiones):
                inf = next_inf
                sup = inf + gap - 1
                if remainder > 0:
                    sup += 1
                    remainder -= 1
                next_inf = sup + 1
                resultado.extend(divide_y_venceras_recursivo(inf, sup, divisiones))

    return resultado


class TestDivideYVencerasRecursivo(unittest.TestCase):
    
    def setUp(self):
        
        self.generador = divide_y_venceras_recursivo    
       
    def test_0(self):
                
        esperados = [(0, 0)]
        self.assertEqual(esperados, list(self.generador(0)))
        
    def test_1(self):       

        esperados = [(0, 1), (0, 0), (1, 1)]
        self.assertEqual(esperados, list(self.generador(1)))

    def test_2(self):
         
        esperados = [(0, 2), (0, 1), (0, 0), (1, 1), (2, 2)]
        self.assertEqual(esperados, list(self.generador(2)))

    def test_3(self):
         
        esperados = [(0, 3), (0, 1), (0, 0), (1, 1), (2, 3), (2, 2), (3, 3)]
        self.assertEqual(esperados, list(self.generador(3)))

    def test_1_4(self):
         
        esperados = [(1, 4), (1, 2), (1, 1), (2, 2), (3, 4), (3, 3), (4, 4)]
        self.assertEqual(esperados, list(self.generador(1, 4)))

    def test_0_4_3(self):
         
        esperados = [(0, 4), (0, 1), (0, 0), (1, 1), (2, 3), (2, 2), (3, 3), 
                     (4, 4)]
        self.assertEqual(esperados, list(self.generador(0, 4, 3)))

    def test_0_9_3(self):
         
        esperados = [(0, 9), (0, 3), (0, 1), (0, 0), (1, 1), (2, 2), (3, 3), 
                     (4, 6), (4, 4), (5, 5), (6, 6), (7, 9), (7, 7), (8, 8), 
                     (9, 9)]
        self.assertEqual(esperados, list(self.generador(0, 9, 3)))                        
 
    def test_100(self):
          
        esperados = [(0, 100), (0, 50), (0, 25), (0, 12), (0, 6), (0, 3), 
                     (0, 1), (0, 0), (1, 1), (2, 3), (2, 2), (3, 3), (4, 6), 
                     (4, 5), (4, 4), (5, 5), (6, 6), (7, 12), (7, 9), (7, 8), 
                     (7, 7), (8, 8), (9, 9), (10, 12), (10, 11), (10, 10), 
                     (11, 11), (12, 12), (13, 25), (13, 19), (13, 16), (13, 14),
                     (13, 13), (14, 14), (15, 16), (15, 15), (16, 16), (17, 19),
                     (17, 18), (17, 17), (18, 18), (19, 19), (20, 25), (20, 22),
                     (20, 21), (20, 20), (21, 21), (22, 22), (23, 25), (23, 24),
                     (23, 23), (24, 24), (25, 25), (26, 50), (26, 38), (26, 32),
                     (26, 29), (26, 27), (26, 26), (27, 27), (28, 29), (28, 28),
                     (29, 29), (30, 32), (30, 31), (30, 30), (31, 31), (32, 32),
                     (33, 38), (33, 35), (33, 34), (33, 33), (34, 34), (35, 35),
                     (36, 38), (36, 37), (36, 36), (37, 37), (38, 38), (39, 50),
                     (39, 44), (39, 41), (39, 40), (39, 39), (40, 40), (41, 41),
                     (42, 44), (42, 43), (42, 42), (43, 43), (44, 44), (45, 50),
                     (45, 47), (45, 46), (45, 45), (46, 46), (47, 47), (48, 50),
                     (48, 49), (48, 48), (49, 49), (50, 50), (51, 100),
                     (51, 75), (51, 63), (51, 57), (51, 54), (51, 52), (51, 51),
                     (52, 52), (53, 54), (53, 53), (54, 54), (55, 57), (55, 56),
                     (55, 55), (56, 56), (57, 57), (58, 63), (58, 60), (58, 59),
                     (58, 58), (59, 59), (60, 60), (61, 63), (61, 62), (61, 61),
                     (62, 62), (63, 63), (64, 75), (64, 69), (64, 66), (64, 65),
                     (64, 64), (65, 65), (66, 66), (67, 69), (67, 68), (67, 67),
                     (68, 68), (69, 69), (70, 75), (70, 72), (70, 71), (70, 70),
                     (71, 71), (72, 72), (73, 75), (73, 74), (73, 73), (74, 74),
                     (75, 75), (76, 100), (76, 88), (76, 82), (76, 79),
                     (76, 77), (76, 76), (77, 77), (78, 79), (78, 78), (79, 79),
                     (80, 82), (80, 81), (80, 80), (81, 81), (82, 82), (83, 88), 
                     (83, 85), (83, 84), (83, 83), (84, 84), (85, 85), (86, 88), 
                     (86, 87), (86, 86), (87, 87), (88, 88), (89, 100), 
                     (89, 94), (89, 91), (89, 90), (89, 89), (90, 90), (91, 91),
                     (92, 94), (92, 93), (92, 92), (93, 93), (94, 94), 
                     (95, 100), (95, 97), (95, 96), (95, 95), (96, 96), 
                     (97, 97), (98, 100), (98, 99), (98, 98), (99, 99), 
                     (100, 100)]        
        self.assertEqual(esperados, list(self.generador(100))) 

    def test_100_3(self):
        
        esperados = [(0, 100), (0, 33), (0, 11), (0, 3), (0, 1), (0, 0), (1, 1),
                     (2, 2), (3, 3), (4, 7), (4, 5), (4, 4), (5, 5), (6, 6), 
                     (7, 7), (8, 11), (8, 9), (8, 8), (9, 9), (10, 10), 
                     (11, 11), (12, 22), (12, 15), (12, 13), (12, 12), (13, 13),
                     (14, 14), (15, 15), (16, 19), (16, 17), (16, 16), (17, 17),
                     (18, 18), (19, 19), (20, 22), (20, 20), (21, 21), (22, 22),
                     (23, 33), (23, 26), (23, 24), (23, 23), (24, 24), (25, 25),
                     (26, 26), (27, 30), (27, 28), (27, 27), (28, 28), (29, 29),
                     (30, 30), (31, 33), (31, 31), (32, 32), (33, 33), (34, 67),
                     (34, 45), (34, 37), (34, 35), (34, 34), (35, 35), (36, 36),
                     (37, 37), (38, 41), (38, 39), (38, 38), (39, 39), (40, 40),
                     (41, 41), (42, 45), (42, 43), (42, 42), (43, 43), (44, 44),
                     (45, 45), (46, 56), (46, 49), (46, 47), (46, 46), (47, 47),
                     (48, 48), (49, 49), (50, 53), (50, 51), (50, 50), (51, 51),
                     (52, 52), (53, 53), (54, 56), (54, 54), (55, 55), (56, 56),
                     (57, 67), (57, 60), (57, 58), (57, 57), (58, 58), (59, 59),
                     (60, 60), (61, 64), (61, 62), (61, 61), (62, 62), (63, 63),
                     (64, 64), (65, 67), (65, 65), (66, 66), (67, 67), 
                     (68, 100), (68, 78), (68, 71), (68, 69), (68, 68), 
                     (69, 69), (70, 70), (71, 71), (72, 75), (72, 73), (72, 72),
                     (73, 73), (74, 74), (75, 75), (76, 78), (76, 76), (77, 77),
                     (78, 78), (79, 89), (79, 82), (79, 80), (79, 79), (80, 80),
                     (81, 81), (82, 82), (83, 86), (83, 84), (83, 83), (84, 84),
                     (85, 85), (86, 86), (87, 89), (87, 87), (88, 88), (89, 89),
                     (90, 100), (90, 93), (90, 91), (90, 90), (91, 91), 
                     (92, 92), (93, 93), (94, 97), (94, 95), (94, 94), (95, 95),
                     (96, 96), (97, 97), (98, 100), (98, 98), (99, 99), 
                     (100, 100)] 
        self.assertEqual(esperados, list(self.generador(0, 100, 3)))


def divide_y_venceras_iterativo(inferior, superior=None, divisiones=2):
    """
    Genera los mismos valores que divide_y_venceras_recursivo, pero sin usar 
    recursión.
    """
    
    if superior is None:
        superior = inferior
        inferior = 0

    resultado = []
    queue = [(inferior, superior)]
    while len(queue) > 0:
        inferior, superior = queue.pop(0)
        resultado.append((inferior, superior))
        if inferior != superior:
            diff = superior - inferior + 1
            if diff <= divisiones:
                for i in range(diff):
                    inf = inferior + i
                    resultado.append((inf, inf))
            else:
                gap = math.floor(diff / divisiones)
                remainder = diff - gap * divisiones
                next_inf = inferior
                queued = []
                for i in range(divisiones):
                    inf = next_inf
                    sup = inf + gap - 1
                    if remainder > 0:
                        sup += 1
                        remainder -= 1
                    next_inf = sup + 1
                    queued.append((inf, sup))
                queue = queued + queue

    return resultado

class TestDivideYVencerasIterativo(TestDivideYVencerasRecursivo):
    
    def setUp(self):
        self.generador = divide_y_venceras_iterativo

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)