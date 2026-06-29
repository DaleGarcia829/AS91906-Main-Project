import pygame
import debug


class Button():
    MIN_BUTTON_W = 100
    MIN_BUTTON_H = 50
    CLICK_OFFSET = 5
    
    DEFAULT_FONT_SIZE = 32
    DEFAULT_FONT = 'freesansbold.ttf'

    FONT_COLOR = pygame.Color('Black')
    HIGHLIGHT_COLOR = pygame.Color('darkgrey')
    BG_COLOR = pygame.Color('White')
    BORDER_COLOR = pygame.Color('#0097b2')

    def __init__(self,x,y,w,h,text, font = None, bg_color = BG_COLOR, f_color = FONT_COLOR, border_color = BORDER_COLOR, highlight_color = HIGHLIGHT_COLOR):
            # init internal variables
            self._mouse_over = False
            self._button_down = False
            self._disabled = False # need to make property for this
            self._border = 4 # configurable yet

            if w < Button.MIN_BUTTON_W:
                self._w = Button.MIN_BUTTON_W
            else:
                self._w = w
            if h < Button.MIN_BUTTON_H:
                self._h= Button.MIN_BUTTON_H
            else:
                self._h = h

            self._x = x
            self._y = y
            if font is None:
                self._font = pygame.font.Font( Button.DEFAULT_FONT, Button.DEFAULT_FONT_SIZE)
            else: 
                self._font = font
            self._text = text
            self._bg_color = bg_color
            self._f_color = f_color
            self._border_color = border_color
            self._highlight_color = highlight_color


    def mouse_move(self, x, y):
            if not self._disabled:
                if self.contains(x,y):
                    self._mouse_over = True
                else:
                    self._mouse_over = False

    def mouse_click(self, event):
            if not self._disabled:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self._mouse_over:
                        self._button_down = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self._button_down and self._mouse_over:
                        # clicked
                        self._button_down = False

        
    def set_action(self, action_function):
            if callable(action_function):
                self._action = action_function

    def click(self):   
            if self._action == None:
                print("No action function set for button:", self._text)
            else:
                self._action()
                
    def contains(self,x,y):
            return self.get_rect().collidepoint(x,y)

    def get_rect(self):
            return pygame.Rect (self._x, self._y, self._w, self._h)
    
    def draw(self, screen):
        # draw rectangle
        pygame.draw.rect(screen, self._border_color, self.get_rect())
        pygame.draw.rect(screen, self._bg_color, pygame.Rect(self._x + self._border, self._y + self._border, \
                                                            self._w - self._border*2, self._h - self._border*2))
        # draw the text
        color = self._f_color
        offset = 0
        if self._mouse_over:
            if self._button_down:
                offset = Button.CLICK_OFFSET
            else:
                color = self._highlight_color
        # create the rendered text as a surface
        rendered_text = self._font.render(self._text, True, color, self._bg_color)
        # get rectangle for this new surface
        rendered_text_rect = rendered_text.get_rect()
        # see the centre of this rectangle to the centre of this button (self)
        rendered_text_rect.center = (self._x + self._w /2 + offset, self._y + self._h /2 + offset )
        screen.blit(rendered_text, rendered_text_rect)

if __name__=="__main__":
    debug.DEBUG_LEVEL= 0
    TEXT_X= 50
    TEXT_Y= 50
    TEXT_W= 200
    TEXT_H= 200
    RED = pygame.Color("Red")
    def test_click():
        print("I was clicked")


    pygame.init()
    screen= pygame.display.set_mode((640,480), pygame.RESIZABLE)
    quitting = False

    my_button = Button(TEXT_X, TEXT_Y, TEXT_W, TEXT_H, "Play", border_color = RED)
    my_button.set_action(test_click)

    # main program loop
    while not quitting:
        coords = pygame.mouse.get_pos()
        # check event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitting = True
            if event.type == pygame.MOUSEMOTION:
                my_button.mouse_move(coords[0], coords[1])
            if event.type == pygame.MOUSEBUTTONDOWN:
                my_button.mouse_click(event)
            if event.type == pygame.MOUSEBUTTONUP:
                my_button.mouse_click(event)

        # clear the screen
        screen.fill(pygame.Color('#4ca626'))

        # draw my button
        my_button.draw(screen)

        pygame.display.flip()

    pygame.quit()
    quit()