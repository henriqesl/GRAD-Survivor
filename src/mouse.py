from .settings import *

def load_mouse_image():
    script_dir = os.path.dirname(__file__)
    assets_path = os.path.join(script_dir, '..', 'assets', 'images')
    mouse_img_original = pygame.image.load(os.path.join(assets_path, 'mouse.png')).convert_alpha()
    return pygame.transform.scale(mouse_img_original, (25, 15))

# --- CLASSE QUE REPRESENTA O PROJÉTIL (MOUSE) ---

class Mouse(pygame.sprite.Sprite):
    def __init__(self, pos, direction, groups, speed=400):
        super().__init__(groups)

        self.image = load_mouse_image()
        self.rect = self.image.get_rect(center=pos)

        self.pos = pygame.Vector2(self.rect.center)
        self.vel = direction * speed
        

    def update(self, dt, jogador=None):
        self.pos += self.vel * dt
        self.rect.center = round(self.pos.x), round(self.pos.y)

        screen_rect = pygame.display.get_surface().get_rect()
        if not screen_rect.contains(self.rect):
            self.kill()

    def check_collision(self, enemy_pos, enemy_radius):
        distance = self.pos.distance_to(enemy_pos)
        return distance < self.radius + enemy_radius

