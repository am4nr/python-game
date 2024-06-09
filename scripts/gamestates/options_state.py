import pygame
import sys

from scripts.gamestates.meta_state import GameState
from scripts.UI.button import Button
from scripts.UI.slider import Slider
from scripts.Utils.settings import *

class OptionsState(GameState):
    buttons = {}

    def enterState(self, game):
        self.buttons["PLAY_BACK"] = Button(
            image=None,
            pos=(400, 550),
            text_input="MAIN MENU",
            font=self.get_font(40),
            base_color="White",
            hovering_color="#d7fcd4",
            callback=lambda: self.main_menu(game)
        )
        if game.previousState == game.states["Play"]:
            self.buttons["RESUME"] = Button(
                image=None,
                pos=(400, 450),
                text_input="CONTINUE",
                font=self.get_font(40),
                base_color="White",
                hovering_color="#d7fcd4",
                callback=lambda: self.play(game)
            )
        self.buttons["NOISE"] = Button(
            image=None,
            pos=(200, 255),
            text_input="Lautstärke",
            font=self.get_font(30),
            base_color="#b68f40",
            hovering_color="#b68f40",
            callback=lambda: self.options(game)
        )
        print("Entered Playstate")
        game.music = game.assets.get("Music","music/loop.wav")
        game.music.load("assets/music/loop.wav")
        game.music.play(-1)

        pygame.mixer.music.play(-1,0.0)
        pygame.mixer.music.set_volume(game.audio_volume)
        
        self.bg = game.assets.get("Image", "background/BG.png")
        self.volume_slider = Slider(300, 250, 200, 20, 0.0, 1.0, game.audio_volume)



    def get_font(self, size):  
        return pygame.font.Font("assets/font/Pacifico.ttf", size)
    
    def play(self, game):
        game.changeState(game.states["Play"])

    def options(self, game):
        game.changeState(game.states["Options"])

    def main_menu(self, game):
        game.changeState(game.states["MainMenu"])
            
    def quit(self, game):
        pygame.quit()
        sys.exit()
        
    def exitState(self, game):
        print("Exit Options")

    def event(self, game, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.volume_slider.check_click(game.mouse_pos)

            for button_name in self.buttons:
                button = self.buttons[button_name]
                if button.checkForInput(game.mouse_pos) is True:
                    callback = button.get_callback()
                    if callback is not None:
                        callback()
                        
        elif event.type == pygame.MOUSEBUTTONUP:
            self.volume_slider.hit = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.volume_slider.check_click(event.pos)
        elif event.type == pygame.MOUSEMOTION:
            self.volume_slider.update(event.pos)

        

    def update(self, game):
        for button_name in self.buttons:
            button = self.buttons[button_name]
            button.changeColor(game.mouse_pos)

        self.volume_slider.update(game.mouse_pos)
        game.audio_volume = self.volume_slider.val
        # Setze die Lautstärke entsprechend der Position des Reglers
        current_volume = self.volume_slider.val
        pygame.mixer.music.set_volume(current_volume)
        if game.assets.collections["Sound"]:
            for sound in game.assets.collections["Sound"]:
                mixer = game.assets.get("Sound", sound)
                mixer.set_volume(game.audio_volume)

    def render(self, game):
        BG = self.bg
        game.screen.blit(BG, (0, 0))

        MENU_TEXT = self.get_font(100).render("OPTIONS", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH / 2, 100))

        game.screen.blit(MENU_TEXT, MENU_RECT)

        for button_name in self.buttons:
            button = self.buttons[button_name]
            button.update(game.screen)
        
        self.volume_slider.render(game.screen)