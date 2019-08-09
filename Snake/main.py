from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.core.window import Window
from random import randrange


SNAKE_VELOCITY = 40


class Snake(Widget):
    velocity_x = NumericProperty(SNAKE_VELOCITY)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def set_pos(self, wid, hei):
        return (wid/2, hei/2+20)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class Food(Widget):
    def random_pos(self, wid, hei):
        food_pos = (
            randrange(0, wid - 40, 40),
            randrange(0, hei - 40, 40)
        )
        return food_pos


class SnakeGame(Widget):
    snake = ObjectProperty(None)
    food = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(SnakeGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'up' and self.snake.velocity_y == 0:
            # self.snake.pos[1] += 40
            self.snake.velocity_y = SNAKE_VELOCITY
            self.snake.velocity_x = 0

        elif keycode[1] == 'down' and self.snake.velocity_y == 0:
            # self.snake.pos[1] -= 40
            self.snake.velocity_y = -SNAKE_VELOCITY
            self.snake.velocity_x = 0

        elif keycode[1] == 'left' and self.snake.velocity_x == 0:
            # self.snake.pos[0] -= 40
            self.snake.velocity_x = -SNAKE_VELOCITY
            self.snake.velocity_y = 0

        elif keycode[1] == 'right' and self.snake.velocity_x == 0:
            # self.snake.pos[0] += 40
            self.snake.velocity_x = SNAKE_VELOCITY
            self.snake.velocity_y = 0

    def update(self, dt):
        self.snake.move()

        if self.snake.top > self.height or self.snake.x < self.x:
            print(self.snake.top)
            print(self.top)
            exit()

        if self.snake.right > self.width or self.snake.y < self.y:
            print(self.snake.right)
            print(self.right)
            exit()


class SnakeApp(App):
    def build(self):
        game = SnakeGame()
        Clock.schedule_interval(game.update, 10/60)
        return game


if __name__ == "__main__":
    SnakeApp().run()