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
            text_input="BACK",
            font=self.get_font(40),
            base_color="White",
            hovering_color="Green",
        )
        self.bg = game.assets.get("Image", "background/BG.png")
        self.volume_slider = Slider(300, 250, 200, 20, 0, 100, 50)
    
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
                        
        if event.type == pygame.MOUSEBUTTONUP:
            self.volume_slider.hit = False

    def update(self, game):
        for button_name in self.buttons:
            button = self.buttons[button_name]
            button.changeColor(game.mouse_pos)

        self.volume_slider.update(game.mouse_pos)
        game.audio_volume = self.volume_slider.val

    def render(self, game):
        BG = self.bg
        game.screen.blit(BG, (0, 0))

        MENU_TEXT = self.get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH / 2, 100))

        game.screen.blit(MENU_TEXT, MENU_RECT)

        for button_name in self.buttons:
            button = self.buttons[button_name]
            button.update(game.screen)
        
        self.volume_slider.render(game.screen)