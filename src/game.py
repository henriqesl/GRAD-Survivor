from settings import *
from player import Player
from mouse import Mouse
from obstacles import Obstacles
from monster_manager import MonsterManager, EVENTO_SPAWN_MONSTRO
from collectible_items import drop_item, aplicar_poder

class Game:
    def __init__(self):
        pygame.display.set_caption("GRAD-Survivor")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.map = pygame.image.load('assets/images/mapa1.0.png').convert()

        # --- GRUPOS ---
        self.all_sprites = pygame.sprite.Group()       # Para desenhar tudo
        self.collision_sprites = pygame.sprite.Group() # Paredes
        self.monster_sprites = pygame.sprite.Group()   # Lógica dos monstros
        self.mouse_sprites = pygame.sprite.Group()     # Lógica dos tiros
        self.collectible_items = pygame.sprite.Group() # Itens coletáveis

        Obstacles(self.collision_sprites)

        self.monster_manager = MonsterManager(self.all_sprites, self.monster_sprites)
        self.game_active = True

        self.shoot_delay = 300
        self.last_shot_time = 0

        self.player_principal = Player(
            (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2),
            [self.all_sprites],
            self.collision_sprites,
            self
        )

        self.item_imagens = {
            'cracha': pygame.image.load('assets/images/cracha.png').convert_alpha(),
            'redbull': pygame.image.load('assets/images/redbull.png').convert_alpha(),
            'subway': pygame.image.load('assets/images/subway.png').convert_alpha(),
        }

    def run(self):
        while True:
            dt = self.clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if self.game_active:
                    if event.type == EVENTO_SPAWN_MONSTRO:
                        self.monster_manager.spawn_monster()

            if self.game_active:
                self.player_principal.update(dt)
                self.monster_sprites.update(dt, self.player_principal)
                self.mouse_sprites.update(dt)
                self.monster_manager.update()

                self.check_shooting()

                # --- COLISÕES DE TIRO COM MONSTRO ---
                colisoes = pygame.sprite.groupcollide(self.mouse_sprites, self.monster_sprites, True, False)
                for projeteis, monstros in colisoes.items():
                    for monstro in monstros:
                        monstro.vida -= 1
                        if monstro.vida <= 0:
                            monstro.kill()
                            drop_item(monstro.rect.center, self.item_imagens, [self.all_sprites, self.collectible_items])

                # --- COLISÕES DE MONSTRO COM JOGADOR ---
                if pygame.sprite.spritecollide(self.player_principal, self.monster_sprites, False):
                    self.game_active = False

                # --- COLETA DE ITENS ---
                coletados = pygame.sprite.spritecollide(self.player_principal, self.collectible_items, False)
                for item in coletados:
                    if not item.used:
                        aplicar_poder(self.player_principal, item.funcao)
                        item.used = True
                        item.kill()

                # --- DESENHO ---
                self.screen.blit(self.map, (0, 0))
                self.all_sprites.draw(self.screen)
            else:
                # Tela de Game Over (não implementada ainda)
                pass

            pygame.display.flip()

    def check_shooting(self):
        mouse_buttons = pygame.mouse.get_pressed()

        if mouse_buttons[0]:
            current_time = pygame.time.get_ticks()

            if current_time - self.last_shot_time > self.shoot_delay:
                self.last_shot_time = current_time
                self.shoot_mouse()

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
