from .settings import *
from . import game_data
from .pathfinding import astar

BASE_IMG_PATH = os.path.join(os.path.dirname(__file__), '..', 'assets', 'images')

class MonstroBase(pygame.sprite.Sprite):
    def __init__(self, posicao_inicial, velocidade, collision_sprites, vida, frames, game_instance):
        super().__init__()
        self.vida = vida
        self.frames = frames
        self.state = 'down'
        self.image = self.frames[self.state][0]

        self.rect = self.image.get_rect(center=posicao_inicial)
        self.velocidade = velocidade
        self.posicao = pygame.Vector2(self.rect.center)
        self.collision_sprites = collision_sprites

        self.game = game_instance
        self.path = []
        self.path_update_cooldown = 500
        self.last_path_update = 0

    def seguir_jogador_direto(self, pos_jogador, dt):
        """Comportamento simples de seguir o jogador em linha reta (fallback)."""
        direcao = pygame.Vector2(pos_jogador) - self.posicao

        if abs(direcao.x) > abs(direcao.y):
            self.state = 'right' if direcao.x > 0 else 'left'
        else:
            self.state = 'down' if direcao.y > 0 else 'up'
        self.image = self.frames[self.state][0]

        if direcao.length() > 0:
            direcao.normalize_ip()

        dx = direcao.x * self.velocidade * dt
        dy = direcao.y * self.velocidade * dt

        self.mover_com_colisao(dx, dy)

    def recalcular_caminho(self, jogador):
        """Tenta calcular um novo caminho. Se falhar, limpa o caminho atual."""
        now = pygame.time.get_ticks()
        if now - self.last_path_update > self.path_update_cooldown:
            self.last_path_update = now
            
            monstro_grid_pos = (int(self.rect.centerx // TILE_SIZE), int(self.rect.centery // TILE_SIZE))
            jogador_grid_pos = (int(jogador.rect.centerx // TILE_SIZE), int(jogador.rect.centery // TILE_SIZE))
            
            target_pos = jogador_grid_pos
            
            grid_height = len(self.game.grid)
            grid_width = len(self.game.grid[0])
            if (0 <= target_pos[1] < grid_height and 0 <= target_pos[0] < grid_width and
                    self.game.grid[target_pos[1]][target_pos[0]] == 1):
                
                vizinhos = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
                encontrou_vizinho_valido = False
                for dx, dy in vizinhos:
                    vizinho_x, vizinho_y = target_pos[0] + dx, target_pos[1] + dy
                    if (0 <= vizinho_y < grid_height and 0 <= vizinho_x < grid_width and
                            self.game.grid[vizinho_y][vizinho_x] == 0):
                        target_pos = (vizinho_x, vizinho_y)
                        encontrou_vizinho_valido = True
                        break
                
                if not encontrou_vizinho_valido:
                    self.path = [] # Limpa o caminho se não encontrar alvo válido
                    return

            path = astar(self.game.grid, monstro_grid_pos, target_pos)
            
            if path:
                self.path = path
            else:
                self.path = []

    def seguir_caminho(self, dt):
        """Move o monstro em direção ao próximo ponto na lista self.path."""
        if not self.path:
            return

        next_node = self.path[0]
        target_pos = (next_node[0] * TILE_SIZE + TILE_SIZE / 2, 
                      next_node[1] * TILE_SIZE + TILE_SIZE / 2)

        direcao = pygame.Vector2(target_pos) - self.posicao

        if abs(direcao.x) > abs(direcao.y):
            self.state = 'right' if direcao.x > 0 else 'left'
        else:
            self.state = 'down' if direcao.y > 0 else 'up'
        self.image = self.frames[self.state][0]

        if direcao.length() < 10:
            self.path.pop(0)
        else:
            if direcao.length() > 0:
                direcao.normalize_ip()
            
            dx = direcao.x * self.velocidade * dt
            dy = direcao.y * self.velocidade * dt
            
            self.mover_com_colisao(dx, dy)

    def update(self, dt, jogador):
        self.recalcular_caminho(jogador)

        # Se existe um caminho inteligente, siga-o
        if self.path:
            self.seguir_caminho(dt)
        # Se não existe caminho siga reto
        else:
            self.seguir_jogador_direto(jogador.rect.center, dt)

    def aumentar_vida(self, wave):
        if wave % 2 == 0:
            self.vida += 1

    def get_vida(self):
        return self.vida

    def mover_com_colisao(self, dx, dy):
        paredes = [
            pygame.Rect(0, 0, 4, 600),
            pygame.Rect(796, 0, 4, 600),
            pygame.Rect(0, 0, 800, 4),
            pygame.Rect(0, 595, 800, 4),
        ]

        # Eixo X
        self.posicao.x += dx
        self.rect.centerx = round(self.posicao.x)
        collided_sprites = pygame.sprite.spritecollide(self, self.collision_sprites, False)
        bloqueadores_x = [obst for obst in collided_sprites if obst.rect not in paredes]
        if bloqueadores_x:
            self.posicao.x -= dx
            self.rect.centerx = round(self.posicao.x)

        # Eixo Y
        self.posicao.y += dy
        self.rect.centery = round(self.posicao.y)
        collided_sprites = pygame.sprite.spritecollide(self, self.collision_sprites, False)
        bloqueadores_y = [obst for obst in collided_sprites if obst.rect not in paredes]
        if bloqueadores_y:
            self.posicao.y -= dy
            self.rect.centery = round(self.posicao.y)


class Monstro(MonstroBase):
    def __init__(self, posicao_inicial, velocidade, collision_sprites, game_instance):
        data = game_data.ENEMY_DATA['monstro']
        paths = data['sprite_paths']
        frames = {
            'left':  [pygame.transform.scale(pygame.image.load(paths['left']).convert_alpha(), (50, 50))],
            'right': [pygame.transform.scale(pygame.image.load(paths['right']).convert_alpha(), (50, 50))],
            'up':    [pygame.transform.scale(pygame.image.load(paths['up']).convert_alpha(), (50, 50))],
            'down':  [pygame.transform.scale(pygame.image.load(paths['down']).convert_alpha(), (50, 50))]
        }
        super().__init__(posicao_inicial, velocidade, collision_sprites, vida=data['health'], frames=frames, game_instance=game_instance)

class Robo(MonstroBase):
    def __init__(self, posicao_inicial, velocidade, collision_sprites, game_instance):
        data = game_data.ENEMY_DATA['robo']
        paths = data['sprite_paths']
        frames = {
            'left':  [pygame.transform.scale(pygame.image.load(paths['left']).convert_alpha(), (50, 50))],
            'right': [pygame.transform.scale(pygame.image.load(paths['right']).convert_alpha(), (50, 50))],
            'up':    [pygame.transform.scale(pygame.image.load(paths['up']).convert_alpha(), (50, 50))],
            'down':  [pygame.transform.scale(pygame.image.load(paths['down']).convert_alpha(), (50, 50))]
        }
        super().__init__(posicao_inicial, velocidade, collision_sprites, vida=data['health'], frames=frames, game_instance=game_instance)
