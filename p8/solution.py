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

    matrix = [["" for j in y] for i in x]

    for i in range(len(x)):
        for j in range(len(y)):
            if x[i] == y[j]:
                if i == 0 or j == 0:
                    matrix[i][j] = x[i]
                else:
                    matrix[i][j] = matrix[i - 1][j - 1] + x[i]
            else:
                matrix[i][j] = max(matrix[i - 1][j], matrix[i][j - 1], key=len)

    subsequence = matrix[-1][-1]

    return subsequence


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
    # Create a (x+1)*(y+1) matrix, with all elements None except the first row (all empty sets)
    matrix = [[set()] * (len(y) + 1)] + [[None] * (len(y) + 1)  for _ in range(len(x))]

    # Set all elements in the first column as empty sets
    for i in range(1, len(x) + 1):
        matrix[i][0] = set()

    for i in range(1, len(x) + 1):
        for j in range(1, len(y) + 1):
            if x[i - 1] == y[j - 1]:
                if len(matrix[i - 1][j - 1]) == 0:
                    # Start of subsequence
                    matrix[i][j] = set(x[i - 1])
                else:
                    # Continue subsequence, append char to all previous subsequences
                    matrix[i][j] = set()
                    for string in matrix[i - 1][j - 1]:
                        matrix[i][j].add(string + x[i - 1])
            else:
                top = matrix[i - 1][j]
                left = matrix[i][j - 1]
                if len(top) == 0:
                    # Subsequences on the left side only (might be an empty set)
                    matrix[i][j] = left.copy()
                else:
                    if len(left) == 0:
                        # Subsequences on the top side only
                        matrix[i][j] = top.copy()
                    else:
                        # Subsequences on both sides
                        top_rank = len(next(iter(top)))
                        left_rank = len(next(iter(left)))
                        if top_rank == left_rank:
                            # Both are the same rank (longest subsequence length), unite both
                            matrix[i][j] = left.union(top)
                        elif top_rank > left_rank:
                            # The top subsequences are longer
                            matrix[i][j] = top.copy()
                        else:
                            # The left subsequences are longer
                            matrix[i][j] = left.copy()

    return matrix[-1][-1]


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
