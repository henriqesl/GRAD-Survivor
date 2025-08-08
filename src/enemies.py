import pygame
import random

# Classe Monstro
class Monstro(pygame.sprite.Sprite):
    def __init__(self, tipo, posicao_inicial, velocidade_monstro, velocidade_robot):
        super().__init__()
        self.tipo = tipo

        if tipo == 'monstro':
            imagem_monstro_original = pygame.image.load('assets/images/monstro_sprite.png').convert_alpha()
            self.image = pygame.transform.scale(imagem_monstro_original, (40, 40))
            self.vida = 1
            self.rect = self.image.get_rect(center=posicao_inicial)
            self.velocidade = velocidade_monstro

        else:  # robot
            imagem_robot_original = pygame.image.load('assets/images/sprite_1_resized.png').convert_alpha()
            self.image = pygame.transform.scale(imagem_robot_original, (40, 40))
            self.vida = 2
            self.rect = self.image.get_rect(center=posicao_inicial)
            self.velocidade = velocidade_robot

    def seguir_jogador(self, pos_jogador):
        distancia_x = pos_jogador[0] - self.rect.centerx
        distancia_y = pos_jogador[1] - self.rect.centery

        if abs(distancia_x) > abs(distancia_y):
            self.rect.x += self.velocidade if distancia_x > 0 else -self.velocidade
        else:
            self.rect.y += self.velocidade if distancia_y > 0 else -self.velocidade

    def update(self):
        self.seguir_jogador(retangulo_jogador.center)

    def aumentar_vida(self, wave):
        if wave % 2 == 0:
            self.vida += 1

    def get_vida(self):
        return self.vida
    
pygame.init()
largura_tela, altura_tela = 800, 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
clock = pygame.time.Clock()

imagem_jogador_original = pygame.image.load('assets/images/sprite_1_resized.png').convert_alpha()
imagem_jogador = pygame.transform.scale(imagem_jogador_original, (50, 50))
retangulo_jogador = imagem_jogador.get_rect(center=(400, 300))

imagem_mapa = pygame.image.load('assets/images/mapa1.0.png')

pontos_de_spawn = [(20, 80), (20, 520), (780, 520), (780, 80)]
EVENTO_SPAWN_MONSTRO = pygame.USEREVENT + 1
pygame.time.set_timer(EVENTO_SPAWN_MONSTRO, 2000)

grupo_monstro = pygame.sprite.Group()

velocidade_monstro = 1.3
velocidade_robot = 1.7
wave = 1
jogo_ativo = True

# Loop principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()

        if evento.type == EVENTO_SPAWN_MONSTRO and jogo_ativo:

            if wave >= 3:
                tipo_monstro = random.choice(['monstro', 'robot'])
            else:
                tipo_monstro = 'monstro'
                
            ponto_spawn = random.choice(pontos_de_spawn)
            monstro = Monstro(tipo_monstro, ponto_spawn, velocidade_monstro, velocidade_robot)
            monstro.aumentar_vida(wave)
            grupo_monstro.add(monstro)

        if not jogo_ativo and evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                jogo_ativo = True
                retangulo_jogador.center = (400, 300)
                grupo_monstro.empty()
                wave = 1
                velocidade_monstro = 1.3

    if jogo_ativo:
        # Atualiza a wave e dificuldade
        if len(grupo_monstro) >= 10 * wave:
            velocidade_monstro += 0.7
            wave += 1

        # Verifica colisões
        for monstro in grupo_monstro:
            if monstro.rect.colliderect(retangulo_jogador):
                jogo_ativo = False
                break

        # Movimento do jogador
        teclas_pressionadas = pygame.key.get_pressed()
        if teclas_pressionadas[pygame.K_w]:
            retangulo_jogador.top -= 2.5
        if teclas_pressionadas[pygame.K_s]:
            retangulo_jogador.top += 2.5
        if teclas_pressionadas[pygame.K_a]:
            retangulo_jogador.left -= 2.5
        if teclas_pressionadas[pygame.K_d]:
            retangulo_jogador.left += 2.5

        # Desenha o jogo
        tela.blit(imagem_mapa, (0, 0))
        tela.blit(imagem_jogador, retangulo_jogador)

        grupo_monstro.update()
        grupo_monstro.draw(tela)

        pygame.display.update()
        clock.tick(60)

    else:
        # Tela de game over (pode customizar)
        tela.fill((0, 0, 0))
        fonte = pygame.font.SysFont(None, 48)
        texto = fonte.render("Game Over! Pressione ESPAÇO para reiniciar.", True, (255, 255, 255))
        tela.blit(texto, (80, 300))
        pygame.display.update()
