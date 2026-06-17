from os.path import exists
import pygame
import debug

class ImageList():
    def __init__(self, filename, width, height, image_type='jpg'):
        if isinstance(filename, list):
            filename = filename[0]
            for ext in ['.png', '.jpg', '.jpeg', '.bmp']:
                if filename.endswith(ext):
                    image_type = ext[1:]
                    filename = filename[:-len(ext)]
                    
        self._images = []
        count = 0
        debug.dprint(2, "filename:" + filename + str(count) + '.' + image_type, exists(filename + str(count) + '.' + image_type))
        while exists(filename + str(count) + '.' + image_type):
            image = pygame.image.load(filename + str(count) + '.' + image_type)
            debug.dprint(2, "image " + filename + str(count) + '.' + image_type + " loaded")
            scaled = pygame.transform.smoothscale(image, [width, height])
            self._images.append(scaled)
            debug.dprint(2, self._images[-1])
            count += 1
        if count == 0:
            debug.dprint(0, f"Images with prefix {filename} failed to load.")
            
    def get_images(self):
        return self._images
        
    images = property(get_images, None, None)

debug.DEBUG_LEVEL = 0
if __name__ == "__main__":
    TEXT_X = 50
    TEXT_Y = 50
    TEXT_W = 50
    TEXT_H = 50
    
    pygame.init()
    screen = pygame.display.set_mode((640, 480), pygame.RESIZABLE)
    image_obj = ImageList("images\\test", TEXT_W, TEXT_H, "jpg")
    debug.dprint(1, "image list test class created")

    quitting = False
    while not quitting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitting = True
                
        screen.fill(pygame.Color('black'))
        
        count = 0
        while count < len(image_obj.images):
            image_Rect = pygame.Rect(TEXT_X + (count * TEXT_H), TEXT_Y, TEXT_W, TEXT_H)
            screen.blit(image_obj.images[count], image_Rect)
            count += 1
            
        pygame.display.flip()

    pygame.quit()
    quit()
