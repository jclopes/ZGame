import sys
import sdl2.ext

class GraphicManager(object):
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

    def drawTest2(self, game):
        factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
        sprite = factory.from_image(self.RESOURCES.get_path("player.bmp"))
        currentPos = game.ownPlayer.currentPos
        sprite.position = currentPos.x, currentPos.y
        spriterenderer = factory.create_sprite_render_system(self.window)
        spriterenderer.render(sprite)
        #self.window.refresh()

    def start(self):
        sdl2.ext.init()
        self.window = sdl2.ext.Window("ZGame", size=(640, 480))
        self.window.show()

    def stop(self):
        sdl2.ext.quit()

   # sample code: import pdb; pdb.set_trace()
