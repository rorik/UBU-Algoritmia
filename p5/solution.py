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

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)