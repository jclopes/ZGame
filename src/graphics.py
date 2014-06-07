import sys
import sdl2.ext

class Graphics(object):
    """handles all graphical parts"""
    def __init__(self):
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

    def close(self):
        sdl2.ext.quit()

   # sample code: import pdb; pdb.set_trace()
