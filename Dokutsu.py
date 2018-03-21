#CODE BY ISA BOLLING
import os
os.environ["PYSDL2_DLL_PATH"] = os.path.dirname(os.path.abspath(__file__))
from sdl2 import *
import sdl2.ext
import ctypes

def main():
    SDL_Init(SDL_INIT_VIDEO)
    #__________________VARIABLES_________________________#
    running = True
    WIDTH = 640
    HEIGHT = 480
    TickRate = 60
    Fullscreen = False

    #_______________Window and Renderer___________________#
    SDL_SetHint(SDL_HINT_RENDER_DRIVER, b'opengl')
    window = SDL_CreateWindow(b"R_Dokutsu Monogatari", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED,
                     WIDTH, HEIGHT, 0)
    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_PRESENTVSYNC)
    SDL_ShowCursor(0)

    #________________CLASSES______________________________#
    class AnimatedCharacter:
        def __init__(self, w, h, x, y):
            self.w = w
            self.h = h
            self.x = x
            self.y = y
            self.s_x = 0
            self.s_y = 0
            self.n = self.s_y
            self.Moving = False
            self.Animate = False
            self.A_Rate = 0
            self.path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "content", "MyChar.bmp")
            self.image = SDL_LoadBMP(self.path.encode('utf-8'))
            self.texture = SDL_CreateTextureFromSurface(renderer, self.image)
            SDL_FreeSurface(self.image)

        def Render(self):
            ScreenWipe()
            self.s_y = self.n
            self.src_rect = SDL_Rect(self.s_x, self.s_y, self.w, self.h)
            self.dest_rect = SDL_Rect(self.x, self.y, 32, 32)
            SDL_RenderCopy(renderer, self.texture, self.src_rect, self.dest_rect )

        def Movement(self, state, direction):
            self.direction = direction
            if (state == True):
                self.Moving = True
                self.Animate = True
                if (direction == 'left'):
                    self.x -= 3
                elif (direction == 'right'):
                    self.x += 3
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
                       self.n = 0
                       self.s_x += 33
                       if self.s_x == 99:
                           self.s_x = 0
                    if self.direction == 'right':
                        self.n = 32
                        self.s_x += 31
                        if self.s_x == 93:
                            self.s_x = 0

            if self.Moving == False:
                if (direction == 'up'):
                    self.s_x = 97
                if (direction == 'down'):
                    self.s_x = 224
                if (direction == ''):
                    self.s_x = 0


        def Quit(self):
            SDL_DestroyTexture(self.texture)
    #________________OBJECTS______________________________#
    Quote = AnimatedCharacter( 32, 32, 450, 260)

    #________________FUNCTIONS____________________________#
    def ScreenPresent():
        SDL_RenderPresent(renderer)

    def ScreenWipe():
        SDL_RenderClear(renderer)

    def WindowState(fs):
        if (fs == True):
            SDL_SetWindowFullscreen(window, SDL_WINDOW_FULLSCREEN)
        elif (fs == False):
            SDL_SetWindowFullscreen(window, 0)

    def TPS(T_rate):
        start_time_ms = int(SDL_GetTicks())
        elapsed_time_ms = int(SDL_GetTicks() - start_time_ms)
        SDL_Delay(1000//T_rate - elapsed_time_ms)
        seconds_per_frame = (SDL_GetTicks() - start_time_ms) / 1000
        ticks = 1/ seconds_per_frame
        print(ticks)

    #______________GENERAL PROCESSING______________________#
    event = SDL_Event()
    while (running):
        direction = ''
        movement = False
        #TICK_RATE__________________________________________#
        TPS(TickRate)

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
            movement = False
            direction = 'up'

        if (key[SDL_SCANCODE_DOWN]):
            movement = False
            direction = 'down'

        if (key[SDL_SCANCODE_F12]):
            if Fullscreen == False:
                Fullscreen = True
            elif Fullscreen == True:
                Fullscreen = False

        if (key[SDL_SCANCODE_ESCAPE]):
            SDL_Quit()
            running = False
            
        # ________________________________________________#
        WindowState(Fullscreen)
        #___________________________________________________#
        while (SDL_PollEvent(ctypes.byref(event))):
            if (event.type == SDL_QUIT):
                SDL_DestroyRenderer(renderer)
                Quote.Quit()
                SDL_DestroyWindow(window)
                running = False
                break

        #LOGIC__________________________________________________#
        Quote.Movement(movement, direction)
        Quote.Animating()

        #RENDERING______________________________________________#
        ScreenWipe()
        SDL_SetRenderDrawColor(renderer, 242, 242, 242, 255)
        Quote.Render()
        ScreenPresent()

    SDL_Quit()
    return 0
    #_____________
main()