import tkinter
from tkinter import ttk
import funcs.basket_score_funcs


class Application(funcs.basket_score_funcs.Funcs):
    """
    Classe Application

    Inicializa a interface do programa
    """
    def __init__(self):
        """Constrói e inicializa os objetos necessários para a interface do programa"""
        self.root = tkinter.Tk()
        self.janela()
        self.frames_janela()
        self.widgets()
        self.tabela_partida_buscada()
        self.tabela_jogos()
        self.montaTabela()
        self.novo_jogo()
        self.buscar_partida()
        self.root.mainloop()

    def janela(self):
        """Define as configurações da janela do programa"""
        self.root.title('Basket Score')
        self.root.configure(background="#4169e1")
        self.root.geometry('700x530')
        self.root.iconbitmap('ícone.ico')
        self.root.resizable(False, False)

    def frames_janela(self):
        """Define os frames da janela do programa

        self.frame_addjogos: contém o campo de entrada para o placar e o botão para adicionar partida
        self.frame_buscarjogos: contém o campo de entrada de buscar de partida, botão para realizar busca e a view de
                                informações da partida encontrada
        self.frame_tabelajogos: contém a view de informações de todos as partidas cadastradas
        """
        self.frame_addjogos = tkinter.Frame(self.root, bd=4, bg='#f5f5f5', highlightbackground='#204ac8', highlightthickness=3)
        self.frame_addjogos.place(relx=0.25, rely=0.02, relwidth=0.5, relheight=0.23)

        self.frame_buscarjogos = tkinter.Frame(self.root, bd=4, bg='#f5f5f5', highlightbackground='#204ac8',
                                               highlightthickness=3)
        self.frame_buscarjogos.place(relx=0.02, rely=0.26, relwidth=0.96, relheight=0.32)

        self.frame_tabelajogos = tkinter.Frame(self.root, bd=4, bg='#f5f5f5', highlightbackground='#204ac8',
                                               highlightthickness=3)
        self.frame_tabelajogos.place(relx=0.02, rely=0.59, relwidth=0.96, relheight=0.39)

    def widgets(self):
        """Cria todos os widgets da janela do programa"""

        # widgets para adicionar jogos
        self.addjogo_label = tkinter.Label(self.frame_addjogos, text='NOVA PARTIDA', font=("Verdana", 13, 'bold'))
        self.addjogo_label.place(relx=0.31, rely=0.01)

        self.placar_label = tkinter.Label(self.frame_addjogos, text='Placar:', font="Verdana")
        self.placar_label.place(relx=0.2, rely=0.4)

        self.placar_entry = tkinter.Entry(self.frame_addjogos, font=("Verdana", 13, 'bold'), width=14)
        self.placar_entry.place(relx=0.4, rely=0.4)

        self.bt_addjogo = tkinter.Button(self.frame_addjogos, text="Adicionar partida", font=("Verdana", 10), width=23,
                                         background='#204ac8', foreground='white', command=self.adicionar_partida)
        self.bt_addjogo.place(relx=0.28, rely=0.72)

        # widgets para buscar jogos específicos
        self.buscarjogo_label = tkinter.Label(self.frame_buscarjogos, text='INFORMAÇÕES DA PARTIDA',
                                              font=("Verdana", 13, 'bold'))
        self.buscarjogo_label.place(relx=0.30, rely=0.01)

        self.numeropartida_label = tkinter.Label(self.frame_buscarjogos, text='Número da partida:', font="Verdana")
        self.numeropartida_label.place(relx=0.19, rely=0.25)

        self.numeropartida_entry = tkinter.Entry(self.frame_buscarjogos, font=("Verdana", 13, 'bold'), width=14)
        self.numeropartida_entry.place(relx=0.45, rely=0.25)

        self.bt_addjogo = tkinter.Button(self.frame_buscarjogos, text="Buscar partida", font=("Verdana", 10), width=23,
                                         background='#204ac8', foreground='white', command=self.buscar_partida)
        self.bt_addjogo.place(relx=0.39, rely=0.48)

    def tabela_partida_buscada(self):
        """Cria e configura a view de partida buscada"""

        self.partidabuscada = ttk.Treeview(self.frame_buscarjogos,
                                           column=('col1', 'col2', 'col3', 'col4', 'col5', 'col6'))
        self.partidabuscada.heading("#0", text='')
        self.partidabuscada.heading("#1", text='Jogo')
        self.partidabuscada.heading("#2", text='Placar')
        self.partidabuscada.heading("#3", text='Mín. da Temporada')
        self.partidabuscada.heading("#4", text='Máx. da Temporada')
        self.partidabuscada.heading("#5", text='Quebra record mín.')
        self.partidabuscada.heading("#6", text='Quebra record máx.')

        self.partidabuscada.column("#0", width='1')
        self.partidabuscada.column("#1", width='40')
        self.partidabuscada.column("#2", width='50')
        self.partidabuscada.column("#3", width='130')
        self.partidabuscada.column("#4", width='130')
        self.partidabuscada.column("#5", width='130')
        self.partidabuscada.column("#6", width='130')

        self.partidabuscada.place(relx=0, rely=0.7, relwidth=1, relheight=0.3)

    def tabela_jogos(self):
        """Cria e configura a view de todas as partidas cadastradas"""
        self.tabelajogos = ttk.Treeview(self.frame_tabelajogos, column=('col1', 'col2', 'col3', 'col4', 'col5', 'col6'))
        self.tabelajogos.heading("#0", text='')
        self.tabelajogos.heading("#1", text='Jogo')
        self.tabelajogos.heading("#2", text='Placar')
        self.tabelajogos.heading("#3", text='Mín. da Temporada')
        self.tabelajogos.heading("#4", text='Máx. da Temporada')
        self.tabelajogos.heading("#5", text='Quebra record mín.')
        self.tabelajogos.heading("#6", text='Quebra record máx.')

        self.tabelajogos.column("#0", width='1')
        self.tabelajogos.column("#1", width='40')
        self.tabelajogos.column("#2", width='50')
        self.tabelajogos.column("#3", width='130')
        self.tabelajogos.column("#4", width='130')
        self.tabelajogos.column("#5", width='130')
        self.tabelajogos.column("#6", width='130')

        self.tabelajogos.place(relx=0, rely=0, relwidth=0.97, relheight=1)

        self.scrolllista = tkinter.Scrollbar(self.frame_tabelajogos, orient='vertical')
        self.tabelajogos.configure(yscroll=self.scrolllista.set)
        self.scrolllista.place(relx=0.97, rely=0.01, relwidth=0.03, relheight=1)


Application()