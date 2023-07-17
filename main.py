import pygame
from apple import Apple
from snake import Snake

# game colorset
WHITE = pygame.Color(245, 245, 245)
RED = pygame.Color(245, 50, 25)
GREEN = pygame.Color(25, 150, 100)
BLACK = pygame.Color(25, 25, 25)

# vector directions
VEC_UP = [0, -1]
VEC_DOWN = [0, 1]
VEC_LEFT = [-1, 0]
VEC_RIGHT = [1, 0]
VEC_INIT = [0, 0]

# game flags
is_active = True            # True if game is active
is_start = False            # True if game is running
is_eaten = True             # True if current apple is eaten by snake
is_collision = False        # True if new apple collides with snake
is_draw = True              # True if the snakes new position should be drawn
is_dead = False             # True if the snake is dead

# window size
window_x = 640
window_y = 480
scale = 20

# initialize game window
pygame.init()
pygame.display.set_caption('My PySnake')
window = pygame.display.set_mode((window_x, window_y))

# set fps controller
clock = pygame.time.Clock()
fps = 50                    # number of mainloop repeats / second; Affects the keyboard responsivnes
frame_counter = 0           
redraw_frames = 5           # defines the number of frames without redrawing the snake; Controls the snake speed

# set soundfiles
step = pygame.mixer.Sound('assets/Step.wav')
step.set_volume(0.1)
eat = pygame.mixer.Sound('assets/Eat.wav')
lose = pygame.mixer.Sound('assets/Lose.wav')

# gameloop
while is_active:
    # check for game quit or key events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_active = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and vector != VEC_DOWN and former_vector != VEC_DOWN:
                vector = VEC_UP
            elif event.key == pygame.K_DOWN and vector != VEC_UP and former_vector != VEC_UP:
                vector = VEC_DOWN
            elif event.key == pygame.K_LEFT and vector != VEC_RIGHT and former_vector != VEC_RIGHT:
                vector = VEC_LEFT
            elif event.key == pygame.K_RIGHT and vector != VEC_LEFT and former_vector != VEC_LEFT:
                vector = VEC_RIGHT
            elif event.key == pygame.K_SPACE and is_start == False:
                is_start = True
                is_dead = False
                # create snake
                snake = Snake(window_x, window_y)
                vector = VEC_RIGHT
                former_vector = VEC_INIT    # used to prevent the snake from changing the direction to the opposite side of it's current direction
            elif event.key == pygame.K_ESCAPE and is_dead == True:
                is_active = False
                

    # clear screen
    window.fill(WHITE)
    # draw rim
    rim = pygame.Rect(0, 0, window_x, window_y)
    pygame.draw.rect(window, BLACK, rim, scale)

    # end screen
    if is_dead:
        # print score
        font_score = pygame.font.Font('assets/Pixeled.ttf', scale * 2)
        score = font_score.render("Score: " + str(snake.length), True, GREEN, WHITE)
        score_rect = score.get_rect()
        score_rect.center = (window_x / 2, window_y / 2 - 2 * scale)
        window.blit(score, score_rect)
        # print 'press space to play'
        font_play = pygame.font.Font('assets/Pixeled.ttf', scale)
        play = font_play.render("Press SPACE to play", True, BLACK, WHITE)
        play_rect = play.get_rect()
        play_rect.center = (window_x / 2, window_y / 2 + 2 * scale)
        window.blit(play, play_rect)
        # print 'press esc to quit'
        font_quit = pygame.font.Font('assets/Pixeled.ttf', scale)
        quit = font_quit.render("Press ESC to quit", True, RED, WHITE)
        quit_rect = quit.get_rect()
        quit_rect.center = (window_x / 2, window_y / 2 + 5 * scale)
        window.blit(quit, quit_rect)
    elif is_start:
        # draw apple
        if is_eaten:
            is_collision = True
            while is_collision:
                target = Apple(window_x, window_y, scale)
                # check collision with head
                if target.x_position == snake.head[0] and target.y_position == snake.head[1]:
                    is_collision = True
                else:
                    is_collision = False
                # check collision with body if exist
                if snake.length > 0:    
                    for i in range(0, len(snake.body), 1):
                        if target.x_position == snake.body[i][0] and target.y_position == snake.body[i][1]:
                            is_collision = True
                            break
                        else:
                            is_collision = False
                # destroy apple if it collides with the snake
                if is_collision:
                    del target      
            is_eaten = False
        targetbox = pygame.Rect([target.position[0], target.position[1], scale, scale])            
        pygame.draw.rect(window, RED, targetbox)

        # is apple eaten
        is_eaten = snake.eat(target.x_position, target.y_position)
        if is_eaten:
            pygame.mixer.Sound.play(eat)
        # move snake by vector
        if is_draw:
            snake.move(scale, vector)
            former_vector = vector.copy()
            pygame.mixer.Sound.play(step)
        # is snake dead
        is_dead = snake.die(window_x, window_y, scale)
        if is_dead:
            pygame.mixer.Sound.play(lose)
            is_start = False
            continue

        # draw snake head
        head = pygame.Rect([snake.head[0], snake.head[1], scale, scale])
        pygame.draw.rect(window, GREEN, head)
        # draw snake body if exist
        if len(snake.body) > 0:
            for position in snake.body:
                body_element = pygame.Rect([position[0], position[1], scale, scale])
                pygame.draw.rect(window, GREEN, body_element)
        is_draw = False
        frame_counter += 1
        if frame_counter == redraw_frames:
            is_draw = True
            frame_counter = 0
    else:
        # welcome screen
        # print title
        font_title = pygame.font.Font('assets/Pixeled.ttf', scale * 2)
        title = font_title.render("My PySnake", True, GREEN, WHITE)
        title_rect = title.get_rect()
        title_rect.center = (window_x / 2, window_y / 2 - 2 * scale)
        window.blit(title, title_rect)
        # print 'press space to play'
        font_play = pygame.font.Font('assets/Pixeled.ttf', scale)
        play = font_play.render("Press SPACE to play", True, BLACK, WHITE)
        play_rect = play.get_rect()
        play_rect.center = (window_x / 2, window_y / 2 + 3 * scale)
        window.blit(play, play_rect)
    # control fps
    clock.tick(fps)
    # update window
    pygame.display.update()