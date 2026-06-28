import pygame
import random

FONT_SIZE = 18
FONT_COLOR = ("#F9F6EE")
FOOD_COLOR = ("#FF0000")
GRID_COLOR_1 = ("#4ca626")
GRID_COLOR_2 = ("#000000")
GREY= ("#808080")

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
       
        self.food_spawn(snake_instance)

    def food_spawn(self, snake_instance):
        while True:
            x = random.randint(1, self._grid_w - 2) * self._tilesize
            y = random.randint(1, self._grid_h - 2) * self._tilesize
           
            collision = False
            for segment in snake_instance._seg_list:
                if segment._x == x and segment._y == y:
                    collision = True
                    break
           
            if not collision:
                self._food_pos = [x, y]
                break

    def handle_input(self, event, snake_instance):
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
        surface.fill(pygame.Color(GRID_COLOR_1))
       
        for row in range(self._grid_h):
            for col in range(self._grid_w):
                if row == 0 or row == self._grid_h - 1 or col == 0 or col == self._grid_w - 1:
                    tile_rect = pygame.Rect(col * self._tilesize, row * self._tilesize, self._tilesize, self._tilesize)
                    pygame.draw.rect(surface, GREY, tile_rect)
                elif (row + col) % 2 == 0:
                    tile_rect = pygame.Rect(col * self._tilesize, row * self._tilesize, self._tilesize, self._tilesize)
                    pygame.draw.rect(surface, pygame.Color(GRID_COLOR_2), tile_rect)

        food_rect = pygame.Rect(self._food_pos[0], self._food_pos[1], self._tilesize, self._tilesize)
        pygame.draw.rect(surface, FOOD_COLOR, food_rect)

        snake_instance.draw()

        font = pygame.font.Font('freesansbold.ttf', FONT_SIZE)
        score_surf = font.render(f"Score: {self.score}", True, FONT_COLOR)
        surface.blit(score_surf, (20, 20))

        if self.game_over:
            over = pygame.Surface((self._screen_w, self._screen_h), pygame.SRCALPHA)
            over.fill((0, 0, 0, 180))
            surface.blit(over, (0, 0))

            go_font = pygame.font.Font('freesansbold.ttf', FONT_SIZE + 4)
            go_surf = go_font.render("GAME OVER", True, FOOD_COLOR)
            go_rect = go_surf.get_rect(center=(self._screen_w // 2, self._screen_h // 2 - 25))
            surface.blit(go_surf, go_rect)

            hint_font = pygame.font.Font('freesansbold.ttf', FONT_SIZE)
            hint_surf = hint_font.render("Press SPACE to Restart or ESC for Menu", True, FONT_COLOR)
            hint_rect = hint_surf.get_rect(center=(self._screen_w // 2, self._screen_h // 2 + 25))
            surface.blit(hint_surf, hint_rect)

    def update(self, snake_instance):
        if self.game_over:
            return

        snake_instance.update()
        head = snake_instance._seg_list[0]

        if head._x == self._food_pos[0] and head._y == self._food_pos[1]:
            snake_instance._grow = True
            self.score += 10          
            self.food_spawn(snake_instance)

        if head._x < self._tilesize or head._x >= self._screen_w - self._tilesize or head._y < self._tilesize or head._y >= self._screen_h - self._tilesize:
            self.game_over = True

        for segment in snake_instance._seg_list[1:]:
            if head._x == segment._x and head._y == segment._y:
                self.game_over = True