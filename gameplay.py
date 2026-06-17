import pygame
import random


class MainGame:
    def __init__(self, screen_w, screen_h, tilesize):
        self._screen_w = screen_w
        self._screen_h = screen_h
        self._tilesize = tilesize
       
        self._grid_w = screen_w // tilesize
        self._grid_h = screen_h // tilesize
       
        self.score = 0
        self.game_over = False
        self._food_pos = [0, 0]
       
    def start_game(self, snake_instance):
        self.score = 0
        self.game_over = False
       
        snake_instance.reset()
        snake_instance._grow = False
       
        self.spawn_food(snake_instance)
    
    def food_spawn(self, snake_instance):
        while True:
            x = random.int(0, self._w -1)* self._tilesize
            y = random.int(0, self._h -1)* self._tilesize
            collision = False
            for segment in snake_instance._seg_list:
                if segment._x == x and segment._y == y:
                    collision = True
                    break
            if not collision:
                self._food_pos = [x, y]
                break

    def input(self, event, snake_instance):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_instance._dir != 1:
                snake_instance._dir = 0                                  
            elif event.key == pygame.K_DOWN and snake_instance._dir != 0:
                snake_instance._dir = 1                                  
            elif event.key == pygame.K_LEFT and snake_instance._dir != 3:
                snake_instance._dir = 2                                  
            elif event.key == pygame.K_RIGHT and snake_instance._dir != 2:
                snake_instance._dir = 3

    def draw(self, surface, snake_instance):
        surface.fill(pygame.Color('#4ca626'))
        food_rect = pygame.Rect(self._food_pos[0], self._food_pos[1], self._tilesize)
        pygame.draw.rect(surface, ("images\\test"), food_rect)
        snake_instance.draw()

        font = pygame.font.Font('freesansbold.ttf', 24)
        score = font.render(f"Scroe: {self.score}", True, pygame.Color('White'))
        surface.blit(score, (45,45))

        if self._game_over:
            over = pygame.Surface((self._screen_w, self._screen_h))