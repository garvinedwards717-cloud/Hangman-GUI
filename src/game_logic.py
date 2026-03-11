import random


class HangmanGame:
    def __init__(self, difficulty="Medium"):
        self.word_sets = {
            "Easy": ["CAT", "DOG", "BOOK", "TREE", "GAME"],
            "Medium": ["PYTHON", "HANGMAN", "PROGRAM", "WINDOW", "BUTTON"],
            "Hard": ["DEVELOPER", "ALGORITHM", "FUNCTION", "COMPUTER", "KEYBOARD"],
        }
        self.set_difficulty(difficulty)

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.words = self.word_sets[difficulty]
        self.reset_game()

    def reset_game(self):
        self.secret_word = random.choice(self.words)
        self.guessed_letters = set()
        self.wrong_guesses = set()
        self.max_wrong = 6
        self.game_over = False
        self.won = False

    def guess_letter(self, letter):
        letter = letter.upper()

        if self.game_over:
            return None

        if not letter.isalpha() or len(letter) != 1:
            return None

        if letter in self.guessed_letters or letter in self.wrong_guesses:
            return None

        if letter in self.secret_word:
            self.guessed_letters.add(letter)
            self.check_game_over()
            return True
        else:
            self.wrong_guesses.add(letter)
            self.check_game_over()
            return False

    def check_game_over(self):
        if all(letter in self.guessed_letters for letter in self.secret_word):
            self.game_over = True
            self.won = True
        elif len(self.wrong_guesses) >= self.max_wrong:
            self.game_over = True
            self.won = False

    def get_display_word(self):
        return " ".join(
            letter if letter in self.guessed_letters else "_"
            for letter in self.secret_word
        )

    def get_wrong_guesses(self):
        return ", ".join(sorted(self.wrong_guesses))