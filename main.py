#Pygame Test 2
#Originaly made on: 4-6-2022

from time import time
from traceback import format_exc as tb_format_exc

#Start Time
START_TIME = time()

try:
    from rich import print
    import pygame
    import pygame.locals as pl

except Exception:
    exit(2)

#Game Class
class Game:
    def __init__(self):
        #Initialize Pygame
        pygame.init()
        #Setup Game Title, Screen Size, FPS and Other Stuff
        self.FPS = 60
        self.TARGET_FPS = 60
        self.RESOLUTION = (1280, 720)

        pygame.display.set_caption("Pygame Test 2")
        pygame.mouse.set_visible(False)
        pygame.display.set_mode(self.RESOLUTION, pl.DOUBLEBUF|pl.HWSURFACE)

        self.screen = pygame.display.get_surface()
        self.screen_center = {"x":self.screen.get_width()/2, "y":self.screen.get_height()/2}  
        self.clock = pygame.time.Clock()
        self.running = True

        self.prev_time = time()
        
        #Colors
        self.color = {
            "WHITE": (255,255,255),
            "GRAY": (100,100,100)
            }

        #Initialize Game Main Loop
        self.main_loop()

    #Get Mouse Position
    def get_mouse_pos(self):
        return pygame.mouse.get_pos()
    
    #Get FPS
    def get_fps(self):
        return round(self.clock.get_fps(), 2)

    #Delta Time
    def deltatime(self):
        now = time()
        dt = (now - self.prev_time) * self.TARGET_FPS
        self.prev_time = now        
        return dt

    #Track Mouse Holding
    def mouse_holding(self):
        return time() - self.cursor["HOLD_TIME"] if self.cursor["HOLD"] else self.cursor["HOLD_TIME"]
           
    #Text Display Function
    def text(self, text, x, y, size=20, color=(255,255,255), center=False):
        font = pygame.font.Font(None, size)
        text = font.render(text, 1, color)
        textrect = text.get_rect()
        textpos = (x,y)
        if center:
            textrect.centerx = x
            textrect.centery = y
            self.screen.blit(text, textrect)    
        else:
            textrect.topleft = textpos
            self.screen.blit(text, textpos)
    
    #Text List Function
    def text_list(self, text_list, x, y=0, size=20, color=(255,255,255), center=False):
        for text in text_list:
            self.text(text, x, y+(round((5*(size/5))*(text_list.index(text)))), size, color, center)
    
    #Move Surface
    def move_surface(self, surface, direction, speed=10):
        if direction == "UP":
            surface.y -= speed*self.dtime
        elif direction == "DOWN":
            surface.y += speed*self.dtime
        elif direction == "LEFT":
            surface.x -= speed*self.dtime
        elif direction == "RIGHT":
            surface.x += speed*self.dtime
    
    #Toggle Game FPS
    def toggle_fps(self):
        if self.FPS == 60:
            self.FPS = 30
        elif self.FPS == 30:
            self.FPS = 20
        elif self.FPS == 20:
            self.FPS = 10
        elif self.FPS == 10:
            self.FPS = 60
    
    #Surface Class
    class Surface:
        def __init__(self, screen, size:tuple, startpos=(0,0), color=(0,0,0)):
            #Setting up Surface Attributes
            self.screen = screen
            self.width = size[0]
            self.height = size[1]
            self.x = startpos[0]
            self.y = startpos[1]
            self.startpos = startpos
            self.color = color
            
            self.surface = pygame.Surface((self.width, self.height))
            self.surface.fill(color)
                        
            #First Update
            self.update(self.startpos)

        def fill(self, color):
            self.surface.fill(color)

        def update(self, pos):
            self.screen.blit(self.surface, pos)

        def get_rect(self):
            return self.surface.get_rect()
                
    #Keybind Class
    class Keybind:
        def __init__(self, key, function:callable, args:tuple=(), kwargs:dict=None):
            if kwargs is None:
                kwargs = {}
            self.key = key
            self.function = function
            self.args = args
            self.kwargs = kwargs
            
        def start(self):
            self.function(*self.args, **self.kwargs)
            
    #Player Movement Update
    def player_movement(self):
        #Check if key is pressed
        keys = pygame.key.get_pressed()
        keybinds = self.player["KEYBINDS"]
        for keybind in keybinds:
            if keys[keybinds[keybind].key]:
                keybinds[keybind].start()

        #Checking if Player is on the Screen
        if self.player_surface.x > self.RESOLUTION[0]:
            self.player_surface.x = self.RESOLUTION[0]
        elif self.player_surface.x < 0:
            self.player_surface.x = 0
        if self.player_surface.y > self.RESOLUTION[1]:
            self.player_surface.y = self.RESOLUTION[1]
        elif self.player_surface.y < 0:
            self.player_surface.y = 0
                                             
    #Setup Player
    def setup_player(self):
        #Initialize Player
        self.player = {
            "SURFACE": self.Surface(self.screen, (100,100), (self.screen_center["x"]-50, self.screen_center["y"]-50), (255,0,0)),
            "SPEED": 30,
            "KEYBINDS": {}
        }
        self.player_surface = self.player["SURFACE"]
        player_speed = self.player["SPEED"]
        
        #Setup Keybinds
        keys_to_bind = {
            "PLAYER_UP": self.Keybind(pl.K_w, self.move_surface, (self.player_surface, "UP", player_speed)),
            "PLAYER_DOWN": self.Keybind(pl.K_s, self.move_surface, (self.player_surface, "DOWN", player_speed)),
            "PLAYER_LEFT": self.Keybind(pl.K_a, self.move_surface, (self.player_surface, "LEFT", player_speed)),
            "PLAYER_RIGHT": self.Keybind(pl.K_d, self.move_surface, (self.player_surface, "RIGHT", player_speed)),
            "TOGGLE_FPS": self.Keybind(pl.K_1, self.toggle_fps)
        }
        for key in keys_to_bind:
            self.player["KEYBINDS"][key] = keys_to_bind[key]    
                       
    #Event Loop
    def event_loop(self):
        for event in pygame.event.get():
            #Game Quit
            if event.type == pl.KEYDOWN and event.key == pl.K_ESCAPE or event.type != pl.KEYDOWN and event.type == pl.QUIT:
                self.running = False

            #Mouse Click
            elif event.type == pl.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.cursor["ICON"].fill(self.color["GRAY"])
                    self.cursor["HOLD"] = True
                    self.cursor["HOLD_TIME"] = time()
            elif event.type == pl.MOUSEBUTTONUP:
                if event.button == 1:
                    self.cursor["ICON"].fill(self.color["WHITE"])
                    self.cursor["HOLD"] = False
                    self.cursor["HOLD_TIME"] = 0
                 
    #Before Game Main Loop
    def before_loop(self):
        self.cursor = {
            "ICON": self.Surface(self.screen, (10,10), (0,0), self.color["WHITE"]),
            "HOLD": False,
            "HOLD_TIME": 0,
        }
        self.setup_player()
           
    #During Game Main Loop
    def during_loop(self):
        self.dtime = self.deltatime()
        self.event_loop()
    
    #Update Priority: Lowest
    def low_update(self):
        self.player_surface.update((self.player_surface.x, self.player_surface.y)) 

    #Update Priority: Medium
    def med_update(self):
        self.text_list([
            f"FPS: {self.get_fps()}",
            f"FPS Limit: {self.FPS}",
            f"Player Pos: {round(self.player['SURFACE'].x, 2)}, {round(self.player['SURFACE'].y, 2)}",
            "",
            f"Running for: {round(time() - START_TIME, 2)}",
            "",
            "1 - Change FPS Limit",
            ], x=10, y=10, size=25, center=False)
    
        self.text_list([
            "Mouse Info:",
            f"Pos: {self.get_mouse_pos()}",
            f"HOLD: {self.cursor['HOLD']}",
            f"HOLD_TIME: {round(self.mouse_holding(), 2)}",
            ], x=10, y=self.RESOLUTION[1]-120, size=25, center=False)
        
    #Update Priority: Highest
    def highest_update(self): 
        self.cursor["ICON"].update(self.get_mouse_pos())
        self.player_movement()
    
    #Update Display
    def update(self):
        self.low_update()
        self.med_update()
        self.highest_update()    
        pygame.display.flip()

    #Game Main Loop
    def main_loop(self):
        #Before Loop
        self.before_loop()
        
        print(f"It took {round(time() - START_TIME, 2)} seconds to start the game since the start of the program.")
                
        while self.running:
            #FPS Limit
            self.clock.tick(self.FPS)
            self.screen.fill((10,10,10))
            #During Loop
            self.during_loop()
            #Frame Update
            self.update()
        
        print(f"The program have been running for {round(time() - START_TIME, 2)} seconds.")
        
        pygame.quit()
        exit(0)

if __name__ == "__main__":
    try:
        Game()
    except Exception:
        print(tb_format_exc())
        exit(1)