import sys
import sdl2
import sdl2.ext

class GraphicManager(object):
    """handles all graphical parts"""
    def __init__(self, eventManager):
        self.eMngr = eventManager 
        self.RESOURCES = sdl2.ext.Resources("..", "resources")

    def draw(self, leftTime, game):
        factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
        # create a sprite for the player
        sprite = factory.from_image(self.RESOURCES.get_path("player.bmp"))
        # magenta is set as the transparent color
        colorTransp = sdl2.pixels.SDL_MapRGB(sprite.surface.format,255,0,255)
        sdl2.surface.SDL_SetColorKey(sprite.surface, sdl2.SDL_TRUE, colorTransp)
        # position of the sprite (the player)
        currentPos = game.ownPlayer.currentPos
        sprite.position = currentPos.x, currentPos.y
        # get render system and render sprites
        spriterenderer = factory.create_sprite_render_system(self.window)
        spriterenderer.render(sprite)
        # fill main window so we erase previous items
        sdl2.ext.fill(self.window.get_surface(), sdl2.ext.Color(0, 0, 0))

    def start(self):
        sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
        sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK)
        #set joystick if there is any
        if sdl2.joystick.SDL_NumJoysticks() > 0:
            print "found joystick. getting first one out of",
            print sdl2.joystick.SDL_NumJoysticks()
            joystick = sdl2.SDL_JoystickOpen(0)
            print [sdl2.joystick.SDL_JoystickNumAxes(joystick),
                sdl2.joystick.SDL_JoystickNumBalls(joystick),
                sdl2.joystick.SDL_JoystickNumButtons(joystick),
                sdl2.joystick.SDL_JoystickNumHats(joystick)]
        self.window = sdl2.ext.Window("ZGame", size=(640, 480))
        self.window.show()

    def stop(self):
        sdl2.ext.quit()

   # sample code: import pdb; pdb.set_trace()
