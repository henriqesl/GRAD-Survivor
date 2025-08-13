from .settings import *
from .player import Player
from .mouse import Mouse
from .obstacles import Obstacles
from .monster_manager import MonsterManager, EVENTO_SPAWN_MONSTRO
from .collectible_items import drop_item, aplicar_poder
from . import game_data
from .tela_inicial import TelaInicial

# algumas partes do codigo em ingles e outras em port
class Game:
    def __init__(self):
        pygame.init() 
        pygame.display.set_caption(game_data.ASSET_PATHS['caption'])
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.game_surface = pygame.Surface((MAP_WIDTH, MAP_HEIGHT))
        self.clock = pygame.time.Clock()
        self.map = pygame.image.load(game_data.ASSET_PATHS['map']).convert()

        pygame.mixer.music.load(game_data.ASSET_PATHS['music'])
        pygame.mixer.music.set_volume(0.4)

        self.game_state = 'start_screen' # Começa na tela inicial
        self.tela_inicial = TelaInicial(self.screen)

        self.heart_full_img = pygame.image.load(game_data.ASSET_PATHS['heart_full'])
        self.heart_empty_img = pygame.image.load(game_data.ASSET_PATHS['heart_empty'])

        # --- GRUPOS ---
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.monster_sprites = pygame.sprite.Group()
        self.mouse_sprites = pygame.sprite.Group()
        self.collectible_items = pygame.sprite.Group()

        self.monster_manager = MonsterManager(self.all_sprites, self.monster_sprites, self.collision_sprites)
        
        self.itens_coletados = {'cracha': 0, 'redbull': 0, 'subway': 0}
        self.inimigos_eliminados = 0

        self.shoot_delay = game_data.PLAYER_DATA['shoot_delay']
        self.last_shot_time = 0
        
        Obstacles(self.collision_sprites)

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
        
        self.item_imagens = {
            name: pygame.image.load(data['image_path']).convert_alpha()
            for name, data in game_data.ITEM_DATA.items()
            }
            
        self.win_screen_img = pygame.image.load("assets/images/win.png").convert()
        self.win_screen_img = pygame.transform.scale(self.win_screen_img, (WINDOW_WIDTH, WINDOW_HEIGHT))
        
        self.game_over_screen_img = pygame.image.load("assets/images/gameover.png").convert()
        self.game_over_screen_img = pygame.transform.scale(self.game_over_screen_img, (WINDOW_WIDTH, WINDOW_HEIGHT))

    def reset_game(self):
        self.player_principal.reset()
        self.monster_manager.reset()
        self.mouse_sprites.empty()
        self.collectible_items.empty()
        self.all_sprites.empty()
        self.all_sprites.add(self.player_principal)
        self.itens_coletados = {'cracha': 0, 'redbull': 0, 'subway': 0}
        self.inimigos_eliminados = 0

    def run(self):
    # A música agora só começa quando o jogo de fato inicia, e não na tela de título.
    
        while True:
            dt = self.clock.tick(FPS) / 1000

            # --- PROCESSAMENTO DE EVENTOS ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # Eventos da TELA INICIAL
                if self.game_state == 'start_screen':
                    if self.tela_inicial.handle_event(event):
                        self.game_state = 'playing'
                        pygame.mixer.music.play(loops=-1) # Inicia a música aqui

                # Eventos DURANTE O JOGO
                elif self.game_state == 'playing':
                    if event.type == EVENTO_SPAWN_MONSTRO:
                        self.monster_manager.spawn_monster()

                # Eventos nas telas de FIM DE JOGO (Vitória ou Game Over)
                elif self.game_state in ('win', 'game_over'):
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.reset_game()
                        self.game_state = 'playing'

            # --- LÓGICA E DESENHO BASEADOS NO ESTADO ---
            
            # Estado: TELA INICIAL
            if self.game_state == 'start_screen':
                self.tela_inicial.update()

            # Estado: JOGANDO
            elif self.game_state == 'playing':
                # (Todo o seu código de lógica do jogo continua aqui, sem alterações)
                # --- ATUALIZAÇÕES ---
                self.player_principal.update(dt)
                self.monster_sprites.update(dt, self.player_principal)
                self.mouse_sprites.update(dt)
                self.monster_manager.update()
                self.collectible_items.update()
                self.check_shooting()
                # --- MUDANÇA DE ESTADO ---
                if self.monster_manager.game_won:
                    self.game_state = 'win'
                if self.player_principal.lives <= 0:
                    self.game_state = 'game_over'
                # --- COLISÕES ---
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
                # --- DESENHO ---
                self.game_surface.blit(self.map, (0, 0))
                self.all_sprites.draw(self.game_surface)
                self.screen.fill((25, 25, 35))
                self.screen.blit(self.game_surface, (0, HUD_HEIGHT))
                self.draw_ui()
            
            # --- MUDANÇA: Estado VITÓRIA ---
            elif self.game_state == 'win':
                # Desenha a imagem de fundo de vitória
                self.screen.blit(self.win_screen_img, (0, 0))
                # Desenha o relatório de estatísticas por cima (MAIS PARA BAIXO)
                self.draw_end_game_report(WINDOW_HEIGHT / 2 + 220)

        # --- MUDANÇA: Estado GAME OVER ---
            elif self.game_state == 'game_over':
                # Desenha a imagem de fundo de game over
                self.screen.blit(self.game_over_screen_img, (0, 0))
                # Desenha o relatório de estatísticas por cima (MAIS PARA BAIXO)
                self.draw_end_game_report(WINDOW_HEIGHT / 2 + 180)
            
            # Atualiza a tela inteira no final do loop, independentemente do estado
            pygame.display.flip()

    def draw_end_game_report(self, y_start):
        # --- Relatório de Fim de Jogo ---
        # FONTES DIMINUÍDAS
        font_titulo = pygame.font.Font(None, 32) 
        font_item = pygame.font.Font(None, 28)
        cor_texto = (255, 255, 255)
        y_offset = y_start
        
        inimigos_texto = font_titulo.render(f"Inimigos Eliminados: {self.inimigos_eliminados}", True, cor_texto)
        inimigos_rect = inimigos_texto.get_rect(center=(WINDOW_WIDTH / 2, y_offset))
        self.screen.blit(inimigos_texto, inimigos_rect)
        
        # ESPAÇAMENTO DIMINUÍDO
        y_offset += 35 

        texto_relatorio = font_titulo.render("Itens Coletados:", True, cor_texto)
        rect_relatorio = texto_relatorio.get_rect(center=(WINDOW_WIDTH / 2, y_offset))
        self.screen.blit(texto_relatorio, rect_relatorio)
        
        # ESPAÇAMENTO DIMINUÍDO
        y_offset += 25

        for item, quantidade in self.itens_coletados.items():
            nome_item_formatado = item.capitalize()
            texto_item = font_item.render(f"{nome_item_formatado}: {quantidade}", True, cor_texto)
            rect_item = texto_item.get_rect(center=(WINDOW_WIDTH / 2, y_offset))
            self.screen.blit(texto_item, rect_item)
            # ESPAÇAMENTO DIMINUÍDO
            y_offset += 28 

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

