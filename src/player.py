import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, game_backup):
        super().__init__(groups)
        self.game = game_backup
        self.load_images()
        self.state, self.frame_index = 'down', 0 
        self.image = self.frames[self.state][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.hitbox_rect = self.rect.inflate(-30, 0) 
    
        self.direction = pygame.Vector2()
        self.speed = 220
        self.base_speed = 220
        self.collision_sprites = collision_sprites

        # --- LÓGICA DE VIDAS E INVENCIBILIDADE ---
        self.max_lives = 3
        self.lives = self.max_lives
        self.invincible = False
        self.invincibility_duration = 1500
        self.last_hit_time = 0

        # --- PODERES E TIMERS ---
        self.power_timers = {
            'speed': 0,
            'intangivel': 0
        }
        self.intangivel = False

    def take_damage(self):
        # --- Função de Levar Dano ---
        current_time = pygame.time.get_ticks()
        if not self.invincible and not self.intangivel:
            self.lives -= 1
            self.invincible = True
            self.last_hit_time = current_time
    
    def check_invincibility(self):
        """Verifica se o tempo de invencibilidade já passou."""
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_hit_time > self.invincibility_duration:
                self.invincible = False

    def reset(self):
        # --- Reiniciar partida ---
        self.lives = self.max_lives
        self.rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.direction = pygame.Vector2()
        self.invincible = False

    def load_images(self):
        # --- Carregar Sprites ---
        self.frames = {
            'left':  [pygame.image.load('assets/images/sprite_2_resized.png').convert_alpha()],
            'right': [pygame.image.load('assets/images/sprite_3_resized.png').convert_alpha()],
            'up':    [pygame.image.load('assets/images/sprite_4_resized.png').convert_alpha()],
            'down':  [pygame.image.load('assets/images/sprite_1_resized.png').convert_alpha()]
        }

        for key, frames_list in self.frames.items():
            for i in range(len(frames_list)):
                frames_list[i] = pygame.transform.scale(frames_list[i], (40, 50))

        self.frames_original = {
            state: [frame.copy() for frame in frames]
            for state, frames in self.frames.items()
        }

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction.length() > 0 else pygame.Vector2()

    def move(self, dt):
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal', self.collision_sprites)  
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical', self.collision_sprites)  
        self.rect.center = self.hitbox_rect.center

    def collision(self, direction, obstacles):
        for obstaculo in obstacles:
            if self.hitbox_rect.colliderect(obstaculo.rect):  
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.hitbox_rect.right = obstaculo.rect.left 
                    if self.direction.x < 0:
                        self.hitbox_rect.left = obstaculo.rect.right  
                if direction == 'vertical':
                    if self.direction.y > 0:
                        self.hitbox_rect.bottom = obstaculo.rect.top 
                    if self.direction.y < 0:
                        self.hitbox_rect.top = obstaculo.rect.bottom

        self.rect.topleft = self.hitbox_rect.topleft

    def animate(self, dt):
        # --- Define o estado (direção) ---
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'
        if self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'

        self.frame_index += 5 * dt if self.direction.length() > 0 else 0
        frames_list = self.frames[self.state]
        self.image = frames_list[int(self.frame_index) % len(frames_list)]

    def aplicar_transparencia_animacoes(self, alpha):
        for state, frames in self.frames_original.items():
            transparent_frames = []
            for frame in frames:
                frame_copy = frame.copy()
                frame_copy.set_alpha(alpha)
                transparent_frames.append(frame_copy)
            self.frames[state] = transparent_frames

    def handle_power_timers(self):
        now = pygame.time.get_ticks()

        # --- Velocidade ---
        if self.power_timers['speed'] > now:
            self.speed = self.base_speed * 2
        else:
            self.speed = self.base_speed

        # --- Intangibilidade ---
        if self.power_timers['intangivel'] > now:
            if not self.intangivel: 
                self.intangivel = True
                self.aplicar_transparencia_animacoes(128) 
        else:
            if self.intangivel:
                self.intangivel = False
                self.frames = {state: [frame.copy() for frame in frames] for state, frames in self.frames_original.items()}

    def update(self, dt):
        self.input()
        self.move(dt)
        self.handle_power_timers()
        self.animate(dt)
        self.check_invincibility()

        if self.invincible:
            # Faz a imagem piscar
            alpha = 128 if pygame.time.get_ticks() % 200 < 100 else 255
            self.image.set_alpha(alpha)
        elif self.intangivel:
            pass
        else:
            self.image.set_alpha(255) # Garante que a imagem volte ao normal
