import pygame
import random
from enemies import Monstro

EVENTO_SPAWN_MONSTRO = pygame.USEREVENT + 1

class MonsterManager:
    def __init__(self, all_sprites_group, monster_sprites_group, collision_sprites):
        self.all_sprites = all_sprites_group
        self.monster_sprites = monster_sprites_group
        self.collision_sprites = collision_sprites

        self.pontos_de_spawn = [(20, 85), (20, 525), (780, 525), (780, 85)]
        self.monsters_per_wave = 10
        self.max_waves = 10
        self.game_won = False

        self.reset()

    def reset(self):
        self.wave = 1
        self.velocidade_monstro = 100
        self.velocidade_robot = 130
        self.spawn_interval = 2000
        self.monsters_spawned_this_wave = 0
        self.game_won = False

        for monstro in self.monster_sprites:
            monstro.kill()

        pygame.time.set_timer(EVENTO_SPAWN_MONSTRO, self.spawn_interval)

    def start_next_wave(self):
        if self.wave >= self.max_waves:
            print("Todas as hordas foram derrotadas! Você venceu!")
            self.game_won = True
            pygame.time.set_timer(EVENTO_SPAWN_MONSTRO, 0)
            return

        self.wave += 1
        self.velocidade_monstro += 20
        self.velocidade_robot += 20
        self.monsters_spawned_this_wave = 0

        self.spawn_interval = max(500, self.spawn_interval - 200)
        pygame.time.set_timer(EVENTO_SPAWN_MONSTRO, self.spawn_interval)

    def spawn_monster(self):
        if self.monsters_spawned_this_wave >= self.monsters_per_wave:
            pygame.time.set_timer(EVENTO_SPAWN_MONSTRO, 0)
            return

        ponto_spawn = random.choice(self.pontos_de_spawn)

        if self.wave >= 3 and random.random() < 0.3:
            tipo = 'robot'
            velocidade = self.velocidade_robot
        else:
            tipo = 'monstro'
            velocidade = self.velocidade_monstro

        monstro = Monstro(tipo, ponto_spawn, velocidade, self.collision_sprites)
        monstro.aumentar_vida(self.wave)

        self.all_sprites.add(monstro)
        self.monster_sprites.add(monstro)
        self.monsters_spawned_this_wave += 1

    def update(self):
        if self.game_won:
            return

        if self.monsters_spawned_this_wave >= self.monsters_per_wave and not self.monster_sprites:
            self.start_next_wave()