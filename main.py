import pygame
from apple import Apple
from snake import Snake

# game colorset
WHITE = pygame.Color(245, 245, 245)
RED = pygame.Color(245, 50, 25)
GREEN = pygame.Color(25, 150, 100)
BODYGREEN = pygame.Color(25, 100, 100)
BLACK = pygame.Color(25, 25, 25)

# vector directions
VEC_UP = [0, -1]
VEC_DOWN = [0, 1]
VEC_LEFT = [-1, 0]
VEC_RIGHT = [1, 0]

# game flags
stop_game = False  # True if game is active

# window size
window_size = (640, 480)
scale = 20

# initialize game window
pygame.init()
pygame.display.set_caption("My PySnake")
window = pygame.display.set_mode(window_size)

# set fps controller
clock = pygame.time.Clock()
fps = 50  # number of mainloop repeats / second; Affects the keyboard responsivnes
frame_counter = 0
redraw_frames = 5  # defines the number of frames without redrawing the snake; Controls the snake speed

# set soundfiles
step = pygame.mixer.Sound("assets/Step.wav")
step.set_volume(0.1)
eat = pygame.mixer.Sound("assets/Eat.wav")
lose = pygame.mixer.Sound("assets/Lose.wav")

snake = None
apple = None


def draw_square_object(pos: (int, int), color: pygame.Color):
    square = pygame.Rect(*pos, scale, scale)
    pygame.draw.rect(window, color, square)


# gameloop
while not stop_game:
    # check for game quit
    stop_game = len(pygame.event.get(pygame.QUIT)) > 0

    # do not draw on every loop - reduces game speed
    clock.tick(fps)
    if not frame_counter == redraw_frames:
        frame_counter += 1
        continue
    else:
        frame_counter = 0

    # only listen keydown events
    for event in pygame.event.get(pygame.KEYDOWN):
        # no snake available currently
        if not snake or not snake.is_alive:
            stop_game = event.key == pygame.K_ESCAPE

            if event.key == pygame.K_SPACE:
                snake = Snake(window_size, scale)
                vector = VEC_RIGHT

        # handle snake movements
        if event.key == pygame.K_UP and vector != VEC_DOWN:
            vector = VEC_UP
        elif event.key == pygame.K_DOWN and vector != VEC_UP:
            vector = VEC_DOWN
        elif event.key == pygame.K_LEFT and vector != VEC_RIGHT:
            vector = VEC_LEFT
        elif event.key == pygame.K_RIGHT and vector != VEC_LEFT:
            vector = VEC_RIGHT

        # solves issue with moving to opposite direction - maybe at costs of responsivnes?
        pygame.event.clear()
        break

    # clear screen
    window.fill(WHITE)
    # draw rim
    rim = pygame.Rect(0, 0, *window_size)
    pygame.draw.rect(window, BLACK, rim, scale)

    # welcome screen
    if not snake:
        # print title
        font_title = pygame.font.Font("assets/Pixeled.ttf", scale * 2)
        title = font_title.render("My PySnake", True, GREEN, WHITE)
        title_rect = title.get_rect()
        title_rect.center = (window_size[0] / 2, window_size[1] / 2 - 2 * scale)
        window.blit(title, title_rect)
        # print 'press space to play'
        font_play = pygame.font.Font("assets/Pixeled.ttf", scale)
        play = font_play.render("Press SPACE to play", True, BLACK, WHITE)
        play_rect = play.get_rect()
        play_rect.center = (window_size[0] / 2, window_size[1] / 2 + 3 * scale)
        window.blit(play, play_rect)

    # play the game
    elif snake.is_alive:
        # draw apple if needed
        if not apple:
            apple = Apple(*window_size, scale, snake.get_nose_to_tail())

        draw_square_object(apple.position, RED)

        # destroy apple if its in snakes mouth
        if snake.try_eat(apple.position):
            pygame.mixer.Sound.play(eat)
            apple = None

        # move snake by vector
        snake.move(vector)
        pygame.mixer.Sound.play(step)

        # draw snake head
        draw_square_object(snake.head, GREEN)

        # draw snake body if exist
        for position in snake.body:
            draw_square_object(position, BODYGREEN)

        # is snake dead
        if snake.died():
            pygame.mixer.Sound.play(lose)
            continue

    # game over
    else:
        # print score
        font_score = pygame.font.Font("assets/Pixeled.ttf", scale * 2)
        score = font_score.render(
            "Score: {}".format(len(snake.body)), True, GREEN, WHITE
        )
        score_rect = score.get_rect()
        score_rect.center = (window_size[0] / 2, window_size[1] / 2 - 2 * scale)
        window.blit(score, score_rect)
        # print 'press space to play'
        font_play = pygame.font.Font("assets/Pixeled.ttf", scale)
        play = font_play.render("Press SPACE to play", True, BLACK, WHITE)
        play_rect = play.get_rect()
        play_rect.center = (window_size[0] / 2, window_size[1] / 2 + 2 * scale)
        window.blit(play, play_rect)
        # print 'press esc to quit'
        font_quit = pygame.font.Font("assets/Pixeled.ttf", scale)
        quit = font_quit.render("Press ESC to quit", True, RED, WHITE)
        quit_rect = quit.get_rect()
        quit_rect.center = (window_size[0] / 2, window_size[1] / 2 + 5 * scale)
        window.blit(quit, quit_rect)

    # update window
    pygame.display.update()
