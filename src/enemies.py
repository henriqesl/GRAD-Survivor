from settings import *

BASE_IMG_PATH = os.path.join(os.path.dirname(__file__), '..', 'assets', 'images')

class Monstro(pygame.sprite.Sprite):
    def __init__(self, tipo, posicao_inicial, velocidade):
        super().__init__()
        self.tipo = tipo

        if tipo == 'monstro':
            caminho_imagem = os.path.join(BASE_IMG_PATH, 'monstro_sprite.png')
            self.vida = 1
        else:
            caminho_imagem = os.path.join(BASE_IMG_PATH, 'sprite_1_resized.png')
            self.vida = 2

        imagem_original = pygame.image.load(caminho_imagem).convert_alpha()
        self.image = pygame.transform.scale(imagem_original, (60, 60))
        self.rect = self.image.get_rect(center=posicao_inicial)
        self.velocidade = velocidade
    
        self.posicao = pygame.Vector2(self.rect.center)

    def seguir_jogador(self, pos_jogador, dt):
        direcao = pygame.Vector2(pos_jogador) - self.posicao
        
        if direcao.length() > 0:  
            direcao.normalize_ip() 

        self.posicao += direcao * self.velocidade * dt
        self.rect.center = round(self.posicao.x), round(self.posicao.y)

    def update(self, dt, jogador):
        self.seguir_jogador(jogador.rect.center, dt)

    def aumentar_vida(self, wave):
        if wave % 2 == 0:
            self.vida += 1

    def get_vida(self):
        return self.vida
    
