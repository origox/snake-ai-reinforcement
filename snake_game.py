import random
import sys
from typing import Any

import pygame
from pygame.math import Vector2
from pygame.rect import Rect

class Fruit:
    def __init__(self) -> None:
        self.position: Vector2
        self.randomize()
        
    def draw(self) -> None:
        fruit_rectangle: Rect = Rect(self.position.x * cell_size, self.position.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, (126, 166, 114), fruit_rectangle)

    def randomize(self) -> None:
        self.x: int = random.randint(0, cell_number - 1)
        self.y: int = random.randint(0, cell_number - 1)
        self.position = Vector2(self.x, self.y)

class Snake:
    def __init__(self) -> None:
        self.body: list[Vector2] = [Vector2(5,10), Vector2(4,10), Vector2(3, 10)]
        self.direction: Vector2 =  Vector2(1,0)
        self.new_block: bool = False

    def draw(self) -> None:
        for block in self.body:
            x_position: int = int(block.x) * cell_size
            y_position: int = int(block.y) * cell_size
            block_rect: Rect = Rect(x_position, y_position, cell_size, cell_size )
            pygame.draw.rect(screen, (183,111, 122), block_rect)

    def move(self) -> None:
        if self.new_block == True:
            body_copy: list[Vector2] = self.body[:]    
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy: list[Vector2] = self.body[:-1]    
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self) -> None:
        self.new_block = True
    
class Game:
    def __init__(self) -> None:
        self.snake: Snake = Snake()
        self.fruit: Fruit = Fruit()

    def update(self) -> None:
        self.snake.move()
        self._check_collision()
        self.check_fail()
        

    def draw(self) -> None:
        self.snake.draw()
        self.fruit.draw()

    def _check_collision(self) -> None:
        if self.snake.body[0] == self.fruit.position:
            print("jummy")
            self.fruit.randomize()
            self.snake.add_block()

    def check_fail(self) -> None:
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
        
    def game_over(self) -> None:
        pygame.quit()
        sys.exit()


pygame.init()

cell_size: int = 40
cell_number: int = 20

screen: Any = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))
clock: Any = pygame.time.Clock()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game: Game = Game()


# Game loop
while  True:
    ## Poll and handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main_game.game_over()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type ==  pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
    screen.fill((175, 215, 70))
    
    main_game.draw()

    pygame.display.update()
    clock.tick(60)
        
# Close game


