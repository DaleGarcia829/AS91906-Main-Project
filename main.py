#import pygame,mysprite, imagelist, debug
import pygame
from button import Button
#constants
SCREEN_X= 640
SCREEN_Y= 480
WINDOW_MODE= pygame.RESIZABLE

BG_COLOR = ("#4ca626")
WHITE = ("#F9F6EE")
#class defs (ex.button)
class MainMenu:
    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.buttons = []
        self._build_menu()

    def _build_menu(self):
        button_w, button_h = 240, 60
        start_y = 200
        spacing = 85
        x_pos = (self.screen_w // 2) - (button_w // 2)

        # We only pass labels here. No functions or app references.
        menu_items = ["Play", "Settings", "High Score", "Quit"]
        for i, label in enumerate(menu_items):
            y_pos = start_y + (i * spacing)
            button = Button(x_pos, y_pos, button_w, button_h, label)
            self.buttons.append(button)
    def draw(self, surface):
        surface.fill(pygame.Color('#4ca626'))
        
       
        title_font = pygame.font.Font('freesansbold.ttf', 48)
        title_surf = title_font.render("MAIN MENU", True, pygame.Color('White'))
        title_rect = title_surf.get_rect(center=(self.screen_w // 2, 100))
        surface.blit(title_surf, title_rect)
        
        for button in self.buttons:
            button.draw(surface)
#function defs




if __name__=="__main__":
    # program initialisation
    pygame.init()
    screen= pygame.display.set_mode((SCREEN_X, SCREEN_Y), pygame.RESIZABLE) 

    # setup variables
    quitting = False
     # main loop- until quit
    while not quitting:
        # check event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitting = True    
        # check events- has anything happened??
            # do something or indicate that something needs to be done
        # take action on events
        # do stuff that happens everytime
            # move or animate
            # check for things
        # clear the screen
        screen.fill(pygame.Color('#4ca626'))
        # draw eveything
        # show the new screen
        pygame.display.flip()
    
    # setup pygame