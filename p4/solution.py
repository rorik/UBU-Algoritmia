# Importaciones
import unittest
from collections import Counter


def reparte(capacidad, elementos):
    """
    Reparte los elementos en varios contenedores de una misma capacidad.
    Los elementos son una colección de valores numéricos.
    El resultado es una lista de listas, cada lista representa los elementos de
    un contenedor.
    """

    cerrados = []
    abiertos = []
    for elemento in elementos:
        destino = None
        for contenedor in abiertos:
            if sum(contenedor) + elemento <= capacidad:
                destino = contenedor
                break

        if destino is None:
            destino = []
            abiertos.append(destino)

        destino.append(elemento)

        if sum(destino) == capacidad:
            abiertos.remove(destino)
            cerrados.append(destino)

    return cerrados + abiertos


class TestReparte(unittest.TestCase):

    def estan_repartidos(self, capacidad, elementos, reparto):
        """
        Comprueba si los elementos están repartidos de acuerdo a una determinada
        capacidad.
        """

        # En todos los contenedores se respeta la capacidad
        self.assertTrue(
            all(sum(contenedor) <= capacidad for contenedor in reparto))

        # Los elementos en el reparto coinciden con los originales
        self.assertEqual(
            Counter(elementos),
            Counter(elemento
                    for contenedor in reparto
                    for elemento in contenedor)
        )

    def test_simple(self):
        """ Primer caso de prueba simple """

        capacidad = 10
        elementos = 100 * [1]
        reparto = reparte(capacidad, elementos)
        self.assertEqual(len(reparto), 10)
        self.estan_repartidos(capacidad, elementos, reparto)

    def tests_varios(self):
        """ Varios casos de prueba"""

        for capacidad, elementos, longitud in (
                (10, 100 * [1], 10),
                (100, 1000 * [1], 10),
                (10, 100 * [9], 100),
                (10, 100 * [4], 50),
                (10, 100 * [3], 34),
                (10, 100 * [6, 3], 100),
                (10, 100 * [6, 5, 4], 150),
                (10, 100 * [5, 1, 4, 3, 2], 150)
        ):
            reparto = reparte(capacidad, elementos)
            self.assertEqual(len(reparto), longitud)
            self.estan_repartidos(capacidad, elementos, reparto)


# ---- seleccion_voraz ----

def seleccion_voraz(conjuntos):
    """
    Dada una secuencia de conjuntos, devuelve otra, tal que los conjuntos
    resultantes de la unión de los conjuntos de las secuencias de entrada y
    salida coincidan.
    La selección de conjuntos es voraz: se selecciona el conjunto que tenga más
    elementos que no estén en ninguno de los conjuntos seleccionados
    previamente.
    Si varios conjuntos tienen el mismo número de elementos, se selecciona el
    que esté primero en la secuencia de entrada.
    La secuencia de salida será una lista, sus elementos deben aparecer en el
    orden de selección.
    """

    abiertos = conjuntos.copy()
    cerrados = []
    resultado = []
    while True:
        maximo = [None, 0]
        for conjunto in abiertos:
            diferencia = len(conjunto.difference(cerrados))
            if diferencia > maximo[1]:
                maximo = [conjunto, diferencia]
        if maximo[0] is None:
            break
        else:
            abiertos.remove(maximo[0])
            cerrados.extend(maximo[0])
            resultado.append(maximo[0])
    return resultado


class TestSeleccionVoraz(unittest.TestCase):

    def test_1(self):
        self.assertEqual(
            seleccion_voraz([{1, 2, 3}, {2, 4}, {3, 4}, {4, 5}]),
            [{1, 2, 3}, {4, 5}])

    def test_2(self):
        self.assertEqual(
            seleccion_voraz([{1, 2, 3}, {2, 3, 4}, {3, 4, 5}]),
            [{1, 2, 3}, {3, 4, 5}]
        )

    def test_3(self):
        self.assertEqual(
            seleccion_voraz([{1, 2}, {2, 3}, {3, 4}, {4, 5}]),
            [{1, 2}, {3, 4}, {4, 5}]
        )

    def test_4(self):
        self.assertEqual(
            seleccion_voraz([{1, 2, 3, 4}, {5, 6, 7}, {8}, {9}, {1, 4, 7},
                             {8, 2, 5}, {9, 3, 6}]),
            [{1, 2, 3, 4}, {5, 6, 7}, {8}, {9}]
        )

    def test_5(self):
        self.assertEqual(
            seleccion_voraz([{1, 4, 7}, {1, 2, 3, 4}, {5, 6, 7}, {8}, {9},
                             {8, 2, 5}, {9, 3, 6}]),
            [{1, 2, 3, 4}, {5, 6, 7}, {8}, {9}]
        )

    def es_seleccion(self, originales, seleccionados):
        """
        Comprueba si las uniones de originales y seleccionados contienen los
        mismos elementos y todos los seleccionados están en los originales.
        """

        self.assertEqual(
            {elemento for conjunto in originales for elemento in conjunto},
            {elemento for conjunto in seleccionados for elemento in conjunto}
        )

        for conjunto in seleccionados:
            self.assertTrue(conjunto in originales)

    def test_multiplos(self):
        """Los conjuntos están formados por múltiplos de enteros"""

        for maximo, longitud in (
                (10, 4),
                (100, 25),
                (1000, 168)
        ):
            conjuntos = []
            for i in range(2, maximo):
                conjuntos.append(set(range(i, maximo, i)))
            seleccionados = seleccion_voraz(conjuntos)
            self.assertEqual(longitud, len(seleccionados))
            self.es_seleccion(conjuntos, seleccionados)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
