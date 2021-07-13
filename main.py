import pygame
import sys
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SCREENWIDTH = 1500
SCREENHEIGHT = 900


class Player:

    def __init__(self, startingposition, side):
        self.height = 80
        self.width = 10
        self.side = side
        self.model = pygame.Rect(startingposition[0], startingposition[1], self.width, self.height)
        self.displacement = 10

    def move_up(self):
        if self.model.top >= 0:
            self.model = self.model.move(0, -self.displacement)

    def move_down(self):
        if self.height + self.model.top <= SCREENHEIGHT:
            self.model = self.model.move(0, self.displacement)

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.model)


class Ball:

    def __init__(self):
        self.width = 10
        self.height = 10
        self.displacement = 5
        self.start = SCREENWIDTH // 2 - 5
        self.hit = pygame.mixer.Sound("hit.wav")
        self.out = pygame.mixer.Sound("out.wav")
        self.wall = pygame.mixer.Sound("wall.wav")
        self.leftscore = 0
        self.rightscore = 0

        if random.randint(0, 1) == 1:
            self.ydirection = 1
        else:
            self.ydirection = -1
        if random.randint(0, 1) == 1:
            self.xdirection = 1
        else:
            self.xdirection = -1

        self.model = pygame.Rect(self.start, random.randint(10, 85)*10, self.width, self.height)

    def randomize_direction(self):
        self.model.top = random.randint(10, 85)*10
        self.model.left = self.start
        if random.randint(0, 1) == 1:
            self.ydirection = 1
        else:
            self.ydirection = -1
        if random.randint(0, 1) == 1:
            self.xdirection = 1
        else:
            self.xdirection = -1

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.model)

    def move(self):
        self.model = self.model.move(self.displacement * self.xdirection, self.displacement * self.ydirection)

    def check_collision(self, players):
        for player in players:
            # left right collision
            if (player.model.left == self.model.left or self.model.left + self.width == player.model.left) and self.model.top <= player.model.top + player.height and self.model.top + self.width >= player.model.top:
                self.xdirection *= -1
                self.hit.play()

            # top down collision
            if player.model.left <= self.model.left + self.width and player.model.left + player.width >= self.model.left and (player.model.top == self.model.top + self.height or player.model.top + player.height == self.model.top):
                self.ydirection *= -1
                self.hit.play()

    def check_borders(self):
        if self.model.left + self.width < 0:
            self.randomize_direction()
            self.out.play()
            self.rightscore += 1

        if self.model.left > SCREENWIDTH:
            self.randomize_direction()
            self.out.play()
            self.leftscore += 1


        if self.model.top < 0 or self.model.top + self.height > SCREENHEIGHT:
            self.ydirection = self.ydirection * -1
            self.wall.play()


def game():
    pygame.init()
    pygame.display.set_caption("Deini's Pong")
    font = pygame.font.Font('freesansbold.ttf', 32)
    text1 = font.render('0', True, WHITE, BLACK)
    textRect1 = text1.get_rect()
    textRect1.center = (40, 50)
    text2 = font.render('0', True, WHITE, BLACK)
    textRect2 = text2.get_rect()
    textRect2.center = (SCREENWIDTH-50, 50)

    player1 = Player((40, 385), 0)
    player2 = Player((SCREENWIDTH-50, 385), 1)

    players = [player1, player2]

    ball = Ball()

    screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    running = True

    i = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_s]:
            player1.move_down()
        if keys[pygame.K_w]:
            player1.move_up()
        if keys[pygame.K_DOWN] and player2.model.top + player2.height <= SCREENHEIGHT:
            player2.move_down()
        if keys[pygame.K_UP] and player2.model.top >= 0:
            player2.move_up()

        ball.move()
        ball.check_collision(players)
        ball.check_borders()

        text1 = font.render(str(ball.leftscore), True, WHITE, BLACK)
        text2 = font.render(str(ball.rightscore), True, WHITE, BLACK)

        screen.fill(BLACK)
        screen.blit(text1, textRect1)
        screen.blit(text2, textRect2)

        player1.draw(screen)
        player2.draw(screen)

        ball.draw(screen)

        pygame.display.update()
        pygame.time.delay(10)

    pygame.display.quit()
    pygame.quit()

if __name__ == '__main__':
    game()
    sys.exit()
