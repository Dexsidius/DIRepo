#CODE BY ISA BOLLING
#Edited by Da'Shawn Larry
import os
os.environ["PYSDL2_DLL_PATH"] = os.path.dirname(os.path.abspath(__file__))
from sdl2 import *
from sdl2.sdlttf import *
import sdl2.ext
import ctypes

#________________CLASSES______________________________#
class Background:
    def __init__(self, w, h, x, y, renderer):
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.s_x = 0
        self.s_y = 0
        self.n = self.s_y
        self.path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "sprites", ".bmp")
        self.image = SDL_LoadBMP(self.path.encode('utf-8'))
        self.bgSurface = SDL_CreateTextureFromSurface(renderer, self.image)
        SDL_FreeSurface(self.image)
    
    def Render(self, renderer):
        ScreenWipe(renderer)
        SDL_RenderCopy(renderer, self.bgSurface, None, None)

    def Quit(self):
        SDL_DestroyTexture(self.bgSurface)

class AnimatedCharacter:
    def __init__(self, w, h, x, y, renderer, character):
        self.w = w                      #width
        self.h = h                      #height
        self.x = x                      #Character's x position
        self.y = y                      #Character's y position
        self.s_x = 0                  #Sprite map x
        self.s_y = 0                    #Sprite map y
        self.n = self.s_y
        self.Moving = False
        self.Animate = False
        self.A_Rate = 0
        self.path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "sprites", character)
        self.image = SDL_LoadBMP(self.path.encode('utf-8'))
        self.texture = SDL_CreateTextureFromSurface(renderer, self.image)
        SDL_FreeSurface(self.image)

    def Render(self, renderer):
        self.s_y = self.n
        self.src_rect = SDL_Rect(self.s_x, self.s_y, self.w, self.h)
        self.dest_rect = SDL_Rect(self.x, self.y, 32, 36)           #Scales the Sprite down to size
        SDL_RenderCopy(renderer, self.texture, self.src_rect, self.dest_rect)

    def Movement(self, state, direction):
        self.direction = direction
        if (state == True):
            self.Moving = True
            self.Animate = True
            if (direction == 'left'):
                self.x -= 2
            elif (direction == 'right'):
                self.x += 2
            elif (direction == 'down'):
                self.y += 2
            elif (direction == 'up'):
                self.y -= 2
        elif (state == False):
            self.Moving = False
            self.Animate = False
    def Animating(self):
        if self.Animate == True:
            self.A_Rate += 1

        #Animations for Movement and Actions
        if self.Moving == True:
            if self.A_Rate == 4:
                self.A_Rate = 0
                if self.direction == 'left':
                    self.n = 108
                    self.s_x += 32
                    if self.s_x >= 95:
                        self.s_x = 0
                if self.direction == 'right':
                    self.n = 36
                    self.s_x += 32
                    if self.s_x >= 95:
                        self.s_x = 0
                if self.direction == 'up':
                    self.n = 0
                    self.s_x += 32
                    if self.s_x >= 95:
                        self.s_x = 0
                if self.direction == 'down':
                    self.n = 72
                    self.s_x += 32
                    if self.s_x >= 95:
                        self.s_x = 0


    def Quit(self):
        SDL_DestroyTexture(self.texture)

    class NPC:
        def __init__(self, w, h, x, y, renderer):
            self.w = w                      #width
            self.h = h                      #height
            self.x = x                      #Character's x position
            self.y = y                      #Character's y position
            self.s_x = 0                    #Sprite map x        
            self.s_y = 0                    #Sprite map y
            self.n = self.s_y
            self.path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "content", "others.bmp")
            self.image = SDL_LoadBMP(self.path.encode('utf-8'))
            self.texture = SDL_CreateTextureFromSurface(renderer, self.image)
            SDL_FreeSurface(self.image)

        def Render(self, renderer):
            self.s_y = self.n
            self.src_rect = SDL_Rect(self.s_x, self.s_y, self.w, self.h)
            self.dest_rect = SDL_Rect(self.x, self.y, 30, 33)
            SDL_RenderCopy(renderer, self.texture, self.src_rect, self.dest_rect)

        def Quit(self):
            SDL_DestroyTexture(self.texture)

class TextObject:
    fonts = dict()
    def __init__(self, renderer, text, width, height, font_name, color = (0, 0, 0), location = (0, 0), font_size = 36):
        self.r = renderer
        if len(font_name) > 1:
            TextObject.fonts[font_name[0]] = TTF_OpenFont(font_name[1], font_size)
        self.color = SDL_Color(color[0], color[1], color[2])
        self.surface = TTF_RenderText_Solid(TextObject.fonts[font_name[0]], text.encode('utf-8'), self.color)
        self.message = SDL_CreateTextureFromSurface(self.r, self.surface)
        SDL_FreeSurface(self.surface)
        self.rect = SDL_Rect(location[0], location[1], width, height)
        self.highlight = False
        SDL_SetTextureBlendMode(self.message, SDL_BLENDMODE_BLEND)

    def Render(self, x=None, y=None, alpha = 255):
        if self.highlight:
            SDL_SetRenderDrawColor(self.r, self.color.r, self.color.g, self.color.b, self.color.a)
            SDL_RenderDrawRect(self.r, self.rect)
        if x is None and y:
            self.rect.y = y
        elif x and y is None:
            self.rect.x = x
        elif x and y:
            self.rect.x = x
            self.rect.y = y
        SDL_SetTextureAlphaMod(self.message, alpha)
        SDL_RenderCopy(self.r, self.message, None, self.rect)

    def __del__(self):
        for keys in list(TextObject.fonts):
            font = TextObject.fonts.pop(keys, None)
            if font: TTF_CloseFont(font)
        SDL_DestroyTexture(self.message)

class Pointer:
    cursors = dict()

    def __init__(self):
        self.x = 0
        self.y = 0
        self.pointer = SDL_Rect(0, 0, 10, 10)
        self.clicking = False
        self.r_clicking = False

    def Compute(self, event):
        self.clicking = False
        self.r_clicking = False

        if (event.type == SDL_MOUSEBUTTONDOWN):
            if (event.button.button == SDL_BUTTON_LEFT):
                self.clicking = True

            if (event.button.button == SDL_BUTTON_RIGHT):
                self.r_clicking = True
        
        if (event.type == SDL_MOUSEBUTTONUP):
            if (event.button.button == SDL_BUTTON_LEFT):
                self.clicking = False
            
            if (event.button.button == SDL_BUTTON_RIGHT):
                self.r_clicking = False

        if (event.type == SDL_MOUSEMOTION):
            self.pointer.x = event.motion.x
            self.pointer.y = event.motion.y

        self.x = self.pointer.x
        self.y = self.pointer.y

    def Is_Touching_Rect(self, rect): #version for rectangles
        return SDL_HasIntersection(self.pointer, rect)

    def Is_Clicking_Rect(self, rect):
        return self.Is_Touching_Rect(rect) and self.clicking

    def Is_Touching(self, item):
        return self.Is_Touching_Rect(item.rect)

    def Is_Clicking(self, item):
        return self.Is_Touching(item) and self.clicking


    def Is_R_Clicking(self, item):
        return self.Is_Touching(item) and self.r_clicking

    def Set_Cursor(self, id):
        if id not in Pointer.cursors:
            Pointer.cursors[id] = SDL_CreateSystemCursor(id)
        SDL_SetCursor(Pointer.cursors[id])

    def __del__(self):
        for cursor in Pointer.cursors:
            SDL_FreeCursor(Pointer.cursors[cursor])

#________________FUNCTIONS____________________________#
def ScreenPresent(renderer):
    SDL_RenderPresent(renderer)

def ScreenWipe(renderer):
    SDL_RenderClear(renderer)

def WindowState(window, renderer, fs):
    if (fs == True):
        SDL_SetWindowFullscreen(window, SDL_WINDOW_FULLSCREEN)
    elif (fs == False):
        SDL_SetWindowFullscreen(window, 0)

def GetCharacters():
    resources = dict()
    for path in os.listdir('sprites'):
        c = path.split(".bmp")
        resources[c[0]] = c
    
    return resources

#def TPS(T_rate):
#    start_time_ms = int(SDL_GetTicks())
#    elapsed_time_ms = int(SDL_GetTicks() - start_time_ms)
#    SDL_Delay(1000//T_rate - elapsed_time_ms)
#    seconds_per_frame = (SDL_GetTicks() - start_time_ms) / 1000
#    ticks = 1 // seconds_per_frame
#    print(ticks)

def main():
    SDL_Init(SDL_INIT_VIDEO)
    if (TTF_Init() == -1):
        print("TTF_Init: ", TTF_GetError())


    #__________________VARIABLES_________________________#
    running = True
    WIDTH = 640
    HEIGHT = 480
    TickRate = 60
    char_selection = ""
    player = None
    Fullscreen = False
    gamestate = 'MENU'

    #_______________Window and Renderer___________________#
    mouse = Pointer()
    SDL_SetHint(SDL_HINT_RENDER_DRIVER, b'opengl')
    window = SDL_CreateWindow(b"R_Dokutsu Monogatari", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED,
                     WIDTH, HEIGHT, 0)
    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_PRESENTVSYNC)
    event = SDL_Event()
    SDL_SetRenderDrawBlendMode(renderer, SDL_BLENDMODE_BLEND)
    SDL_ShowCursor(SDL_ENABLE)
    
    #________________OBJECTS______________________________#

    menu_items = {
        "New Game": TextObject(renderer, "New Game", 200, 50, ['joystix', b'joystix.ttf'], location=(240, 260)),
        "Load Game": TextObject(renderer, "Load Game", 200, 50, ['joystix'], location=(240, 320))
    }

    characters = GetCharacters()

    if (player):
        player = AnimatedCharacter(32, 36, 0, 0, renderer, character_selection)

    #______________GENERAL PROCESSING______________________#
    event = SDL_Event()
    while (running):
        direction = ''
        movement = False
        #TICK_RATE__________________________________________#
        #TPS(TickRate)

        #EVENTS_____________________________________________#
        #___KeyEvents_______________________________________#
        key = SDL_GetKeyboardState(None)

        if (key[SDL_SCANCODE_LEFT]):
            movement = True
            direction = 'left'

        if (key[SDL_SCANCODE_RIGHT]):
            movement = True
            direction = 'right'

        if (key[SDL_SCANCODE_UP]):
            movement = True
            direction = 'up'

        if (key[SDL_SCANCODE_DOWN]):
            movement = True
            direction = 'down'

        if (key[SDL_SCANCODE_F12]):
            if Fullscreen == False:
                Fullscreen = True
            elif Fullscreen == True:
                Fullscreen = False

        if (key[SDL_SCANCODE_ESCAPE]):
            SDL_Quit()
            TTF_Quit()
            running = False
            
        # ________________________________________________#
        WindowState(window, renderer, Fullscreen)
        #___________________________________________________#
        while (SDL_PollEvent(ctypes.byref(event))):
            mouse.Compute(event)
            if (event.type == SDL_QUIT):
                SDL_DestroyRenderer(renderer)
                #background.Quit()
                SDL_DestroyWindow(window)
                running = False
                break

        #LOGIC__________________________________________________#
        if (gamestate == 'MENU'):
            for item in menu_items:
                if (mouse.Is_Touching(menu_items[item])):
                    menu_items[item].highlight = True
                else:
                    menu_items[item].highlight = False
                
                if (mouse.Is_Clicking(menu_items[item])):
                    if (item == "NEW GAME"):
                        gamestate == 'CHARACTER SELECTION'

        if (gamestate == 'CHARACTER SELECTION'):
            pass

        if (gamestate == 'GAME'):
            if (player):
                player.Movement(movement, direction)
                player.Animating()
        


        #RENDERING______________________________________________#
        SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255)
        SDL_RenderClear(renderer)

        if (gamestate == 'MENU'):
            for item in menu_items:
                menu_items[item].Render()
        
        if (gamestate == 'CHARACTER SELECTION'):
            pass


       # background.Render()
        SDL_RenderPresent(renderer)
        SDL_Delay(10)
        
    SDL_Quit()
    return 0
    #_____________
main()