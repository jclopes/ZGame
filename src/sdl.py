#! /usr/bin/env python

import sys
import sdl2.ext
from zgame import Game

RESOURCES = sdl2.ext.Resources("..", "resources")


def main():
    sdl2.ext.init()

    window = sdl2.ext.Window("ZGame", size=(640, 480))
    window.show()

    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
    sprite = factory.from_image(RESOURCES.get_path("player.bmp"))

    spriterenderer = factory.create_sprite_render_system(window)
    spriterenderer.render(sprite)

    processor = sdl2.ext.TestEventProcessor()
    processor.run(window)

    import pdb; pdb.set_trace()

    playFile = open(sys.argv[1], 'r')
    game = Game(playFile)
    game.run()

    sdl2.ext.quit()


if __name__ == '__main__':
    sys.exit(main())
