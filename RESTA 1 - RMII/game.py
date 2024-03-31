import pygame
import pygame_menu
import sys
import threading
import Pyro4


def login(Erro=None):
    def connect_button_clicked():
        game()

    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((400, 520))
    pygame.display.set_caption('RESTA UM - MENU')

    mytheme = pygame_menu.themes.Theme(
        background_color=(0, 0, 0, 0),
        title_background_color=(14, 36, 23),
        title_font_shadow=True,
        widget_padding=18,
        widget_alignment=pygame_menu.locals.ALIGN_LEFT
    )

    menu = pygame_menu.Menu('CLIENTE - LOGIN', 400, 520, theme=mytheme)

    if Erro == True:
        menu.add.label('IP ou Porta incorretos, verifique com o servidor', font_size=15, margin=(0, 0), font_color=(255, 0, 0))

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

def end(status = None):
    class EndScreen:
        def __init__(self):
            self.font_color = (128, 128, 128)
            self.seconds = 5

            pygame.init()
            clock = pygame.time.Clock()

            screen = pygame.display.set_mode((300, 200))
            pygame.display.set_caption('')

            self.mytheme = pygame_menu.themes.Theme(background_color=(0, 0, 0, 0),
                                                    title_background_color=(14, 36, 23),
                                                    title_font_shadow=True,
                                                    widget_padding=5,
                                                    )

            self.menu = pygame_menu.Menu(f"", 300, 200, theme=self.mytheme)
            self.menu.add.label(status, font_size=30, margin=(0, 0), font_color=(255, 0, 0))
            label = self.menu.add.label(f'Encerrando: {self.seconds}', font_size=30, margin=(0, 0), font_color=self.font_color)

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
def game():
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
            self.send_movement = None
            self.current_local_play = None
            self.second_player = False #Alterar depois
            self.player_id = None
            self.game_started = False
            self.player_turn = None

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

            self.server_uri = "PYRONAME:TESTE"
            self.server = Pyro4.Proxy(self.server_uri)
            self.player_id = self.server.register_client("oi")

            # Cria o tabuleiro
            self.board = [row[:] for row in self.server.get_board()]

            # RMI e Thread
            self.chat_messages = []
            self.chat_messages_print = []
            self.client = None
            self.chat_input = ""




        def draw_board(self):
            # Desenha o tabuleiro
            board_surface = pygame.Surface((self.BOARD_WIDTH, self.BOARD_WIDTH))
            board_surface.fill(self.LIGHT_GREEN)

            for row in range(self.ROW_COUNT):
                for col in range(self.COL_COUNT):
                    pygame.draw.rect(board_surface, self.DARK_GREEN, (col * self.CELL_SIZE, row * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE), 1)
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

            y_offset = 60

            for message in self.chat_messages_print:
                text_surface2 = font.render(message, True, self.LIGHT_GREEN)
                chat_surface.blit(text_surface2, (30, y_offset))
                y_offset += 25

            self.screen.blit(chat_surface, (600, 0))

            # Remova mensagens antigas se o limite for atingido
            if len(self.chat_messages_print) > 19:
                self.chat_messages_print.pop(0)

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
                print("O jogador desistiu.")
                end(f" Desistiu")

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
                #print(self.player_turn) #debug

        def run(self):
            run = True
            while run:
                pygame.event.pump()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        col = event.pos[0] // self.CELL_SIZE
                        row = event.pos[1] // self.CELL_SIZE
                        self.handle_surrender_button_click(event.pos)
                        if not self.second_player:
                            print("aguarde")#debug
                        else:
                            if self.player_id == self.player_turn: # Se for a vez do cliente
                                # Movimentos
                                if 0 <= row < self.ROW_COUNT and 0 <= col < self.COL_COUNT:
                                    if self.selected_ball is None and self.board[row][col] == 1:
                                        self.selected_ball = (row, col)
                                    elif self.selected_ball is not None and self.board[row][col] == 1:
                                        self.selected_ball = (row, col)
                                    elif self.selected_ball is not None and self.board[row][col] == 0:
                                        src_row, src_col = self.selected_ball
                                        if self.valid_move(src_row, src_col, row, col):
                                            self.current_local_play = self.board
                                            self.server.update_board(self.board)
                                            print(f"JOGADA FEITA: {self.board}")  #debug
                                            self.server.player_turn(self.player_id) #muda jogada para o outro jogador
                                            print(self.player_turn)
                                    else:
                                        print("NÃO PODE")  #debug
                            else: #Quando não for a vez
                                print(f"VEZ DO JOGADOR: {self.player_turn}")

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            # Enviar mensagem de chat
                            message = self.chat_input
                            self.chat_messages_print.append(f"Você: {self.chat_input}")
                            print(message)#debug
                            if message:
                                self.chat_messages.append(message)
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

                # FIM DE JOGO
                if not self.check_available_moves():
                    text = self.font_size1.render("Game Over Player", True, (255, 0, 0), self.BLACK, )
                    self.screen.blit(text, (self.BOARD_WIDTH // 8, (self.HEIGHT // 2) - 30))

                pygame.display.flip()

                self.clock.tick(self.FPS)

            pygame.quit()

    if __name__ == "__main__":
        game = Game_Client()
        game.run()


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

    menu.add.button('Cliente', login)
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