import pygame
import sys
from scripts.gamestates.meta_state import GameState

class GameOver(GameState):
    def __init__(self, game):
        self.game = game
        self.bg = game.assets.get("Image", "background/BG.png")
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
    
    def get_font(self, size):  
        return pygame.font.Font("assets/font/Pacifico.ttf", size)

    def enterState(self):
        pass

    def exitState(self):
        pass  

    def event(self):
        for event in self.pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == self.pygame.KEYDOWN:
                self.game.changeState(self.game.previousState) 

    def update(self):
        pass  

    def render(self):
        self.game.screen.fill(self.BLACK)
        game_over_text = self.get_font(70).render("GAME OVER", True, "#b68f40")
        text_rect = game_over_text.get_rect(center=(self.game.WIDTH / 2, self.game.HEIGHT / 2))
        self.game.screen.blit(game_over_text, text_rect)
        self.pygame.display.flip()