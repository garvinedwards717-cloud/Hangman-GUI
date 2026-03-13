

import pygame

BG_COLOR = (20, 20, 30)
LINE_COLOR = (255, 255, 255)
WIN_COLOR = (0, 220, 100)
LOSE_COLOR = (220, 60, 60)
BODY_COLOR = (255, 120, 120)
TEXT_COLOR = (230, 230, 230)
ACCENT_COLOR = (100, 180, 255)
BUTTON_COLOR = (45, 45, 70)
BUTTON_HOVER_COLOR = (80, 140, 220)
BUTTON_SELECTED_COLOR = (0, 200, 255)
FONT_NAME = "Segoe UI Emoji"


def draw_gradient_background(screen, width, height):
    for y in range(height):
        color = (
            10,
            min(20 + y // 10, 60),
            min(35 + y // 14, 90),
        )
        pygame.draw.line(screen, color, (0, y), (width, y))


def draw_button(screen, rect, text, font, mouse_pos, selected=False):
    hovered = rect.collidepoint(mouse_pos)

    fill_color = BUTTON_COLOR
    border_color = ACCENT_COLOR
    text_color = TEXT_COLOR

    if selected:
        fill_color = (35, 70, 110)
        border_color = BUTTON_SELECTED_COLOR
    elif hovered:
        fill_color = BUTTON_HOVER_COLOR
        border_color = (140, 220, 255)

    pygame.draw.rect(screen, fill_color, rect, border_radius=12)
    pygame.draw.rect(screen, border_color, rect, width=3, border_radius=12)

    text_surface = font.render(text, True, text_color)
    screen.blit(
        text_surface,
        (
            rect.centerx - text_surface.get_width() // 2,
            rect.centery - text_surface.get_height() // 2,
        ),
    )


def get_menu_buttons(width, height):
    button_width = 200
    button_height = 50

    return {
        "play": pygame.Rect(width // 2 - 100, 145, 200, 50),

        "easy": pygame.Rect(310, 235, button_width, button_height),
        "medium": pygame.Rect(310, 300, button_width, button_height),
        "hard": pygame.Rect(310, 365, button_width, button_height),

        "animals": pygame.Rect(530, 235, button_width, button_height),
        "movies": pygame.Rect(530, 300, button_width, button_height),
        "programming": pygame.Rect(530, 365, button_width, button_height),
        "countries": pygame.Rect(530, 430, button_width, button_height),
        "food": pygame.Rect(530, 495, button_width, button_height),
        "random": pygame.Rect(530, 560, button_width, button_height),

        "sound": pygame.Rect(35, 610, 180, 50),
        "quit": pygame.Rect(width - 215, 610, 180, 50),
    }


def draw_start_menu(screen, width, height, selected_difficulty, selected_category, sound_on, game):
    draw_gradient_background(screen, width, height)

    title_font = pygame.font.SysFont(FONT_NAME, 76, bold=True)
    subtitle_font = pygame.font.SysFont(FONT_NAME, 28)
    button_font = pygame.font.SysFont(FONT_NAME, 24, bold=True)
    info_font = pygame.font.SysFont(FONT_NAME, 22)
    label_font = pygame.font.SysFont(FONT_NAME, 26, bold=True)

    mouse_pos = pygame.mouse.get_pos()
    buttons = get_menu_buttons(width, height)

    title = title_font.render("Hangman", True, LINE_COLOR)
    subtitle = subtitle_font.render("A polished Python word game", True, ACCENT_COLOR)

    screen.blit(title, (width // 2 - title.get_width() // 2, 5))
    screen.blit(subtitle, (width // 2 - subtitle.get_width() // 2, 95))

    draw_button(screen, buttons["play"], "Play", button_font, mouse_pos)

    difficulty_label = label_font.render("Difficulty", True, TEXT_COLOR)
    category_label = label_font.render("Category", True, TEXT_COLOR)
    screen.blit(difficulty_label, (360, 200))
    screen.blit(category_label, (585, 200))

    draw_button(
        screen, buttons["easy"], "Easy", button_font, mouse_pos,
        selected=(selected_difficulty == "Easy")
    )
    draw_button(
        screen, buttons["medium"], "Medium", button_font, mouse_pos,
        selected=(selected_difficulty == "Medium")
    )
    draw_button(
        screen, buttons["hard"], "Hard", button_font, mouse_pos,
        selected=(selected_difficulty == "Hard")
    )

    draw_button(
        screen, buttons["animals"], "🐾 Animals", button_font, mouse_pos,
        selected=(selected_category == "Animals")
    )
    draw_button(
        screen, buttons["movies"], "🎬 Movies", button_font, mouse_pos,
        selected=(selected_category == "Movies")
    )
    draw_button(
        screen, buttons["programming"], "💻 Programming", button_font, mouse_pos,
        selected=(selected_category == "Programming")
    )
    draw_button(
        screen, buttons["countries"], "🌎 Countries", button_font, mouse_pos,
        selected=(selected_category == "Countries")
    )
    draw_button(
        screen, buttons["food"], "🍔 Food", button_font, mouse_pos,
        selected=(selected_category == "Food")
    )
    draw_button(
        screen, buttons["random"], "🎲 Random", button_font, mouse_pos,
        selected=(selected_category == "Random")
    )

    sound_label = "Sound: On" if sound_on else "Sound: Off"
    draw_button(screen, buttons["sound"], sound_label, button_font, mouse_pos)
    draw_button(screen, buttons["quit"], "Quit", button_font, mouse_pos)

    difficulty_text = info_font.render(
        f"Selected Difficulty: {selected_difficulty}",
        True,
        TEXT_COLOR,
    )
    category_text = info_font.render(
        f"Selected Category: {selected_category}",
        True,
        ACCENT_COLOR,
    )
    score_text = info_font.render(f"Score: {game.score}", True, TEXT_COLOR)
    streak_text = info_font.render(f"Streak: {game.streak}", True, TEXT_COLOR)
    best_text = info_font.render(f"Best Streak: {game.best_streak}", True, TEXT_COLOR)

    screen.blit(difficulty_text, (35, 210))
    screen.blit(category_text, (35, 245))
    screen.blit(score_text, (35, 285))
    screen.blit(streak_text, (35, 320))
    screen.blit(best_text, (35, 355))

    pygame.display.flip()


def draw_game_screen(screen, game, font):
    draw_gradient_background(screen, screen.get_width(), screen.get_height())

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
    category_surface = info_font.render(
        f"Category: {game.category}",
        True,
        ACCENT_COLOR
    )

    screen.blit(difficulty_surface, (480, 95))
    screen.blit(category_surface, (480, 125))

    score_surface = info_font.render(f"Score: {game.score}", True, ACCENT_COLOR)
    streak_surface = info_font.render(f"Streak: {game.streak}", True, ACCENT_COLOR)
    best_surface = info_font.render(f"Best: {game.best_streak}", True, ACCENT_COLOR)

    screen.blit(score_surface, (480, 155))
    screen.blit(streak_surface, (650, 155))
    screen.blit(best_surface, (790, 155))

    word_surface = font.render(game.get_display_word(), True, LINE_COLOR)
    screen.blit(word_surface, (480, 215))

    wrong_surface = wrong_font.render(
        f"Wrong: {game.get_wrong_guesses()}",
        True,
        BODY_COLOR
    )
    screen.blit(wrong_surface, (480, 325))

    guesses_left = game.max_wrong - len(game.wrong_guesses)
    status_surface = info_font.render(
        f"Guesses left: {guesses_left}",
        True,
        TEXT_COLOR
    )
    screen.blit(status_surface, (480, 385))

    help_surface = info_font.render(
        "Type letters on your keyboard",
        True,
        TEXT_COLOR
    )
    screen.blit(help_surface, (480, 445))

    controls_surface = info_font.render(
        "1 = Easy   2 = Medium   3 = Hard   SHIFT = Menu",
        True,
        TEXT_COLOR
    )
    screen.blit(controls_surface, (480, 495))

    pygame.display.flip()


def draw_win_screen(screen, width, height, difficulty, game):
    draw_gradient_background(screen, width, height)

    font = pygame.font.SysFont(FONT_NAME, 82, bold=True)
    small_font = pygame.font.SysFont(FONT_NAME, 32)
    accent_font = pygame.font.SysFont(FONT_NAME, 38, bold=True)

    text = font.render("YOU WON!", True, WIN_COLOR)
    diff_text = small_font.render(f"Difficulty: {difficulty}", True, LINE_COLOR)
    category_text = small_font.render(f"Category: {game.category}", True, LINE_COLOR)
    score_text = accent_font.render(f"Score: {game.score}", True, ACCENT_COLOR)
    streak_text = accent_font.render(
        f"Streak: {game.streak}   Best: {game.best_streak}",
        True,
        ACCENT_COLOR
    )
    restart = small_font.render(
        "Press ENTER to restart or SHIFT for menu",
        True,
        LINE_COLOR
    )

    screen.blit(text, (width // 2 - text.get_width() // 2, 140))
    screen.blit(diff_text, (width // 2 - diff_text.get_width() // 2, 270))
    screen.blit(category_text, (width // 2 - category_text.get_width() // 2, 315))
    screen.blit(score_text, (width // 2 - score_text.get_width() // 2, 380))
    screen.blit(streak_text, (width // 2 - streak_text.get_width() // 2, 430))
    screen.blit(restart, (width // 2 - restart.get_width() // 2, 520))

    pygame.display.flip()


def draw_lose_screen(screen, width, height, secret_word, difficulty, game):
    draw_gradient_background(screen, width, height)

    draw_gallows(screen)
    draw_hangman(screen, 6, dead=True)

    font = pygame.font.SysFont(FONT_NAME, "Segoe UI Emoji", bold=True)
    small_font = pygame.font.SysFont(FONT_NAME, 30)

    text = font.render("Game Over", True, LOSE_COLOR)
    diff_text = small_font.render(f"Difficulty: {difficulty}", True, LINE_COLOR)
    category_text = small_font.render(f"Category: {game.category}", True, LINE_COLOR)
    word_text = small_font.render(f"The word was: {secret_word}", True, LINE_COLOR)
    score_text = small_font.render(f"Score: {game.score}", True, ACCENT_COLOR)
    streak_text = small_font.render(f"Streak: {game.streak}   Best: {game.best_streak}", True, ACCENT_COLOR)
    restart = small_font.render("Press ENTER to restart or SHIFT for menu", True, LINE_COLOR)

    screen.blit(text, (560, 100))
    screen.blit(diff_text, (560, 180))
    screen.blit(category_text, (560, 225))
    screen.blit(word_text, (560, 270))
    screen.blit(score_text, (560, 315))
    screen.blit(streak_text, (560, 360))
    screen.blit(restart, (560, 405))

    pygame.display.flip()


def draw_gallows(screen):
    pygame.draw.line(screen, LINE_COLOR, (80, 520), (290, 520), 6)
    pygame.draw.line(screen, LINE_COLOR, (180, 520), (180, 100), 6)
    pygame.draw.line(screen, LINE_COLOR, (180, 100), (360, 100), 6)
    pygame.draw.line(screen, LINE_COLOR, (360, 100), (360, 150), 4)


def draw_hangman(screen, wrong_count, dead=False):
    head_center = (360, 190)

    if wrong_count > 0:
        pygame.draw.circle(screen, LINE_COLOR, head_center, 35, 3)

        if dead:
            pygame.draw.line(screen, LOSE_COLOR, (345, 178), (355, 188), 2)
            pygame.draw.line(screen, LOSE_COLOR, (355, 178), (345, 188), 2)
            pygame.draw.line(screen, LOSE_COLOR, (365, 178), (375, 188), 2)
            pygame.draw.line(screen, LOSE_COLOR, (375, 178), (365, 188), 2)
        else:
            pygame.draw.circle(screen, LINE_COLOR, (350, 184), 3)
            pygame.draw.circle(screen, LINE_COLOR, (370, 184), 3)

    if wrong_count > 1:
        pygame.draw.line(screen, LINE_COLOR, (360, 225), (360, 340), 4)

    if wrong_count > 2:
        pygame.draw.line(screen, LINE_COLOR, (360, 250), (315, 295), 4)

    if wrong_count > 3:
        pygame.draw.line(screen, LINE_COLOR, (360, 250), (405, 295), 4)

    if wrong_count > 4:
        pygame.draw.line(screen, LINE_COLOR, (360, 340), (325, 420), 4)

    if wrong_count > 5:
        pygame.draw.line(screen, LINE_COLOR, (360, 340), (395, 420), 4)

        if not dead:
            pygame.draw.arc(screen, LINE_COLOR, (345, 195, 30, 18), 3.5, 5.9, 2)