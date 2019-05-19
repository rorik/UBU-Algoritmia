import os

try:
    os.chdir(os.path.join(os.getcwd(), 'p9'))
    print(os.getcwd())
except:
    pass
import unittest


class CaminosMinimosFloyd:
    """
    Clase para representar los caminos mínimos entre todos los nodos de un grafo.
    Los caminos deben calcularse con el algoritmo de Floyd.
    El espacio de almacenamiento debe ser O(n^2), siendo n el número de nodos.
    """

    #: dict[tuple[str], int]
    def __init__(self, grafo):
        """
        Constructor que recibe el grafo sobre el que calcular los caminos
        mínimos.
        El grafo que se recibe es un diccionario donde las claves son arcos 
        (pares de nodos) y los valores son el peso de los arcos.
        """

        # Get all the nodes and remove all the duplicates
        vertices = list(set([node for edge in grafo.keys() for node in edge]))
        # Create a dict mapping each node with its corresponding index
        self._vertices_indices = {}
        for i, node in enumerate(vertices):
            self._vertices_indices[node] = i
        # Get the infinite distance (in this implementation it's the distance of the longest non-cyclic path + 1)
        inf = sum(grafo.values()) + 1
        # Initialize the dist and next matrices
        self._dist = [[inf] * len(vertices) for _ in range(len(vertices))]
        self._next = [[None] * len(vertices) for _ in range(len(vertices))]
        # Set all the given weights
        for edge, weight in grafo.items():
            origin, target = self._vertices_indices[edge[0]], self._vertices_indices[edge[1]]
            self._dist[origin][target] = weight
            self._next[origin][target] = vertices[target]
        # Set to 0 the distance between a vertex and itself
        for i in range(len(vertices)):
            self._dist[i][i] = 0
            self._next[i][i] = vertices[i]
        # Floyd-Warshall algorithm
        for k in range(len(vertices)):
            for i in range(len(vertices)):
                for j in range(len(vertices)):
                    if self._dist[i][j] > self._dist[i][k] + self._dist[k][j]:
                        self._dist[i][j] = self._dist[i][k] + self._dist[k][j]
                        self._next[i][j] = self._next[i][k]

    def distancia(self, origen, destino):
        """
        Devuelve la distancia del camino mínimo ente origen y destino.
        Si no hay camino devuelve None.
        """

        if self._next[self._vertices_indices[origen]][self._vertices_indices[destino]] is None:
            return None

        return self._dist[self._vertices_indices[origen]][self._vertices_indices[destino]]

    def camino(self, origen, destino):
        """
        Devuelve en una lista de nodos el camino mínimo entre origen y
        destino.
        Si no hay camino devuelve None.
        """
        if self._next[self._vertices_indices[origen]][self._vertices_indices[destino]] is None:
            return None

        path = [origen]
        position = origen
        while position is not destino:
            position = self._next[self._vertices_indices[position]][self._vertices_indices[destino]]
            path.append(position)

        return path


class TestCaminosMinimosFloyd(unittest.TestCase):
    """Tests para la clase CaminosMinimosFloyd."""

    def test_7_nodos_12_arcos(self):
        grafo = {
            ("a", "b"): 2,
            ("a", "d"): 1,
            ("b", "d"): 3,
            ("b", "e"): 10,
            ("c", "a"): 4,
            ("c", "f"): 5,
            ("d", "c"): 2,
            ("d", "e"): 7,
            ("d", "f"): 8,
            ("d", "g"): 4,
            ("e", "g"): 6,
            ("g", "f"): 1
        }

        caminos = CaminosMinimosFloyd(grafo)

        for origen, destino, distancia, camino in (
                ("a", "a", 0, ["a"]),
                ("a", "b", 2, ["a", "b"]),
                ("a", "c", 3, ["a", "d", "c"]),
                ("a", "d", 1, ["a", "d"]),
                ("a", "e", 8, ["a", "d", "e"]),
                ("a", "f", 6, ["a", "d", "g", "f"]),
                ("a", "g", 5, ["a", "d", "g"]),
                ("b", "a", 9, ["b", "d", "c", "a"]),
                ("c", "e", 12, ["c", "a", "d", "e"]),
                ("d", "b", 8, ["d", "c", "a", "b"]),
                ("e", "f", 7, ["e", "g", "f"]),
                ("e", "a", None, None),
                ("f", "d", None, None)
        ):
            self.assertEqual(caminos.distancia(origen, destino), distancia)
            self.assertEqual(caminos.camino(origen, destino), camino)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
