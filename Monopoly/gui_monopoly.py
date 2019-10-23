import sys
from PyQt5.QtWidgets import (QLineEdit, QWidget, QApplication, QLabel,
                             QMainWindow, QGridLayout, QPushButton,
                             QStackedWidget, QVBoxLayout, QHBoxLayout,
                             QMessageBox, QErrorMessage)
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
import monopoly_console as ms


# self.board_positions = [
#    20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
#    19, "", "", "", "", "", "", "", "", "", 31,
#    18, "", "", "", "", "", "", "", "", "", 32,
#    17, "", "", "", "", "", "", "", "", "", 33,
#    16, "", "", "", "", "", "", "", "", "", 34,
#    15, "", "", "", "", "", "", "", "", "", 35,
#    14, "", "", "", "", "", "", "", "", "", 36,
#    13, "", "", "", "", "", "", "", "", "", 37,
#    12, "", "", "", "", "", "", "", "", "", 38,
#    11, "", "", "", "", "", "", "", "", "", 39,
#    10,  9,  8,  7,  6,  5,  4,  3,  2,  1,  0
# ]


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
      self.players = []

      for player in self.names_screen.player_names:
         name = player.text()
         
         if name == "":
            error = QErrorMessage()
            error.showMessage("Please give all players names")
            error.exec_()
            return

         self.players.append(ms.Player(name))

      self.game = Monopoly(self.players)
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

      self.main_layout = QVBoxLayout()
      self.turn_layout = QHBoxLayout()
      self.board_layout = QGridLayout()
      self.player_info_layout = QGridLayout()
      self.buttons_layout = QHBoxLayout()

      self.board_layout.setSpacing(0)

      if len(players) > 1:
         ordered_players = self.order_players(players)
      else:
         ordered_players = players

      turn_label = QLabel(f"Turn of {ordered_players[0]}")
      turn_label.setFont(QtGui.QFont("Comic Sans MS", 20, QtGui.QFont.Bold))

      self.board = [
         "Free Parking", "Strand", "Fleet Street", "Chance", "Trafalgar Square",
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
         10: 30, 11: 19, 12: 31, 13: 18, 14: 32,
         15: 17, 16: 33, 17: 16, 18: 34, 19: 15,
         20: 35, 21: 14, 22: 36, 23: 13, 24: 37,
         25: 12, 26: 38, 27: 11, 28: 39, 29: 10,
         30: 9, 31: 8, 32: 7, 33: 6, 34: 5,
         35: 4, 36: 3, 37: 2, 38: 1, 39: 0
      }

      positions = [(i, j) for i in range(11) for j in range(11)]

      for position, name in zip(positions, self.board):
         if name == "":
            continue
         
         # tile = QGridLayout()
         label = QLabel(name)
         label.setAlignment(Qt.AlignVCenter)
         label.setMargin(20)
         label.setStyleSheet("border: 1px solid black")
         # tile.addWidget(label, 0, 0)
         self.board_layout.addWidget(label, *position)


         # for i, player in enumerate(ordered_players):
            # tile.addWidget(QLabel(f"{player}"), 0, i)

         # self.board_layout.addLayout(tile, *position)

      roll_button = QPushButton("Roll")
      balance_info = QLabel("Money left:")
      balance = QLabel(f"{ordered_players[0].get_balance()}")
      possessions_info = QLabel("You have these properties:")
      possessions = QLabel(f"{ordered_players[0].get_possessions()}")

      self.turn_layout.addWidget(turn_label)
      self.turn_layout.setAlignment(Qt.AlignCenter)
      self.buttons_layout.addWidget(roll_button)
      self.player_info_layout.addWidget(balance_info, 1, 0, Qt.AlignCenter)
      self.player_info_layout.addWidget(balance, 2, 0, Qt.AlignCenter)
      self.player_info_layout.addWidget(possessions_info, 1, 2, Qt.AlignCenter)
      self.player_info_layout.addWidget(possessions, 2, 2, Qt.AlignCenter)

      self.main_layout.addLayout(self.turn_layout)
      self.main_layout.addLayout(self.board_layout)
      self.main_layout.addLayout(self.player_info_layout)
      self.main_layout.addLayout(self.buttons_layout)

      self.setLayout(self.main_layout)

      self.get_tile()

   def order_players(self, players):
      """ roll dices for players to order them """

      rolls = []

      for player in players:
         rolls.append(sum(ms.roll()))

      rolls_players = sorted(set(zip(rolls, players)), key=lambda x: -x[0])
      ordered_players = [player[1] for player in rolls_players]

      message_box = QMessageBox()
      message = "Order of players:\n"

      for roll, player in rolls_players:
         message += f"- {player} rolled {roll}\n"

      message_box.setText(message)
      message_box.exec_()

      return ordered_players

   def get_tile(self):
      for i in range(0, 40):
         property_name = self.board_layout.itemAt(i).widget().text()
         # property_name = self.board_layout.itemAt(i).itemAt(0).widget().text()
         true_position = self.board_positions[i]
         print(f"Property: {property_name} {true_position}")



if __name__ == "__main__":
   app = QApplication(sys.argv)

   window = MainWindow()
   window.show()

   app.exec_()