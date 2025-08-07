from settings import *

def load_mouse_image():
    script_dir = os.path.dirname(__file__)
    assets_path = os.path.join(script_dir, '..', 'assets')
    mouse_img_original = pygame.image.load(os.path.join(assets_path, 'mouse.png')).convert_alpha()
    return pygame.transform.scale(mouse_img_original, (15, 8))

class Mouse:
    def __init__(self, pos, direction, speed=550, radius=8):
        self.pos = pygame.Vector2(pos)
        self.vel = direction * speed
        self.radius = radius
        self.image = load_mouse_image()
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, dt):
        self.pos += self.vel * dt
        self.rect.center = self.pos

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def check_collision(self, enemy_pos, enemy_radius):
        distance = self.pos.distance_to(enemy_pos)
        return distance < self.radius + enemy_radius

