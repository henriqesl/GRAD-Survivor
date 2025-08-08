from settings import *

def load_mouse_image():
    """
    carrega a imagem do projétil, ajusta as redimensões
    """
    script_dir = os.path.dirname(__file__)
    assets_path = os.path.join(script_dir, '..', 'assets', 'images')
    mouse_img_original = pygame.image.load(os.path.join(assets_path, 'mouse.png')).convert_alpha()
    return pygame.transform.scale(mouse_img_original, (25, 15))

# --- CLASSE QUE REPRESENTA O PROJÉTIL (MOUSE) ---

class Mouse(pygame.sprite.Sprite):
    def __init__(self, pos, direction, groups, speed=400):
        """
        inicializa a classe Mouse.
        - pos: A posição inicial (x, y) de onde o mouse é criado
        - direction: Um vetor do pygame para indicar a direção do movimento
        - groups: Os grupos de sprites aos quais este projétil pertencerá
        - speed: A velocidade de movimento do mouse em p/s
        """
        
        super().__init__(groups)

        self.image = load_mouse_image()
        self.rect = self.image.get_rect(center=pos)

        self.pos = pygame.Vector2(self.rect.center)
        self.vel = direction * speed
        

    def update(self, dt, jogador=None):
        """
        Atualiza a posição do mouse. Ignora o jogador.
        """
        self.pos += self.vel * dt
        self.rect.center = round(self.pos.x), round(self.pos.y)

        screen_rect = pygame.display.get_surface().get_rect()
        if not screen_rect.contains(self.rect):
            self.kill()

    def check_collision(self, enemy_pos, enemy_radius):
        """
        verifica se o mouse colidiu com um inimigo
        - enemy_pos: A posição do centro do inimigo
        - enemy_radius: O raio de colisão do inimigo
        """
        distance = self.pos.distance_to(enemy_pos)
        # True = colisão
        return distance < self.radius + enemy_radius

