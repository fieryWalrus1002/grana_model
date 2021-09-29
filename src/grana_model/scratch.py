"""Showcase what the output of pymunk.pyglet_util draw methods will look like.
See pygame_util_demo.py for a comparison to pygame.
"""

__docformat__ = "reStructuredText"

import pyglet
import pymunk
import pymunk.pyglet_util


window = pyglet.window.Window(1000, 700, vsync=False)
space = pymunk.Space()
space.gravity = -9000.0, -900.0
draw_options = pymunk.pyglet_util.DrawOptions()

b = pymunk.Body(100, 10, body_type=pymunk.Body.DYNAMIC)

c1 = pymunk.Circle(b, 10)

b.position = (500, 700)
space.add(b, c1)


textbatch = pyglet.graphics.Batch()
pyglet.text.Label(
    "Demo example of shapes drawn by pyglet_util.draw()",
    x=5,
    y=5,
    batch=textbatch,
    color=(100, 100, 100, 255),
)
batch = pyglet.graphics.Batch()

# otherwise save screenshot wont work
_ = pyglet.window.FPSDisplay(window)


@window.event
def update():
    global space
    space.step(1 / 60)


@window.event
def on_draw():
    pyglet.gl.glClearColor(255, 255, 255, 255)
    window.clear()
    space.debug_draw(draw_options)
    textbatch.draw()
    space.step(1)


@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.P:
        pyglet.image.get_buffer_manager().get_color_buffer().save(
            "pyglet_util_demo.png"
        )


pyglet.clock.schedule_interval(window.update, 1.0 / 60.0)
pyglet.app.run()
