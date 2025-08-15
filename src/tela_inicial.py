from .settings import *
import pygame

class TelaInicial:
    def __init__(self, screen):
        self.screen = screen

        # Imagem de fundo da tela inicial
        self.fundo_inicial = pygame.image.load("assets/images/tela_inicial.png").convert()
        self.fundo_inicial = pygame.transform.scale(self.fundo_inicial, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Carregar a imagem de fundo para a cutscene 
        self.fundo_cutscene = pygame.image.load("assets/images/inicio_grad.png").convert() 
        self.fundo_cutscene = pygame.transform.scale(self.fundo_cutscene, (WINDOW_WIDTH, WINDOW_HEIGHT))
        
        # Imagem do personagem para a cutscene
        self.personagem_img = pygame.image.load("assets/images/personagem_cutscene.png").convert_alpha()
    
        # Caixa de diálogo
        altura_caixa = 110
        grossura_borda = 3
        cor_fundo = (0, 0, 0)
        cor_borda = (255, 255, 255)

        self.caixa_dialogo = pygame.Surface((WINDOW_WIDTH - 40, altura_caixa))
        self.caixa_dialogo.set_alpha(220) # Um pouco mais opaco para melhor leitura

        # Desenha a borda (retângulo maior)
        pygame.draw.rect(self.caixa_dialogo, cor_borda, self.caixa_dialogo.get_rect())
        
        # Desenha o fundo (retângulo menor, dentro da borda)
        fundo_rect = self.caixa_dialogo.get_rect().inflate(-grossura_borda * 2, -grossura_borda * 2)
        pygame.draw.rect(self.caixa_dialogo, cor_fundo, fundo_rect)

        # Lista de falas da cutscene
        self.cutscene_falas = [
            "Preciso terminar esse projeto de IP o quanto antes cara...",
            "Vou acabar tendo que virar a noite no GRAD pra concluir",
            "",  # Pausa para tela apagar
            "M-Mas que barulheira é essa? quem pode ser em plena madrugada?"
        ]
        self.fala_index = 0
        self.texto_atual = ""
        self.tempo_ultima_letra = 0
        self.velocidade_digito = 50  # ms por letra
        self.cutscene_ativa = False
        self.tempo_pausa = 0
        self.tela_apagada = False

    def iniciar_cutscene(self):
        self.cutscene_ativa = True
        self.fala_index = 0
        self.texto_atual = ""
        self.tempo_ultima_letra = pygame.time.get_ticks()

    def update_tela_inicial(self):
        """Desenha a tela inicial (GRAD SURVIVAL)"""
        self.screen.blit(self.fundo_inicial, (0, 0))

    def update_cutscene(self):
        """Controla e desenha a cutscene"""
        agora = pygame.time.get_ticks()

        # Cena de tela apagada (apenas fundo preto)
        if self.fala_index == 2 and not self.tela_apagada:
            self.tela_apagada = True
            self.tempo_pausa = agora

        if self.tela_apagada:
            self.screen.fill((0, 0, 0))
            # Espera 3 segundos e vai para próxima fala
            if agora - self.tempo_pausa > 3000:
                self.tela_apagada = False
                self.fala_index += 1
                self.texto_atual = ""
                self.tempo_ultima_letra = agora
            return

        # Fundo da cutscene
        self.screen.blit(self.fundo_cutscene, (0, 0))
        
        pos_personagem_y = WINDOW_HEIGHT - self.personagem_img.get_height()
        self.screen.blit(self.personagem_img, (40, pos_personagem_y))

        pos_caixa_y = WINDOW_HEIGHT - 130 
        self.screen.blit(self.caixa_dialogo, (20, pos_caixa_y))

        # Efeito de digitação
        if self.fala_index < len(self.cutscene_falas):
            fala = self.cutscene_falas[self.fala_index]
            if len(self.texto_atual) < len(fala) and agora - self.tempo_ultima_letra > self.velocidade_digito:
                self.texto_atual += fala[len(self.texto_atual)]
                self.tempo_ultima_letra = agora

            font = pygame.font.Font(None, 32)
            texto_surface = font.render(self.texto_atual, True, (255, 255, 255))
            # --- Lógica de alinhamento do texto ---
            caixa_rect_na_tela = self.caixa_dialogo.get_rect(topleft=(20, pos_caixa_y))
            texto_rect = texto_surface.get_rect()
            texto_rect.centery = caixa_rect_na_tela.centery
            texto_rect.centerx = caixa_rect_na_tela.centerx

            self.screen.blit(texto_surface, texto_rect)
        else:
            self.cutscene_ativa = False

    def avancar_fala(self):
        """Avança para a próxima fala"""
        if self.fala_index < len(self.cutscene_falas) - 1:
            self.fala_index += 1
            self.texto_atual = ""
            self.tempo_ultima_letra = pygame.time.get_ticks()
        else:
            self.cutscene_ativa = False
            return True  # Indica que terminou
        return False
