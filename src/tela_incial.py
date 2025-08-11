from .settings import *

class TelaInicial:
    def __init__(self, screen):
        self.screen = screen
        self.fundo = pygame.image.load("assets/images/inicio.png").convert()
        self.botao_img = pygame.image.load("assets/images/play.png").convert_alpha()
        self.botao_rect = self.botao_img.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 150))

    def desenhar(self):
        self.screen.blit(self.fundo, (0, 0))
        self.screen.blit(self.botao_img, self.botao_rect)

    def verificar_clique(self, pos_mouse):
        return self.botao_rect.collidepoint(pos_mouse)
