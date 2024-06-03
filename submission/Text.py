import pygame


#font rendering takes time
#optimize font storage
class Text:
    def __init__(self):
        self.fonts = {}
    
    def add_font(self, fontFile, size, name):
        fontObj = pygame.font.Font(fontFile, size)
        self.fonts[name + str(size)] = fontObj
    
    def render(self, text, font, size, color):
        if (font + str(size)) not in self.fonts:
            print(f"Font not added: {font}, {size}px")
            assert(False)

        surface = self.fonts[font + str(size)].render(text, True, color)
        return surface
    
    def getHeight(self, fontName, size):
        return self.fonts[fontName + str(size)].get_linesize()
    
    def optimize():
        pass


def init():
    global text
    text=Text()


def add(fontFile, size, name):
    text.add_font(fontFile, size, name)

def render(textToBeRendered, fontName, size, color):
    return text.render(textToBeRendered, fontName, size,color)

def getHeight(fontName, size):
    return text.getHeight(fontName, size)

def optimize():
    pass


    

