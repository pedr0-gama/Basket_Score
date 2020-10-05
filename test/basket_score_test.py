import unittest
import sqlite3


class BD_teste():

    def conecta_bd(self):
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()

    def desconecta_bd(self):
        self.conn.close()

    def montaTabela(self):
        self.conecta_bd()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS jogos(
                jogo INTEGER PRIMARY KEY,
                placar INTEGER(20),
                min_temporada INTEGER(20),
                máx_temporada INTEGER(20),
                quebra_min INTEGER(20),
                quebra_máx INTEGER(20)
            )
            """)
        self.conn.commit()


class Funcs_ajustadas(BD_teste):
    def adicionar_partida(self, placar_adicionado):
        try:
            int(placar_adicionado)
        except ValueError:
            return 'Valor inválido: digite um valor numérico inteiro'
        else:
            if 0 <= int(placar_adicionado) <= 1000:
                self.placar = int(placar_adicionado)

                self.mín_temporada = self.máx_temporada = self.placar
                self.cursor.execute('''SELECT placar, min_temporada, máx_temporada, quebra_min, quebra_máx FROM jogos 
                                    WHERE jogo = (SELECT MAX(jogo) FROM jogos)''')
                dados_últimapartida = self.cursor.fetchone()

                if dados_últimapartida is None:
                    self.quebra_mín = self.quebra_máx = 0

                else:
                    if self.placar >= dados_últimapartida[1]:
                        self.mín_temporada = dados_últimapartida[1]
                        self.quebra_mín = dados_últimapartida[3]
                    else:
                        self.mín_temporada = self.placar
                        self.quebra_mín = dados_últimapartida[3] + 1

                    if self.placar <= dados_últimapartida[2]:
                        self.máx_temporada = dados_últimapartida[2]
                        self.quebra_máx = dados_últimapartida[4]
                    else:
                        self.máx_temporada = self.placar
                        self.quebra_máx = dados_últimapartida[4] + 1

                self.cursor.execute('''INSERT INTO jogos (placar, min_temporada, máx_temporada, quebra_min, quebra_máx) 
                                                                           VALUES (?,?,?,?,?)''',
                                    (self.placar, self.mín_temporada, self.máx_temporada,
                                     self.quebra_mín, self.quebra_máx))
                self.conn.commit()
                self.cursor.execute('''SELECT placar, min_temporada, máx_temporada, quebra_min, quebra_máx FROM jogos 
                                    WHERE jogo = (SELECT MAX(jogo) FROM jogos)''')
                dados_últimapartida_1 = self.cursor.fetchone()
                return dados_últimapartida_1

            else:
                return 'Insira um valor inteiro entre 0 e 1000'

    def buscar_partida(self, numero_partida):
        jogos = list()

        self.cursor.execute('''SELECT jogo FROM jogos''')
        partida = self.cursor.fetchall()

        for i in range(0, len(partida)):
            jogos.append(partida[i][0])

        try:
            if int(numero_partida) in jogos:
                self.cursor.execute('''SELECT placar, min_temporada, máx_temporada, quebra_min, quebra_máx 
                                    FROM jogos WHERE jogo = ?''', (numero_partida,))
                partida_buscada = self.cursor.fetchone()
                return partida_buscada
            else:
                return 'Partida não encontrada'

        except ValueError:
            return 'Valor inválido: digite um valor numérico inteiro'


class basket_score_tests(unittest.TestCase, Funcs_ajustadas):

    def test_adicionar_partida_ValueError(self):
        partida_adicionada = self.adicionar_partida('s')
        self.assertEqual('Valor inválido: digite um valor numérico inteiro', partida_adicionada)

    def test_adicionar_partida_erro_de_intervalo(self):
        partida_adicionada = self.adicionar_partida(-1)
        self.assertEqual('Insira um valor inteiro entre 0 e 1000', partida_adicionada)

        partida_adicionada = self.adicionar_partida(1001)
        self.assertEqual('Insira um valor inteiro entre 0 e 1000', partida_adicionada)

    def test_adicionar_partida_banco_de_dados(self):
        self.montaTabela()

        partida_adicionada = self.adicionar_partida(12)
        self.assertEqual((12, 12, 12, 0, 0), partida_adicionada)

        partida_adicionada = self.adicionar_partida(24)
        self.assertEqual((24, 12, 24, 0, 1), partida_adicionada)

        partida_adicionada = self.adicionar_partida(10)
        self.assertEqual((10, 10, 24, 1, 1), partida_adicionada)

        partida_adicionada = self.adicionar_partida(12)
        self.assertEqual((12, 10, 24, 1, 1), partida_adicionada)

        self.desconecta_bd()

    def test_buscar_partida_banco_de_dados_ValueError(self):
        self.montaTabela()
        partida_buscada = self.buscar_partida('s')
        self.assertEqual('Valor inválido: digite um valor numérico inteiro', partida_buscada)
        self.desconecta_bd()

    def test_buscar_partida_erro_de_intervalo(self):
        self.montaTabela()

        self.adicionar_partida(12)
        partida_buscada = self.buscar_partida(2)
        self.assertEqual('Partida não encontrada', partida_buscada)

        self.desconecta_bd()

    def test_buscar_partida_banco_de_dados(self):
        self.montaTabela()

        partida_adicionada1 = self.adicionar_partida(12)
        partida_adicionada2 = self.adicionar_partida(24)
        partida_adicionada3 = self.adicionar_partida(10)

        partida_buscada = self.buscar_partida(1)
        self.assertEqual(partida_adicionada1, partida_buscada)

        partida_buscada = self.buscar_partida(2)
        self.assertEqual(partida_adicionada2, partida_buscada)

        partida_buscada = self.buscar_partida(3)
        self.assertEqual(partida_adicionada3, partida_buscada)

        self.desconecta_bd()


