import Pyro4

@Pyro4.expose
@Pyro4.behavior(instance_mode='single')
class GameServer(object):
    def __init__(self):
        #INICIAL
        # self.initial_board = [
        #         [-1, -1, 1, 1, 1, -1, -1],
        #         [-1, -1, 1, 1, 1, -1, -1],
        #         [1, 1, 1, 1, 1, 1, 1],
        #         [1, 1, 1, 0, 1, 1, 1],
        #         [1, 1, 1, 1, 1, 1, 1],
        #         [-1, -1, 1, 1, 1, -1, -1],
        #         [-1, -1, 1, 1, 1, -1, -1],
        #     ]

        #testar empate
        # self.initial_board = [
        #             [-1, -1, 1, 0, 0, -1, -1],
        #             [-1, -1, 1, 0, 0, -1, -1],
        #             [0, 0, 0, 0, 0, 0, 0],
        #             [0, 0, 1, 0, 0, 0, 0],
        #             [0, 0, 0, 0, 0, 0, 0],
        #             [-1, -1, 0, 0, 0, -1, -1],
        #             [-1, -1, 0, 0, 1, -1, -1],
        #         ]

        #testar vencedor
        self.initial_board = [
            [-1, -1, 1, 0, 0, -1, -1],
            [-1, -1, 1, 0, 0, -1, -1],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [-1, -1, 0, 0, 0, -1, -1],
            [-1, -1, 0, 0, 0, -1, -1],
        ]

        self.board = self.initial_board
        self.clients = []
        self.chat_messages = []
        self.current_player = "P1"
        self.ROW_COUNT, self.COL_COUNT = 7, 7
        self.winner = None
        self.surrender = False
        self.flag = 1

    def register_client(self, client):
        self.clients.append(client)
        if len(self.clients) == 0:
            GameServer()
        elif len(self.clients) == 1:
            self.board = self.initial_board
            return "P1"
        elif len(self.clients) == 2:
            return "P2"
        else:
            print("ASSISTINDO")
        print(len(self.clients))

    def number_of_clients(self):
        return len(self.clients)

    def update_board(self, move):
        self.board = [row[:] for row in move]

    def get_board(self):
        return self.board

    def player_turn(self, id):
        if id == "P1":
            self.current_player = "P2"
            print(self.current_player)
        elif id == "P2":
            self.current_player = "P1"
            print(self.current_player)

    def get_current_player(self):
        return self.current_player

    def update_chat_messages(self, messages, nickname):
        self.chat_messages.append(nickname + ": " + messages)
        print(f"CHAT:{self.chat_messages}")
        # Remova mensagens antigas se o limite for atingido
        if len(self.chat_messages) > 19:
            self.chat_messages.pop(0)

    def get_chat_messages(self):
        return self.chat_messages

    def check_available_moves(self):
        # Verifica movimentos disponíveis
        for row in range(self.ROW_COUNT):
            for col in range(self.COL_COUNT):
                if self.board[row][col] == 1:
                    # Verifica possíveis movimentos para cada peça
                    for delta_row, delta_col in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                        new_row, new_col = row + delta_row, col + delta_col
                        jump_row, jump_col = row + delta_row // 2, col + delta_col // 2

                        # Verifica se o movimento é válido
                        if (
                                0 <= new_row < self.ROW_COUNT
                                and 0 <= new_col < self.COL_COUNT
                                and self.board[new_row][new_col] == 0
                                and self.board[jump_row][jump_col] == 1
                        ):
                            return True  # Pelo menos um movimento disponível

        return False  # Nenhum movimento disponível

    def check_winner(self, id=None, surrender=False):
        if surrender:
            print(f"{id} - Desistiu")
            if id == "P1":
                self.winner = "P2"
            elif id == "P2":
                self.winner = "P1"
            self.surrender = True
        elif sum(row.count(1) for row in self.board) == 1:
            if self.flag == 1:
                self.winner = id
                self.flag = self.flag + 1
            else:
                print(f"{self.winner} Ganhou")

            return True
        elif not self.check_available_moves():
            self.winner = "EMPATE"
            return True
        return None

    def get_winner(self):
        return self.winner, self.surrender


daemon = Pyro4.Daemon("192.168.15.100") #MUDAR PARA IP DA MÁQUINA
server = GameServer()
ns = Pyro4.locateNS()
uri = daemon.register(server)
ns.register("TESTE", uri)
print("Server started on: TESTE")
daemon.requestLoop()