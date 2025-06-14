import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from helper import create_countries_list, normalize

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Guess the Flag")
        self.setGeometry(1000, 500, 500, 300)

        self.countries = create_countries_list()
        self.index = 0

        self.chances = 5
        self.guess_num = 1
        self.streak = 0

        self.start_screen()

    def start_screen(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.welcome_label = QLabel("Welcome to Guess the Flag!\nWould you like to begin?", self)
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setWordWrap(True)
        layout.addWidget(self.welcome_label)

        start_button = QPushButton("Begin", self)
        start_button.setFixedSize(120, 40)
        layout.addWidget(start_button, alignment=Qt.AlignCenter)

        start_button.clicked.connect(self.on_begin)

    def on_begin(self):
        self.initUI()
        self.load_question()

    def initUI(self):
        central = QWidget() # central area of the window
        self.setCentralWidget(central)
        layout = QVBoxLayout(central) # adds a vertical box layout to central. now widgets will stack top to bottom

        # flag description
        self.description_label = QLabel("", self) # creates empty description label
        self.description_label.setWordWrap(True) # allows label's text to wrap onto multiple lines (instead of running off edge)
        layout.addWidget(self.description_label) # adds description label to the central layout

        # prompt text
        self.prompt_label = QLabel("What country does this flag belong to?", self) # creates prompt label
        layout.addWidget(self.prompt_label) # adds prompt label to the central layout

        # guess number
        guess_layout = QHBoxLayout() # creates a layout to put the guess number (horizontal, so adds widgets left to right)
        self.guess_label = QLabel(f"Guess #{self.guess_num}: ", self)
        guess_layout.addWidget(self.guess_label) # adds the guess number to the guess layout
        # input (text box)
        self.input_line = QLineEdit(self) # creates a text box for user's input
        self.input_line.setMinimumWidth(200) # never narrower than 200px
        self.input_line.setMaximumWidth(300) # never wider than 300px
        self.input_line.setMinimumHeight(30) # never shorter than 30px
        guess_layout.addWidget(self.input_line) # adds text box to the guess layout
        # submit button
        submit_button = QPushButton("Submit Guess", self) # creates button for submission
        submit_button.setFixedSize(120, 40)
        submit_button.clicked.connect(self.check_guess) # connects clicked signal to check_guess() so it runs the code to check the guess
        self.input_line.returnPressed.connect(self.check_guess) # connects "enter" key to check_guess() as well
        guess_layout.addWidget(submit_button) # adds button to the central layout

        layout.addLayout(guess_layout) # adds the guess layout to the main layout

        # info (streak & chances & messages)
        self.info_label = QLabel("", self) # creates label for streak, chances, etc
        self.info_label.setWordWrap(True) # allows label's text to wrap onto multiple lines (instead of running off edge)
        layout.addWidget(self.info_label) # adds info label to the central layout

    def load_question(self):
        self.chances = 5
        self.guess_num = 1
        self.guess_label.setText(f"Guess #{self.guess_num}: ")

        # for when list is over
        if self.index >= len(self.countries):
            QMessageBox.information(self, f"Wow! You go through the entire game! I actually can't believe it...")
            self.close()
            return

        # unpack the next question
        name, description, answers = self.countries[self.index] # take name, description, and answer set from current countries[index]
        self.current_name = name
        self.current_answers = answers
        self.description_label.setText(description)
        
        # update streak & chances in info label
        self.streak_message()

        self.input_line.clear() # clear the input line (because it's a new question)
        self.input_line.setFocus() # also allow the textbox to be the focus off the bat

    def check_guess(self):
        guess = self.input_line.text() # sets guess to whatever the user inputted

        if normalize(guess) == "":
            self.info_label.setText(
                f"You have to input something in the text box!\n"
                f"You still have {self.chances} chances remaining!"
            )

        # if guess is INCORRECT
        elif normalize(guess) not in self.current_answers:
            self.chances -= 1
            self.guess_num += 1
            self.input_line.clear()

            # if user still has chances
            if self.chances > 0:
                self.info_label.setText(
                    f"Sorry, {guess} is not correct! Try again.\n"
                    f"You have {self.chances} chances remaining!"
                )
                self.guess_label.setText(f"Guess #{self.guess_num}: ") # gotta update the guess number text
                
                return

            # if user ran out of chances
            response = QMessageBox.question(
                self, "You Lose, Keep Playing?",
                f"The correct answer was {self.current_name}!\n"
                "Would you like to keep playing?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes # this allows yes to be the default option
            )
            self.streak = 0 # streak gets reset to 0
            self.guess_num = 0

            if response == QMessageBox.Yes:
                self.index += 1
                self.load_question()
            else:
                QMessageBox.information(
                    self, "Thanks for Playing",
                    f"Thanks for playing!"
                )
                self.close()

        # if guess is CORRECT
        else:
            response = QMessageBox.question(
                self, "You Win, Keep Playing?",
                f"You win! It was {self.current_name}!\n"
                "Would you like to keep playing?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes # this allows yes to be the default option
            )
            self.streak += 1
            self.guess_num = 0

            if response == QMessageBox.Yes:
                self.index += 1
                self.load_question()
            else:
                QMessageBox.information(
                    self, "Thanks for Playing",
                    f"Thanks for playing! Your latest streak was {self.streak}"
                )
                self.close()

    def streak_message(self):
        info = ""
        if self.streak > 1:
            info += f"Streak: {self.streak}\n"
        if self.streak == 10:
            info += "Keep it up! You are on fire\n"
        if self.streak == 20:
            info += "You're a pro!\n"
        info += f"You have {self.chances} chances remaining!"
        self.info_label.setText(info)

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("gui_image.png"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
