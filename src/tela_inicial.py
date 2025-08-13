from .settings import *

class TelaInicial:
    def __init__(self, screen):
        self.screen = screen
        self.fundo = pygame.image.load("assets/images/tela_inicial.png").convert()
        self.fundo = pygame.transform.scale(self.fundo, (WINDOW_WIDTH, WINDOW_HEIGHT))
        
    def update(self):
        self.screen.blit(self.fundo, (0,0))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            return True
        return False
