from Settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.load_images()
        self.state, self.frame_index = 'down', 0 
        self.image = self.frames[self.state][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.hitbox_rect = self.rect.inflate(-60, 0)
    
        # movemento 
        self.direction = pygame.Vector2()
        self.speed = 500
        self.base_speed = 500
        self.collision_sprites = collision_sprites

        # Poderes e timers
        self.power_timers = {
            'speed': 0,
            'intangivel': 0
        }
        self.intangivel = False

    def load_images(self):
        self.frames = {'left': [], 'right': [], 'up': [], 'down': []}

        for state in self.frames.keys():
            for folder_path, sub_folders, file_names in walk(join('images', 'player', state)):
                if file_names:
                    for file_name in sorted(file_names, key=lambda name: int(name.split('.')[0])):
                        full_path = join(folder_path, file_name)
                        surf = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surf)

        # Guardar cópia original para restaurar depois
        self.frames_original = {state: [frame.copy() for frame in frames] for state, frames in self.frames.items()}

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction.length() > 0 else pygame.Vector2()

    def move(self, dt):
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                if direction == 'vertical':
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom

    def animate(self, dt):
        # Definir estado (direção)
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'
        if self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'

        # Avança frames se estiver se movendo
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

        # Velocidade
        if self.power_timers['speed'] > now:
            self.speed = self.base_speed * 2
        else:
            self.speed = self.base_speed

        # Intangibilidade
        if self.power_timers['intangivel'] > now:
            if not self.intangivel: 
                self.intangivel = True
                self.aplicar_transparencia_animacoes(128) 
        else:
            if self.intangivel:
                self.intangivel = False
                # Restaurar frames originais
                self.frames = {state: [frame.copy() for frame in frames] for state, frames in self.frames_original.items()}

    def update(self, dt):
        self.input()
        self.move(dt)
        self.handle_power_timers()
        self.animate(dt)