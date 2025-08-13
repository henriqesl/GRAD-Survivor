from .settings import *
from . import game_data

class TelaInicial:
    def __init__(self, screen):
        self.screen = screen
        self.fundo = pygame.image.load(game_data.ASSET_PATHS['initial_screen_bg']).convert()
        self.botao_img = pygame.image.load(game_data.ASSET_PATHS['initial_screen_button']).convert_alpha()
        self.botao_rect = self.botao_img.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 150))

    def desenhar(self):
        self.screen.blit(self.fundo, (0, 0))
        self.screen.blit(self.botao_img, self.botao_rect)

    def verificar_clique(self, pos_mouse):
        return self.botao_rect.collidepoint(pos_mouse)
