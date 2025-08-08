from settings import *
from player import Player
from mouse import Mouse
from obstacles import Obstacles

class Game:
    def __init__(self):
        pygame.display.set_caption("GRAD-Survivor")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.map = pygame.image.load('assets/images/mapa1.0.png')

        self.all_sprites = pygame.sprite.Group()
        self.colision_sprites = pygame.sprite.Group()

        Obstacles(self.collision_sprites)

        self.player_principal = Player(
            (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2),
            self.all_sprites,
            self.collision_sprites
        )

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000  # delta time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Atualizações
            self.all_sprites.update(dt)

            # Desenho
            self.screen.blit(self.map, (0, 0))
            self.all_sprites.draw(self.screen)
            pygame.display.flip()

        pygame.quit()

jogo = Game()

jogo.run()