import random
import json
from pathlib import Path


SAVE_FILE = Path("save_data.json")


class HangmanGame:
    def __init__(self, difficulty="Medium", category=None):
        self.word_sets = {
            "Easy": {
                "Animals": ["CAT", "DOG", "LION", "FROG", "BEAR"],
                "Food": ["CAKE", "RICE", "APPLE", "BREAD", "PIZZA"],
                "Countries": ["CHAD", "MALI", "CHILE", "INDIA", "JAPAN"],
            },
            "Medium": {
                "Programming": ["PYTHON", "BUTTON", "WINDOW", "CODING", "SCRIPT"],
                "Movies": ["BATMAN", "FROZEN", "AVATAR", "JOKER", "ALIENS"],
                "Animals": ["MONKEY", "RABBIT", "TIGERS", "DONKEY", "PIGEON"],
            },
            "Hard": {
                "Programming": ["DEVELOPER", "ALGORITHM", "FUNCTION", "COMPUTER", "KEYBOARD"],
                "Countries": ["ARGENTINA", "PORTUGAL", "SINGAPORE", "AUSTRALIA", "PAKISTAN"],
                "Movies": ["INCEPTION", "INTERSTELLAR", "GLADIATOR", "CASABLANCA", "WHIPLASH"],
            },
        }

        self.score = 0
        self.streak = 0
        self.best_streak = 0
        self.category = ""
        self.selected_category = category

        self.load_progress()
        self.set_difficulty(difficulty)

    def load_progress(self):
        if SAVE_FILE.exists():
            try:
                data = json.loads(SAVE_FILE.read_text())
                self.best_streak = data.get("best_streak", 0)
            except Exception:
                self.best_streak = 0

    def save_progress(self):
        data = {
            "best_streak": self.best_streak
        }
        try:
            SAVE_FILE.write_text(json.dumps(data))
        except Exception:
            pass

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.categories = self.word_sets[difficulty]

        if self.selected_category not in self.categories:
            self.selected_category = None

        self.reset_game()

    def set_category(self, category):
        if category == "Random":
            self.selected_category = None
        else:
            self.selected_category = category

        self.reset_game()

    def reset_game(self):
        if self.selected_category and self.selected_category in self.categories:
            self.category = self.selected_category
        else:
            self.category = random.choice(list(self.categories.keys()))

        self.secret_word = random.choice(self.categories[self.category])

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
        if all(l in self.guessed_letters for l in self.secret_word):
            self.game_over = True
            self.won = True
            self.apply_win_rewards()

        elif len(self.wrong_guesses) >= self.max_wrong:
            self.game_over = True
            self.won = False
            self.apply_loss_penalty()

    def apply_win_rewards(self):
        difficulty_bonus = {
            "Easy": 10,
            "Medium": 20,
            "Hard": 30,
        }

        remaining_bonus = self.max_wrong - len(self.wrong_guesses)
        round_score = difficulty_bonus[self.difficulty] + (remaining_bonus * 5)

        self.score += round_score
        self.streak += 1

        if self.streak > self.best_streak:
            self.best_streak = self.streak
            self.save_progress()

    def apply_loss_penalty(self):
        self.streak = 0

    def get_display_word(self):
        return " ".join(
            letter if letter in self.guessed_letters else "_"
            for letter in self.secret_word
        )

    def get_wrong_guesses(self):
        return ", ".join(sorted(self.wrong_guesses))