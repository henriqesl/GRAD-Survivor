import pygame
import random

class Monstro:
    def __init__(self, posicao_inicial, velocidade):
        imagem_monstro_original = pygame.image.load('sprite_1_resized.png').convert_alpha()
        self.imagem_monstro = pygame.transform.scale(imagem_monstro_original, (40, 40))
        self.vida = 1
        self.retangulo = self.imagem_monstro.get_rect(center=posicao_inicial)
        self.velocidade = velocidade

    def desenhar(self, tela):
        tela.blit(self.imagem_monstro, self.retangulo)

    def seguir_jogador(self, pos_jogador):
        distancia_x = pos_jogador[0] - self.retangulo.centerx
        distancia_y = pos_jogador[1] - self.retangulo.centery

        if abs(distancia_x) > abs(distancia_y):
            if distancia_x > 0:
                self.retangulo.x += self.velocidade
            else:
                self.retangulo.x -= self.velocidade
        else:
            if distancia_y > 0:
                self.retangulo.y += self.velocidade
            else:
                self.retangulo.y -= self.velocidade

    def aumentar_vida(self, wave):
        if wave % 2 == 0:
            self.vida += 1

    def get_vida(self):
        print(self.vida)

    def colisao(self, retangulo_jogador):
        return self.retangulo.colliderect(retangulo_jogador)



pygame.init()
largura_tela, altura_tela = 800, 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
clock = pygame.time.Clock()

imagem_jogador_original = pygame.image.load('sprite_1_resized.png').convert_alpha()
imagem_jogador = pygame.transform.scale(imagem_jogador_original, (50, 50))
retangulo_jogador = imagem_jogador.get_rect(center=(400, 300))

imagem_mapa = pygame.image.load('mapa1.0.png')

monstros = []

pontos_de_spawn = [(20, 80), (20, 520), (780, 520), (780, 80)]

EVENTO_SPAWN_MONSTRO = pygame.USEREVENT + 1
pygame.time.set_timer(EVENTO_SPAWN_MONSTRO, 2000)

velocidade_geral = 1.3
wave = 1
jogo_ativo = True

# Loop principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()

        if evento.type == EVENTO_SPAWN_MONSTRO:
            ponto_spawn = random.choice(pontos_de_spawn)
            monstro_atual = Monstro(ponto_spawn, velocidade_geral)
            monstro_atual.aumentar_vida(wave)
            monstro_atual.get_vida()
            monstros.append(monstro_atual)


        if evento.type == pygame.KEYDOWN and not jogo_ativo:
            if evento.key == pygame.K_SPACE:
                retangulo_jogador
                jogo_ativo = True

    if jogo_ativo:
        if len(monstros) >= 10 * wave:
            velocidade_geral += 1.3
            wave += 1

        for monstro in monstros:
            if monstro.colisao(retangulo_jogador):
                jogo_ativo = False
                monstros.clear()
                

        teclas_pressionadas = pygame.key.get_pressed()
        if teclas_pressionadas[pygame.K_w]:
            retangulo_jogador.top -= 2.5
        elif teclas_pressionadas[pygame.K_s]:
            retangulo_jogador.top += 2.5
        elif teclas_pressionadas[pygame.K_a]:
            retangulo_jogador.left -= 2.5
        elif teclas_pressionadas[pygame.K_d]:
            retangulo_jogador.left += 2.5

        # Desenha o fundo e o jogador
        tela.blit(imagem_mapa, (0, 0))
        tela.blit(imagem_jogador, retangulo_jogador)

        # Atualiza e desenha cada monstro para seguir o jogador
        for monstro in monstros:
            monstro.seguir_jogador(retangulo_jogador.center)
            monstro.desenhar(tela)

        pygame.display.update()
        clock.tick(60)


    else:
        retangulo_jogador.center = (400, 300)
