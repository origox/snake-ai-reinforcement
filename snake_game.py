import random
import sys
from typing import Any

import pygame
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.time import Clock

class Score:
    def __init__(self, screen: Any, x: int, y: int) -> None:
        self.x_position: int = x
        self.y_position: int = y
        self.screen: Any = screen
        self.font = pygame.font.SysFont("comicsansms", 22)


    def draw(self, score: int) -> None:
        text = self.font.render("Score: " + str(score), True, (0,0,0))
        self.screen.blit(text, [0, 0])
    

class Fruit:
    def __init__(self, screen: Any, cell_size: int, cell_number: int) -> None:
        self.position: Vector2
        self.screen: Any = screen
        self.cell_size: int = cell_size
        self.cell_number: int = cell_number
        self.randomize()
        
    def draw(self) -> None:
        fruit_rectangle: Rect = Rect(self.position.x * self.cell_size, self.position.y * self.cell_size, self.cell_size, self.cell_size)
        pygame.draw.rect(self.screen, (183,50, 50), fruit_rectangle)

    def randomize(self) -> None:
        self.x: int = random.randint(0, self.cell_number - 1)
        self.y: int = random.randint(0, self.cell_number - 1)
        self.position = Vector2(self.x, self.y)

class Snake:
    def __init__(self, screen: Any, cell_size: int, cell_number: int) -> None:
        self.screen = screen
        self.cell_size: int = cell_size
        self.cell_number: int = cell_number
        self.body: list[Vector2] = [Vector2(5,10), Vector2(4,10), Vector2(3, 10)]
        self.direction: Vector2 =  Vector2(1,0)
        self.new_block: bool = False

    def draw(self) -> None:
        for block in self.body:
            x_position: int = int(block.x) * self.cell_size
            y_position: int = int(block.y) * self.cell_size
            block_rect: Rect = Rect(x_position, y_position, self.cell_size, self.cell_size )
            pygame.draw.rect(self.screen, (50,50, 192), block_rect)

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
    def __init__(self, cell_size: int, cell_number: int) -> None:
        # initialize pygame
        pygame.init()
        pygame.display.set_caption("Snake")
        self.score = 0


        # timing parameters
        self.clock: Any = Clock()
        self.SCREEN_UPDATE: int = pygame.USEREVENT
        pygame.time.set_timer(self.SCREEN_UPDATE, 150)

        # graphics
        self.cell_size: int = cell_size
        self.cell_number: int = cell_number
        self.width: int = cell_size * cell_number
        self.height: int = cell_size * cell_number
        self.screen: Any = pygame.display.set_mode((self.width, self.height))
        
        # game components
        self.snake: Snake = Snake(self.screen, self.cell_size, self.cell_number)
        self.fruit: Fruit = Fruit(self.screen, self.cell_size, self.cell_number)
        self.score_board: Score = Score(self.screen, 10,10)

    def play_step(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._game_over()
            if event.type == self.SCREEN_UPDATE:
                self._update()
            if event.type ==  pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if self.snake.direction.y != 1:
                        self.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_DOWN:
                    if self.snake.direction.y != -1:
                        self.snake.direction = Vector2(0, 1)
                if event.key == pygame.K_LEFT:
                    if self.snake.direction.x != 1:
                        self.snake.direction = Vector2(-1, 0)
                if event.key == pygame.K_RIGHT:
                    if self.snake.direction.x != -1:
                        self.snake.direction = Vector2(1, 0)
        self.clock.tick(60)
        pygame.display.update()
    
    def _update(self) -> None:
        self.snake.move()
        self._check_collision()
        self._check_fail()
        self._draw()
        

    def _draw(self) -> None:
        self.screen.fill((175, 215, 70))
        self.snake.draw()
        self.fruit.draw()
        self.score_board.draw(self.score)
        

    def _check_collision(self) -> None:
        if self.snake.body[0] == self.fruit.position:
            print("jummy")
            self.fruit.randomize()
            self.snake.add_block()
            self.score += 1

    def _check_fail(self) -> None:
        if not 0 <= self.snake.body[0].x < self.cell_number or not 0 <= self.snake.body[0].y < self.cell_number:
            self._game_over()
        
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self._game_over()
        
    def _game_over(self) -> None:
        pygame.quit()
        sys.exit()





CELL_SIZE = 40
CELL_NUMBER = 20

main_game: Game = Game(CELL_SIZE, CELL_NUMBER)

# Game loop
while  True:
    main_game.play_step()
 
        



