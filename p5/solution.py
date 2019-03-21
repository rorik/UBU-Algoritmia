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
        self.subcunjuntos = [[i] for i in iterable]
        self.altura = [0] * len(iterable)
        self.padre = iterable

    def __len__(self):
        """Devuelve el número de subconjuntos en la partición."""

        return len(self.subcunjuntos)

    def numero(self, k=None):
        """
        Devuelve el número de elementos del subconjunto al que pertenece el 
        elemento k. 
        Si k es None devuelve el número total de elementos.
        """

        if k is None:
            return sum([len(i) for i in self.subcunjuntos])

        for i in self.subcunjuntos:
            if k in i:
                return len(i)

        return None

    def __getitem__(self, k):
        """
        Devuelve el subconjunto al que pertenece el elemento k.
        El subconjunto se identifica mediante uno de sus elementos.
        """

        for i in self.subcunjuntos:
            if k in i:
                if len(i) == 1:
                    return i[0]
                return i

        return None

    def __iter__(self):
        """
        Devuelve un iterador sobre los subconjuntos.
        Cada subconjunto se identifica mediante uno de sus elementos.
        """

        yield from self.padre

    def une(self, a, b):
        """Une los subconjuntos a los que pertencen a y b."""
        i_a = None
        i_b = None
        for i in range(len(self)):
            if a in self.subcunjuntos[i]:
                i_a = i
                if i_b is not None:
                    break
            if b in self.subcunjuntos[i]:
                i_b = i
                if i_a is not None:
                    break

        if i_a is None or i_b is None:
            return None

        if self.altura[i_a] == self.altura[i_b]:
            self.altura[i_a] += 1
            self.subcunjuntos[i_a].extend(self.subcunjuntos[i_b])
            self.subcunjuntos.pop(i_b)
            self.altura.pop(i_b)
        elif self.altura[i_a] > self.altura[i_b]:
            self.subcunjuntos[i_a].extend(self.subcunjuntos[i_b])
            self.subcunjuntos.pop(i_b)
            self.altura.pop(i_b)
        else:
            self.subcunjuntos[i_b].extend(self.subcunjuntos[i_a])
            self.subcunjuntos.pop(i_a)
            self.altura.pop(i_a)


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
    nodos = []
    for n1,n2 in grafo:
        if n1 not in grafo:
            nodos.append(n1)
        if n2 not in grafo:
            nodos.append(n2)

    p = Particion(nodos)
    arbol_extendido = {}
    
    for arco in grafo:
        n1, n2 = arco
        peso = grafo[arco]
        if p[n1] != p[n2]:
            p.une(n1,n2)
            arbol_extendido[(n1,n2)] = peso
    
    return arbol_extendido
        


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