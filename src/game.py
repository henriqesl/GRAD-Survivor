from settings import *
from player import Player
from mouse import Mouse
from obstacles import Obstacles
from monster_manager import MonsterManager, EVENTO_SPAWN_MONSTRO
from collectible_items import drop_item, aplicar_poder

class Game:
    def __init__(self):
        pygame.init() 
        pygame.display.set_caption("GRAD-Survivor")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.game_surface = pygame.Surface((MAP_WIDTH, MAP_HEIGHT))
        self.clock = pygame.time.Clock()
        self.map = pygame.image.load('assets/images/mapa1.0.png').convert()

        pygame.mixer.music.load('assets/sounds/interstellar.mp3')
        pygame.mixer.music.set_volume(0.4)

        self.heart_full_img = pygame.image.load('assets/images/coracao.png')
        self.heart_empty_img = pygame.image.load('assets/images/coracao_apagado.png')

        # --- GRUPOS ---
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.monster_sprites = pygame.sprite.Group()
        self.mouse_sprites = pygame.sprite.Group()
        self.collectible_items = pygame.sprite.Group()

        self.monster_manager = MonsterManager(self.all_sprites, self.monster_sprites)
        self.game_active = True
        self.win_condition = False

        self.shoot_delay = 300
        self.last_shot_time = 0
        
        Obstacles(self.collision_sprites)

        self.player_principal = Player(
            (MAP_WIDTH / 2, MAP_HEIGHT / 2),
            [self.all_sprites],
            self.collision_sprites,
            self
        )

        self.item_imagens = {
            'cracha': pygame.image.load('assets/images/cracha.png').convert_alpha(),
            'redbull': pygame.image.load('assets/images/redbull.png').convert_alpha(),
            'subway': pygame.image.load('assets/images/subway.png').convert_alpha(),
        }

    def reset_game(self):
        # --- REINICIA A PARTIDA ---
        self.game_active = True
        self.win_condition = False
        self.player_principal.reset()
        self.monster_manager.reset()
        self.mouse_sprites.empty()
        self.collectible_items.empty()
        self.all_sprites.empty()
        self.all_sprites.add(self.player_principal)

    def run(self):
        pygame.mixer.music.play(loops=1)

        while True:
            dt = self.clock.tick(FPS) / 1000

            # --- EVENTOS ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if self.game_active:
                    if event.type == EVENTO_SPAWN_MONSTRO:
                        self.monster_manager.spawn_monster()
                else: 
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.reset_game()

            # --- LÓGICA PRINCIPAL DO JOGO ---
            if self.game_active:
                # --- ATUALIZAÇÕES ---
                self.player_principal.update(dt)
                self.monster_sprites.update(dt, self.player_principal)
                self.mouse_sprites.update(dt)
                self.monster_manager.update()

                if self.monster_manager.game_won:
                    self.game_active = False
                    self.win_condition = True

                self.check_shooting()
                self.collectible_items.update()

                # --- COLISÕES ---
                colisoes_tiro_monstro = pygame.sprite.groupcollide(self.mouse_sprites, self.monster_sprites, True, False)
                for projeteis, monstros in colisoes_tiro_monstro.items():
                    for monstro in monstros:
                        monstro.vida -= 1
                        if monstro.vida <= 0:
                            drop_item(monstro.rect.center, self.item_imagens, [self.all_sprites, self.collectible_items])
                            monstro.kill()
                
                monsters_hit = pygame.sprite.spritecollide(self.player_principal, self.monster_sprites, False)
                if monsters_hit:
                    self.player_principal.take_damage()
                
                if self.player_principal.lives <= 0:
                    self.game_active = False

                coletados = pygame.sprite.spritecollide(self.player_principal, self.collectible_items, True)
                for item in coletados:
                    aplicar_poder(self.player_principal, item.funcao)

                # --- DESENHO ---
                if self.game_active:
                    self.game_surface.blit(self.map, (0, 0))
                    self.all_sprites.draw(self.game_surface)

                    self.screen.fill((25, 25, 35)) # Cor escura para o HUD
                    self.screen.blit(self.game_surface, (0, HUD_HEIGHT))
                    self.draw_ui()
            
            else:
                if self.win_condition:
                    # Tela de Vitória
                    self.screen.fill((20, 100, 20))
                    font = pygame.font.Font(None, 48)
                    texto = font.render("Você Venceu! Pressione ESPAÇO.", True, (255, 255, 255))
                    rect_texto = texto.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
                    self.screen.blit(texto, rect_texto)
                else:
                    # Tela de Game Over
                    self.screen.fill((0, 0, 0))
                    font = pygame.font.Font(None, 48)
                    texto = font.render("Game Over! Pressione ESPAÇO para reiniciar.", True, (255, 255, 255))
                    rect_texto = texto.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
                    self.screen.blit(texto, rect_texto)
            
            pygame.display.flip()

    def draw_ui(self):
        for i in range(self.player_principal.max_lives):
            pos_x = 30 + i * (self.heart_full_img.get_width() + 6)
            heart_rect = self.heart_full_img.get_rect(topleft=(pos_x, 0))
            heart_rect.centery = HUD_HEIGHT / 2
            
            if i < self.player_principal.lives:
                self.screen.blit(self.heart_full_img, heart_rect)
            else:
                self.screen.blit(self.heart_empty_img, heart_rect)

        font = pygame.font.Font(None, 40)
        wave_text = font.render(f'Horda: {self.monster_manager.wave}', True, (255, 255, 255))
        wave_rect = wave_text.get_rect(topright=(WINDOW_WIDTH - 30, 0))
        wave_rect.centery = HUD_HEIGHT / 2
        self.screen.blit(wave_text, wave_rect)

    def check_shooting(self):
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0] and pygame.mouse.get_pos()[1] > HUD_HEIGHT:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time > self.shoot_delay:
                self.last_shot_time = current_time
                self.shoot_mouse()

    def shoot_mouse(self):
        mouse_pos_screen = pygame.mouse.get_pos()
        mouse_pos_game = (mouse_pos_screen[0], mouse_pos_screen[1] - HUD_HEIGHT)

        player_pos = self.player_principal.rect.center
        direction = pygame.Vector2(mouse_pos_game) - pygame.Vector2(player_pos)
        if direction.length() > 0:
            direction.normalize_ip()
        Mouse(pos=player_pos, direction=direction, groups=[self.all_sprites, self.mouse_sprites])

if __name__ == '__main__':
    jogo = Game()
    jogo.run()
