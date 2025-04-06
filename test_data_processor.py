import unittest
from DataProcessor import DataProcessor

class TestDataProcessor(unittest.TestCase):

    def setUp(self):
        self.dp = DataProcessor()

    def agregar_velas(self, velas):
        for vela in velas:
            self.dp.agregar_vela(vela)

    def test_martillo(self):
        vela = {'open': 10, 'close': 10.2, 'high': 10.3, 'low': 9.0}
        self.agregar_velas([vela])
        self.assertTrue(self.dp.detectar_martillo())

    def test_envolvente(self):
        velas = [
            {'open': 10.5, 'close': 10.0, 'high': 10.6, 'low': 9.9},
            {'open': 9.9, 'close': 10.6, 'high': 10.7, 'low': 9.8}
        ]
        self.agregar_velas(velas)
        self.assertTrue(self.dp.detectar_envolvente())

    def test_inside_bar(self):
        velas = [
            {'open': 10, 'close': 11, 'high': 12, 'low': 9},
            {'open': 10.5, 'close': 10.6, 'high': 11.5, 'low': 9.5}
        ]
        self.agregar_velas(velas)
        self.assertTrue(self.dp.detectar_inside_bar())

    def test_outside_bar(self):
        velas = [
            {'open': 10, 'close': 10.5, 'high': 11, 'low': 9.5},
            {'open': 9, 'close': 11.5, 'high': 12, 'low': 8.5}
        ]
        self.agregar_velas(velas)
        self.assertTrue(self.dp.detectar_outside_bar())

    def test_doji(self):
        vela = {'open': 10, 'close': 10.01, 'high': 10.5, 'low': 9.5}
        self.agregar_velas([vela])
        self.assertTrue(self.dp.detectar_doji())

    def test_estrella_fugaz(self):
        vela = {'open': 10, 'close': 10.1, 'high': 12, 'low': 9.8}
        self.agregar_velas([vela])
        self.assertTrue(self.dp.detectar_estrella_fugaz())

    def test_hombre_colgado(self):
        vela = {'open': 10.5, 'close': 10.6, 'high': 10.8, 'low': 9.5}
        self.agregar_velas([vela])
        self.assertTrue(self.dp.detectar_hombre_colgado())

    def test_tres_soldados_blancos(self):
        velas = [
            {'open': 10, 'close': 11, 'high': 11.1, 'low': 9.9},
            {'open': 11.1, 'close': 12, 'high': 12.1, 'low': 11},
            {'open': 12.1, 'close': 13, 'high': 13.1, 'low': 12}
        ]
        self.agregar_velas(velas)
        self.assertTrue(self.dp.detectar_tres_soldados_blancos())

    def test_tres_cuervos_negros(self):
        velas = [
            {'open': 13, 'close': 12, 'high': 13.1, 'low': 11.9},
            {'open': 12, 'close': 11, 'high': 12.1, 'low': 10.9},
            {'open': 11, 'close': 10, 'high': 11.1, 'low': 9.9}
        ]
        self.agregar_velas(velas)
        self.assertTrue(self.dp.detectar_tres_cuervos_negros())

if __name__ == '__main__':
    unittest.main()
