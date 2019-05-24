import random
import unittest

class Particion:
    """
    Clase que implementa una partición de un conjunto en subconjuntos disjuntos.
    Una partición se corresponde con una estructura Unión-Pertenencia.
    """

    def __init__(self, iterable):
        """
        Crea una partición con los elementos del iterable.
        Inicialmente cada elemento forma un subconjunto.
        """
        self._padres = {}
        self._subconjuntos = {}
        for elemento in iterable:
            self._padres[elemento] = None
            self._subconjuntos[elemento] = [[elemento], 0, elemento]

    def __len__(self):
        """Devuelve el número de subconjuntos en la partición."""

        return len(self._subconjuntos)

    def _get_root(self, k):
        while self._padres[k] is not None:
            k = self._padres[k]
        return k

    def numero(self, k=None):
        """
        Devuelve el número de elementos del subconjunto al que pertenece el 
        elemento k. 
        Si k es None devuelve el número total de elementos.
        """

        if k is None:
            return len(self._padres)

        subconjunto = self._get_subconjunto(k)
        return None if subconjunto is None else len(subconjunto[0])

    def _get_subconjunto(self, k):
        if k in self._padres:
            return self._subconjuntos[self._get_root(k)]
        return None

    def __getitem__(self, k):
        """
        Devuelve el subconjunto al que pertenece el elemento k.
        El subconjunto se identifica mediante uno de sus elementos.
        """
        subconjunto = self._get_subconjunto(k)
        if subconjunto is None:
            return None
        if len(subconjunto[0]) == 1:
            return subconjunto[0][0]
        return subconjunto[0]

    def __iter__(self):
        """
        Devuelve un iterador sobre los subconjuntos.
        Cada subconjunto se identifica mediante uno de sus elementos.
        """
        for elemento, padre in self._padres.items():
            if padre is None:
                yield elemento

    def une(self, a, b):
        """Une los subconjuntos a los que pertencen a y b."""

        subconjunto_a = self._get_subconjunto(a)
        subconjunto_b = self._get_subconjunto(b)

        if subconjunto_a is None or subconjunto_b is None:
            return None

        if subconjunto_a[1] >= subconjunto_b[1]:
            if subconjunto_a[1] == subconjunto_b[1]:
                subconjunto_a[1] += 1
            subconjunto_a[0].extend(subconjunto_b[0])
            self._subconjuntos.pop(subconjunto_b[2])
            self._padres[subconjunto_b[2]] = subconjunto_a[2]
        else:
            subconjunto_b[0].extend(subconjunto_a[0])
            self._subconjuntos.pop(subconjunto_a[2])
            self._padres[subconjunto_a[2]] = subconjunto_b[2]


class TestParticion(unittest.TestCase):

    def test_particion(self, n=100):
        """
        Función que realiza varias pruebas sobre la clase Particion,
        siendo n el número de elementos.
        """

        p = Particion(range(n))

        # Tenemos n elementos
        self.assertEqual(p.numero(), n)

        # Tenemos n subconjuntos
        self.assertEqual(len(p), n)

        # Los elmentos 0, 1, ... n-1 están cada uno en un subconjunto
        for v in range(n):
            self.assertEqual(p.numero(v), 1)
            self.assertEqual(p[v], v)

        # Comprobamos que tenemos los valores 0, 1, ... n-1
        s = set(range(n))
        for v in p:
            self.assertEqual(p[v], v)
            self.assertIn(v, s)
            s.remove(v)
        self.assertFalse(s)

        # Hacemos n - 1 uniones, comprobando la situación de la partición
        for v in range(1, n):
            self.assertEqual(p.numero(0), v)
            self.assertEqual(p.numero(v), 1)
            self.assertNotEqual(p[0], p[v])
            self.assertNotEqual(p[v - 1], p[v])
            p.une(0, v)
            self.assertEqual(p[0], p[v])
            self.assertEqual(p[v - 1], p[v])
            self.assertEqual(len(p), n - v)

    def test_uniones_aleatorias(self, n=100, repeticiones=10, semilla=1):
        """
        Partición con n elementos, en la que hacemos varias uniones aleatorias
        sobre particiones de n elementos.
        """

        random.seed(semilla)
        for i in range(repeticiones):
            p = Particion(range(n))
            s = set(range(n))
            self.assertEqual(p.numero(), n)
            while len(p) > 1:
                a, b = random.sample(s, 2)
                self.assertNotEqual(p[a], p[b])
                num = p.numero(a) + p.numero(b)
                p.une(a, b)
                self.assertEqual(p[a], p[b])
                self.assertEqual(num, p.numero(a))
                self.assertEqual(num, p.numero(b))
                s.remove(b)
                self.assertEqual(p.numero(), n)


def arbol_extendido_kruskal(grafo): #TODO
    """
    Dado un grafo devuelve otro grafo con el árbol expandido mínimo,
    utilizando el algoritmo de Kruskal.
    Los grafos son diccionario donde las claves son arcos (pares de nodos) y los
    valores son el peso de los arcos.
    """
    nodos = set([nodo for arco in grafo for nodo in arco])
    p = Particion(nodos)
    abiertos = list(grafo.items())
    abiertos.sort(key=lambda arco: arco[1], reverse=True)
    cerrados = {}
    while len(abiertos) > 0:
        arco = abiertos.pop()
        subconjunto_origen = p[arco[0][0]]
        if not isinstance(subconjunto_origen, list) or not arco[0][1] in subconjunto_origen:
            p.une(*arco[0])
            cerrados[arco[0]] = arco[1]
    return cerrados


class TestArbolExtendidoKruskal(unittest.TestCase):
    
    def test_6_nodos_9_arcos(self):
            
        g = {("a", "b"): 13, 
             ("a", "c"): 8,
             ("a", "d"): 1,
             ("b", "c"): 15,
             ("c", "d"): 5,
             ("c", "e"): 3,
             ("d", "e"): 4,
             ("d", "f"): 5,
             ("e", "f"): 2}
    
        t = {("a", "b"): 13, 
             ("a", "d"): 1,
             ("c", "e"): 3,
             ("d", "e"): 4,
             ("e", "f"): 2}
        
        self.assertEqual(arbol_extendido_kruskal(g), t)
    
    def test_7_nodos_12_arcos(self):
    
        g = {("a", "b"): 2, 
             ("a", "c"): 4,
             ("a", "d"): 1,
             ("b", "d"): 3,
             ("b", "e"): 10,
             ("c", "d"): 2,
             ("c", "f"): 5,
             ("d", "e"): 7,
             ("d", "f"): 8,
             ("d", "g"): 4,
             ("e", "g"): 6,
             ("f", "g"): 1}
        
        t = {("a", "b"): 2, 
             ("a", "d"): 1,
             ("c", "d"): 2,
             ("d", "g"): 4,
             ("e", "g"): 6,
             ("f", "g"): 1}
    
        self.assertEqual(arbol_extendido_kruskal(g), t)
        
    def test_grafo_aleatorio(self, n=10, repeticiones=10, semilla=1):
        """Tests con grafos completos aleatorios de n nodos"""
        
        random.seed(semilla)
        for _ in range(repeticiones):
            
            # Creamos el grafo
            g = {(i, j): n + 1 for i in range(n - 1) for j in range(i + 1, n)}
            for i in range(1, n + 1):
                g[random.randint(0, i - 1), i] = i
            t = arbol_extendido_kruskal(g)
            
            # Comprobamos que los arcos del árbol están en el grado y 
            # que el peso total es el esperado
            total = 0
            for arco, peso in t.items():
                self.assertEqual(peso, g[arco])
                total += peso
            self.assertEqual(total, n * (n + 1) / 2)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)