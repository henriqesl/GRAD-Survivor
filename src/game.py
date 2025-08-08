from settings import *
from player import Player
from mouse import Mouse
from obstacles import Obstacles

class Game:
    def __init__(self):
        pygame.display.set_caption("GRAD-Survivor")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.map = pygame.image.load('assets/images/mapa1.0.png').convert()

        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        Obstacles(self.collision_sprites)

        self.player_principal = Player(
            (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2),
            self.all_sprites,
            self.collision_sprites,
            self
        )

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000  # delta time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.shoot_mouse()

            # Atualizações
            self.all_sprites.update(dt)

            # Desenho
            self.screen.blit(self.map, (0, 0))
            self.all_sprites.draw(self.screen)
            pygame.display.flip()

        pygame.quit()

    def shoot_mouse(self):
        """
        Cria um projétil (Mouse) na posição do jogador, na direção do cursor.
        """
        mouse_pos = pygame.mouse.get_pos()
        player_pos = self.player_principal.rect.center
        
        direction = pygame.Vector2(mouse_pos) - pygame.Vector2(player_pos)
        if direction.length() > 0:
            direction.normalize_ip()

        # Cria a instância do Mouse, adicionando-a automaticamente ao self.all_sprites
        Mouse(
            pos=player_pos, 
            direction=direction, 
            groups=[self.all_sprites]
        )

if __name__ == '__main__':
    jogo = Game()
    jogo.run()