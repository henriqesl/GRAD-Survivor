import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

# Posição inicial do jogador
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# Lista para armazenar as balas
bullets = []

running = True
dt = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Atira ao clicar
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            direction = (mouse_pos - player_pos).normalize()
            bullets.append({
                "pos": end_pos.copy(),
                "vel": direction * 600  # velocidade da bala
            })

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    player_pos.x = max(0, min(player_pos.x, screen.get_width() - 100))
    player_pos.y = max(0, min(player_pos.y, screen.get_height() - 100))

    # Atualiza balas
    for bullet in bullets:
        bullet["pos"] += bullet["vel"] * dt

    # Limpa tela
    screen.fill("black")

    # Desenha o jogador
    pygame.draw.circle(screen, "white", player_pos, 40)

    # Desenha o cano
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
    direction = (mouse_pos - player_pos).normalize()
    end_pos = player_pos + direction * 60
    pygame.draw.line(screen, "white", player_pos, end_pos, 6)

    # Desenha balas
    for bullet in bullets:
        pygame.draw.circle(screen, "yellow", (int(bullet["pos"].x), int(bullet["pos"].y)), 5)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
