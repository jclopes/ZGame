import sys
import sdl2
import sdl2.ext

class GraphicManager(object):
    """handles all graphical parts"""
    def __init__(self, eventManager):
        self.eMngr = eventManager 
        self.RESOURCES = sdl2.ext.Resources("..", "resources")

    def drawTest(self):
        sdl2.ext.init()

        window = sdl2.ext.Window("ZGame", size=(640, 480))
        window.show()

        factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
        sprite = factory.from_image(self.RESOURCES.get_path("player.bmp"))

        spriterenderer = factory.create_sprite_render_system(window)
        spriterenderer.render(sprite)

        processor = sdl2.ext.TestEventProcessor()
        processor.run(window)

    def drawTest2(self, leftTime, game):
        factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
        sprite = factory.from_image(self.RESOURCES.get_path("player.bmp"))
        currentPos = game.ownPlayer.currentPos
        sprite.position = currentPos.x, currentPos.y
        spriterenderer = factory.create_sprite_render_system(self.window)
        spriterenderer.render(sprite)
        #self.window.refresh()
        if leftTime > 0: 
            #print "got left time", 
            #print leftTime
            pass

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
