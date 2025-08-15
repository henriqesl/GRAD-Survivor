import pygame
import random
from . import game_data
from .enemies import Monstro, Robo

EVENTO_SPAWN_MONSTRO = pygame.USEREVENT + 1

class MonsterManager:
    # Passo 1: Adicionar game_instance
    def __init__(self, all_sprites_group, monster_sprites_group, collision_sprites, game_instance):
        self.all_sprites = all_sprites_group
        self.monster_sprites = monster_sprites_group
        self.collision_sprites = collision_sprites
        self.game = game_instance # Guarda a referência do jogo

        self.pontos_de_spawn = game_data.GAME_SETUP['spawn_points']
        self.monsters_per_wave = game_data.GAME_SETUP['monsters_per_wave']
        self.max_waves = game_data.GAME_SETUP['max_waves']
        self.game_won = False

        self.reset()

    def reset(self):
        self.wave = 1
        self.velocidade_monstro = game_data.ENEMY_DATA['monstro']['speed']
        self.velocidade_robot = game_data.ENEMY_DATA['robo']['speed']
        self.spawn_interval = game_data.GAME_SETUP['initial_spawn_interval']
        self.monsters_spawned_this_wave = 0
        self.game_won = False

        for monstro in self.monster_sprites:
            monstro.kill()

        pygame.time.set_timer(EVENTO_SPAWN_MONSTRO, self.spawn_interval)

    def start_next_wave(self):
        if self.wave >= game_data.GAME_SETUP['max_waves']:
            print("Todas as hordas foram derrotadas! Você venceu!")
            self.game_won = True
            pygame.time.set_timer(EVENTO_SPAWN_MONSTRO, 0)
            return

        self.wave += 1
        self.velocidade_monstro += game_data.GAME_SETUP['wave_speed_increase']
        self.velocidade_robot += game_data.GAME_SETUP['wave_speed_increase']
        self.monsters_spawned_this_wave = 0

        self.spawn_interval = max(game_data.GAME_SETUP['min_spawn_interval'], self.spawn_interval - game_data.GAME_SETUP['spawn_interval_reduction'])
        pygame.time.set_timer(EVENTO_SPAWN_MONSTRO, self.spawn_interval)

    def spawn_monster(self):
        if self.monsters_spawned_this_wave >= self.monsters_per_wave:
            pygame.time.set_timer(EVENTO_SPAWN_MONSTRO, 0)
            return

        ponto_spawn = random.choice(self.pontos_de_spawn)

        # Passo 2: Passar self.game ao criar os monstros
        if self.wave >= game_data.GAME_SETUP['robot_spawn_wave_start'] and random.random() < game_data.GAME_SETUP['robot_spawn_chance']:
            monstro = Robo(ponto_spawn, self.velocidade_robot, self.collision_sprites, self.game)
        else:
            monstro = Monstro(ponto_spawn, self.velocidade_monstro, self.collision_sprites, self.game)

        monstro.aumentar_vida(self.wave)

        self.all_sprites.add(monstro)
        self.monster_sprites.add(monstro)
        self.monsters_spawned_this_wave += 1

    def update(self):
        if self.game_won:
            return

        if self.monsters_spawned_this_wave >= self.monsters_per_wave and not self.monster_sprites:
            self.start_next_wave()