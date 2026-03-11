import sys
from pathlib import Path
import pygame

from game_logic import HangmanGame
from ui import draw_game_screen, draw_win_screen, draw_lose_screen


WIDTH = 900
HEIGHT = 600
FPS = 60


def load_sound(path):
    try:
        if Path(path).exists():
            return pygame.mixer.Sound(path)
    except pygame.error:
        return None
    return None


def main() -> None:
    pygame.init()

    try:
        pygame.mixer.init()
    except pygame.error:
        pass

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Hangman GUI")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 54)

    sounds_dir = Path("sounds")
    correct_sound = load_sound(sounds_dir / "correct.wav")
    wrong_sound = load_sound(sounds_dir / "wrong.wav")
    win_sound = load_sound(sounds_dir / "win.wav")
    lose_sound = load_sound(sounds_dir / "lose.wav")

    background_music = sounds_dir / "background.mp3"
    if background_music.exists():
        try:
            pygame.mixer.music.load(str(background_music))
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)
        except pygame.error:
            pass

    game = HangmanGame("Medium")
    played_end_sound = False

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if game.game_over:
                    if event.key == pygame.K_RETURN:
                        game.reset_game()
                        played_end_sound = False
                else:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                    elif event.key == pygame.K_1:
                        game.set_difficulty("Easy")
                        played_end_sound = False

                    elif event.key == pygame.K_2:
                        game.set_difficulty("Medium")
                        played_end_sound = False

                    elif event.key == pygame.K_3:
                        game.set_difficulty("Hard")
                        played_end_sound = False

                    else:
                        key_name = pygame.key.name(event.key).upper()

                        if len(key_name) == 1 and key_name.isalpha():
                            result = game.guess_letter(key_name)

                            if result is True and correct_sound:
                                correct_sound.play()
                            elif result is False and wrong_sound:
                                wrong_sound.play()

        if game.game_over:
            if not played_end_sound:
                if game.won and win_sound:
                    win_sound.play()
                elif not game.won and lose_sound:
                    lose_sound.play()
                played_end_sound = True

            if game.won:
                draw_win_screen(screen, WIDTH, HEIGHT, game.difficulty)
            else:
                draw_lose_screen(screen, WIDTH, HEIGHT, game.secret_word, game.difficulty)
        else:
            draw_game_screen(screen, game, font)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()