import os
import unittest
try:
	os.chdir(os.path.join(os.getcwd(), 'p8'))
	print(os.getcwd())
except:
	pass


def subsecuencia_comun_mas_larga(x, y):
    """
    Dadas dos cadenas x e y devuelve una que es subsecuencia de ambas y que 
    tiene la longitud máxima de todas las subsecuencias comunes.
    """
    
    pass


def es_subsecuencia(subsecuencia, secuencia):
    """Indica si el primer argumento es subsecuencia del segundo"""
    
    it = iter(secuencia)   
    return all(c in it for c in subsecuencia)


class TestEsSubsecuencia(unittest.TestCase):

    def test_positivos(self):
        
        for subsecuencia, secuencia in (
                ("GTTC", "GTTCCTAATA"),
                ("CCTA", "GTTCCTAATA"),
                ("AATA", "GTTCCTAATA"),
                ("GTCAT", "GTTCCTAATA"),
                ("TCTAA", "GTTCCTAATA"),
                ("GTTCCTAATA", "GTTCCTAATA"),
        ):
            self.assertTrue(es_subsecuencia(subsecuencia, secuencia))
            
    def test_negativos(self):
        
        for subsecuencia, secuencia in (
                ("GTTCCTTATA", "GTTCCTAATA"),
                ("GGTTCCTAATA", "GTTCCTAATA"),            
                ("GTTCCTAATAA", "GTTCCTAATA"),
                ("GG", "GTTCCTAATA"), 
                ("AC", "GTTCCTAATA"), 
                ("TGTCCTAATA", "GTTCCTAATA"),
                ("ATAA", "GTTCCTAATA"), 

        ):
            self.assertFalse(es_subsecuencia(subsecuencia, secuencia))


class TestSubsecuenciaComunMasLarga(unittest.TestCase):

    def test_subsecuencia_comun_mas_larga(self):
        
        for s1, s2, longitud in (
            ("GTTCCTAATA", "CGATAATTGAGA", 6),
            ("ACDAADDADDDDCCBCBCAD", "ADBDBBCDBDAABBDDDCBB", 11),
            ("BBDABCCADCCADADDCACAACBA", "DBCBBDCBADABBBCCCDCACAADDACADD", 17),
            ("01111000000111100011", "10010100000100101111", 14),
            ('TTTATTTCGTCTAACTTATGACGTCCCTTCACGATCCAA',
             'TGGCCGGTTATTCAAGAGCGATATGTGCTATAAAGTGCC', 23)
        ):    
            for x, y in ((s1, s2), (s2, s1)):
                subsecuencia = subsecuencia_comun_mas_larga(x, y)
                self.assertEqual(len(subsecuencia), longitud)
                for secuencia in x, y:
                    self.assertTrue(es_subsecuencia(subsecuencia, secuencia))


def subsecuencias_comunes_mas_largas(x, y):
    """
    Dadas dos cadenas x e y devuelve un conjunto con todas las subsecuencias de 
    ambas que tienen longitud máxima.
    """
    
    pass


class TestSubsecuenciasComunesMasLarga(unittest.TestCase):

    def test_subsecuencias_comunes_mas_largas(self):
        
        for s1, s2, longitud, numero in ( 
                ("GTTCCTAATA", "CGATAATTGAGA", 6, 3),
                ("ACDAADDADDDDCCBCBCAD", "ADBDBBCDBDAABBDDDCBB", 11, 4),
                ("BBDABCCADCCADADDCACAACBA", "DBCBBDCBADABBBCCCDCACAADDACADD", 
                 17, 1),
                ("01111000000111100011", "10010100000100101111", 14, 10),
                ('TTTATTTCGTCTAACTTATGACGTCCCTTCACGATCCAA',
                 'TGGCCGGTTATTCAAGAGCGATATGTGCTATAAAGTGCC', 23, 20)
            
        ):    
            for x, y in ((s1, s2), (s2, s1)):
                subsecuencias = subsecuencias_comunes_mas_largas(x, y)
                self.assertTrue(isinstance(subsecuencias, set))
                self.assertEqual(len(subsecuencias), numero)
                for subsecuencia in subsecuencias:
                    self.assertEqual(len(subsecuencia), longitud)
                    for secuencia in x, y:
                        self.assertTrue(es_subsecuencia(subsecuencia, secuencia))               


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)