from settings import *

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, rect, group):
        super().__init__(group)  # Adiciona automaticamente ao grupo
        self.image = pygame.Surface((rect.width, rect.height))
        self.image.fill((255, 0, 0))  # Cor de preenchimento (vermelho) para visualização
        self.rect = rect

class Obstacles:
    def __init__(self, obstaculos_group):
        # Definindo os obstáculos como instâncias da classe Obstacle
        self.obstacles = [
            Obstacle(pygame.Rect((0, 0, 4, 600)), obstaculos_group),
            Obstacle(pygame.Rect((796, 0, 4, 600)), obstaculos_group),
            Obstacle(pygame.Rect((0, 0, 800, 4)), obstaculos_group),
            Obstacle(pygame.Rect((0, 595, 800, 4)), obstaculos_group),
            Obstacle(pygame.Rect((0, 56, 57, 3)), obstaculos_group),
            Obstacle(pygame.Rect((40, 51, 12, 5)), obstaculos_group),
            Obstacle(pygame.Rect((743, 53, 53, 3)), obstaculos_group),
            Obstacle(pygame.Rect((746, 48, 12, 5)), obstaculos_group),
            Obstacle(pygame.Rect((0, 493, 55, 3)), obstaculos_group),
            Obstacle(pygame.Rect((40, 488, 12, 5)), obstaculos_group),
            Obstacle(pygame.Rect((744, 492, 55, 3)), obstaculos_group),
            Obstacle(pygame.Rect((747, 487, 12, 5)), obstaculos_group),
            Obstacle(pygame.Rect((0, 369, 186, 82)), obstaculos_group),
            Obstacle(pygame.Rect((0, 173, 186, 80)), obstaculos_group),
            Obstacle(pygame.Rect((619, 169, 185, 80)), obstaculos_group),
            Obstacle(pygame.Rect((619, 374, 185, 81)), obstaculos_group),
            Obstacle(pygame.Rect((464, 33, 88, 52)), obstaculos_group),
            Obstacle(pygame.Rect((308, 4, 185, 4)), obstaculos_group)
        ]