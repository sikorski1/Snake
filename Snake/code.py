from sys import exit
import pygame
from pygame.math import Vector2
from random import randint


class Snake:
    def __init__(self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False

        self.head_up = pygame.image.load("graphics/head_up.png").convert_alpha()
        self.head_down = pygame.image.load("graphics/head_down.png").convert_alpha()
        self.head_right = pygame.image.load("graphics/head_right.png").convert_alpha()
        self.head_left = pygame.image.load("graphics/head_left.png").convert_alpha()

        self.tail_up = pygame.image.load("graphics/tail_up.png").convert_alpha()
        self.tail_down = pygame.image.load("graphics/tail_down.png").convert_alpha()
        self.tail_left = pygame.image.load("graphics/tail_left.png").convert_alpha()
        self.tail_right = pygame.image.load("graphics/tail_right.png").convert_alpha()

        self.body_vertical = pygame.image.load("graphics/body_vertical.png").convert_alpha()
        self.body_horizontal = pygame.image.load("graphics/body_horizontal.png").convert_alpha()

        self.angle_ur = pygame.image.load("graphics/angle_uprig-leftdow.png").convert_alpha()
        self.angle_ul = pygame.image.load("graphics/angle_uplef-rigdow.png").convert_alpha()
        self.angle_dr = pygame.image.load("graphics/angle_dowrig-lefup.png").convert_alpha()
        self.angle_dl = pygame.image.load("graphics/angle_dowlef-rigup.png").convert_alpha()

        self.crunch_sound = pygame.mixer.Sound("sound/Sound_crunch.wav")

    def draw_snake(self):
        head_position = self.update_head_graphics()
        tail_position = self.update_tail_graphics()
        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            if index == 0:
                screen.blit(head_position, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(tail_position, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if (previous_block.x == -1 and next_block.y == -1) or (
                            previous_block.y == -1 and next_block.x == -1):
                        screen.blit(self.angle_dl, block_rect)
                    elif (previous_block.x == -1 and next_block.y == 1) or (
                            previous_block.y == 1 and next_block.x == -1):
                        screen.blit(self.angle_ul, block_rect)
                    elif (previous_block.x == 1 and next_block.y == -1) or (
                            previous_block.y == -1 and next_block.x == 1):
                        screen.blit(self.angle_dr, block_rect)
                    elif (previous_block.x == 1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == 1):
                        screen.blit(self.angle_ur, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            return self.head_left
        elif head_relation == Vector2(-1, 0):
            return self.head_right
        elif head_relation == Vector2(0, 1):
            return self.head_up
        elif head_relation == Vector2(0, -1):
            return self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            return self.tail_right
        elif tail_relation == Vector2(-1, 0):
            return self.tail_left
        elif tail_relation == Vector2(0, 1):
            return self.tail_down
        elif tail_relation == Vector2(0, -1):
            return self.tail_up

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy

    def increase_body(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def game_over(self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.direction = Vector2(0, 0)


class Fruit:
    def __init__(self):
        self.image = pygame.image.load("graphics/apple.png")
        self.x = randint(0, cell_number - 1)
        self.y = randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(self.image, fruit_rect)
        # pygame.draw.rect(screen, (126, 166, 114), fruit_rect)

    def randomize(self):
        self.x = randint(0, cell_number - 1)
        self.y = randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    def draw_grass(self):
        grass_surface = pygame.image.load("graphics/grass.png")
        screen.blit(grass_surface, (0, 0))
        screen.blit(grass_surface, (500, 0))
        screen.blit(grass_surface, (0, 500))
        screen.blit(grass_surface, (500, 500))

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = self.fruit.image.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 5,
                              apple_rect.height)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(self.fruit.image, apple_rect)
        pygame.draw.rect(screen, (120, 209, 1), bg_rect, 2)

    def update(self):
        self.snake.move_snake()
        self.collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.draw_score()
        self.snake.draw_snake()
        self.fruit.draw_fruit()

    def collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.play_crunch_sound()
            self.snake.increase_body()
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.snake.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.snake.game_over()


pygame.init()

cell_size = 50
cell_number = 20
screen = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))

pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
main = Main()
game_font = pygame.font.Font("font/PoetsenOne-Regular.ttf", 25)
screen_update = pygame.USEREVENT
pygame.time.set_timer(screen_update, 100)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == screen_update:
            main.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main.snake.direction.y != 1:
                    main.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if main.snake.direction.y != -1:
                    main.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_RIGHT:
                if main.snake.direction.x != -1:
                    main.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_LEFT:
                if main.snake.direction.x != 1:
                    main.snake.direction = Vector2(-1, 0)
    screen.fill((100, 100, 200))
    main.draw_elements()
    pygame.display.update()
    clock.tick(60)
