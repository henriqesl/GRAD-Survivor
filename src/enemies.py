from settings import *

BASE_IMG_PATH = os.path.join(os.path.dirname(__file__), '..', 'assets', 'images')

class Monstro(pygame.sprite.Sprite):
    def __init__(self, tipo, posicao_inicial, velocidade, collision_sprites):
        super().__init__()
        self.tipo = tipo

        if tipo == 'monstro':
            caminho_imagem = os.path.join(BASE_IMG_PATH, 'monstro_sprite.png')
            self.vida = 1
        else:
            caminho_imagem = os.path.join(BASE_IMG_PATH, 'sprite_1_resized.png')
            self.vida = 2

        imagem_original = pygame.image.load(caminho_imagem).convert_alpha()
        self.image = pygame.transform.scale(imagem_original, (50, 50))
        self.rect = self.image.get_rect(center=posicao_inicial)
        self.velocidade = velocidade
    
        self.posicao = pygame.Vector2(self.rect.center)
        self.collision_sprites = collision_sprites

    def seguir_jogador(self, pos_jogador, dt):
        direcao = pygame.Vector2(pos_jogador) - self.posicao
        
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
            # Lista dos retângulos das paredes que o monstro deve ignorar
        paredes = [
            pygame.Rect(0, 0, 4, 600),
            pygame.Rect(796, 0, 4, 600),
            pygame.Rect(0, 0, 800, 4),
            pygame.Rect(0, 595, 800, 4),
        ]

        # Move no eixo X
        self.posicao.x += dx
        self.rect.centerx = round(self.posicao.x)

        collided_sprites = pygame.sprite.spritecollide(self, self.collision_sprites, False)
        bloqueadores_x = [obst for obst in collided_sprites if obst.rect not in paredes]

        if bloqueadores_x:
            self.posicao.x -= dx
            self.rect.centerx = round(self.posicao.x)

        # Move no eixo Y
        self.posicao.y += dy
        self.rect.centery = round(self.posicao.y)

        collided_sprites = pygame.sprite.spritecollide(self, self.collision_sprites, False)
        bloqueadores_y = [obst for obst in collided_sprites if obst.rect not in paredes]

        if bloqueadores_y:
            self.posicao.y -= dy
            self.rect.centery = round(self.posicao.y)
