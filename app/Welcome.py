#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function

import pygame
import qrcode
from pygame import mixer
from pygame.locals import *

from app.droid_configuration import *
from app.droid_database import *
from app.droid_remote_control.RPi_Server_Code import start_rpi_server
from app.droid_screen import DroidScreen
from app.web_server.droide_web_server import start_web_server
from wall_e import WallE

POS_3 = 350

POS_2 = 290

POS_1 = 230


def start_modules():
    print("** loading configuration")
    init_configuration()
    print("** loading database")
    init_db()
    print("** Starting RPI server")
    start_rpi_server()
    print("** Starting web server")
    start_web_server()


class App:
    def __init__(self):

        start_modules()

        self.screen = DroidScreen()
        self.feature = pygame.Surface((300, 50))
        self.font = pygame.font.Font(None, 40)
        self.font_small = pygame.font.Font(None, 30)
        self.font_smaller = pygame.font.Font(None, 20)

    def end(self):
        pygame.quit()
        sys.exit()

    def shutdown(self):
        pygame.quit()
        subprocess.call("sudo shutdown --poweroff now", shell=True)

    def lego_mood(self):
        print("lego mood")
        call_script("lego_mood/LegoMood.py")
        print("lego mood done")

    def random_picker(self):
        print("random_picker")
        call_script("random_picker/random_picker.py")
        print("random_picker done")

    def meeting_timer(self):
        call_script("meeting_timer/meeting_timer.py")

    def draw_feature(self, text, pos):
        feature_1_text = self.font_small.render(text, True, (255, 255, 255))
        self.feature.fill((100, 100, 255))
        # feature_1.blit(feature_1_text, (10,10))
        self.screen.main_panel.blit(self.feature, (10, pos), None, BLEND_RGBA_MULT)
        self.screen.main_panel.blit(feature_1_text, (20, pos + 15))

    def draw_busy(self, text, pos):
        feature_1_text = self.font_small.render(text, True, (255, 255, 255))
        self.feature.fill((255, 140, 140))
        #  feature.blit(feature_1_text, (10,10))
        self.screen.main_panel.blit(self.feature, (10, pos), None, BLEND_RGBA_MULT)
        self.screen.main_panel.blit(feature_1_text, (20, pos + 15))

    def exterminate(self):
        mixer.music.load(path_to_sound('Exterminate.mp3'))
        mixer.music.play()

    def run(self):

        wall_e = WallE()
        wall_e_2 = WallE()
        all_sprites_list = pygame.sprite.Group()

        all_sprites_list.add(wall_e)
        all_sprites_list.add(wall_e_2)

        wall_e.rect.x = 10
        wall_e.rect.y = 10

        # charge une image de fond.
        img_back = pygame.image.load(path_to_image('background2.png'))
        startup_text = self.font.render("Welcome, Droid...", True, (200, 125, 125))
        remote_control = "http://" + current_host_name() + ":5000/remote_control"
        web_text = self.font_smaller.render(remote_control, True, (125, 125, 125))
        if not exists(path_to_tmp_file('qrcode.png')):
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=5,
                border=1,
            )
            qr.add_data(remote_control)
            qr.make(fit=True)
            qr.make_image().save(path_to_tmp_file("qrcode.png"))

        rc_qrcode_image = pygame.image.load(path_to_tmp_file('qrcode.png'))

        top_panel = pygame.Surface((320, 50))
        top_panel.fill((180, 180, 180))

        bottom_text = self.font_smaller.render("Shutdown...", True, (255, 255, 255))
        bottom_panel = pygame.Surface((320, 30))
        bottom_panel.fill((255, 0, 0))

        state = "ready"

        while True:  # main game loop

            self.screen.clear()

            all_sprites_list.update()

            self.screen.main_panel.blit(img_back, (0, 0))

            wall_e.move(-1)
            wall_e_2.move()

            all_sprites_list.draw(self.screen.main_panel)

            self.screen.main_panel.blit(top_panel, (0, 0), None, BLEND_RGBA_MULT)
            self.screen.main_panel.blit(startup_text, (40, 11))
            self.screen.main_panel.blit(web_text, (10, 57))
            self.screen.main_panel.blit(rc_qrcode_image, (9, 68))

            self.screen.main_panel.blit(bottom_panel, (0, 450), None, BLEND_RGBA_MULT)
            self.screen.main_panel.blit(bottom_text, (10, 458))

            if state == "ready":
                self.draw_feature("Random Picker", POS_1)
                self.draw_feature("Lego Mood", POS_2)
                self.draw_feature("Meeting Timer", POS_3)

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.end()
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    self.end()
                elif event.type == MOUSEBUTTONDOWN and state == "ready":
                    pos = pygame.mouse.get_pos()
                    x = pos[0]
                    y = pos[1]
                    if POS_1 < x < POS_1 + 50 and 10 < y < 300:
                        state = "random_picker"
                        self.draw_busy("Random Picker", POS_1)

                    elif POS_2 < x < POS_2 + 50 and 10 < y < 300:
                        state = "lego_mood"
                        self.draw_busy("Lego Mood", POS_2)

                    elif POS_3 < x < POS_3 + 50:

                        state = "meeting_timer"
                        self.draw_busy("Meeting Timer", POS_3)

                    elif 0 < x < 50:

                        self.exterminate()
                    elif x > 450:
                        self.shutdown()

            self.screen.tick(60)
            self.screen.flip()

            if state != "ready":
                self.screen.hide()
                if state == "lego_mood":
                    self.lego_mood()
                elif state == "random_picker":
                    self.random_picker()
                elif state == "meeting_timer":
                    self.meeting_timer()
                state = "ready"
                self.screen.restore()

            pygame.display.flip()
