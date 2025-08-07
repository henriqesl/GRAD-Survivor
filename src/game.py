from settings import *
from mouse import Mouse


pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

script_dir = os.path.dirname(__file__)
assets_path = os.path.join(script_dir, '..', 'assets')

# --- IMAGENS ---
player_img = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, 'jogador.png')).convert_alpha(), (60, 55))
enemy_img = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, 'inimigo_2.png')).convert_alpha(), (60, 55))
background_img = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, 'mapa.jpg')).convert(), (800, 600))

# --- JOGADOR ---
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player_hitbox_radius = 25

# --- INIMIGOS ---
enemies = [
    {"pos": pygame.Vector2(200, 200), "hitbox_radius": 30, "hp": 1, "sprite": enemy_img},
    {"pos": pygame.Vector2(500, 500), "hitbox_radius": 35, "hp": 2, "sprite": enemy_img},
    {"pos": pygame.Vector2(700, 250), "hitbox_radius": 40, "hp": 3, "sprite": enemy_img}
]

# --- MOUSES (TIROS) ---
mouses = []
last_shot_time = 0
shot_cooldown = 250

running = True
dt = 0
vel_player = 250

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Atirar mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            current_time = pygame.time.get_ticks()
            if current_time - last_shot_time >= shot_cooldown:
                mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
                direction = (mouse_pos - player_pos).normalize()
                mouses.append(Mouse(player_pos, direction))
                last_shot_time = current_time

    # --- MOVIMENTO JOGADOR ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= vel_player * dt
    if keys[pygame.K_s]:
        player_pos.y += vel_player * dt
    if keys[pygame.K_a]:
        player_pos.x -= vel_player * dt
    if keys[pygame.K_d]:
        player_pos.x += vel_player * dt

    # Limita jogador na tela
    player_pos.x = max(player_hitbox_radius, min(player_pos.x, screen.get_width() - player_hitbox_radius))
    player_pos.y = max(player_hitbox_radius, min(player_pos.y, screen.get_height() - player_hitbox_radius))

    # --- ATUALIZA MOUSES E CHECA COLISÕES ---
    mouses_to_keep = []
    for mouse in mouses:
        mouse.update(dt)
        hit_enemy = False
        
        for enemy in enemies:
            if mouse.check_collision(enemy["pos"], enemy["hitbox_radius"]):
                enemy["hp"] -= 1
                hit_enemy = True
                break

        if not hit_enemy:
            mouses_to_keep.append(mouse)

    mouses = mouses_to_keep

    # Remove inimigos mortos
    enemies = [e for e in enemies if e["hp"] > 0]

    # --- DESENHO ---
    screen.blit(background_img, (0, 0))

    for enemy in enemies:
        rect = enemy["sprite"].get_rect(center=enemy["pos"])
        screen.blit(enemy["sprite"], rect)

    for mouse in mouses:
        mouse.draw(screen)

    player_rect = player_img.get_rect(center=player_pos)
    screen.blit(player_img, player_rect)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
