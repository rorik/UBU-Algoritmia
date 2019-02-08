from abc import ABCMeta, abstractmethod

class GrafoAbstracto(metaclass=ABCMeta):
    """Clase abstracta para trabajar con Grafos."""

    def __init__(self, dirigido = False):
        """Constructor. El argumento indica si el grafo es dirigido"""
        self._dirigido = dirigido

    def dirigido(self):
        """Indica si el grafo es o no dirigido"""
        return self._dirigido

    @abstractmethod
    def __len__( self ):
        """Número de nodos del grafo."""

    @abstractmethod
    def num_arcos(self):
        """Devuelve el número de arcos"""

    @abstractmethod       
    def inserta(self, nodo, destino = None, etiqueta = 1):
        """
        Inserta un nodo al grafo (si destino es None) o un arco.
        Si el arco ya existía se actualiza su etiqueta.
        Si alguno de los nodos del arco no está en el grafo, se inserta.
        Se supone que None no es una etiqueta válida.
        """

    @abstractmethod       
    def __contains__(self, nodo):
        """Indica si el nodo está en el grafo."""      
        
    @abstractmethod        
    def __getitem__(self, arco):
        """Dado un arco (un par de nodos) devuelve la etiqueta si el arco está
        en el grafo, en caso contrario devuelve None"""

    @abstractmethod        
    def __iter__(self):
        """Iterador sobre los nodos del grafo"""

    @abstractmethod
    def vecinos(self, origen):
        """Devuelve un iterable de los pares (destino,etiqueta) para un nodo 
        origen dado"""

class GrafoMatriz(GrafoAbstracto):
    """
    Implementación del tipo Grafo utilizando una matriz de adyacencia para 
    almacenar la información de los arcos.
    La matriz podría ser una lista de lista.
    """

    def __init__(self, dirigido = False):
        GrafoAbstracto.__init__(self, dirigido)
        self._matrix = []
        self._nodos = {}

    def __len__( self ):
        """Número de nodos del grafo."""
        return len(self._nodos)

    def num_arcos(self):
        """Devuelve el número de arcos"""
        arcos = 0
        if self.dirigido():
            for column in self._matrix:
                for arco in column:
                    if arco is not None:
                        arcos += 1
        else:
            for i in range(len(self)):
                for j in range(i+1):
                    if self._matrix[i][j] is not None:
                        arcos += 1
        return arcos

    def inserta(self, nodo, destino = None, etiqueta = 1):
        """
        Inserta un nodo al grafo (si destino es None) o un arco.
        Si el arco ya existía se actualiza su etiqueta.
        Si alguno de los nodos del arco no está en el grafo, se inserta.
        Se supone que None no es una etiqueta válida.
        """
        self._insertar_if(nodo)
        if destino is not None:
            self._insertar_if(destino)
            self._actualizar_arco(nodo, destino, etiqueta)

    def __contains__(self, nodo):
        """Indica si el nodo está en el grafo."""  
        return nodo in self._nodos
    
    def __getitem__(self, arco):
        """Dado un arco (un par de nodos) devuelve la etiqueta si el arco está
        en el grafo, en caso contrario devuelve None"""
        if self.__contains__(arco[0]) and self.__contains__(arco[1]):
            return self._obtener_arco(arco[0], arco[1])
        return None

    def __iter__(self):
        """Iterador sobre los nodos del grafo"""
        yield from self._nodos.keys()

    def vecinos(self, origen):
        """Devuelve un iterable de los pares (destino,etiqueta) para un nodo 
        origen dado"""
        posicion = self._posicion(origen)
        vecinos = []
        if posicion is not None:
            for i, etiqueta in enumerate(self._matrix[posicion]):
                if etiqueta is not None:
                    vecinos.append([self._obtener_vecino(i), etiqueta])
        return vecinos    

    def _insertar(self, nodo):
        """
        Inserta el nodo en la matriz y la lista de nodos.
        """
        self._nodos[nodo] = len(self)
        for column in self._matrix:
            column.append(None)
        self._matrix.append([None] * (len(self)))

    def _insertar_if(self, nodo):
        """
        Inserta el nodo si no existe ya en el grafo.
        """
        if not self.__contains__(nodo):
            self._insertar(nodo)

    def _posicion(self, nodo):
        """
        Devuelve la posicion de un nodo en los ejes de la matriz.
        """
        return self._nodos.get(nodo, None)

    def _actualizar_arco(self, nodo, destino, etiqueta):
        if etiqueta is None:
            raise ValueError("La etiqueta no puede ser None")
        self._matrix[self._posicion(nodo)][self._posicion(destino)] = etiqueta
        if not self.dirigido():
            self._matrix[self._posicion(destino)][self._posicion(nodo)] = etiqueta

    def _obtener_arco(self, nodo, destino):
        return self._matrix[self._posicion(nodo)][self._posicion(destino)]

    def _obtener_vecino(self, posicion):
        for k, v in self._nodos.items():
            if v == posicion:
                return k
        return None

class GrafoListas(GrafoAbstracto):
    """
    Implementación del tipo Grafo utilizando listas de adyacencia.
    Cada nodo tiene asociada una 'lista' con la información de los arcos que
    salen del nodo. 
    Dicha lista no tinene que ser necesariamente del tipo 'list' de Python.
    """

    def __init__(self, dirigido = False):
        GrafoAbstracto.__init__(self, dirigido)
        self._nodos = {}

    def __len__( self ):
        """Número de nodos del grafo."""
        return len(self._nodos)

    def num_arcos(self):
        """Devuelve el número de arcos"""
        arcos = 0
        for vecinos in self._nodos.values():
            arcos += len(vecinos)
        if not self.dirigido():
            arcos /= 2
        return arcos

    def inserta(self, nodo, destino = None, etiqueta = 1):
        """
        Inserta un nodo al grafo (si destino es None) o un arco.
        Si el arco ya existía se actualiza su etiqueta.
        Si alguno de los nodos del arco no está en el grafo, se inserta.
        Se supone que None no es una etiqueta válida.
        """
        self._insertar_if(nodo)
        if destino is not None:
            self._insertar_if(destino)
            self._actualizar_arco(nodo, destino, etiqueta)

    def __contains__(self, nodo):
        """Indica si el nodo está en el grafo."""  
        return nodo in self._nodos
    
    def __getitem__(self, arco):
        """Dado un arco (un par de nodos) devuelve la etiqueta si el arco está
        en el grafo, en caso contrario devuelve None"""
        if self.__contains__(arco[0]) and self.__contains__(arco[1]):
            for target in self._nodos[arco[0]]:
                if target[0] == arco[1]:
                    return target[1]
        return None

    def __iter__(self):
        """Iterador sobre los nodos del grafo"""
        yield from self._nodos.keys()

    def vecinos(self, origen):
        """Devuelve un iterable de los pares (destino,etiqueta) para un nodo 
        origen dado"""
        return self._nodos[origen]

    def _insertar_if(self, nodo):
        """
        Inserta el nodo si no existe ya en el grafo.
        """
        if not self.__contains__(nodo):
            self._nodos[nodo] = []

    def _actualizar_arco(self, nodo, destino, etiqueta, reversable = True):
        if etiqueta is None:
            raise ValueError("La etiqueta no puede ser None")
        
        updated = False
        for arco in self._nodos[nodo]:
            if arco[0] == destino:
                arco[1] = etiqueta
                updated = True
    
        if not updated:
            self._nodos[nodo].append([destino, etiqueta])
            if not self.dirigido():
                self._nodos[destino].append([nodo, etiqueta])
        elif not self.dirigido():
            for arco in self._nodos[destino]:
                if arco[0] == nodo:
                    arco[1] = etiqueta

def test_grafo(grafo):
    """Función que prueba las funciones sobre grafos. Espera un grafo vacío."""

    num_final = 10  # número de nodos del grafo final
    num_arcos = 0
    conjunto_nodos = set()  # nodos que debería tener el grafo
    conjunto_arcos = set()  # arcos que debería tener el grafo
    
    # Insertamos nodos y arcos en el grafo, comprobando que la información es 
    # coherente con lo que tenemos en conjunto_nodos y conjunto_arcos
    for n in range(num_final):
        assert len(grafo) == n
        nodo_n = "n" + str(n)
        grafo.inserta(nodo_n)
        conjunto_nodos.add(nodo_n)
        assert nodo_n in grafo 
        assert n not in grafo
        for m in range(n):
            nodo_m = "n" + str(m)
            etiqueta = num_final * n + m
            grafo.inserta(nodo_m, nodo_n, etiqueta)
            conjunto_arcos.add((nodo_m, nodo_n, etiqueta))
            num_arcos += 1
            assert num_arcos == grafo.num_arcos()
            assert grafo[nodo_m, nodo_n] == etiqueta
            if grafo.dirigido():
                assert grafo[nodo_n, nodo_m] == None
            else:
                assert grafo[nodo_n, nodo_m] == etiqueta
                conjunto_arcos.add((nodo_n, nodo_m, etiqueta))
    
    # Recorremos comproabando los nodos y para cada nodo sus vecinos
    for nodo_n in grafo:
        assert nodo_n in conjunto_nodos
        conjunto_nodos.remove(nodo_n)
        for nodo_m, etiqueta in grafo.vecinos(nodo_n):
            assert (nodo_n, nodo_m, etiqueta) in conjunto_arcos
            conjunto_arcos.remove((nodo_n, nodo_m, etiqueta))
            
    # Comprobamos que hemos recorrido todos los nodos y arcos
    assert len(conjunto_nodos) == 0
    assert len(conjunto_arcos) == 0

if __name__ == "__main__":     
    test_grafo(GrafoMatriz(False))
    test_grafo(GrafoMatriz(True))
    print("OK")

if __name__ == "__main__":     
    test_grafo(GrafoListas(False))
    test_grafo(GrafoListas(True))
    print("OK")
