from settings import *

def load_mouse_image():
    """
    carrega a imagem do projétil, ajusta as redimensões
    """
    script_dir = os.path.dirname(__file__)
    assets_path = os.path.join(script_dir, 'assets', 'images')
    mouse_img_original = pygame.image.load(os.path.join(assets_path, 'mouse.png')).convert_alpha()
      # redimensiona para 15x8 e a retorna
    return pygame.transform.scale(mouse_img_original, (20, 10))

# --- CLASSE QUE REPRESENTA O PROJÉTIL (MOUSE) ---

class Mouse(pygame.sprite.Sprite):
    def __init__(self, pos, direction, groups, speed=550):
        """
        inicializa a classe Mouse.
        - pos: A posição inicial (x, y) de onde o mouse é criado
        - direction: Um vetor do pygame para indicar a direção do movimento
        - groups: Os grupos de sprites aos quais este projétil pertencerá
        - speed: A velocidade de movimento do mouse em p/s
        """
        
        super().__init__(groups)

        self.pos = pygame.Vector2(pos)
        self.vel = direction * speed
        self.image = load_mouse_image()
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, dt):
        """
        atualiza a posição do mouse a cada quadro, usando 
        - DeltaTime (dt). 
        """
        self.pos += self.vel * dt
        self.rect.center = self.pos

        screen_rect = pygame.display.get_surface().get_rect()
        if not screen_rect.contains(self.rect):
            self.kill() # Remove o sprite de todos os grupos

    def check_collision(self, enemy_pos, enemy_radius):
        """
        verifica se o mouse colidiu com um inimigo
        - enemy_pos: A posição do centro do inimigo
        - enemy_radius: O raio de colisão do inimigo
        """
        distance = self.pos.distance_to(enemy_pos)
        # True = colisão
        return distance < self.radius + enemy_radius

