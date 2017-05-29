import pygame

from app.droide_ui import Screen, Button, Panel
from app.droid_brick_pi import BRICK_PI


class LegoMoodScreen(Screen):
    def __init__(self, main_screen):
        Screen.__init__(self, background_image_name="brick_img/brick-background.png")

        self.main_screen = main_screen

        btn_back = Button("Back", on_click=self.back)
        self.add_ui_element(btn_back, (10, 400))

        top_panel = Panel("Lego Mood")
        self.add_ui_element(top_panel, (0, 0))

    def set_up(self):
        Screen.set_up(self)
        # get app surface size
        rect = self.app.get_surface_rect()
        # create full_background
        full_background = pygame.Surface((rect.w, rect.h))
        # fill it
        for i in range(0, 13):
            for j in range(0, 20):
                full_background.blit(self.background, (i * 25, j * 25))
        # overwrite self background with new background
        self.background = full_background

    def back(self, owner):
        self.app.set_current_screen(self.main_screen)

    def render(self, display):
        Screen.render(self, display)
        # read brick pi value
        if BRICK_PI.update_values():
            value = BRICK_PI.read_color_sensor()
            self.log.debug("read brickpi value " + str(value))


