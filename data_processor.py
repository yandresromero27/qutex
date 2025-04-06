import pandas as pd

class DataProcessor:
    def __init__(self):
        self.velas = []
        self.ema_anteriores = {}
        self.emas = {}
        self.rsis = {}

    def agregar_vela(self, vela):
        self.velas.append(vela)
        if len(self.velas) > 200:
            self.velas.pop(0)

    def calcular_tendencia(self):
        if len(self.velas) < 2:
            return "Indefinida"
        return "Alcista" if self.velas[-1]['close'] > self.velas[-2]['close'] else "Bajista"

    def calcular_ema(self, periodo=5):
        if len(self.velas) < periodo:
            return 0.0
        precios_cierre = [v['close'] for v in self.velas[-periodo:]]
        return pd.Series(precios_cierre).ewm(span=periodo, adjust=False).mean().iloc[-1]

    def guardar_ema(self, periodo, valor):
        self.emas[periodo] = valor

    def obtener_ema_anterior(self, periodo):
        return self.ema_anteriores.get(periodo)

    def guardar_ema_anterior(self, periodo, valor):
        self.ema_anteriores[periodo] = valor

    def calcular_rsi(self, periodo=14):
        if len(self.velas) < periodo + 1:
            return 0.0
        precios = [v['close'] for v in self.velas]
        df = pd.DataFrame(precios, columns=['close'])
        delta = df['close'].diff()
        ganancia = delta.where(delta > 0, 0)
        perdida = -delta.where(delta < 0, 0)
        media_ganancia = ganancia.rolling(window=periodo).mean()
        media_perdida = perdida.rolling(window=periodo).mean()
        rs = media_ganancia / media_perdida
        rsi = 100 - (100 / (1 + rs))
        return rsi.iloc[-1] if not rsi.empty else 0.0

    def guardar_rsi(self, periodo, valor):
        self.rsis[periodo] = valor

    def detectar_martillo(self):
        if len(self.velas) < 1:
            return False

        vela = self.velas[-1]
        cuerpo = abs(vela['close'] - vela['open'])
        mecha_inferior = vela['open'] - vela['low'] if vela['open'] < vela['close'] else vela['close'] - vela['low']
        mecha_superior = vela['high'] - vela['close'] if vela['open'] < vela['close'] else vela['high'] - vela['open']

        if cuerpo == 0:
            return False

        if mecha_inferior > 2 * cuerpo and mecha_superior < cuerpo:
            return True

        return False

    def detectar_envolvente(self):
        if len(self.velas) < 2:
            return False

        vela1 = self.velas[-2]
        vela2 = self.velas[-1]

        es_bajista = vela1['close'] < vela1['open'] and vela2['close'] > vela2['open']
        envuelve = vela2['open'] < vela1['close'] and vela2['close'] > vela1['open']

        if es_bajista and envuelve:
            return True

        es_alcista = vela1['close'] > vela1['open'] and vela2['close'] < vela2['open']
        envuelve = vela2['open'] > vela1['close'] and vela2['close'] < vela1['open']

        if es_alcista and envuelve:
            return True

        return False

    def detectar_inside_bar(self):
        if len(self.velas) < 2:
            return False

        vela_anterior = self.velas[-2]
        vela_actual = self.velas[-1]

        return vela_actual['high'] < vela_anterior['high'] and vela_actual['low'] > vela_anterior['low']

    def detectar_outside_bar(self):
        if len(self.velas) < 2:
            return False

        vela_anterior = self.velas[-2]
        vela_actual = self.velas[-1]

        return vela_actual['high'] > vela_anterior['high'] and vela_actual['low'] < vela_anterior['low']

    def detectar_doji(self):
        if len(self.velas) < 1:
            return False

        vela = self.velas[-1]
        cuerpo = abs(vela['close'] - vela['open'])
        rango_total = vela['high'] - vela['low']

        return cuerpo <= 0.1 * rango_total

    def detectar_estrella_fugaz(self):
        if len(self.velas) < 1:
            return False

        vela = self.velas[-1]
        cuerpo = abs(vela['close'] - vela['open'])
        mecha_superior = vela['high'] - max(vela['close'], vela['open'])
        mecha_inferior = min(vela['close'], vela['open']) - vela['low']

        return mecha_superior > 2 * cuerpo and mecha_inferior < cuerpo

    def detectar_hombre_colgado(self):
        if len(self.velas) < 1:
            return False

        vela = self.velas[-1]
        cuerpo = abs(vela['close'] - vela['open'])
        mecha_inferior = min(vela['close'], vela['open']) - vela['low']
        mecha_superior = vela['high'] - max(vela['close'], vela['open'])

        return mecha_inferior > 2 * cuerpo and mecha_superior < cuerpo

    def detectar_tres_soldados_blancos(self):
        if len(self.velas) < 3:
            return False

        v1, v2, v3 = self.velas[-3:]
        return all(v['close'] > v['open'] for v in [v1, v2, v3]) and \
               v2['open'] > v1['open'] and v2['close'] > v1['close'] and \
               v3['open'] > v2['open'] and v3['close'] > v2['close']

    def detectar_tres_cuervos_negros(self):
        if len(self.velas) < 3:
            return False

        v1, v2, v3 = self.velas[-3:]
        return all(v['close'] < v['open'] for v in [v1, v2, v3]) and \
               v2['open'] < v1['open'] and v2['close'] < v1['close'] and \
               v3['open'] < v2['open'] and v3['close'] < v2['close']

    def verificar_patrones_tecnicos(self):
        patrones_detectados = []

        if self.detectar_martillo():
            patrones_detectados.append("Martillo")
        if self.detectar_envolvente():
            patrones_detectados.append("Envolvente")
        if self.detectar_inside_bar():
            patrones_detectados.append("Inside Bar")
        if self.detectar_outside_bar():
            patrones_detectados.append("Outside Bar")
        if self.detectar_doji():
            patrones_detectados.append("Doji")
        if self.detectar_estrella_fugaz():
            patrones_detectados.append("Estrella Fugaz")
        if self.detectar_hombre_colgado():
            patrones_detectados.append("Hombre Colgado")
        if self.detectar_tres_soldados_blancos():
            patrones_detectados.append("Tres Soldados Blancos")
        if self.detectar_tres_cuervos_negros():
            patrones_detectados.append("Tres Cuervos Negros")

        return patrones_detectados
