import sys
import sdl2
import sdl2.ext
from direction import Direction

class GraphicManager(object):
    """handles all graphical parts"""
    def __init__(self, eventManager):
        self.eMngr = eventManager 
        self.RESOURCES = sdl2.ext.Resources("..", "resources")
        self.playerSubImgPosFromDirection = { 
            Direction.N : 0,
            Direction.NNE : 1,
            Direction.NE : 2,
            Direction.NEE : 3,
            Direction.E : 4,
            Direction.SEE : 5,
            Direction.SE : 6,
            Direction.SSE : 7,
            Direction.S : 8,
            Direction.SSW : 9,
            Direction.SW : 10,
            Direction.SWW : 11,
            Direction.W : 12,
            Direction.NWW : 13,
            Direction.NW : 14,
            Direction.NNW : 15,
            Direction.O : 16 }

    def draw(self, leftTime, game):
        #TODO there should be a field size and screen size and the positions should be translated
        factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
        # create a sprite for the player
        spriteWholeImage = factory.from_image(self.RESOURCES.get_path("player.bmp"))
        # get the right piece of the image
        offset = self.playerSubImgPosFromDirection[game.ownPlayer.faceDirection.direction] * 20
        sprite = spriteWholeImage.subsprite((offset,0,20,20))
        # magenta is set as the transparent color
        colorTransp = sdl2.pixels.SDL_MapRGB(sprite.surface.format,255,0,255)
        sdl2.surface.SDL_SetColorKey(sprite.surface, sdl2.SDL_TRUE, colorTransp)
        # position of the sprite (the player)
        currentPos = game.ownPlayer.position
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
