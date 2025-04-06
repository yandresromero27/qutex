
import unittest
from data_processor import DataProcessor

class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        self.dp = DataProcessor()

    def agregar_velas(self, velas):
        for vela in velas:
            self.dp.agregar_vela(vela)

    def test_detectar_martillo(self):
        vela = {'open': 100, 'close': 102, 'high': 103, 'low': 95}
        self.dp.agregar_vela(vela)
        self.assertTrue(self.dp.detectar_martillo())

    def test_detectar_envolvente(self):
        velas = [
            {'open': 105, 'close': 100, 'high': 106, 'low': 99},
            {'open': 99, 'close': 107, 'high': 108, 'low': 98}
        ]
        self.agregar_velas(velas)
        self.assertTrue(self.dp.detectar_envolvente())

    def test_detectar_inside_bar(self):
        velas = [
            {'open': 100, 'close': 105, 'high': 110, 'low': 90},
            {'open': 102, 'close': 103, 'high': 108, 'low': 92}
        ]
        self.agregar_velas(velas)
        self.assertTrue(self.dp.detectar_inside_bar())

    def test_detectar_outside_bar(self):
        velas = [
            {'open': 100, 'close': 105, 'high': 110, 'low': 100},
            {'open': 108, 'close': 107, 'high': 112, 'low': 95}
        ]
        self.agregar_velas(velas)
        self.assertTrue(self.dp.detectar_outside_bar())

    def test_detectar_doji(self):
        vela = {'open': 100, 'close': 100.5, 'high': 110, 'low': 90}
        self.dp.agregar_vela(vela)
        self.assertTrue(self.dp.detectar_doji())

    def test_detectar_estrella_fugaz(self):
        vela = {'open': 100, 'close': 101, 'high': 115, 'low': 99}
        self.dp.agregar_vela(vela)
        self.assertTrue(self.dp.detectar_estrella_fugaz())

    def test_detectar_hombre_colgado(self):
        vela = {'open': 100, 'close': 101, 'high': 102, 'low': 90}
        self.dp.agregar_vela(vela)
        self.assertTrue(self.dp.detectar_hombre_colgado())

    def test_detectar_tres_soldados_blancos(self):
        velas = [
            {'open': 100, 'close': 105, 'high': 106, 'low': 99},
            {'open': 106, 'close': 110, 'high': 111, 'low': 105},
            {'open': 111, 'close': 115, 'high': 116, 'low': 110}
        ]
        self.agregar_velas(velas)
        self.assertTrue(self.dp.detectar_tres_soldados_blancos())

    def test_detectar_tres_cuervos_negros(self):
        velas = [
            {'open': 115, 'close': 110, 'high': 116, 'low': 109},
            {'open': 109, 'close': 105, 'high': 110, 'low': 104},
            {'open': 104, 'close': 100, 'high': 105, 'low': 99}
        ]
        self.agregar_velas(velas)
        self.assertTrue(self.dp.detectar_tres_cuervos_negros())

if __name__ == '__main__':
    unittest.main()
