""" Monopoly game

GUI done in PyQt5 using monopoly_core.py
"""


import sys
import time
from PyQt5.QtWidgets import (
    QLineEdit,
    QWidget,
    QApplication,
    QLabel,
    QMainWindow,
    QGridLayout,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QErrorMessage,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsGridLayout,
    QGraphicsWidget,
    QGraphicsLinearLayout,
    QGraphicsTextItem,
    QGraphicsEllipseItem,
)
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
import monopoly_core as mp_core


class MainWindow(QMainWindow):
    """ main window where i display the various widgets """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Monopoly")
        self.central_widget = QStackedWidget()

        self.title_screen = TitleScreen()
        self.title_screen.start_game.clicked.connect(self.choose_names)

        self.setCentralWidget(self.central_widget)
        self.central_widget.addWidget(self.title_screen)

    def choose_names(self):
        """ check the nb players field, open the names screen """

        try:
            nb_players = int(self.title_screen.nb_players.text())

            if nb_players > 6:
                error = QErrorMessage()
                error.showMessage("Can't have more than 6 players")
                error.exec_()
                return

        except Exception as e:
            error = QErrorMessage()
            error.showMessage(f"{e}")
            error.exec_()
        else:
            self.names_screen = NamesPlayers(nb_players)
            self.central_widget.addWidget(self.names_screen)
            self.central_widget.setCurrentWidget(self.names_screen)

            self.names_screen.confirm_button.clicked.connect(self.create_players)

    def create_players(self):
        """ check the names fields, open the game screen """

        players = []

        for player in self.names_screen.player_names:
            name = player.text()

            if name == "":
                error = QErrorMessage()
                error.showMessage("Please give all players names")
                error.exec_()
                return

            players.append(mp_core.Player(name))

        self.game = Monopoly(players)
        self.central_widget.addWidget(self.game)
        self.central_widget.setCurrentWidget(self.game)


class TitleScreen(QWidget):
    """ title screen, ask how many players """

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()
        description_layout = QHBoxLayout()
        nb_players_layout = QGridLayout()
        button_layout = QHBoxLayout()

        description = QLabel("Hallo, this is my Monopoly GUI game")
        label = QLabel("How many players? :")
        self.nb_players = QLineEdit()
        self.start_game = QPushButton("Start game")

        description_layout.addWidget(description)
        nb_players_layout.addWidget(label, 2, 0)
        nb_players_layout.addWidget(self.nb_players, 2, 1)
        button_layout.addWidget(self.start_game)

        for layout in [description_layout, nb_players_layout, button_layout]:
            main_layout.addLayout(layout)

        self.setLayout(main_layout)


class NamesPlayers(QWidget):
    """ name screen, ask the names of the players """

    def __init__(self, nb_players):
        super().__init__()

        self.player_names = []

        main_layout = QVBoxLayout()
        names_layout = QGridLayout()
        button_layout = QHBoxLayout()

        for i in range(nb_players):
            label = QLabel("Name :")
            player_name = QLineEdit()
            names_layout.addWidget(label, i, 0)
            names_layout.addWidget(player_name, i, 1)
            self.player_names.append(player_name)

        self.confirm_button = QPushButton("Confirm")

        button_layout.addWidget(self.confirm_button)

        main_layout.addLayout(names_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)


class Monopoly(QWidget):
    """ actual game, display the board and everything """

    def __init__(self, players):
        super().__init__()

        self.players = players

        self.main_layout = QVBoxLayout()
        self.turn_layout = QHBoxLayout()
        self.board_layout = QHBoxLayout()
        self.player_info_layout = QGridLayout()
        self.buttons_layout = QHBoxLayout()

        self.message_box = QMessageBox()
        self.ask = QMessageBox()

        if len(players) > 1:
            self.ordered_players = self.order_players()
        else:
            self.ordered_players = self.players

        self.player_generator()

        self.turn_label = QLabel()
        self.balance_info = QLabel()
        self.balance = QLabel()
        self.position_info = QLabel()
        self.position = QLabel()
        self.possessions_info = QLabel()
        self.possessions = QLabel()
        roll_button = QPushButton("Roll")

        self.view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.board = Board(self.players)
        self.board.setParent(self)
        self.scene.addItem(self.board)
        self.view.setScene(self.scene)

        self.pass_player_turn()
        self.update_interface()

        self.turn_layout.addWidget(self.turn_label)
        self.turn_layout.setAlignment(Qt.AlignCenter)
        self.board_layout.addWidget(self.view)
        self.player_info_layout.addWidget(self.balance_info, 1, 0, Qt.AlignCenter)
        self.player_info_layout.addWidget(self.balance, 2, 0, Qt.AlignCenter)
        self.player_info_layout.addWidget(self.position_info, 1, 1, Qt.AlignCenter)
        self.player_info_layout.addWidget(self.position, 2, 1, Qt.AlignCenter)
        self.player_info_layout.addWidget(self.possessions_info, 1, 2, Qt.AlignCenter)
        self.player_info_layout.addWidget(self.possessions, 2, 2, Qt.AlignCenter)
        self.buttons_layout.addWidget(roll_button)

        self.main_layout.addLayout(self.turn_layout)
        self.main_layout.addLayout(self.board_layout)
        self.main_layout.addLayout(self.player_info_layout)
        self.main_layout.addLayout(self.buttons_layout)

        self.setLayout(self.main_layout)

        roll_button.clicked.connect(self.play_turn)

    def player_generator(self):
        """ Generator for player turns """

        self.gen = (player for player in self.ordered_players)

    def pass_player_turn(self):
        try:
            self.current_player = next(self.gen)
        except StopIteration:
            self.player_generator()
            self.current_player = next(self.gen)

    def get_current_player(self):
        return self.current_player

    def update_turn(self):
        self.turn_label.setText(f"Turn of {self.current_player}")
        self.turn_label.setFont(QtGui.QFont("Comic Sans MS", 20, QtGui.QFont.Bold))

    def update_balance(self):
        self.balance_info.setText("Money left:")
        self.balance.setText(f"{self.current_player.get_balance()}")

    def update_position(self):
        tile = self.board.get_tile_current_player(self.current_player)

        self.position_info.setText("Current position:")
        self.position.setText(f"{tile.get_name()}")

    def update_possessions(self):
        self.possessions_info.setText("You have these properties:")
        self.possessions.setText(f"{self.current_player.get_possessions()}")

    def update_interface(self):
        self.update_turn()
        self.update_balance()
        self.update_position()
        self.update_possessions()

    def order_players(self):
        """ roll dices for players to order them """

        rolls = []

        for player in self.players:
            rolls.append(sum(mp_core.roll()[0:2]))

        rolls_players = sorted(set(zip(rolls, self.players)), key=lambda x: -x[0])
        ordered_players = [player[1] for player in rolls_players]

        message = "Order of players:\n"

        for roll, player in rolls_players:
            message += f"- {player} rolled {roll}\n"

        self.message_box.setText(message)
        self.message_box.exec_()

        return ordered_players

    def popup(self, message):
        self.message_box.setText(message)
        self.message_box.exec_()

    def play_turn(self, doubles = 0):
        """ Play the turn 
        
        Roll dice
        Move player
        Interact with the board
        Check bankrupcy
        """

        die1, die2, sum_dice = self.roll()

        current_tile = self.move_player(sum_dice)
        self.interact_board(current_tile)

        if die1 == die2:
            doubles += 1
            self.play_turn(doubles)
            self.update_interface()
        else:
            self.pass_player_turn()
            self.update_interface()

    def roll(self):
        """ roll and get new position """

        die1, die2, sum_dice = mp_core.roll()

        self.popup(f"{self.current_player} rolled {die1} and {die2}: {sum_dice}")

        return die1, die2, sum_dice

    def move_player(self, sum_dice):
        """ Move player on the board

        Get new position --> new tile
        Remove player from old tile
        Add player to new tile
        """
        
        # get the new tile according to the position of current player
        current_tile = self.board.get_tile_current_player(self.current_player)
        current_real_pos = self.board.board_positions[current_tile.get_pos()]
        new_real_pos = current_real_pos + sum_dice

        # if player gets passed last position of the board
        # "reset" the number to loop through the board
        if new_real_pos >= 40:
            new_real_pos -= 40

        # use the real position to get the fake position
        new_fake_pos = list(
            self.board.board_positions.keys()
        )[list(self.board.board_positions.values()).index(new_real_pos)]
        # use the fake position to get the new tile
        new_tile = self.board.get_tile(tile_pos = new_fake_pos)

        # add/remove token from new/current tile
        current_player_token = current_tile.get_token(self.current_player)
        current_tile.remove_token(current_player_token)
        new_tile.add_token(current_player_token)

        # remove token from layout
        current_tile.remove_token_layout(current_player_token)

        # add token in layout
        new_tile.display_game_pieces()

        # change token's tile
        current_player_token.set_tile(new_tile)

        time.sleep(0.5)

        self.popup(f"You landed on {new_tile.get_name()}")

        return new_tile

    def interact_board(self, tile):
        tile_name = tile.get_name()
        tile_pos = tile.get_pos()
        tile_real_pos = self.board.board_positions[tile_pos]

        if tile_name in mp_core.PROPERTIES[tile_real_pos]:
            if tile.is_owned():
                owner = tile.get_owner()
                rent = mp_core.PROPERTIES[tile_real_pos][tile_name]["Rent"]
                self.current_player.pay(rent)
                owner.receive(rent)
            else:
                price = mp_core.PROPERTIES[tile_real_pos][tile_name]["Price"]
                player_balance = self.current_player.get_balance()

                if player_balance < price:
                    self.message_box.setText("You don't have enough money to buy")
                    self.message_box.exec_()
                else:    
                    buy = self.ask.question(self, "", f"Buy {tile_name} for {price}?", self.ask.Yes | self.ask.No)
                    self.ask.exec_()
                    
                    if buy == self.ask.Yes:
                        self.current_player.add_possession(tile_name, price)
                        tile.set_owner(self.current_player)
                    


class Board(QGraphicsWidget):
    def __init__(self, players):
        super().__init__()
        self.total_tokens = []

        for player in players:
            self.total_tokens.append(Token(player))

        self.board_layout = QGraphicsGridLayout()
        self.board_layout.setSpacing(0)

        self.properties = [
            "Free Parking", "Strand", "Chance", "Fleet Street", "Trafalgar Square",
            "Fenchurch Street station", "Leicester Square", "Coventry Street", "Water Works", "Piccadilly", "Go to Jail",
            "Vine Street", "", "", "", "", "", "", "", "", "", "Regent Street",
            "Marlborough Street", "", "", "", "", "", "", "", "", "", "Oxford Street",
            "Community Chest", "", "", "", "", "", "", "", "", "", "Community Chest",
            "Bow Street", "", "", "", "", "", "", "", "", "", "Bond Street",
            "Marylebine station", "", "", "", "", "", "", "", "", "", "Liverpool Street station",
            "Northumberland Avenue", "", "", "", "", "", "", "", "", "", "Chance",
            "Whitehall", "", "", "", "", "", "", "", "", "", "Park Lane",
            "Electric Company", "", "", "", "", "", "", "", "", "", "Super Tax",
            "Pall Mall", "", "", "", "", "", "", "", "", "", "Mayfair",
            "Visit Jail", "Pentonville Road", "Euston Road", "Chance", "The Angel Islington", "King's Cross station",
            "Income Tax", "Whitechapel Road", "Community Chest", "Old Kent Road", "Start"
        ]

        self.board_positions = {
            0: 20, 1: 21, 2: 22, 3: 23, 4: 24,
            5: 25, 6: 26, 7: 27, 8: 28, 9: 29,
            10: 30, 11: 19, 21: 31, 22: 18, 32: 32,
            33: 17, 43: 33, 44: 16, 54: 34, 55: 15,
            65: 35, 66: 14, 76: 36, 77: 13, 87: 37,
            88: 12, 98: 38, 99: 11, 109: 39, 110: 10,
            111: 9, 112: 8, 113: 7, 114: 6, 115: 5,
            116: 4, 117: 3, 118: 2, 119: 1, 120: 0
        }

        positions = [(i, j) for i in range(11) for j in range(11)]

        for position, name in zip(positions, self.properties):
            if name == "":
                continue
            
            self.board_layout.addItem(Tile(name, grid2pos(position), players, parent=self), *position)

        self.setLayout(self.board_layout)

    def get_tile_current_player(self, current_player):
        for i in range(0, 40):
            tile = self.board_layout.itemAt(i)
            tokens = tile.has_tokens()

            if tokens:
                for token in tokens:
                    player = token.get_player()

                    if player == current_player:
                        return tile

    def get_tile(self, tile_name = None, tile_pos = None):
        """ Get tile object from name or pos """
        
        for i in range(0, 40):
            tile = self.board_layout.itemAt(i)
            
            if tile_name == tile.get_name():
                return tile

            if tile_pos == tile.get_pos():
                return tile


class Tile(QGraphicsWidget):
    def __init__(self, name, position, players, parent):
        super().__init__(parent=parent)
        self.name = name
        self.position = position
        self.tokens = []
        self.owner = False

        self.layout = QGraphicsLinearLayout()
        self.token_layout = QGraphicsGridLayout()
        self.token_layout.setSpacing(0.5)

        self.name_on_tile = QGraphicsWidget()
        self.info = QGraphicsWidget()

        self.layout.setOrientation(Qt.Vertical)
        self.setContentsMargins(75, 0, 90, 0)

        property_name = QGraphicsTextItem(self.name, parent=self.name_on_tile)
        
        if name in parent.properties:
            self.real_pos = parent.board_positions[parent.properties.index(name)]

            if self.real_pos in mp_core.PROPERTIES:
                self.price = mp_core.PROPERTIES[self.real_pos][name]["Price"]
                self.rent = mp_core.PROPERTIES[self.real_pos][name]["Rent"]
                money_info = QGraphicsTextItem(f"Price: {self.price}", parent=self.info)

            elif self.real_pos in mp_core.SPECIAL_CASES:
                tile = list(mp_core.SPECIAL_CASES[self.real_pos].keys())[0]

                if tile == "Start":
                    money_start = QGraphicsTextItem("Free monay: 200", parent=self.info)

                    for player in players:
                        token = Token(player)
                        token.set_tile(tile)
                        self.tokens.append(token)

                    self.display_game_pieces()

                elif tile in ["Income Tax", "Super Tax"]:
                    money = mp_core.SPECIAL_CASES[self.real_pos][tile]
                    money_tax = QGraphicsTextItem(f"Tax: -{money}", parent=self.info)

        self.layout.addItem(self.name_on_tile)
        self.layout.addItem(self.info)
        self.layout.addItem(self.token_layout)
        self.setLayout(self.layout)

        self.layout.setAlignment(self.layout, Qt.AlignCenter)

    def is_owned(self):
        if self.owner:
            return True
        else:
            return False

    def set_owner(self, player):
        self.owner = player

    def get_owner(self):
        return self.owner

    def add_token(self, token):
        self.tokens.append(token)

    def remove_token(self, token):
        self.tokens.remove(token)

    def get_name(self):
        return self.name

    def get_pos(self):
        return self.position

    def display_game_pieces(self):
        if len(self.tokens) == 6 or len(self.tokens) == 5 or len(self.tokens) == 4:
            sub_layout = True
            sub_pos = 0
        else:
            sub_layout = False

        for i, token in enumerate(self.tokens):
            if (len(self.tokens) == 4 and i >= 2) or (
                len(self.tokens) >= 5 and i >= 3
            ):
                if sub_layout:
                    self.token_layout.addItem(token, 1, sub_pos)
                    sub_pos += 1
            else:
                self.token_layout.addItem(token, 0, i)

        return self.token_layout

    def paint(self, painter, option, widget):
        painter.drawRects(self.boundingRect())

    def has_tokens(self):
        if self.tokens != []:
            return self.tokens
        else:
            return

    def get_token(self, player):
        for token in self.tokens:
            if player == token.get_player():
                return token

        return

    def remove_token_layout(self, token):
        self.token_layout.removeItem(token)


class Token(QGraphicsWidget):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.token = QGraphicsEllipseItem(0, 0, 20, 20, parent=self)

    def get_current_tile(self):
        return self.current_tile

    def set_tile(self, new_tile):
        self.current_tile = new_tile

    def get_player(self):
        return self.player


def grid2pos(values: list):
    row, column = values
    pos = (row * 10) + row + column
    return pos


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec_()



