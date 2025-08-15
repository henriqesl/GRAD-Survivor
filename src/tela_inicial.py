from .settings import *
import pygame
import math
import random
import time

class TelaInicial:
    def __init__(self, screen):
        self.screen = screen

        # Imagem de fundo da tela inicial (mantida para fallback)
        self.fundo_inicial = pygame.image.load("assets/images/tela_inicial.png").convert()
        self.fundo_inicial = pygame.transform.scale(self.fundo_inicial, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Carregar a imagem de fundo para a cutscene 
        self.fundo_cutscene = pygame.image.load("assets/images/inicio_grad.png").convert() 
        self.fundo_cutscene = pygame.transform.scale(self.fundo_cutscene, (WINDOW_WIDTH, WINDOW_HEIGHT))
        
        self.novo_fundo = pygame.image.load("assets/images/inicio_grad.png").convert() 
        self.novo_fundo = pygame.transform.scale(self.novo_fundo, (WINDOW_WIDTH, WINDOW_HEIGHT))

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
            "Preciso terminar esse projeto de IP o quanto antes...",
            "Vou acabar virando a noite no GRAD pra concluir isso logo.",
            "",  # Pausa para tela apagar
            "M-Mas que barulheira é essa? Em plena madrugada, o que será?"
        ]
        self.fala_index = 0
        self.texto_atual = ""
        self.tempo_ultima_letra = 0
        self.velocidade_digito = 50  # ms por letra
        self.cutscene_ativa = False
        self.tempo_pausa = 0
        self.tela_apagada = False

        # === NOVOS ELEMENTOS PARA TELA INICIAL MODERNA ===
        # Cores baseadas nas suas telas de fim
        self.GREEN = (0, 255, 0)
        self.DARK_GREEN = (0, 100, 0)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        
        # Partículas para efeito de fundo
        self.particles = []
        for _ in range(15):
            self.particles.append({
                'x': random.randint(0, WINDOW_WIDTH),
                'y': random.randint(0, WINDOW_HEIGHT),
                'speed': random.uniform(0.3, 1.5),
                'brightness': random.randint(80, 200)
            })
        
        # Linhas de glitch para efeito visual
        self.glitch_lines = []
        
        # Tempo de início para efeitos
        self.start_time = time.time()

    def iniciar_cutscene(self):
        self.cutscene_ativa = True
        self.fala_index = 0
        self.texto_atual = ""
        self.tempo_ultima_letra = pygame.time.get_ticks()

    def create_glitch_effect(self):
        """Cria efeito de glitch nas bordas"""
        # Atualizar linhas de glitch
        if random.random() < 0.08:  # 8% chance de nova linha
            self.glitch_lines.append({
                'y': random.randint(0, WINDOW_HEIGHT),
                'width': random.randint(30, 150),
                'life': 8,
                'offset': random.randint(-15, 15)
            })
        
        # Desenhar linhas de glitch
        for line in self.glitch_lines[:]:
            if line['life'] > 0:
                color = self.GREEN if random.random() > 0.3 else self.WHITE
                pygame.draw.rect(self.screen, color, 
                               (line['offset'], line['y'], line['width'], 1))
                line['life'] -= 1
            else:
                self.glitch_lines.remove(line)

    def update_particles(self):
        """Atualiza partículas de fundo"""
        for particle in self.particles:
            particle['y'] += particle['speed']
            if particle['y'] > WINDOW_HEIGHT:
                particle['y'] = -10
                particle['x'] = random.randint(0, WINDOW_WIDTH)
            
            # Pequeno movimento horizontal
            particle['x'] += random.uniform(-0.3, 0.3)
            particle['x'] = max(0, min(WINDOW_WIDTH, particle['x']))

    def draw_particles(self):
        """Desenha partículas de fundo"""
        for particle in self.particles:
            alpha_factor = 0.4 + 0.3 * math.sin(time.time() * 2 + particle['x'] * 0.01)
            alpha = int(particle['brightness'] * alpha_factor)
            
            # Criar surface temporária para alpha
            temp_surf = pygame.Surface((2, 2))
            temp_surf.set_alpha(alpha)
            temp_surf.fill(self.GREEN)
            
            self.screen.blit(temp_surf, (int(particle['x']), int(particle['y'])))

    def draw_scanlines(self):
        """Desenha linhas de varredura para efeito retrô"""
        for y in range(0, WINDOW_HEIGHT, 3):
            alpha = 20
            line_surf = pygame.Surface((WINDOW_WIDTH, 1))
            line_surf.set_alpha(alpha)
            line_surf.fill((0, 50, 0))
            self.screen.blit(line_surf, (0, y))

    def update_tela_inicial(self):
        """Desenha a tela inicial moderna no estilo das telas de fim"""
        # Fundo escuro
        self.screen.fill(self.BLACK)
        
        # Efeitos visuais de fundo
        self.update_particles()
        self.draw_particles()
        self.create_glitch_effect()
        self.draw_scanlines()
        
        # Tempo atual para animações
        current_time = time.time() - self.start_time
        
        # === TÍTULO PRINCIPAL ===
        # Efeito pulsante no título
        pulse = 1 + 0.15 * math.sin(current_time * 2.5)
        title_color = tuple(min(255, int(c * pulse)) for c in self.GREEN)
        
        # Fontes (usando as padrões do pygame)
        font_huge = pygame.font.Font(None, 120)
        font_large = pygame.font.Font(None, 80)
        font_medium = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 32)
        
        # GRAD
        grad_text = font_huge.render("GRAD", True, title_color)
        grad_rect = grad_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 100))
        
        # Pequeno efeito de tremulação no título principal
        shake_x = random.randint(-1, 1) if random.random() < 0.1 else 0
        shake_y = random.randint(-1, 1) if random.random() < 0.1 else 0
        grad_rect.x += shake_x
        grad_rect.y += shake_y
        
        self.screen.blit(grad_text, grad_rect)
        
        # SURVIVE
        survive_text = font_large.render("SURVIVE", True, title_color)
        survive_rect = survive_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 30))
        self.screen.blit(survive_text, survive_rect)
        
        # === SUBTÍTULO ===
        subtitle = "Sobreviva às hordas do GRAD"
        subtitle_color = tuple(int(c * 0.8) for c in self.WHITE)  # Um pouco mais escuro
        subtitle_text = font_medium.render(subtitle, True, subtitle_color)
        subtitle_rect = subtitle_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 30))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # === INSTRUÇÕES PISCANDO ===
        if int(current_time * 2) % 2:  # Piscar a cada 0.5 segundos
            instruction = "Pressione qualquer tecla para começar"
            instruction_text = font_small.render(instruction, True, self.GREEN)
            instruction_rect = instruction_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 100))
            self.screen.blit(instruction_text, instruction_rect)
        
        # === ELEMENTOS DECORATIVOS ===
        # Barras laterais com gradiente simulado
        bar_width = 20
        for i in range(bar_width):
            alpha = int(255 * (1 - i / bar_width) * 0.3)
            bar_surf = pygame.Surface((1, WINDOW_HEIGHT))
            bar_surf.set_alpha(alpha)
            bar_surf.fill(self.GREEN)
            
            # Barra esquerda
            self.screen.blit(bar_surf, (i, 0))
            # Barra direita
            self.screen.blit(bar_surf, (WINDOW_WIDTH - 1 - i, 0))
        
        # === INFORMAÇÕES EXTRAS (CANTO INFERIOR) ===
        # Versão
        version_text = font_small.render("v2.0.1", True, self.GRAY)
        self.screen.blit(version_text, (20, WINDOW_HEIGHT - 30))
        
        # Status (simulado)
        status_text = font_small.render("Sistema: ONLINE", True, self.GREEN)
        status_rect = status_text.get_rect()
        status_rect.bottomright = (WINDOW_WIDTH - 20, WINDOW_HEIGHT - 30)
        self.screen.blit(status_text, status_rect)
        
        # === EFEITO ADICIONAL: CURSOR PISCANDO ===
        if int(current_time * 3) % 2:  # Cursor piscando mais rápido
            cursor_y = WINDOW_HEIGHT//2 + 130
            pygame.draw.rect(self.screen, self.GREEN, (WINDOW_WIDTH//2 + 140, cursor_y, 2, 20))

    def update_cutscene(self):
        """Controla e desenha a cutscene"""
        agora = pygame.time.get_ticks()

        # Lógica para a pausa com a tela preta
        if self.fala_index == 2 and not self.tela_apagada:
            self.tela_apagada = True
            self.tempo_pausa = agora
        
        if self.tela_apagada:
            # Garante que a tela fique preta durante a pausa
            self.screen.fill((0, 0, 0))
            
            if agora - self.tempo_pausa > 3000:
                self.tela_apagada = False
                self.fala_index += 1
                self.texto_atual = ""
                self.tempo_ultima_letra = agora
            return

        # --- PARTE PRINCIPAL DO DESENHO ---
        # 1. Fundo da cena (agora condicional)
        if self.fala_index < 3:
            # Se estivermos antes da pausa (índice 0, 1)
            self.screen.blit(self.fundo_cutscene, (0, 0))
        else:
            # Se estivermos depois da pausa (índice 3 em diante)
            self.screen.blit(self.novo_fundo, (0, 0))

        # 2. Personagem
        pos_personagem_y = WINDOW_HEIGHT - self.personagem_img.get_height()
        self.screen.blit(self.personagem_img, (40, pos_personagem_y))

        # 3. Caixa de diálogo
        pos_caixa_y = WINDOW_HEIGHT - 130 
        self.screen.blit(self.caixa_dialogo, (20, pos_caixa_y))

        # 4. Texto
        if self.fala_index < len(self.cutscene_falas):
            fala = self.cutscene_falas[self.fala_index]
            if len(self.texto_atual) < len(fala) and agora - self.tempo_ultima_letra > self.velocidade_digito:
                self.texto_atual += fala[len(self.texto_atual)]
                self.tempo_ultima_letra = agora

            font = pygame.font.Font(None, 32)
            texto_surface = font.render(self.texto_atual, True, (255, 255, 255))
            
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