import sys
from pathlib import Path
import pygame

from game_logic import HangmanGame
from ui import (
    draw_game_screen,
    draw_lose_screen,
    draw_start_menu,
    draw_win_screen,
    get_menu_buttons,
)

WIDTH = 1040
HEIGHT = 700
FPS = 60


def load_sound(path):
    try:
        if Path(path).exists():
            return pygame.mixer.Sound(path)
    except pygame.error:
        return None
    return None


def safe_play(sound, sound_on):
    if sound_on and sound:
        sound.play()


def main():
    pygame.init()

    mixer_available = True
    try:
        pygame.mixer.init()
    except pygame.error:
        mixer_available = False

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Hangman GUI")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 54)

    sounds_dir = Path("sounds")

    correct_sound = load_sound(sounds_dir / "correct.wav") if mixer_available else None
    wrong_sound = load_sound(sounds_dir / "wrong.wav") if mixer_available else None
    win_sound = load_sound(sounds_dir / "win.wav") if mixer_available else None
    lose_sound = load_sound(sounds_dir / "lose.wav") if mixer_available else None

    background_music = sounds_dir / "background.mp3"
    sound_on = True

    if mixer_available and background_music.exists():
        try:
            pygame.mixer.music.load(str(background_music))
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)
        except pygame.error:
            pass

    selected_difficulty = "Medium"
    selected_category = "Random"
    game = HangmanGame(selected_difficulty)

    played_end_sound = False
    current_screen = "menu"

    running = True

    while running:
        clock.tick(FPS)

        buttons = get_menu_buttons(WIDTH, HEIGHT)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif current_screen == "menu":

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos

                    if buttons["play"].collidepoint(mouse_pos):
                        game.set_difficulty(selected_difficulty)
                        game.set_category(selected_category)
                        played_end_sound = False
                        current_screen = "game"

                    elif buttons["easy"].collidepoint(mouse_pos):
                        selected_difficulty = "Easy"

                    elif buttons["medium"].collidepoint(mouse_pos):
                        selected_difficulty = "Medium"

                    elif buttons["hard"].collidepoint(mouse_pos):
                        selected_difficulty = "Hard"

                    elif buttons["animals"].collidepoint(mouse_pos):
                        selected_category = "Animals"

                    elif buttons["movies"].collidepoint(mouse_pos):
                        selected_category = "Movies"

                    elif buttons["programming"].collidepoint(mouse_pos):
                        selected_category = "Programming"

                    elif buttons["countries"].collidepoint(mouse_pos):
                        selected_category = "Countries"

                    elif buttons["food"].collidepoint(mouse_pos):
                        selected_category = "Food"

                    elif buttons["random"].collidepoint(mouse_pos):
                        selected_category = "Random"

                    elif buttons["sound"].collidepoint(mouse_pos):
                        sound_on = not sound_on

                        if mixer_available:
                            if sound_on:
                                try:
                                    pygame.mixer.music.play(-1)
                                except pygame.error:
                                    pass
                            else:
                                pygame.mixer.music.stop()

                    elif buttons["quit"].collidepoint(mouse_pos):
                        running = False

            else:
                if event.type == pygame.KEYDOWN:

                    if game.game_over:
                        if event.key == pygame.K_RETURN:
                            game.reset_game()
                            played_end_sound = False

                        elif event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                            current_screen = "menu"
                            played_end_sound = False

                    else:
                        if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                            current_screen = "menu"

                        elif event.key == pygame.K_1:
                            selected_difficulty = "Easy"
                            game.set_difficulty("Easy")
                            played_end_sound = False

                        elif event.key == pygame.K_2:
                            selected_difficulty = "Medium"
                            game.set_difficulty("Medium")
                            played_end_sound = False

                        elif event.key == pygame.K_3:
                            selected_difficulty = "Hard"
                            game.set_difficulty("Hard")
                            played_end_sound = False

                        else:
                            key_name = pygame.key.name(event.key).upper()

                            if len(key_name) == 1 and key_name.isalpha():
                                result = game.guess_letter(key_name)

                                if result is True:
                                    safe_play(correct_sound, sound_on)
                                elif result is False:
                                    safe_play(wrong_sound, sound_on)

        if current_screen == "menu":
            draw_start_menu(
                screen,
                WIDTH,
                HEIGHT,
                selected_difficulty,
                selected_category,
                sound_on,
                game,
            )

        elif game.game_over:

            if not played_end_sound:
                if game.won:
                    safe_play(win_sound, sound_on)
                else:
                    safe_play(lose_sound, sound_on)
                played_end_sound = True

            if game.won:
                draw_win_screen(screen, WIDTH, HEIGHT, game.difficulty, game)
            else:
                draw_lose_screen(
                    screen,
                    WIDTH,
                    HEIGHT,
                    game.secret_word,
                    game.difficulty,
                    game,
                )

        else:
            draw_game_screen(screen, game, font)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()