from .settings import *

BASE_IMG_PATH = os.path.join(os.path.dirname(__file__), '..', 'assets', 'images')

class MonstroBase(pygame.sprite.Sprite):
    def __init__(self, posicao_inicial, velocidade, collision_sprites, vida, frames):
        super().__init__()
        self.vida = vida
        self.frames = frames
        self.state = 'down'
        self.image = self.frames[self.state][0]

        self.rect = self.image.get_rect(center=posicao_inicial)
        self.velocidade = velocidade
        self.posicao = pygame.Vector2(self.rect.center)
        self.collision_sprites = collision_sprites

    def seguir_jogador(self, pos_jogador, dt):
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

    def update(self, dt, jogador):
        self.seguir_jogador(jogador.rect.center, dt)

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
    def __init__(self, posicao_inicial, velocidade, collision_sprites):
        frames = {
            'left':  [pygame.transform.scale(pygame.image.load(os.path.join(BASE_IMG_PATH, 'monstro sprite_esquerda.png')).convert_alpha(), (50, 50))],
            'right': [pygame.transform.scale(pygame.image.load(os.path.join(BASE_IMG_PATH, 'monstro_sprite_direita.png')).convert_alpha(), (50, 50))],
            'up':    [pygame.transform.scale(pygame.image.load(os.path.join(BASE_IMG_PATH, 'monstro_sprite_costas.png')).convert_alpha(), (50, 50))],
            'down':  [pygame.transform.scale(pygame.image.load(os.path.join(BASE_IMG_PATH, 'monstro_sprite.png')).convert_alpha(), (50, 50))]
        }
        super().__init__(posicao_inicial, velocidade, collision_sprites, vida=1, frames=frames)


class Robo(MonstroBase):
    def __init__(self, posicao_inicial, velocidade, collision_sprites):
        frames = {
            'left':  [pygame.transform.scale(pygame.image.load(os.path.join(BASE_IMG_PATH, 'robo_esquerda_sprite.png')).convert_alpha(), (50, 50))],
            'right': [pygame.transform.scale(pygame.image.load(os.path.join(BASE_IMG_PATH, 'robo_direita_sprite.png')).convert_alpha(), (50, 50))],
            'up':    [pygame.transform.scale(pygame.image.load(os.path.join(BASE_IMG_PATH, 'robo_costas_sprite.png')).convert_alpha(), (50, 50))],
            'down':  [pygame.transform.scale(pygame.image.load(os.path.join(BASE_IMG_PATH, 'robo_frente_sprite.png')).convert_alpha(), (50, 50))]
        }
        super().__init__(posicao_inicial, velocidade, collision_sprites, vida=2, frames=frames)
