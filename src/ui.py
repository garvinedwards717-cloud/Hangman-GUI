import pygame

BG_COLOR = (20, 20, 30)
LINE_COLOR = (255, 255, 255)
WIN_COLOR = (0, 220, 100)
LOSE_COLOR = (220, 60, 60)
BODY_COLOR = (255, 120, 120)
TEXT_COLOR = (230, 230, 230)
FONT_NAME = "Arial"


def draw_game_screen(screen, game, font):
    screen.fill(BG_COLOR)

    draw_gallows(screen)
    draw_hangman(screen, len(game.wrong_guesses), game.game_over and not game.won)

    title_font = pygame.font.SysFont(FONT_NAME, 42, bold=True)
    info_font = pygame.font.SysFont(FONT_NAME, 30)
    wrong_font = pygame.font.SysFont(FONT_NAME, 28)

    title_surface = title_font.render("Hangman", True, TEXT_COLOR)
    screen.blit(title_surface, (560, 40))

    difficulty_surface = info_font.render(
        f"Difficulty: {game.difficulty}",
        True,
        TEXT_COLOR
    )
    screen.blit(difficulty_surface, (480, 95))

    word_surface = font.render(game.get_display_word(), True, LINE_COLOR)
    screen.blit(word_surface, (480, 150))

    wrong_surface = wrong_font.render(
        f"Wrong: {game.get_wrong_guesses()}",
        True,
        BODY_COLOR
    )
    screen.blit(wrong_surface, (480, 260))

    guesses_left = game.max_wrong - len(game.wrong_guesses)
    status_surface = info_font.render(
        f"Guesses left: {guesses_left}",
        True,
        TEXT_COLOR
    )
    screen.blit(status_surface, (480, 320))

    help_surface = info_font.render(
        "Type letters on your keyboard",
        True,
        TEXT_COLOR
    )
    screen.blit(help_surface, (480, 380))

    controls_surface = info_font.render(
        "1 = Easy   2 = Medium   3 = Hard",
        True,
        TEXT_COLOR
    )
    screen.blit(controls_surface, (480, 430))

    pygame.display.flip()


def draw_win_screen(screen, width, height, difficulty):
    screen.fill(BG_COLOR)

    font = pygame.font.SysFont(FONT_NAME, 64, bold=True)
    small_font = pygame.font.SysFont(FONT_NAME, 32)

    text = font.render("You Won!", True, WIN_COLOR)
    diff_text = small_font.render(f"Difficulty: {difficulty}", True, LINE_COLOR)
    restart = small_font.render("Press ENTER to restart", True, LINE_COLOR)

    screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - 70))
    screen.blit(diff_text, (width // 2 - diff_text.get_width() // 2, height // 2 + 5))
    screen.blit(restart, (width // 2 - restart.get_width() // 2, height // 2 + 50))

    pygame.display.flip()



def draw_lose_screen(screen, width, height, secret_word, difficulty):
    screen.fill(BG_COLOR)

    # Draw gallows + full hangman with red dead eyes
    draw_gallows(screen)
    draw_hangman(screen, 6, dead=True)

    font = pygame.font.SysFont(FONT_NAME, 64, bold=True)
    small_font = pygame.font.SysFont(FONT_NAME, 30)

    text = font.render("Game Over", True, LOSE_COLOR)
    diff_text = small_font.render(f"Difficulty: {difficulty}", True, LINE_COLOR)
    word_text = small_font.render(f"The word was: {secret_word}", True, LINE_COLOR)
    restart = small_font.render("Press ENTER to restart", True, LINE_COLOR)

    screen.blit(text, (560, 140))
    screen.blit(diff_text, (560, 240))
    screen.blit(word_text, (560, 285))
    screen.blit(restart, (560, 330))

    pygame.display.flip()


def draw_gallows(screen):
    pygame.draw.line(screen, LINE_COLOR, (80, 520), (280, 520), 5)
    pygame.draw.line(screen, LINE_COLOR, (180, 520), (180, 100), 5)
    pygame.draw.line(screen, LINE_COLOR, (180, 100), (360, 100), 5)
    pygame.draw.line(screen, LINE_COLOR, (360, 100), (360, 150), 5)


def draw_hangman(screen, wrong_count, dead=False):
    if wrong_count > 0:
        pygame.draw.circle(screen, LINE_COLOR, (360, 190), 35, 3)

        if dead:
            pygame.draw.line(screen, LOSE_COLOR, (345, 178), (355, 188), 2)
            pygame.draw.line(screen, LOSE_COLOR, (355, 178), (345, 188), 2)
            pygame.draw.line(screen, LOSE_COLOR, (365, 178), (375, 188), 2)
            pygame.draw.line(screen, LOSE_COLOR, (375, 178), (365, 188), 2)

    if wrong_count > 1:
        pygame.draw.line(screen, LINE_COLOR, (360, 225), (360, 340), 3)
    if wrong_count > 2:
        pygame.draw.line(screen, LINE_COLOR, (360, 250), (310, 300), 3)
    if wrong_count > 3:
        pygame.draw.line(screen, LINE_COLOR, (360, 250), (410, 300), 3)
    if wrong_count > 4:
        pygame.draw.line(screen, LINE_COLOR, (360, 340), (320, 420), 3)
    if wrong_count > 5:
        pygame.draw.line(screen, LINE_COLOR, (360, 340), (400, 420), 3)