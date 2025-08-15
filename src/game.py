from .settings import *
from .player import Player
from .mouse import Mouse
from .obstacles import Obstacles
from .monster_manager import MonsterManager, EVENTO_SPAWN_MONSTRO
from .collectible_items import drop_item, aplicar_poder
from . import game_data
from .tela_inicial import TelaInicial
from .end_screens import WinScreen, GameOverScreen

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(game_data.ASSET_PATHS['caption'])
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.game_surface = pygame.Surface((MAP_WIDTH, MAP_HEIGHT))
        self.clock = pygame.time.Clock()
        self.map = pygame.image.load(game_data.ASSET_PATHS['map']).convert()

        self.game_state = 'start_screen'
        self.tela_inicial = TelaInicial(self.screen)

        self.heart_full_img = pygame.image.load(game_data.ASSET_PATHS['heart_full'])
        self.heart_empty_img = pygame.image.load(game_data.ASSET_PATHS['heart_empty'])

        self.musica_inicio = game_data.ASSET_PATHS['music_start'] # Crie essa entrada em game_data
        self.musica_principal = game_data.ASSET_PATHS['music_main']  # Renomeie a entrada 'music' para 'music_main'

        # Efeitos Sonoros (SFX)
        self.som_win = pygame.mixer.Sound(game_data.ASSET_PATHS['sound_win'])
        self.som_game_over = pygame.mixer.Sound(game_data.ASSET_PATHS['sound_game_over'])
        
        # Ajuste de volumes (0.0 a 1.0)
        self.som_win.set_volume(0.5)
        self.som_game_over.set_volume(0.5)

        # --- GRUPOS ---
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.monster_sprites = pygame.sprite.Group()
        self.mouse_sprites = pygame.sprite.Group()
        self.collectible_items = pygame.sprite.Group()

        self.monster_manager = MonsterManager(self.all_sprites, self.monster_sprites, self.collision_sprites, self)

        self.itens_coletados = {'cracha': 0, 'redbull': 0, 'subway': 0}
        self.inimigos_eliminados = 0

        self.shoot_delay = game_data.PLAYER_DATA['shoot_delay']
        self.last_shot_time = 0

        self.needs_reset = False

        self.grid = []
        Obstacles(self.collision_sprites)
        self.create_grid()

        self.player_principal = Player(
            (MAP_WIDTH / 2, MAP_HEIGHT / 2),
            [self.all_sprites],
            self.collision_sprites,
            self
        )

        self.item_imagens = {
            name: pygame.image.load(data['image_path']).convert_alpha()
            for name, data in game_data.ITEM_DATA.items()
        }

        # Telas recebem a referência do jogo
        self.win_screen = WinScreen(self)
        self.game_over_screen = GameOverScreen(self)

        pygame.mixer.music.load(self.musica_inicio)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(loops=-1)

    def create_grid(self):
        from .settings import TILE_SIZE, MAP_WIDTH, MAP_HEIGHT

        grid_width = MAP_WIDTH // TILE_SIZE
        grid_height = MAP_HEIGHT // TILE_SIZE
        self.grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]

        for obstacle in self.collision_sprites:
            for x in range(obstacle.rect.left, obstacle.rect.right, TILE_SIZE):
                for y in range(obstacle.rect.top, obstacle.rect.bottom, TILE_SIZE):
                    grid_x = x // TILE_SIZE
                    grid_y = y // TILE_SIZE
                    if 0 <= grid_y < grid_height and 0 <= grid_x < grid_width:
                        self.grid[grid_y][grid_x] = 1

    def reset_game(self):
        self.player_principal.reset()
        self.monster_manager.reset()
        self.mouse_sprites.empty()
        self.collectible_items.empty()
        self.all_sprites.empty()
        self.all_sprites.add(self.player_principal)
        self.itens_coletados.update({'cracha': 0, 'redbull': 0, 'subway': 0})
        self.inimigos_eliminados = 0
        self.win_screen.reset()
        self.game_over_screen.reset()

        # Reinicia a música do menu
        pygame.mixer.music.load(self.musica_inicio)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(loops=-1)

    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if self.game_state == 'start_screen':
                    if event.type == pygame.KEYDOWN:
                        pygame.mixer.music.stop() 
                        self.game_state = 'cutscene'
                        self.tela_inicial.iniciar_cutscene()

                elif self.game_state == 'cutscene':
                    if event.type == pygame.KEYDOWN:
                        terminou = self.tela_inicial.avancar_fala()
                        if terminou:
                            self.game_state = 'playing'
                            # Troca para a música principal do jogo
                            pygame.mixer.music.load(self.musica_principal)
                            pygame.mixer.music.set_volume(0.4)
                            pygame.mixer.music.play(loops=-1)

                elif self.game_state == 'playing':
                    if event.type == EVENTO_SPAWN_MONSTRO:
                        self.monster_manager.spawn_monster()

                elif self.game_state in ('win', 'game_over'):
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.needs_reset = True

            if self.needs_reset:
                self.reset_game()
                self.game_state = 'playing'

                pygame.mixer.music.load(self.musica_principal)
                pygame.mixer.music.set_volume(0.4) # Pode ajustar o volume
                pygame.mixer.music.play(loops=-1)
                self.needs_reset = False

            if self.game_state == 'start_screen':
                self.tela_inicial.update_tela_inicial()

            elif self.game_state == 'cutscene':
                self.tela_inicial.update_cutscene()

            elif self.game_state == 'playing':
                self.player_principal.update(dt)
                self.monster_sprites.update(dt, self.player_principal)
                self.mouse_sprites.update(dt)
                self.monster_manager.update()
                self.collectible_items.update()
                self.check_shooting()

                if self.monster_manager.game_won and self.game_state != 'win':
                    pygame.mixer.music.stop() 
                    self.som_win.play()       
                    self.game_state = 'win'

                if self.player_principal.lives <= 0 and self.game_state != 'game_over':
                    pygame.mixer.music.stop()       
                    self.som_game_over.play() 
                    self.game_state = 'game_over'

                colisoes_tiro_monstro = pygame.sprite.groupcollide(self.mouse_sprites, self.monster_sprites, True, False)
                for projeteis, monstros in colisoes_tiro_monstro.items():
                    for monstro in monstros:
                        monstro.vida -= 1
                        if monstro.vida <= 0:
                            self.inimigos_eliminados += 1
                            drop_item(monstro.rect.center, self.item_imagens, [self.all_sprites, self.collectible_items])
                            monstro.kill()

                if pygame.sprite.spritecollide(self.player_principal, self.monster_sprites, False):
                    self.player_principal.take_damage()

                coletados = pygame.sprite.spritecollide(self.player_principal, self.collectible_items, True)
                for item in coletados:
                    if item.funcao in self.itens_coletados:
                        self.itens_coletados[item.funcao] += 1
                    aplicar_poder(self.player_principal, item.funcao)

                self.game_surface.blit(self.map, (0, 0))
                self.all_sprites.draw(self.game_surface)
                self.screen.fill((25, 25, 35))
                self.screen.blit(self.game_surface, (0, HUD_HEIGHT))
                self.draw_ui()

            elif self.game_state == 'win':
                self.win_screen.update(dt)
                self.win_screen.draw()

            elif self.game_state == 'game_over':
                self.game_over_screen.update(dt)
                self.game_over_screen.draw()

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
