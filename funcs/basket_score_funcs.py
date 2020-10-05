from tkinter import *
from tkinter import messagebox
import sqlite3


class Banco_Dados():
    """
    Classe Banco_Dados

    Engloba as funções responsáveis por inicializar o banco de dados do programa
    """
    def conecta_bd(self):
        """Função responsável por criar conexão com o banco de dados 'jogos'"""
        self.conn = sqlite3.connect("jogos.bd")
        self.cursor = self.conn.cursor()  # reduz o comando para facilitar o uso

    def desconecta_bd(self):
        """Função responsável por encerrar conexão com o banco de dados 'jogos'"""
        self.conn.close()

    def montaTabela(self):
        """Função responsável por criar a tabela do banco de dados 'jogos' (caso não exista)

        - jogo: número da partida (valor autoincrementado a cada placar adicionado)
        - placar: quantidade de pontos feitos em cada jogo (informado pelo usuário)
        - min_temporada: armazena o valor mínimo de pontos feitos em um jogo durante a temporada
        - máx_temporada: armazena o valor máximo de pontos feitos em um jogo durante a temporada
        - quebra_min: armazena a quantidade de vezes que o recorde mínimo de pontos feitos foi quebrado durante a
                      temporada
        - quebra_máx: armazena a quantidade de vezes que o recorde máximo de pontos feitos foi quebrado durante a
                      temporada
        """
        self.conecta_bd()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS jogos (
                jogo INTEGER PRIMARY KEY,
                placar INTEGER(20),
                min_temporada INTEGER(20),
                máx_temporada INTEGER(20),
                quebra_min INTEGER(20),
                quebra_máx INTEGER(20)
            )
            """)
        self.conn.commit()
        self.desconecta_bd()


class Funcs(Banco_Dados):
    """
    Classe Funcs

    Engloba as funções responsáveis por adicionar novas partidas ao banco de dados, calcular recordes máximo e mínimo,
    e a quantidade de vezes que esses recordes são quebrados
    """
    def adicionar_partida(self):
        """
        Adiciona nova partida ao banco de dados: a cada nova partida é amarzenado a quantidade de pontos marcados,
                                                 atualiza o mínimo e o máximo da temporada e quantas vezes foram
                                                 quebrados o recorde mínimo e o recorde máximo

        - self.placar: pontos feitos na partida (valor informado pelo usuário). Este valor deve ser um valor
                     inteiro, positivo, no intervalo entre 0 e 1000.
        - self.mín_temporada: menor valor de pontos feito na temporada
        - self.máx_temporada: maior valor de pontos feito na temporada
        - self.quebra_mín: quantidade de vezes que o recorde mínimo foi quebrado
        - self.quebra_máx: quantidade de vezes que o recorde máximo foi quebrado

        Mensagens de erro que podem ser expressas:

        - placar fora do intervalo de 0 a 1000: 'Erro de entrada. Valor inválido: digite um valor numérico inteiro'
        - valor inserido não númerico/inteiro: 'Erro de entrada. Valor inválido: digite um valor numérico inteiro'
        """
        if self.placar_entry.get():
            try:
                int(self.placar_entry.get())
            except ValueError:
                messagebox.showerror('Erro de entrada', 'Valor inválido: digite um valor numérico inteiro')
                self.placar_entry.delete(0, 'end')
            else:
                if 0 <= int(self.placar_entry.get()) <= 1000:
                    self.placar = int(self.placar_entry.get())

                    self.mín_temporada = self.máx_temporada = self.placar
                    self.conecta_bd()
                    self.cursor.execute('''SELECT placar, min_temporada, máx_temporada, quebra_min, quebra_máx FROM 
                                        jogos WHERE jogo = (SELECT MAX(jogo) FROM jogos)''')
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

                    self.desconecta_bd()

                    self.conecta_bd()
                    self.cursor.execute('''INSERT INTO jogos (placar, min_temporada, máx_temporada, quebra_min, quebra_máx) 
                                                                        VALUES (?,?,?,?,?)''',
                                        (self.placar, self.mín_temporada, self.máx_temporada,
                                         self.quebra_mín, self.quebra_máx))
                    self.conn.commit()
                    self.desconecta_bd()
                    self.novo_jogo()
                    self.placar_entry.delete(0, 'end')

                else:
                    messagebox.showerror('Erro de entrada', 'Insira um valor inteiro entre 0 e 1000')
                    self.placar_entry.delete(0, 'end')

    def novo_jogo(self):
        """
        Atualiza a view: a cada nova partida é atualizada a view com o número do jogo, placar, mínimo da temporada,
                         máximo da temporada, quebra do recorde mínimo e quebra do recorde máximo
        """
        self.tabelajogos.delete(*self.tabelajogos.get_children())
        self.conecta_bd()
        lista = self.cursor.execute("""SELECT jogo, placar, min_temporada, máx_temporada, quebra_min, quebra_máx 
                                    FROM jogos""")
        for i in lista:
            self.tabelajogos.insert("", END, values=i)
        self.desconecta_bd()

    def buscar_partida(self):
        """
        Busca no banco de dados: a partir do valor digitado pelo usuário é realizada uma pesquisa no banco de dados e
                                 são apresentados os respectivos dados acerca da partida.

        Mensagens de erro que podem ser expressas:

        - número da partida não consta no banco: 'Erro de entrada. Partida não encontrada'
        - valor inserido não númerico/inteiro: 'Erro de entrada. Valor inválido: digite um valor numérico inteiro'
        """
        jogos = list()

        self.conecta_bd()
        self.cursor.execute('''SELECT jogo FROM jogos''')
        partida = self.cursor.fetchall()
        self.desconecta_bd()

        for i in range(0, len(partida)):
            jogos.append(partida[i][0])

        if self.numeropartida_entry.get():
            try:
                if int(self.numeropartida_entry.get()) in jogos:
                    self.conecta_bd()
                    self.partidabuscada.delete(*self.partidabuscada.get_children())
                    partida_buscada = self.cursor.execute('''SELECT jogo, placar, min_temporada, máx_temporada, quebra_min, 
                                                            quebra_máx FROM jogos WHERE jogo = ?''',
                                                          (self.numeropartida_entry.get(),))
                    for i in partida_buscada:
                        self.partidabuscada.insert("", END, values=i)
                    self.desconecta_bd()
                    self.numeropartida_entry.delete(0, 'end')
                else:
                    messagebox.showerror('Erro de entrada', 'Partida não encontrada')
                    self.numeropartida_entry.delete(0, 'end')

            except ValueError:
                messagebox.showerror('Erro de entrada', 'Valor inválido: digite um valor numérico inteiro')
                self.numeropartida_entry.delete(0, 'end')
