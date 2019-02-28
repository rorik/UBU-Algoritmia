## ---- generador_recurrencia ----

def generador_recurrencia(coeficientes, funcion_adicional, iniciales):
    """
    Generador de valores de acuerdo a una recurrencia:
    F(n) = coeficientes[0]*F(n-1) + coeficientes[1]*F(n-2) + ...
         + funcion_adicional(n)
    Los valores iniciales son F(0) = iniciales[0], F(1) = iniciales[1],...
    Los valores que se generan son F(0), F(1), F(2),...
    Se deben generar los valores de uno en uno, no hay que devolver varios.
    Debe generar valores indefinidamente, no hay que poner límites.
    Aunque sea una recurrencia, los valores *no* deben calcularse recursivamente.
    """
    previos = []
    n = 0
    while True:
        result = 0
        if n < len(iniciales):
            result = iniciales[n]
        else:
            for i, coeficiente in enumerate(coeficientes):
                if len(previos) <= i:
                    break
                result += coeficiente*previos[-i-1]
            result += funcion_adicional(n)
        yield result
        n += 1
        previos.append(result)


def comprueba_recurrencia(coeficientes, funcion_adicional, iniciales,
                          funcion_alternativa, numero_comprobaciones = 100,
                          epsilon = 0.1):
    """
    Dada una recurrencia (definida en términos de sus coeficientes,
    condiciones inciales y la función_adicional) comprueba si los valores
    generados son (aproximadamente) los mismos que los definidos por una función
    alternativa, para un determinado número de comprobaciones.
    """
    
    iterador = generador_recurrencia(coeficientes, funcion_adicional, iniciales)
    for n in range(numero_comprobaciones):
        if abs(next(iterador) - funcion_alternativa(n)) > epsilon:
            return False
    return True


def test_generador_recurrencia():
    """Casos de prueba para la función generador_recurrencia."""

    # Recurrencia f(0)=0, f(n)=f(n-1)+1, que se corresponde con f(n)=n
    assert comprueba_recurrencia([1], lambda n: 1, [0], lambda n: n)

    # Recurrencia f(0)=1, f(n)=2*f(n-1), que se corresponde con f(n)=2**n
    assert comprueba_recurrencia([2], lambda n: 0, [1], lambda n: 2**n)

    # Recurrencia f(0)=0, f(n)=f(n-1)+n, que se corresponde con f(n)=n*(n+1)/2
    assert comprueba_recurrencia([1], lambda n: n, [0],
                                 lambda n: n * (n + 1) / 2)

    # Recurrencia f(0)=0, f(n)=f(n-1)+n/2, que se corresponde con f(n)=n*(n+1)/4
    assert comprueba_recurrencia([1], lambda n: n / 2, [0],
                                 lambda n: n * (n + 1) / 4)

    # Recurrencia f(0)=1, f(n)=f(n-1)+2**n, que se corresponde con
    # f(n)=2**(n+1)-1
    assert comprueba_recurrencia([1], lambda n: 2 ** n, [1],
                                 lambda n: 2 ** (n + 1) - 1)

    # Recurrencia f(0)=0, f(1)=1, f(n)=4f(n-1)-4f(n-2), que se corresponde con
    # f(n)=2**(n-1)*n
    assert comprueba_recurrencia([4, -4], lambda n: 0, [0, 1],
                                 lambda n: 2 ** (n - 1) * n)

    # Recurrencia f(0)=0, f(1)=1, f(n)=2f(n-1)-f(n-2)+1, que se corresponde con
    # f(n)=n*(n+1)/2
    assert comprueba_recurrencia([2, -1], lambda n: 1, [0, 1],
                                 lambda n: n * (n + 1) / 2)

    # Recurrencia f(0)=0, f(1)=1, f(2)=2, f(n)=f(n-1)+f(n-2)-f(n-3), que se
    # corresponde con f(n)=n
    assert comprueba_recurrencia([1, 1, -1],lambda n: 0, [0, 1, 2],
                                 lambda n: n)

if __name__ == "__main__": 
    test_generador_recurrencia()
    print("OK")


## ---- RecurrenciaMaestra ----

from math import log

class RecurrenciaMaestra: 
    """
    Clase que representa una recurrencia de las que se consideran en el 
    teorema maestro, de la forma T(n)=aT(n/b)+n^k. Se interpreta que en n/b
    la división es entera.
    Además de los métodos que aparecen a continuación, tienen que funcionar 
    los siguientes operadores: 
        ==, !=,
        str(): la representación como cadena debe ser 'aT(n/b)+n^k'
        []: el parámetro entre corchetes es el valor de n para calcular T(n).
    """
    
    def __init__(self, a, b, k, inicial = 0):
        """
        Constructor de la clase, los parámetros a, b, y k son los que
        aparecen en la fórmula aT(n/b)+n^k. El parámetro inicial es el valor
        para T(0).
        """
        
        self._a = a
        self._b = b
        self._k = k
        self._inicial = inicial

        
    def metodo_maestro(self):
        """
        Devuelve una cadena con el tiempo de la recurrencia de acuerdo al 
        método maestro. La salida está en el formato "O(n^x)" o "O(n^x*log(n))",
        siendo x un número.
        """
        o = log(self._a, self._b)
        if o > self._k:
            return "O(n^{})".format(o)
        elif self._k <= 1:
            return "O(n^{}*log(n))".format(self._k)
        else:
            return "O(n^{})".format(self._k)
       
    def __iter__(self):
        """
        Generador de valores de la recurrencia: T(0), T(1), T(2), T(3)..., 
        indefinidamente.
        Aunque sea una recurrencia, los valores *no* deben calcularse 
        recursivamente.
        """
        
        previos = [self._inicial]
        n = 1
        yield self._inicial
        while True:
            result = self._a * previos[int(n/self._b)] + pow(n, self._k)
            yield result
            n += 1
            previos.append(result)

    def __eq__(self, value):
        if isinstance(value, RecurrenciaMaestra):
            return value._a == self._a and value._b == self._b and value._k == self._k and value._inicial == self._inicial
        return False
    
    def __str__(self):
        return "{}T(n/{})+n^{}".format(self._a, self._b, self._k)
    
    def __getitem__(self, n):
        return self._inicial if n == 0 else self._a * self[int(n/self._b)] + pow(n, self._k)


def test_recurrencia_maestra_metodo_maestro(): 
    """Casos de prueba para RecurrenciaMaestra.metodo_maestro().""" 
    
    # Recurrencia T(n)=3T(n/2)+O(n^2)
    resultado = RecurrenciaMaestra(3, 2, 2).metodo_maestro()
    assert resultado == "O(n^2)"
    
    # Recurrencia T(n)=2T(n/2)+O(n)
    resultado = RecurrenciaMaestra(2, 2, 1).metodo_maestro()
    assert resultado == "O(n^1*log(n))"

    # Recurrencia T(n)=3T(n/2)+O(n)
    resultado = RecurrenciaMaestra(3, 2, 1).metodo_maestro()
    # esperamos algo parecido a "O(n^1.5849625007211563)"
    assert "O(n^1.58" in resultado
    assert "log" not in resultado    

                 
if __name__ == "__main__":
    test_recurrencia_maestra_metodo_maestro()
    print("OK")


def test_recurrencia_maestra_operadores(): 
    """Casos de prueba para los operadores de RecurrenciaMaestra."""
    
    r1 = RecurrenciaMaestra(2, 2, 2)
    
    # Tests para los operadores == y !=
    assert r1 == RecurrenciaMaestra(2, 2, 2)
    assert not r1 != RecurrenciaMaestra(2, 2, 2)
    for a, b, k in ((1, 1, 1), (1, 1, 2), (1, 2, 1), (2, 1, 1) ):
        assert r1 != RecurrenciaMaestra(a, b, k)
        assert not r1 == RecurrenciaMaestra(a, b, k)

    # Tests para str()
    assert str(r1) == "2T(n/2)+n^2"
    assert str(RecurrenciaMaestra(7, 4, 3)) == "7T(n/4)+n^3"
    
    # Tests para []
    for n, valor in enumerate((0, 1, 6, 11, 28, 37, 58, 71, 120, 137, 174, 195, 
                               260, 285, 338, 367, 496, 529, 598, 635)):
        assert r1[n] == valor
        
    r2 = RecurrenciaMaestra(1, 2, 0, 1) 
    for n, valor in enumerate((1, 2, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 
                               6, 6, 6, 6)):
        assert r2[n] == valor 
               
    r3 = RecurrenciaMaestra(4, 3, 1)
    for n, valor in enumerate((0, 1, 2, 7, 8, 9, 14, 15, 16, 37, 38, 39, 44, 45,
                               46, 51, 52, 53, 74, 75)):
        assert r3[n] == valor  


if __name__ == "__main__":
    test_recurrencia_maestra_operadores()
    print("OK")


def test_recurrencia_maestra_genera(): 
    """Casos de prueba para la iteración sobre RecurrenciaMaestra."""
    
    for v1, v2 in zip(RecurrenciaMaestra(2, 2, 2),
                      (0, 1, 6, 11, 28, 37, 58, 71, 120, 137, 174, 195, 260, 
                       285, 338, 367, 496, 529, 598, 635)):
        assert v1 == v2

    for v1, v2 in zip(RecurrenciaMaestra(1, 2, 0, 1),
                      (1, 2, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6,
                       6)):
        assert v1 == v2
        
    for v1, v2 in zip(RecurrenciaMaestra(4, 3, 1),
                      (0, 1, 2, 7, 8, 9, 14, 15, 16, 37, 38, 39, 44, 45, 46, 51,
                       52, 53, 74, 75)):
        assert v1 == v2        

        
if __name__ == "__main__":
    test_recurrencia_maestra_genera()
    print("OK")