from settings import *

def load_mouse_image():
    """
    carrega a imagem do projétil, ajusta as redimensões
    """
    script_dir = os.path.dirname(__file__)
    assets_path = os.path.join(script_dir, '..', 'assets')
    mouse_img_original = pygame.image.load(os.path.join(assets_path, 'mouse.png')).convert_alpha()
      # redimensiona para 15x8 e a retorna
    return pygame.transform.scale(mouse_img_original, (15, 8))

# --- CLASSE QUE REPRESENTA O PROJÉTIL (MOUSE) ---

class Mouse:
    def __init__(self, pos, direction, speed=550, radius=8):
        """
        inicializa a classe Mouse.
        - pos: A posição inicial (x, y) de onde o mouse é criado
        - direction: Um vetor do pygame para indicar a direção do movimento
        - speed: A velocidade de movimento do mouse em p/s
        - radius: O raio para detecção de colisão
        """
        # (pos) é parametro de construção inicial
        self.pos = pygame.Vector2(pos)
        self.vel = direction * speed
        self.radius = radius
        self.image = load_mouse_image()
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, dt):
        """
        atualiza a posição do mouse a cada quadro, usando 
        - DeltaTime (dt). 
        """
        self.pos += self.vel * dt
        self.rect.center = self.pos

    def draw(self, screen):
         """
        Método para desenhar a imagem do mouse na tela.
        - screen: A superfície da tela principal do Pygame
        """
        # blit = desenhar uma tela sob a outra
        screen.blit(self.image, self.rect)

    def check_collision(self, enemy_pos, enemy_radius):
        """
        verifica se o mouse colidiu com um inimigo
        - enemy_pos: A posição do centro do inimigo
        - enemy_radius: O raio de colisão do inimigo
        """
        distance = self.pos.distance_to(enemy_pos)
        # True = colisão
        return distance < self.radius + enemy_radius

