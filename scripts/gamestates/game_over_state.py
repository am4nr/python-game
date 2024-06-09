import pygame
import sys
from scripts.Utils.settings import *
from scripts.gamestates.meta_state import GameState
from scripts.UI.button import Button

class GameOverState(GameState):
    buttons={}
    
    def enterState(self, game):
        print("Entered Game Over State")
        self.buttons["RESTART"] = Button(
            None,
            pos=(WIDTH / 2, HEIGHT / 2 + 100),
            text_input="RESTART",
            font=self.get_font(40),
            base_color="White",
            hovering_color="#d7fcd4",
            callback=lambda: self.restart(game)
        )
        self.buttons["MAIN_MENU"] = Button(
            None,
            pos=(WIDTH / 2, HEIGHT / 2 + 200),
            text_input="MAIN MENU",
            font=self.get_font(40),
            base_color="White",
            hovering_color="#d7fcd4",
            callback=lambda: self.main_menu(game)
        )
        self.bg = game.assets.get("Image", "background/BG.png")
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.game = game
        
    def main_menu(self, game):
        game.changeState(game.states["MainMenu"])
        
    def restart(self, game):
        game.level_manager.current_level.load()
        game.changeState(game.states["Play"])
        
    def get_font(self, size):  
        return pygame.font.Font("assets/font/Pacifico.ttf", size)
    
    def exitState(self):
        print("Exited Game Over State")  

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
            button.update(game.screen)

    def render(self, game):
        game.screen.fill(self.BLACK)
        game_over_text = self.get_font(70).render("GAME OVER", True, "#b68f40")
        text_rect = game_over_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        game.screen.blit(game_over_text, text_rect)
        
        for button_name in self.buttons:
            button = self.buttons[button_name]
            button.update(game.screen)