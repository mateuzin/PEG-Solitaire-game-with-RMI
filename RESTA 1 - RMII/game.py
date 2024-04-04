import pygame
import pygame_menu
import sys
import threading
import Pyro4
import time

server_running_thread = True

def login_client(Erro=None):
    def connect_button_clicked():
        ip = ip_entry.get_value()
        server_id = server_id_entry.get_value()
        nickname = nickname_entry.get_value()

        start_client(ip, server_id, nickname)

    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((500, 520))
    pygame.display.set_caption('RESTA UM - MENU')

    mytheme = pygame_menu.themes.Theme(
        background_color=(0, 0, 0, 0),
        title_background_color=(14, 36, 23),
        title_font_shadow=True,
        widget_padding=18,
        widget_alignment=pygame_menu.locals.ALIGN_LEFT
    )

    menu = pygame_menu.Menu('CLIENTE - LOGIN', 500, 520, theme=mytheme)

    if Erro == True:
        menu.add.label('IP ou ID incorretos, verifique com o servidor', font_size=15, margin=(0, 0), font_color=(255, 0, 0))

    ip_entry = menu.add.text_input('IP do SDN: ', default="192.168.15.100", maxchar=15, )  # retirar default
    server_id_entry = menu.add.text_input('ID do Servidor: ', default="TESTE", maxchar=15, )
    nickname_entry = menu.add.text_input('Nome: ', default="Exemplo", maxchar=15)

    menu.add.button('Iniciar', connect_button_clicked)
    menu.add.button('Voltar para Menu', main)
    menu.add.button('Sair', pygame_menu.events.EXIT)

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        menu.update(events)
        screen.fill((14, 36, 23))
        menu.draw(screen)

        pygame.display.flip()
        clock.tick(30)

def login_server(Erro=None):
    def connect_button_clicked():
        ip = ip_entry.get_value()
        server_id = server_id_entry.get_value()
        threading.Thread(target=start_server, args=(ip, server_id)).start()
        server_interface(ip, server_id)

    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((500, 520))
    pygame.display.set_caption('RESTA UM - MENU')

    mytheme = pygame_menu.themes.Theme(
        background_color=(0, 0, 0, 0),
        title_background_color=(14, 36, 23),
        title_font_shadow=True,
        widget_padding=18,
        widget_alignment=pygame_menu.locals.ALIGN_LEFT
    )

    menu = pygame_menu.Menu('SERVIDOR - LOGIN', 500, 520, theme=mytheme)

    if Erro == True:
        menu.add.label('IP incorreto, verifique com o servidor de nomes', font_size=15, margin=(0, 0), font_color=(255, 0, 0))

    ip_entry = menu.add.text_input('IP do SDN: ', default="192.168.15.100", maxchar=15, )  # retirar default
    server_id_entry = menu.add.text_input('ID do Servidor: ', default="TESTE", maxchar=15, )

    menu.add.button('Iniciar', connect_button_clicked)
    menu.add.button('Voltar para Menu', main)
    menu.add.button('Sair', pygame_menu.events.EXIT)

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        menu.update(events)
        screen.fill((14, 36, 23))
        menu.draw(screen)

        pygame.display.flip()
        clock.tick(30)

def server_interface(ip,server_id):

    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((400, 400))
    pygame.display.set_caption('RESTA UM - MENU')
    font_color = (128, 128, 128)

    mytheme = pygame_menu.themes.Theme(
        background_color=(0, 0, 0, 0),
        title_background_color=(14, 36, 23),
        title_font_shadow=True,
        widget_padding=18,
        widget_alignment=pygame_menu.locals.ALIGN_LEFT
    )

    menu = pygame_menu.Menu('SERVIDOR', 400, 400, theme=mytheme)

    menu.add.label(f'IP: {ip}', font_size=30, margin=(0, 0), font_color=font_color)
    menu.add.label(f'ID do Servidor: {server_id}', font_size=30, margin=(0, 0), font_color=font_color)
    menu.add.button('Sair', pygame_menu.events.EXIT)


    while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            menu.update(events)
            screen.fill((14, 36, 23))
            menu.draw(screen)

            pygame.display.flip()
            clock.tick(30)


def end(status=None):
    class EndScreen:
        def __init__(self):
            self.font_color = (128, 128, 128)
            self.seconds = 5

            pygame.init()
            clock = pygame.time.Clock()

            screen = pygame.display.set_mode((300, 160))

            self.mytheme = pygame_menu.themes.Theme(background_color=(0, 0, 0, 0),
                                                    title_background_color=(14, 36, 23),
                                                    title_font_shadow=True,
                                                    widget_padding=5,
                                                    )

            self.menu = pygame_menu.Menu(f"", 300, 160, theme=self.mytheme)
            self.menu.add.label(status, font_size=30, margin=(0, 0), font_color=(255, 0, 0))
            label = self.menu.add.label(f'Encerrando: {self.seconds}', font_size=30, margin=(0, 0),
                                        font_color=self.font_color)

            pygame.display.flip()  # Atualiza a tela antes da contagem regressiva

            while self.seconds > 0:
                events = pygame.event.get()
                for e in events:
                    if e.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                screen.fill((14, 36, 23))
                self.menu.update(events)
                self.menu.draw(screen)
                pygame.display.flip()
                clock.tick(1)
                self.seconds -= 1
                label.set_title(f'Encerrando: {self.seconds}')

            # Adiciona a mensagem após a contagem regressiva
            self.menu.draw(screen)
            pygame.display.flip()

            pygame.quit()
            sys.exit()

    if __name__ == "__main__":
        end_screen = EndScreen()


def start_client(ip, server_id, nickname):
    class Game_Client:

        def __init__(self):
            pygame.init()

            # Constantes
            self.WIDTH, self.HEIGHT = 1000, 600
            self.BOARD_WIDTH = 600  # Largura do tabuleiro
            self.chat_width, self.chat_height = 400, 600
            self.ROW_COUNT, self.COL_COUNT = 7, 7
            self.CELL_SIZE = self.BOARD_WIDTH // self.COL_COUNT
            self.FPS = 60

            # Variáveis
            self.selected_ball = None
            self.second_player = False
            self.player_id = None
            self.nickname = nickname
            self.ip = ip
            self.game_started = False
            self.player_turn = None

            self.chat_messages_print = []
            self.client = None
            self.chat_input = ""

            # Cores e imagens
            self.BLACK = (0, 0, 0)
            self.LIGHT_GREEN = (222, 252, 221)
            self.DARK_GREEN = (14, 36, 23)
            self.font_size1 = pygame.font.Font(None, 80)
            self.font_size2 = pygame.font.Font(None, 15)

            # Inicializa a tela
            self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
            pygame.display.set_caption("RESTA UM")
            self.clock = pygame.time.Clock()

            # RMI
            try:
                self.server_uri = "PYRONAME:" + server_id + "@" + ip + ":9090"
                self.server = Pyro4.Proxy(self.server_uri)
                if self.server.number_of_clients() == 0:
                    self.player_id = "P1"
                elif self.server.number_of_clients() == 1:
                    self.player_id = "P2"
                else:
                    self.player_id = "ASSISTINDO"

                self.server.register_client(self.player_id)
                # Cria o tabuleiro
                self.board = [row[:] for row in self.server.get_board()]
            except Pyro4.errors.CommunicationError:
                login_client(True)


        def draw_board(self):
            # Desenha o tabuleiro
            board_surface = pygame.Surface((self.BOARD_WIDTH, self.BOARD_WIDTH))
            board_surface.fill(self.LIGHT_GREEN)

            for row in range(self.ROW_COUNT):
                for col in range(self.COL_COUNT):
                    pygame.draw.rect(board_surface, self.DARK_GREEN,
                                     (col * self.CELL_SIZE, row * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE), 1)
                    if self.board[row][col] == 1:
                        pygame.draw.circle(
                            board_surface,
                            self.DARK_GREEN,
                            (col * self.CELL_SIZE + self.CELL_SIZE // 2, row * self.CELL_SIZE + self.CELL_SIZE // 2),
                            self.CELL_SIZE // 3,
                        )
                    elif self.selected_ball is not None and (
                            self.board[row][col] == 0
                            and (
                                    (abs(self.selected_ball[0] - row) == 2 and self.selected_ball[1] == col
                                     and self.board[self.selected_ball[0] - (self.selected_ball[0] - row) // 2][
                                         col] == 1)
                                    or
                                    (abs(self.selected_ball[1] - col) == 2 and self.selected_ball[0] == row
                                     and self.board[row][
                                         self.selected_ball[1] - (self.selected_ball[1] - col) // 2] == 1)
                            )
                    ):
                        pygame.draw.circle(
                            board_surface,
                            (128, 128, 128),
                            (col * self.CELL_SIZE + self.CELL_SIZE // 2, row * self.CELL_SIZE + self.CELL_SIZE // 2),
                            self.CELL_SIZE // 3,
                        )
                    elif self.board[row][col] == -1:
                        pygame.draw.rect(
                            board_surface,
                            self.DARK_GREEN,
                            (col * self.CELL_SIZE, row * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE),
                        )

            self.screen.blit(board_surface, (0, 0))

        def draw_chat(self):
            # Desenha o chat
            chat_surface = pygame.Surface((self.chat_width, self.chat_height))
            chat_surface.fill(self.LIGHT_GREEN)

            input_rect = pygame.draw.rect(
                chat_surface,
                self.DARK_GREEN,
                (24, 556, 352, 32),
            )

            pygame.draw.rect(
                chat_surface,
                self.BLACK,
                (0, 50, self.chat_width - 5, self.chat_height - 114),
            )

            pygame.draw.rect(
                chat_surface,
                self.BLACK,
                (0, 50, self.chat_width - 5, self.chat_height - 114),
            )

            # Renderiza a entrada de chat
            font = pygame.font.Font(None, 24)
            text_surface = font.render(self.chat_input, True, self.LIGHT_GREEN)
            chat_surface.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

            y_offset = 500

            for message in reversed(self.chat_messages_print):
                text_surface2 = font.render(message, True, self.LIGHT_GREEN)
                chat_surface.blit(text_surface2, (30, y_offset))
                y_offset -= 25

            self.screen.blit(chat_surface, (600, 0))

        def draw_surrender_button(self):
            self.quit_button_rect = pygame.Rect(880, 8, 100, 40)
            # Desenha o botão para desistir
            pygame.draw.rect(self.screen, self.DARK_GREEN, self.quit_button_rect)

            font = pygame.font.Font(None, 30)
            text_surface = font.render("Desistir", True, self.LIGHT_GREEN)
            text_rect = text_surface.get_rect(center=self.quit_button_rect.center)
            self.screen.blit(text_surface, text_rect)

        def handle_surrender_button_click(self, pos):
            # Verifica se o botão de desistir foi clicado
            if self.quit_button_rect.collidepoint(pos):
                self.server.check_winner(self.player_id, True)
                print("O jogador desistiu.")

        def draw_status_message(self):
            self.status_rect = pygame.Rect(700, 8, 100, 40)

            if not self.second_player:
                status_message = "AGUADANDO PLAYER 2"
            elif self.second_player and self.player_id == self.player_turn:
                status_message = "SUA VEZ"
            else:
                status_message = "AGUARDE SUA VEZ"

            pygame.draw.rect(self.screen, self.LIGHT_GREEN, self.status_rect)

            font = pygame.font.Font(None, 30)
            text_surface = font.render(status_message, True, self.DARK_GREEN)
            text_rect = text_surface.get_rect(center=self.status_rect.center)
            self.screen.blit(text_surface, text_rect)

        def selected_piece(self):
            # Destaca a peça selecionada
            if self.selected_ball is not None:
                pygame.draw.circle(
                    self.screen,
                    (74, 96, 83),
                    (self.selected_ball[1] * self.CELL_SIZE + self.CELL_SIZE // 2,
                     self.selected_ball[0] * self.CELL_SIZE + self.CELL_SIZE // 2),
                    self.CELL_SIZE // 3,
                    50,
                )

        def valid_move(self, src_row, src_col, row, col):
            # Realiza a movimentação
            if (
                    abs(src_row - row) == 2
                    and src_col == col
                    and self.board[src_row - (src_row - row) // 2][col] == 1
            ):
                # Move a peça
                self.board[row][col] = 1
                self.board[src_row][src_col] = 0

                # Remove a peça pulada
                jumped_row, jumped_col = (src_row - (src_row - row) // 2, col)
                self.board[jumped_row][jumped_col] = 0

                self.selected_ball = None
                print()
                return True

            elif (
                    abs(src_col - col) == 2
                    and src_row == row
                    and self.board[row][src_col - (src_col - col) // 2] == 1
            ):
                # Move a peça
                self.board[row][col] = 1
                self.board[src_row][src_col] = 0

                # Remove a peça pulada
                jumped_row, jumped_col = (row, src_col - (src_col - col) // 2)
                self.board[jumped_row][jumped_col] = 0

                self.selected_ball = None
                return True

            return False

        def number_of_players(self):
            if not self.game_started:
                if self.player_id == "P1":
                    if self.server.number_of_clients() == 2:
                        self.second_player = True
                        self.game_started = True
                elif self.player_id == "P2":
                    self.second_player = True
                    self.game_started = True
            else:
                self.player_turn = self.server.get_current_player()
                # print(self.player_turn) #debug

        def start_ping(self):
            self.running = True
            threading.Thread(target=self.ping_thread).start()

        def stop_ping(self):
            self.running = False

        def ping_thread(self):
            while self.running:
                try:
                    response = self.server.ping(self.player_id)
                    print("Received response:", response)
                except Pyro4.errors.CommunicationError:
                    print("Server not responding. Connection lost.")
                    break
                time.sleep(5)  # Ping a cada 5 segundos

        def run(self):
            run = True
            while run:
                pygame.event.pump()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        self.stop_ping()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        col = event.pos[0] // self.CELL_SIZE
                        row = event.pos[1] // self.CELL_SIZE
                        self.handle_surrender_button_click(event.pos)
                        if not self.second_player:
                            print("aguarde")  # debug
                        else:
                            if self.player_id == self.player_turn:  # Se for a vez do cliente
                                # Movimentos
                                if 0 <= row < self.ROW_COUNT and 0 <= col < self.COL_COUNT:
                                    if self.selected_ball is None and self.board[row][col] == 1:
                                        self.selected_ball = (row, col)
                                    elif self.selected_ball is not None and self.board[row][col] == 1:
                                        self.selected_ball = (row, col)
                                    elif self.selected_ball is not None and self.board[row][col] == 0:
                                        src_row, src_col = self.selected_ball
                                        if self.valid_move(src_row, src_col, row, col):
                                            self.server.update_board(self.board)
                                            print(f"JOGADA FEITA: {self.board}")  # debug
                                            self.server.check_winner(self.player_id)
                                            self.server.player_turn(self.player_id)  # muda jogada para o outro jogador
                                            print(self.player_turn)
                                    else:
                                        print("NÃO PODE")  # debug
                            else:  # Quando não for a vez
                                print(f"VEZ DO JOGADOR: {self.player_turn}")

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            # Enviar mensagem de chat
                            message = self.chat_input
                            if message:
                                self.server.update_chat_messages(message, self.nickname)
                                self.chat_input = ""
                        elif event.key == pygame.K_BACKSPACE:
                            self.chat_input = self.chat_input[:-1]
                        else:
                            self.chat_input += event.unicode
                self.draw_chat()
                self.draw_board()
                self.draw_surrender_button()
                self.draw_status_message()
                self.number_of_players()
                self.selected_piece()
                self.board = self.server.get_board()
                self.chat_messages_print = self.server.get_chat_messages()

                # FIM DE JOGO

                winner, surrender = self.server.get_winner()
                if self.server.check_winner() or surrender:
                    self.stop_ping()
                    if winner == "EMPATE":
                        end("EMPATE")
                    elif winner == self.player_id:
                        end("Você Ganhou")
                    else:
                        if surrender:
                            end("Você desistiu")
                        else:
                            end("Você Perdeu")

                pygame.display.flip()

                self.clock.tick(self.FPS)

            pygame.quit()

    if __name__ == "__main__":
        game = Game_Client()
        game.start_ping()
        game.run()
        game.stop_ping()

def start_server(ip,server_id):
    @Pyro4.expose
    @Pyro4.behavior(instance_mode='single')
    class GameServer(object):
        def __init__(self):
            # INICIAL
            self.initial_board = [
                    [-1, -1, 1, 1, 1, -1, -1],
                    [-1, -1, 1, 1, 1, -1, -1],
                    [1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 0, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1],
                    [-1, -1, 1, 1, 1, -1, -1],
                    [-1, -1, 1, 1, 1, -1, -1],
                ]

            # testar empate
            # self.initial_board = [
            #             [-1, -1, 1, 0, 0, -1, -1],
            #             [-1, -1, 1, 0, 0, -1, -1],
            #             [0, 0, 0, 0, 0, 0, 0],
            #             [0, 0, 1, 0, 0, 0, 0],
            #             [0, 0, 0, 0, 0, 0, 0],
            #             [-1, -1, 0, 0, 0, -1, -1],
            #             [-1, -1, 0, 0, 1, -1, -1],
            #         ]

            # testar vencedor
            # self.initial_board = [
            #     [-1, -1, 1, 0, 0, -1, -1],
            #     [-1, -1, 1, 0, 0, -1, -1],
            #     [0, 0, 0, 0, 0, 0, 0],
            #     [0, 0, 1, 0, 0, 0, 0],
            #     [0, 0, 0, 0, 0, 0, 0],
            #     [-1, -1, 0, 0, 0, -1, -1],
            #     [-1, -1, 0, 0, 0, -1, -1],
            # ]

            self.board = self.initial_board
            self.clients = []
            self.chat_messages = []
            self.current_player = "P1"
            self.ROW_COUNT, self.COL_COUNT = 7, 7
            self.winner = None
            self.surrender = False
            self.flag = 1
            self.client_ping_times = {}
            self.running = True
            threading.Thread(target=self.check_clients).start()
        def register_client(self, client):
            self.clients.append(client)
            print(client)
            self.client_ping_times[client] = time.time()
            if len(self.clients) == 1:
                self.board = self.initial_board

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

        def ping(self, client):

            self.client_ping_times[client] = time.time()
            return "pong"

        def check_clients(self):
            while self.running:
                # Verifica o tempo de ping de cada cliente
                for client in list(self.client_ping_times.keys()):
                    last_ping_time = self.client_ping_times[client]
                    if time.time() - last_ping_time > 10:
                        print(f"Cliente {client} desconectado.")
                        self.clients.remove(client)
                        self.check_winner(client, True)
                        del self.client_ping_times[client]
                        if len(self.clients) == 0:
                            self.__init__()

                time.sleep(5)

    if __name__ == "__main__":
        try:
            daemon = Pyro4.Daemon(ip)  # MUDAR PARA IP DA MÁQUINA
            server = GameServer()
            ns = Pyro4.locateNS()
            uri = daemon.register(server)
            ns.register(server_id, uri)
            print(f"Server started on: {server_id}")
            daemon.requestLoop()
        except Pyro4.errors.NamingError:
            login_server(True)


def main():
    pygame.init()
    clock = pygame.time.Clock()

    surface = pygame.display.set_mode((350, 440))
    pygame.display.set_caption('RESTA UM - MENU')

    mytheme = pygame_menu.themes.Theme(background_color=(0, 0, 0, 0),
                                       title_background_color=(14, 36, 23),
                                       cursor_selection_color=(222, 252, 221),
                                       title_font_shadow=True,
                                       widget_padding=25,
                                       )

    menu = pygame_menu.Menu('Resta 1', 350, 440, theme=mytheme)

    menu.add.button('Cliente', login_client)
    menu.add.button('Servidor', login_server)
    menu.add.button('Sair', pygame_menu.events.EXIT)

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        menu.update(events)
        surface.fill((14, 36, 23))
        menu.draw(surface)

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()
