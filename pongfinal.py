import pygame, sys, random
from pygame.locals import *


class Button:
    def __init__(self, pos, text_input, font, base_color, hovering_color):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.font = font
        self.font = pygame.font.Font("PressStart2P-Regular.ttf", 20)
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.text_rect.left, self.text_rect.right) and position[
            1
        ] in range(self.text_rect.top, self.text_rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.text_rect.left, self.text_rect.right) and position[
            1
        ] in range(self.text_rect.top, self.text_rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


pygame.init()
fps = pygame.time.Clock()

# colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# globals
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH // 2
HALF_PAD_HEIGHT = PAD_HEIGHT // 2
# added code for paddle height
LPAD_HEIGHT = PAD_HEIGHT
RPAD_HEIGHT = PAD_HEIGHT
HALF_RPAD_HEIGHT = RPAD_HEIGHT // 2
HALF_LPAD_HEIGHT = LPAD_HEIGHT // 2
MIN_PAD_HEIGHT = 40
MAX_PAD_HEIGHT = 120
SCALE_PER_POINT = 8
# end of added code
ball_pos = [0, 0]
ball_vel = [0, 0]
paddle1_vel = 0
paddle2_vel = 0
l_score = 0
r_score = 0
AI_player = False


SCREEN = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Pong: The Game")

font = pygame.font.Font("PressStart2P-Regular.ttf", 20)


def get_font(size):  # used to get Title font
    return pygame.font.Font("PressStart2P-Regular.ttf", size)


pygame.mixer.init()
pygame.mixer.music.load("Song.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.03)


# helper function that spawns a ball, returns a position vector and a velocity vector
# if right is True, spawn to the right, else spawn to the left
def ball_init(right):
    global ball_pos, ball_vel  # these are vectors stored as lists
    ball_pos = [WIDTH // 2, HEIGHT // 2]
    horz = random.randrange(2, 4)
    vert = random.randrange(1, 3)

    if right == False:
        horz = -horz

    ball_vel = [horz, -vert]


# define event handlers
def init():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, l_score, r_score, AI_player  # these are floats
    global score1, score2  # these are ints
    paddle1_pos = [HALF_PAD_WIDTH - 1, HEIGHT // 2]
    paddle2_pos = [WIDTH + 1 - HALF_PAD_WIDTH, HEIGHT // 2]
    l_score = 0
    r_score = 0
    if random.randrange(0, 2) == 0:
        ball_init(True)
    else:
        ball_init(False)


# helper funciton to make the paddel smaller
def update_paddle_heights():
    global LPAD_HEIGHT, RPAD_HEIGHT, HALF_LPAD_HEIGHT, HALF_RPAD_HEIGHT

    diff = l_score - r_score  # positive = left winning

    # losing player gets bigger paddle
    l_change = -diff * SCALE_PER_POINT
    r_change = diff * SCALE_PER_POINT

    LPAD_HEIGHT = max(MIN_PAD_HEIGHT, min(MAX_PAD_HEIGHT, PAD_HEIGHT + l_change))
    RPAD_HEIGHT = max(MIN_PAD_HEIGHT, min(MAX_PAD_HEIGHT, PAD_HEIGHT + r_change))

    HALF_LPAD_HEIGHT = LPAD_HEIGHT // 2
    HALF_RPAD_HEIGHT = RPAD_HEIGHT // 2


def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, ball_pos, ball_vel, l_score, r_score

        SCREEN.fill("black")

        pygame.draw.line(SCREEN, WHITE, [WIDTH // 2, 0], [WIDTH // 2, HEIGHT], 1)
        pygame.draw.line(SCREEN, WHITE, [PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1)
        pygame.draw.line(
            SCREEN, WHITE, [WIDTH - PAD_WIDTH, 0], [WIDTH - PAD_WIDTH, HEIGHT], 1
        )
        pygame.draw.circle(SCREEN, WHITE, [WIDTH // 2, HEIGHT // 2], 70, 1)

        if AI_player:
            if paddle1_pos[1] < ball_pos[1]:
                paddle1_vel = 2
            elif paddle1_pos[1] > ball_pos[1]:
                paddle1_vel = -2  # AI LOGIC
            else:
                paddle1_vel = 0

        # update paddle's vertical position, keep paddle on the screen
        if (
            paddle1_pos[1] > HALF_LPAD_HEIGHT
            and paddle1_pos[1] < HEIGHT - HALF_LPAD_HEIGHT
        ):
            paddle1_pos[1] += paddle1_vel
        elif paddle1_pos[1] <= HALF_LPAD_HEIGHT and paddle1_vel > 0:
            paddle1_pos[1] += paddle1_vel
        elif paddle1_pos[1] >= HEIGHT - HALF_LPAD_HEIGHT and paddle1_vel < 0:
            paddle1_pos[1] += paddle1_vel

        if (
            paddle2_pos[1] > HALF_RPAD_HEIGHT
            and paddle2_pos[1] < HEIGHT - HALF_RPAD_HEIGHT
        ):
            paddle2_pos[1] += paddle2_vel
        elif paddle2_pos[1] <= HALF_RPAD_HEIGHT and paddle2_vel > 0:
            paddle2_pos[1] += paddle2_vel
        elif paddle2_pos[1] >= HEIGHT - HALF_RPAD_HEIGHT and paddle2_vel < 0:
            paddle2_pos[1] += paddle2_vel

        # update ball
        ball_pos[0] += int(ball_vel[0])
        ball_pos[1] += int(ball_vel[1])

        # draw paddles and ball
        pygame.draw.circle(SCREEN, RED, ball_pos, 20, 0)
        pygame.draw.polygon(
            SCREEN,
            GREEN,
            [
                [paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_LPAD_HEIGHT],
                [paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] + HALF_LPAD_HEIGHT],
                [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_LPAD_HEIGHT],
                [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_LPAD_HEIGHT],
            ],
            0,
        )
        pygame.draw.polygon(
            SCREEN,
            GREEN,
            [
                [paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_RPAD_HEIGHT],
                [paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] + HALF_RPAD_HEIGHT],
                [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] + HALF_RPAD_HEIGHT],
                [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] - HALF_RPAD_HEIGHT],
            ],
            0,
        )

        # ball collision check on top and bottom walls
        if int(ball_pos[1]) <= BALL_RADIUS:
            ball_vel[1] = -ball_vel[1]
        if int(ball_pos[1]) >= HEIGHT + 1 - BALL_RADIUS:
            ball_vel[1] = -ball_vel[1]

        # ball collison check on gutters or paddles
        if float(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH and int(ball_pos[1]) in range(
            paddle1_pos[1] - HALF_LPAD_HEIGHT, paddle1_pos[1] + HALF_LPAD_HEIGHT, 1
        ):
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] *= 1.1
            ball_vel[1] *= 1.1
        elif int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH:
            r_score += 1
            if AI_player != True:
                update_paddle_heights()
            ball_init(True)

        if int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH and int(
            ball_pos[1]
        ) in range(
            paddle2_pos[1] - HALF_RPAD_HEIGHT, paddle2_pos[1] + HALF_RPAD_HEIGHT, 1
        ):
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] *= 1.1
            ball_vel[1] *= 1.1
        elif int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH:
            l_score += 1
            if AI_player != True:
                update_paddle_heights()
            ball_init(False)

        # # helper funciton to make the paddle smaller
        # def update_paddle_height(side):
        #     global LPAD_HEIGHT, RPAD_HEIGHT, HALF_RPAD_HEIGHT, HALF_LPAD_HEIGHT

        #     diff = min(5, abs(l_score - r_score))

        #     shrink = 8 * (diff + 1)

        #     if side == 'l':
        #         LPAD_HEIGHT = max(40, PAD_HEIGHT - shrink)
        #         HALF_LPAD_HEIGHT = LPAD_HEIGHT // 2
        #     elif side == 'r':
        #         RPAD_HEIGHT = max(40, PAD_HEIGHT - shrink)
        #         HALF_RPAD_HEIGHT = RPAD_HEIGHT // 2
        # # end of helper function

        # update scores
        myfont1 = pygame.font.Font("PressStart2P-Regular.ttf", 15)
        label1 = myfont1.render("Score " + str(l_score), 1, (255, 255, 0))
        SCREEN.blit(label1, (95, 20))

        myfont2 = pygame.font.Font("PressStart2P-Regular.ttf", 15)
        label2 = myfont2.render("Score " + str(r_score), 1, (255, 255, 0))
        SCREEN.blit(label2, (405, 20))

        PLAY_BACK = Button(
            pos=(300, 385),
            text_input="BACK",
            font=font,
            base_color="White",
            hovering_color="Yellow",
        )

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

            elif event.type == pygame.KEYDOWN:
                if event.key == K_UP:
                    paddle2_vel = -8
                elif event.key == K_DOWN:
                    paddle2_vel = 8
                elif event.key == K_w:
                    paddle1_vel = -8
                elif event.key == K_s:
                    paddle1_vel = 8

                if not AI_player:
                    if event.key == K_w:
                        paddle1_vel = -8
                    elif event.key == K_s:  # AI LOGIC
                        paddle1_vel = 8

            elif event.type == pygame.KEYUP:
                if event.key in (K_w, K_s):
                    paddle1_vel = 0
                elif event.key in (K_UP, K_DOWN):
                    paddle2_vel = 0

            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        fps.tick(60)


init()


def difficulty_menu():
    global AI_player  # AI LOGIC
    while True:
        SCREEN.fill("black")

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(30).render("SELECT DIFFICULTY", True, "Yellow")
        MENU_RECT = MENU_TEXT.get_rect(center=(300, 100))

        EASY = Button(
            pos=(300, 190),
            text_input="EASY",
            font=get_font(20),
            base_color="White",
            hovering_color="Yellow",
        )
        MEDIUM = Button(
            pos=(300, 240),
            text_input="MEDIUM",
            font=get_font(20),
            base_color="White",
            hovering_color="Yellow",
        )
        HARD = Button(
            pos=(300, 290),
            text_input="HARD",
            font=get_font(20),
            base_color="White",
            hovering_color="Yellow",
        )
        PLAY_BACK = Button(
            pos=(300, 375),
            text_input="BACK",
            font=font,
            base_color="White",
            hovering_color="Yellow",
        )
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [EASY, MEDIUM, HARD, PLAY_BACK]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if EASY.checkForInput(MENU_MOUSE_POS):
                    init()
                    AI_player = (
                        True if EASY.checkForInput(MENU_MOUSE_POS) else False
                    )  # AI LOGIC
                    play()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if MEDIUM.checkForInput(MENU_MOUSE_POS):
                    init()
                    AI_player = (
                        True if MEDIUM.checkForInput(MENU_MOUSE_POS) else False
                    )  # AI LOGIC
                    play()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if HARD.checkForInput(MENU_MOUSE_POS):
                    init()
                    AI_player = (
                        True if HARD.checkForInput(MENU_MOUSE_POS) else False
                    )  # AI LOGIC
                    play()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(MENU_MOUSE_POS):
                    main_menu()

        pygame.display.update()


init()


def main_menu():
    global AI_player  # AI LOGIC
    while True:
        SCREEN.fill("black")

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(30).render("PONG:THE GAME", True, "Yellow")
        MENU_RECT = MENU_TEXT.get_rect(center=(300, 100))

        PLAY_AI = Button(
            pos=(300, 190),
            text_input="VS AI",
            font=get_font(20),
            base_color="White",
            hovering_color="Yellow",
        )
        PLAY_FRIEND = Button(
            pos=(300, 240),
            text_input="VS FRIEND",
            font=get_font(20),
            base_color="White",
            hovering_color="Yellow",
        )
        QUIT_BUTTON = Button(
            pos=(300, 290),
            text_input="QUIT",
            font=get_font(20),
            base_color="White",
            hovering_color="Yellow",
        )
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_AI, PLAY_FRIEND, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_AI.checkForInput(MENU_MOUSE_POS):
                    init()
                    AI_player = (
                        True if PLAY_AI.checkForInput(MENU_MOUSE_POS) else False
                    )  # AI LOGIC
                    difficulty_menu()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_FRIEND.checkForInput(MENU_MOUSE_POS):
                    init()
                    AI_player = False  # AI LOGIC
                    play()

        pygame.display.update()


main_menu()
