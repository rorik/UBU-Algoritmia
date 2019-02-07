## ---- iterador_con_sustitucion ----
def iterador_con_sustitucion(iterable, cambios):
    """
    Dado un iterable genera sus valores una vez aplicadas las sustituciones 
    indicadas por el diccionario de cambios.
    Los valores no hay que devolverlos todos a la vez, se deben generar de uno 
    en uno.
    """

    for k in iterable:
        yield cambios.get(k, k)

def test_iterador_con_sustitucion(): 
    """
    Casos de prueba para iterador_con_sustitucion().
    """
    
    for iterable, cambios, iterable_sustituido in (
        ([1, 2, 3, 4, 1, 2], {2: 1, 1: 2, 3: 5}, [2, 1, 5, 4, 2, 1]),
        ([1, 2, 3, 4, 1, 2] * 100, {2: 1, 1: 2, 3: 5}, 
            [2, 1, 5, 4, 2, 1] * 100),
        ("abcdb" * 100, {'a': 'z', 'b': 'a', 'd': 'y'},
            ['z', 'a', 'c', 'y', 'a'] * 100)
    ):
        assert (list(iterador_con_sustitucion(iterable, cambios)) 
                == iterable_sustituido)
        it = iterador_con_sustitucion(iterable, cambios)
        for e in iterable_sustituido:
            assert e == next(it)
            
    for v in iterador_con_sustitucion(range(10**100), {0: 0}):
        if v >= 100:
            break
            
    return True
            
if __name__ == "__main__": 
    test_iterador_con_sustitucion()
    print("OK")

## ---- iterador_anidado ----

import collections   # por si es necesario usar collections.Iterable

def iterador_anidado(elemento):
    """
    Iterador que genera los valores en elemento recursivamente: si elemento no 
    es iterable genera solo elemento, pero si elemento es iterable genera sus
    elementos de manera recursiva.
    Los valores se deben generar de uno en uno.
    """
    
    if isinstance(elemento, collections.Iterable):
        for e in elemento:
            yield from iterador_anidado(e)
    else:
        yield elemento

def test_iterador_anidado():
    """
    Casos de prueba para iterador_anidado()
    """
    
    assert isinstance([4], collections.Iterable)

    assert not isinstance(4, collections.Iterable)
    
    assert list(iterador_anidado(4)) == [4]

    assert list(iterador_anidado([4])) == [4]

    assert list(iterador_anidado((4,))) == [4]

    assert list(iterador_anidado([[4]])) == [4]

    assert list(iterador_anidado([1, [2, [3], 4]])) == [1, 2, 3, 4]

    l1 = []; l2 = []; l3 = []
    for i in range(100):
        l1 += [i]
        l2 = [l2, i]
        assert l1 == list(iterador_anidado(l2))
        l3 = [(l3, [i])]
        assert l1 == list(iterador_anidado(l3))
        
    for v in iterador_anidado(range(10**100)):
        if v > 100:
            break
    
    return True

if __name__ == "__main__": 
    test_iterador_anidado()
    print("OK")

## ---- generador_media_movil ----

def generador_media_movil(iterable, longitud):
    """
    Dado un iterable de valores numéricos, genera los valores de la media móvil 
    de la longitud indicada.
    Por ejemplo, si la longitud es 3, generaría la media de los 3 primeros
    valores, de los valores del 2º al 4º, de los valores del 3º al 5º...
    Los valores se deben generar de uno en uno.
    """ 

    for i in range(len(iterable) - longitud + 1):
        yield sum(iterable[i:i+longitud])/longitud

def test_generador_media_movil(): 
    """
    Casos de prueba para generador_media_movil().
    """
    
    for secuencia in (list(range(10)), tuple(range(10)), range(10)):
        assert (list(generador_media_movil(secuencia, 1))
                == [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])
        assert (list(generador_media_movil(secuencia, 2))
                == [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5])
        assert (list(generador_media_movil(secuencia, 3))
                == [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0])   
        assert (list(generador_media_movil(secuencia, 4)) 
                == [1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5])  
        assert (list(generador_media_movil(secuencia, 5))
                == [2.0, 3.0, 4.0, 5.0, 6.0, 7.0])  

    assert list(generador_media_movil(range(100), 1)) == list(range(100))    
    assert list(generador_media_movil(range(100), 3)) == list(range(1, 99))    
    assert list(generador_media_movil(range(100), 5)) == list(range(2, 98))
    
    assert list(generador_media_movil(range(100), 2)) == [x + 0.5 for x in range(99)]
    assert list(generador_media_movil(range(100), 4)) == [x + 1.5 for x in range(97)]

    assert (list(generador_media_movil(range(100, 0, -1), 1)) 
            == list(range(100, 0, -1)))
    assert (list(generador_media_movil(range(100, 0, -1), 3)) 
            == list(range(99, 1, -1)))
    assert (list(generador_media_movil(range(100, 0, -1), 5)) 
            == list(range(98, 2, -1)))
    
    it = generador_media_movil(range(1000),4)
    for v in range(997):
        assert next(it) == v + 1.5 
        
    assert list(generador_media_movil([1, 2] * 1000, 2)) == [1.5] * 1999     
    assert list(generador_media_movil([1, 2] * 1000, 3)) == [4/3, 5/3] * 999
       
    for v in generador_media_movil(range(10**18), 10):
        if v >= 100:
            break
        
    return True

if __name__ == "__main__": 
    test_generador_media_movil()
    print("OK")

## ---- iterador_incluido ----

def iterador_incluido(itera_1, itera_2):
    """
    Dado un primer iterador o iterable, comprueba que sus elementos están
    incluidos en el mismo orden en los elementos de un segundo iterador o 
    iterable.
    """

    position = 0
    for e in itera_1:
        try:
            position = itera_2[position:].index(e)
        except ValueError:
            return False
    return True

def test_iterador_incluido():
    """
    Casos de prueba para iterador_incluido().
    """
    
    assert iterador_incluido(range(100), range(100))     
    assert iterador_incluido(range(99), range(100))     
    assert iterador_incluido(range(1,100), range(100))     

    assert not iterador_incluido(range(100), range(99))
    assert not iterador_incluido(range(100), range(1, 100))
    
    assert iterador_incluido(range(10, 90, 3), range(100))
    assert not iterador_incluido(range(10, 110, 3), range(100))

    assert not iterador_incluido(range(10, 110, 3), range(100))    
    
    l = list(range(10, 90, 3))
    assert iterador_incluido(l, range(100))
    l[20] = 11
    assert not iterador_incluido(l, range(100))
    assert not iterador_incluido(iter(l), range(100))
    
    assert iterador_incluido(range(1000), range(10**100))
    assert not iterador_incluido(range(10**100), range(1000))
    
    return True
    
if __name__ == "__main__": 
    test_iterador_incluido()
    print("OK")
