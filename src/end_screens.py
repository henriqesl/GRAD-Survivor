import pygame
import math
import random
from .settings import WINDOW_WIDTH, WINDOW_HEIGHT, HUD_HEIGHT


def clamp_color(value):
    """Garante que o valor de cor está entre 0 e 255 como inteiro."""
    return max(0, min(255, int(value)))


def safe_color(r, g, b):
    """Retorna uma tupla de cor segura (R, G, B) com inteiros válidos."""
    return (clamp_color(r), clamp_color(g), clamp_color(b))


class EndGameReportMixin:
    def draw_end_game_report(self, screen, itens_coletados, inimigos_eliminados, y_start):
        font_titulo = pygame.font.Font(None, 32)
        font_item = pygame.font.Font(None, 28)
        cor_texto = (255, 255, 255)
        y_offset = y_start

        inimigos_texto = font_titulo.render(f"Inimigos Eliminados: {inimigos_eliminados}", True, cor_texto)
        inimigos_rect = inimigos_texto.get_rect(center=(WINDOW_WIDTH / 2, y_offset))
        screen.blit(inimigos_texto, inimigos_rect)
        y_offset += 20

        texto_relatorio = font_titulo.render("Itens Coletados:", True, cor_texto)
        rect_relatorio = texto_relatorio.get_rect(center=(WINDOW_WIDTH / 2, y_offset))
        screen.blit(texto_relatorio, rect_relatorio)
        y_offset += 20

        for item, quantidade in itens_coletados.items():
            nome_item_formatado = item.capitalize()
            texto_item = font_item.render(f"{nome_item_formatado}: {quantidade}", True, cor_texto)
            rect_item = texto_item.get_rect(center=(WINDOW_WIDTH / 2, y_offset))
            screen.blit(texto_item, rect_item)
            y_offset += 20


class WinScreen(EndGameReportMixin):
    def __init__(self, screen, itens_coletados, inimigos_eliminados):
        self.screen = screen
        self.itens_coletados = itens_coletados
        self.inimigos_eliminados = inimigos_eliminados

        self.BRIGHT_GREEN = (50, 255, 50)
        self.GOLD = (255, 215, 0)
        self.MONITOR_BORDER = (26, 26, 42)
        self.WHITE = (255, 255, 255)

        try:
            self.font_large = pygame.font.Font("assets/fonts/pixel.ttf", 48)
            self.font_medium = pygame.font.Font("assets/fonts/pixel.ttf", 16)
            self.font_small = pygame.font.Font("assets/fonts/pixel.ttf", 14)
        except:
            self.font_large = pygame.font.Font(None, 48)
            self.font_medium = pygame.font.Font(None, 20)
            self.font_small = pygame.font.Font(None, 16)

        self.win_time = 0

    def reset(self):
        self.win_time = 0

    def update(self, dt):
        self.win_time += 0.1

    def draw_text_with_glow(self, text, font, color, pos):
        for offset in range(2, 0, -1):
            glow_alpha = 40 * offset
            glow_surface = font.render(text, True, safe_color(*color))
            glow_surface.set_alpha(glow_alpha)
            for dx in range(-offset, offset + 1):
                for dy in range(-offset, offset + 1):
                    self.screen.blit(glow_surface, (pos[0] + dx, pos[1] + dy))
        main_surface = font.render(text, True, safe_color(*color))
        self.screen.blit(main_surface, pos)

    def draw_win_monitor_border(self):
        pygame.draw.rect(self.screen, self.MONITOR_BORDER, (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.draw.rect(self.screen, (20, 80, 20), (20, 20, WINDOW_WIDTH-40, WINDOW_HEIGHT-70))
        led_alpha = int(127 + 127 * math.sin(self.win_time * 3))
        led_color = safe_color(led_alpha//4, 255, led_alpha//4)
        pygame.draw.circle(self.screen, led_color, (WINDOW_WIDTH - 40, WINDOW_HEIGHT - 35), 8)
        pygame.draw.circle(self.screen, self.BRIGHT_GREEN, (WINDOW_WIDTH - 40, WINDOW_HEIGHT - 35), 8, 2)

    def draw_win_scanlines(self):
        for y in range(0, WINDOW_HEIGHT, 6):
            alpha = 15 + int(10 * math.sin(self.win_time + y * 0.1))
            if alpha > 0:
                line_surface = pygame.Surface((WINDOW_WIDTH, 2))
                line_surface.set_alpha(alpha)
                line_surface.fill(self.BRIGHT_GREEN)
                scan_y = (y + self.win_time * 2) % WINDOW_HEIGHT
                self.screen.blit(line_surface, (0, scan_y))

    def draw_win_content(self):
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2
        pulse = math.sin(self.win_time * 4)
        brightness = int(200 + 55 * pulse)
        win_text = "YOU WIN!"
        self.draw_text_with_glow(win_text, self.font_large, (brightness, 255, brightness),
                                 (center_x - self.font_large.size(win_text)[0]//2, center_y - 100))
        congratulations_lines = [
            "VOCÊ DERROTOU TODAS AS HORDAS DE INIMIGOS",
            "COM AJUDA DOS SEUS SUBWAYS E RED BULLS!",
            "UM VERDADEIRO GRAD SURVIVOR!"
        ]
        for i, line in enumerate(congratulations_lines):
            line_surface = self.font_medium.render(line, True, (180, 255, 180))
            line_rect = line_surface.get_rect(center=(center_x, center_y + i * 25))
            self.screen.blit(line_surface, line_rect)
        blink_alpha = int(127 + 127 * math.sin(self.win_time * 5))
        instruction = "PRESSIONE ESPACO PARA JOGAR NOVAMENTE!"
        instruction_surface = self.font_small.render(instruction, True, self.GOLD)
        instruction_surface.set_alpha(blink_alpha)
        instruction_rect = instruction_surface.get_rect(center=(center_x, center_y + 100))
        self.screen.blit(instruction_surface, instruction_rect)

    def draw(self):
        for y in range(WINDOW_HEIGHT):
            shade = clamp_color(20 + 10 * math.sin(y * 0.01))
            pygame.draw.line(self.screen, safe_color(0, shade, 0), (0, y), (WINDOW_WIDTH, y))
        self.draw_win_monitor_border()
        self.draw_win_scanlines()
        self.draw_win_content()
        self.draw_end_game_report(self.screen, self.itens_coletados, self.inimigos_eliminados, WINDOW_HEIGHT / 2 + 180)


class GameOverScreen(EndGameReportMixin):
    def __init__(self, screen, itens_coletados, inimigos_eliminados):
        self.screen = screen
        self.itens_coletados = itens_coletados
        self.inimigos_eliminados = inimigos_eliminados

        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.MONITOR_BORDER = (26, 26, 42)
        self.CYAN = (0, 255, 255)
        self.GREEN = (0, 255, 65)

        try:
            self.font_large = pygame.font.Font("assets/fonts/pixel.ttf", 48)
            self.font_medium = pygame.font.Font("assets/fonts/pixel.ttf", 16)
            self.font_small = pygame.font.Font("assets/fonts/pixel.ttf", 14)
        except:
            self.font_large = pygame.font.Font(None, 48)
            self.font_medium = pygame.font.Font(None, 20)
            self.font_small = pygame.font.Font(None, 16)

        self.static_particles = []
        self.crack_lines = []
        self.scanline_offset = 0
        self.game_over_time = 0
        self.init_static_particles()
        self.init_crack_lines()

    def reset(self):
        self.game_over_time = 0

    def init_static_particles(self):
        for _ in range(150):
            x = random.randint(30, WINDOW_WIDTH - 30)
            y = random.randint(30, WINDOW_HEIGHT - 30)
            self.static_particles.append([x, y, random.randint(1, 3)])

    def init_crack_lines(self):
        self.crack_lines.append({
            'start': (100, 150),
            'end': (400, 350),
            'branches': [((200, 200), (180, 250)), ((300, 300), (350, 280)), ((350, 320), (380, 370))]
        })
        self.crack_lines.append({
            'start': (600, 100),
            'end': (580, 400),
            'branches': [((590, 200), (620, 180)), ((585, 300), (560, 320))]
        })

    def draw_monitor_border(self):
        pygame.draw.rect(self.screen, self.MONITOR_BORDER, (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.draw.rect(self.screen, self.BLACK, (20, 20, WINDOW_WIDTH-40, WINDOW_HEIGHT-70))
        led_alpha = int(127 + 127 * math.sin(self.game_over_time * 3))
        led_color = safe_color(255, led_alpha//4, led_alpha//4)
        pygame.draw.circle(self.screen, led_color, (WINDOW_WIDTH - 40, WINDOW_HEIGHT - 35), 8)
        pygame.draw.circle(self.screen, self.RED, (WINDOW_WIDTH - 40, WINDOW_HEIGHT - 35), 8, 2)

    def draw_static(self):
        for particle in self.static_particles:
            if random.random() < 0.6:
                intensity = random.randint(50, 200)
                color = safe_color(intensity, intensity, intensity)
                pygame.draw.rect(self.screen, color, (particle[0], particle[1], particle[2], particle[2]))
            particle[0] += random.randint(-1, 1)
            particle[1] += random.randint(-1, 1)

    def draw_scanlines(self):
        for y in range(0, WINDOW_HEIGHT, 4):
            alpha = 20 + int(15 * math.sin(self.game_over_time + y * 0.1))
            if alpha > 0:
                line_surface = pygame.Surface((WINDOW_WIDTH, 2))
                line_surface.set_alpha(alpha)
                line_surface.fill(self.GREEN)
                scan_y = (y + self.scanline_offset) % WINDOW_HEIGHT
                self.screen.blit(line_surface, (0, scan_y))
        self.scanline_offset = (self.scanline_offset + 0.5) % 4

    def draw_crack_overlay(self):
        for crack in self.crack_lines:
            pygame.draw.line(self.screen, safe_color(200, 200, 200), crack['start'], crack['end'], 3)
            for branch in crack['branches']:
                pygame.draw.line(self.screen, safe_color(150, 150, 150), branch[0], branch[1], 2)

    def draw_game_over_content(self):
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2
        flicker = int(200 + 55 * math.sin(self.game_over_time * 8))
        game_over_color = safe_color(255, flicker//4, flicker//4)
        game_over_text = "GAME OVER"
        self.draw_text_with_glow(game_over_text, self.font_large, game_over_color,
                                 (center_x - self.font_large.size(game_over_text)[0]//2, center_y - 80))
        message_lines = ["REPENSE ANTES DE PASSAR UMA MADRUGADA", "NO GRAD..."]
        for i, line in enumerate(message_lines):
            line_surface = self.font_medium.render(line, True, self.RED)
            line_rect = line_surface.get_rect(center=(center_x, center_y + i * 25))
            self.screen.blit(line_surface, line_rect)
        blink_alpha = int(127 + 127 * math.sin(self.game_over_time * 4))
        instruction = "PRESSIONE ESPACO PARA TENTAR NOVAMENTE"
        instruction_surface = self.font_small.render(instruction, True, self.YELLOW)
        instruction_surface.set_alpha(blink_alpha)
        instruction_rect = instruction_surface.get_rect(center=(center_x, center_y + 80))
        self.screen.blit(instruction_surface, instruction_rect)

    def draw_text_with_glow(self, text, font, color, pos):
        for offset in range(2, 0, -1):
            glow_alpha = 40 * offset
            glow_surface = font.render(text, True, safe_color(*color))
            glow_surface.set_alpha(glow_alpha)
            for dx in range(-offset, offset + 1):
                for dy in range(-offset, offset + 1):
                    self.screen.blit(glow_surface, (pos[0] + dx, pos[1] + dy))
        main_surface = font.render(text, True, safe_color(*color))
        self.screen.blit(main_surface, pos)

    def update(self, dt):
        self.game_over_time += dt * 4

    def draw(self):
        for y in range(WINDOW_HEIGHT):
            shade = clamp_color(10 + 15 * math.sin(y * 0.01))
            color = safe_color(shade, shade, shade + 10)
            pygame.draw.line(self.screen, color, (0, y), (WINDOW_WIDTH, y))
        self.draw_monitor_border()
        self.draw_static()
        self.draw_scanlines()
        self.draw_crack_overlay()
        self.draw_game_over_content()
        self.draw_end_game_report(self.screen, self.itens_coletados, self.inimigos_eliminados, WINDOW_HEIGHT / 2 + 180)
