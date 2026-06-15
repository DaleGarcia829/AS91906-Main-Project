#import pygame,mysprite, imagelist, debug
import pygame
from button import Button
from mysprite import MySprite
#constants
SCREEN_X= 1000
SCREEN_Y= 625
TILESIZE = 16
WINDOW_MODE= pygame.RESIZABLE

BG_COLOR = ("#4ca626")
WHITE = ("#F9F6EE")
#class defs (ex.button)
class MainMenu:
    #function defs
    def __init__(self, screen_w, screen_h):
        self._screen_w = screen_w
        self._screen_h = screen_h
        self._buttons = []
        self._build_menu()
        

    def _build_menu(self):
        button_w, button_h = 240, 60
        start_y = 200
        spacing = 85
        x_pos = (self._screen_w // 2) - (button_w // 2)

     
        menu_items = ["Play", "Settings", "High Score", "Quit"]
        for i, label in enumerate(menu_items):
            y_pos = start_y + (i * spacing)
            button = Button(x_pos, y_pos, button_w, button_h, label)
            self._buttons.append(button)

    def draw(self, surface):
        surface.fill(pygame.Color('#4ca626'))
        
       
        title_font = pygame.font.Font('freesansbold.ttf', 48)
        title_surf = title_font.render("MAIN MENU", True, pygame.Color('White'))
        title_rect = title_surf.get_rect(center=(self._screen_w // 2, 100))
        surface.blit(title_surf, title_rect)
        
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
    def __init__(self, x, y, screen, dir=UP):
        self._x = x
        self._y = y
        self._dir = dir
        self._screen = screen
    def reset (self):
        # create empty snake
        self._seg_list = []
        # create head snake
        self._seg_list.append(MySprite(self._x, self._y, self._w, self._h, self._images, self._screen))
        # create tail snake
        self._seg_list.append(MySprite(self._x, self._y, self._w, self._h, self._images, self._screen))

    def update(self):

            # delete tail
            # create new head
        self._seg_list.insert(Snake.HEAD, MySprite(self._x, self._y, self._w, self._h, self._images, self._screen))
        self._x += Snake.VECTOR[self._dir][0]*TILESIZE

        if self._grow:
            self._seg_list.pop(Snake.TAIL)       

    def draw(self):
        for segment in self._seg_list:
            segment.draw()





    
            






if __name__ == "__main__":
    # program initialisation
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y), pygame.RESIZABLE)
    pygame.display.set_caption("Snake Game")
    
    # setup variables
    quitting = False
    current_state = "menu"
    main_menu = MainMenu(SCREEN_X, SCREEN_Y)
    clock = pygame.time.Clock()

    # main loop- until quit
    while not quitting:
        coords = pygame.mouse.get_pos()

        # check event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitting = True    
        
            # check events- has anything happened??
            if current_state == "menu":
                if event.type == pygame.MOUSEMOTION:
                    for button in main_menu._buttons:
                        button.mouse_move(coords[0], coords[1])

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in main_menu._buttons:
                        button.mouse_click(event)
                
                if event.type == pygame.MOUSEBUTTONUP:
                    for button in main_menu._buttons:
                        down = button._button_down
                        over = button._mouse_over
                        button.mouse_click(event)

                        if down and over:
                            if button._text == "Play":
                                current_state = "playing"
                            elif button._text == "Settings":
                                current_state = "settings"
                            elif button._text == "High Score":
                                current_state = "highscore"
                            elif button._text == "Quit":
                                quitting = True
                                
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                current_state = "menu"
                
        # take action on events
        # do stuff that happens everytime
            # move or animate
            # check for things
            
        # clear the screen
        screen.fill(pygame.Color('#4ca626'))
        
        # draw eveything
        if current_state == "menu":
            main_menu.draw(screen)
        elif current_state == "playing":
            screen.fill(pygame.Color('darkblue'))
        elif current_state == "settings":
            screen.fill(pygame.Color('darkblue'))
        elif current_state == "highscore":
            screen.fill(pygame.Color('darkblue'))
            
        # show the new screen
        pygame.display.flip()