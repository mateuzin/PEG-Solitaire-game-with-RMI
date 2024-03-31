import Pyro4

@Pyro4.expose
@Pyro4.behavior(instance_mode='single')
class GameServer(object):
    def __init__(self):
        self.initial_board = [
            [-1, -1, 1, 1, 1, -1, -1],
            [-1, -1, 1, 1, 1, -1, -1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [-1, -1, 1, 1, 1, -1, -1],
            [-1, -1, 1, 1, 1, -1, -1],
        ]
        self.board = self.initial_board
        self.clients = []
        self.current_player = "P1"

    def register_client(self, client):
        self.clients.append(client)
        if len(self.clients) == 0:
            self.board = self.initial_board
        elif len(self.clients) == 1:
            self.board = self.initial_board
            return "P1"
        elif len(self.clients) == 2:
            return "P2"
        else:
            print("ASSISTINDO")
        print(client)

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

daemon = Pyro4.Daemon()
server = GameServer()
ns = Pyro4.locateNS()
uri = daemon.register(server)
ns.register("TESTE", uri)
print("Server started on: TESTE")
daemon.requestLoop()