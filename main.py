import pygame
from button import Button
from mysprite import MySprite
from imagelist import ImageList
from gameplay import MainGame

# Screen size 
SCREEN_X = 640
SCREEN_Y = 512
TILESIZE = 32
WINDOW_MODE = pygame.RESIZABLE
FONT_SIZE = 36


BG_COLOR = ("#4ca626")
WHITE = ("#F9F6EE")
BLACK = ("#000000")
SNAKE_COLOR = ("#38b6ff")
class MainMenu():
    def __init__(self, screen_w, screen_h):
        self._screen_w = screen_w
        self._screen_h = screen_h
        self._buttons = []
        self._build_menu()
        
    def _build_menu(self):
        # Setting up button sizes and layout math
        button_w, button_h = 180, 45
        start_y = 150
        spacing = 65
        # centres buttons
        x_pos = (self._screen_w // 2) - (button_w // 2)

        # Loop through our menu labels to create the buttons automatically
        menu_items = ["Play", "Settings", "High Score", "Quit"]
        for i, label in enumerate(menu_items):
            y_pos = start_y + (i * spacing)
            button = Button(x_pos, y_pos, button_w, button_h, label)
            self._buttons.append(button)

    def draw(self, surface):
        surface.fill(pygame.Color(BG_COLOR))
        
        # Drawing the big main title text
        title_font = pygame.font.Font('freesansbold.ttf', FONT_SIZE)
        title_surf = title_font.render("SNAKE GAME!", True, pygame.Color(WHITE))
        title_rect = title_surf.get_rect(center=(self._screen_w // 2, 60))
        surface.blit(title_surf, title_rect)
        
        # Draw all 4 buttons 
        for button in self._buttons:
            button.draw(surface)

class Snake ():
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    VECTOR = [(0, -1), (0,1), (-1, 0), (1,0)]
    HEAD = 0
    TAIL = -1
    def __init__(self, screen, x, y, w, h, images, dir=UP):
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._head_image = ImageList(images, w, h)
        self._body_image = ImageList(images, w, h)
        self._dir = dir
        self._screen = screen
        self._grow = False
        self._seg_list = []

    def reset (self):
        self._x = (SCREEN_X // 2) // TILESIZE * TILESIZE
        self._y = (SCREEN_Y // 2) // TILESIZE * TILESIZE
        self._dir = Snake.UP
        self._grow = False
        self._seg_list = []
        
        self._seg_list.append(MySprite(self._x, self._y, self._w, self._h, self._head_image, self._screen))
        self._seg_list.append(MySprite(self._x, self._y + TILESIZE, self._w, self._h, self._body_image, self._screen))

    def update(self):
        self._x += Snake.VECTOR[self._dir][0] * TILESIZE
        self._y += Snake.VECTOR[self._dir][1] * TILESIZE
        
        self._seg_list.insert(Snake.HEAD, MySprite(self._x, self._y, self._w, self._h, self._head_image, self._screen))
        
        if len(self._seg_list) > 1:
            self._seg_list[1]._images = self._body_image
        
        if not self._grow:
            self._seg_list.pop(Snake.TAIL)   
        else: 
            self._grow = False    

    def draw(self):
        for segment in self._seg_list:
            rect = pygame.Rect(segment._x, segment._y, self._w, self._h)
            pygame.draw.rect(self._screen, BLACK, rect)
            pygame.draw.rect(self._screen, SNAKE_COLOR, rect.inflate(-4, -4))


# main loop
if __name__ == "__main__":
    pygame.init()

    window = pygame.display.set_mode((SCREEN_X, SCREEN_Y), pygame.RESIZABLE)
    
    game_surface = pygame.Surface((SCREEN_X, SCREEN_Y))
    
    pygame.display.set_caption("Snake Game")
    
    quitting = False
    is_fullscreen = False
    current_state = "menu"
    
    main_menu = MainMenu(SCREEN_X, SCREEN_Y)
    
    player_snake = Snake(game_surface, 500, 50, TILESIZE, TILESIZE, ["images\\snake\\snake", "images\\snake\\snakebody"])

    game_screen = MainGame(SCREEN_X, SCREEN_Y, TILESIZE)
    
    clock = pygame.time.Clock()

    while not quitting:
        window_w, window_h = window.get_size()
        
        scale_x = window_w / SCREEN_X
        scale_y = window_h / SCREEN_Y
        scale = min(scale_x, scale_y) 
        
        scaled_w = int(SCREEN_X * scale)
        scaled_h = int(SCREEN_Y * scale)
        
        offset_x = (window_w - scaled_w) // 2
        offset_y = (window_h - scaled_h) // 2

        mouse = pygame.mouse.get_pos()
        x = int((mouse[0] - offset_x) / scale)
        y = int((mouse[1] - offset_y) / scale)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitting = True    
            
            # Fullscreen controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11 or (event.key == pygame.K_RETURN and (event.mod & pygame.KMOD_ALT)):
                    is_fullscreen = not is_fullscreen
                    if is_fullscreen:
                        window = pygame.display.set_mode(pygame.FULLSCREEN)
                    else:
                        window = pygame.display.set_mode((SCREEN_X, SCREEN_Y), pygame.RESIZABLE)
        
            # MENU SCREEN 
            if current_state == "menu":
                if event.type == pygame.MOUSEMOTION:
                    for button in main_menu._buttons:
                        button.mouse_move(x, y)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=event.button, pos=(x, y))
                    for button in main_menu._buttons:
                        button.mouse_click(event)
                
                if event.type == pygame.MOUSEBUTTONUP:
                    event = pygame.event.Event(pygame.MOUSEBUTTONUP, button=event.button, pos=(x, y))
                    for button in main_menu._buttons:
                        down = button._button_down
                        over = button._mouse_over
                        button.mouse_click(event)

                        if down and over:
                            if button._text == "Play":
                                current_state = "playing"
                                game_screen.start_game(player_snake)
                            elif button._text == "Quit":
                                quitting = True
                                
            elif current_state == "playing":
                game_screen.handle_input(event, player_snake) 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        current_state = "menu"
                    elif event.key == pygame.K_SPACE and game_screen.game_over:
                        game_screen.start_game(player_snake) 
                                
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                current_state = "menu"
                
        if current_state == "playing":
            game_screen.update(player_snake)
            clock.tick(10) 
        else:
            clock.tick(60) 
      
        game_surface.fill(pygame.Color(BG_COLOR))
        
        if current_state == "menu":
            main_menu.draw(game_surface)
        elif current_state == "playing":
            game_screen.draw(game_surface, player_snake)
        window.fill(pygame.Color(BG_COLOR))
        
        scaled_surf = pygame.transform.scale(game_surface, (scaled_w, scaled_h))
        window.blit(scaled_surf, (offset_x, offset_y))
        
        pygame.display.flip()

    pygame.quit()

