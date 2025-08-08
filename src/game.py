from settings import *
from player import Player
from mouse import Mouse
from obstacles import Obstacles
from monster_manager import MonsterManager, EVENTO_SPAWN_MONSTRO

class Game:
    def __init__(self):
        pygame.display.set_caption("GRAD-Survivor")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.map = pygame.image.load('assets/images/mapa1.0.png').convert()

        # --- GRUPOS ---
        self.all_sprites = pygame.sprite.Group()       # Para DESENHAR tudo
        self.collision_sprites = pygame.sprite.Group() # Para colisões de parede
        self.monster_sprites = pygame.sprite.Group()   # Para LÓGICA dos monstros
        self.mouse_sprites = pygame.sprite.Group()     # Para LÓGICA dos tiros

        self.monster_manager = MonsterManager(self.all_sprites, self.monster_sprites)
        self.game_active = True
        
        Obstacles(self.collision_sprites)

        # Criamos o jogador e o adicionamos ao grupo de desenho
        self.player_principal = Player(
            (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2),
            [self.all_sprites], # Adiciona a all_sprites para ser desenhado
            self.collision_sprites,
            self
        )

    def run(self):
        while True:
            dt = self.clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if self.game_active:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.shoot_mouse()
                    if event.type == EVENTO_SPAWN_MONSTRO:
                        self.monster_manager.spawn_monster()
                else:
                    # Lógica para reiniciar
                    pass

            if self.game_active:
                # --- ATUALIZAÇÕES SEPARADAS ---
                # Aqui está a solução! Cada grupo é atualizado com seus próprios argumentos.

                # 1. O Player é atualizado sozinho, com os argumentos que ele espera.
                self.player_principal.update(dt)

                # 2. Os Monstros são atualizados, recebendo o jogador.
                self.monster_sprites.update(dt, self.player_principal)

                # 3. Os Mouses (tiros) são atualizados.
                self.mouse_sprites.update(dt)
                
                # O manager de waves também é atualizado
                self.monster_manager.update()

                # --- COLISÕES ---
                if pygame.sprite.spritecollide(self.player_principal, self.monster_sprites, False):
                    self.game_active = False

                pygame.sprite.groupcollide(self.mouse_sprites, self.monster_sprites, True, True)

                # --- DESENHO ---
                # O all_sprites continua desenhando tudo de uma vez, pois todos os
                # sprites foram adicionados a ele no momento da criação.
                self.screen.blit(self.map, (0, 0))
                self.all_sprites.draw(self.screen)
            else:
                # Lógica da tela de Game Over
                pass
            
            pygame.display.flip()

    def shoot_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        player_pos = self.player_principal.rect.center
        direction = pygame.Vector2(mouse_pos) - pygame.Vector2(player_pos)
        if direction.length() > 0:
            direction.normalize_ip()

        Mouse(
            pos=player_pos, 
            direction=direction, 
            groups=[self.all_sprites, self.mouse_sprites]
        )
        
if __name__ == '__main__':
    jogo = Game()
    jogo.run()