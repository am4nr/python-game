import pygame
import sys


from scripts.gamestates.meta_state import GameState
from scripts.Utils.settings import *
from scripts.UI.button import Button


class MainMenuState(GameState):
    buttons = {}

    def enterState(self, game):
        self.buttons["PLAY_BUTTON"] = Button(
            game.assets.get("Image", "objects/buttons/play_button.png"),
            pos=(WIDTH / 2, HEIGHT / 4 + 90),
            text_input="",
            font=self.get_font(30),
            base_color="#d7fcd4",
            hovering_color="White",
            callback=lambda: self.play(game)
        )
        self.buttons["OPTIONS_BUTTON"] = Button(
            game.assets.get("Image", "objects/buttons/options_button.png"),
            pos=(WIDTH / 2, 2 * HEIGHT / 4 + 65),
            text_input="",
            font=self.get_font(30),
            base_color="#d7fcd4",
            hovering_color="White",
            callback=lambda: self.options(game)
        )
        self.buttons["QUIT_BUTTON"] = Button(
            game.assets.get("Image", "objects/buttons/cancel_button.png"),
            pos=(WIDTH / 2, 3 * HEIGHT / 4 + 50),
            text_input="",
            font=self.get_font(30),
            base_color="#d7fcd4",
            hovering_color="White",
            callback=lambda: self.quit(game)
            (game)
        )
        self.bg = game.assets.get("Image", "background/BG.png")
        
        self.confirm_sound = game.assets.get("Sound", "SFX/confirmbeep.wav")


    def get_font(self, size):  
        return pygame.font.Font("assets/font/Pacifico.ttf", size)

    def play(self, game):
        self.confirm_sound.play()
        game.level_manager.current_level.load()
        game.changeState(game.states["Play"])

    def options(self, game):
        game.changeState(game.states["Options"])

    def main_menu(self, game):
        game.changeState(game.states["MainMenu"])
        
    def quit(self, game):
        pygame.quit()
        sys.exit()
        
    def exitState(self, game):
        print("Exit Mainmenu")

    def event(self, game, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button_name in self.buttons:
                button = self.buttons[button_name]
                if button.checkForInput(game.mouse_pos) is True:
                    callback = button.get_callback()
                    callback()

    def update(self, game):
        for button_name in self.buttons:
            button = self.buttons[button_name]
            button.changeColor(game.mouse_pos)

    def render(self, game):
        BG = self.bg
        game.screen.blit(BG, (0, 0))

        MENU_TEXT = self.get_font(70).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH / 2, 100))

        game.screen.blit(MENU_TEXT, MENU_RECT)

        for button_name in self.buttons:
            button = self.buttons[button_name]
            button.update(game.screen)
