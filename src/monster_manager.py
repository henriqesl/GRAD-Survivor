import pygame
import random
from enemies import Monstro 

EVENTO_SPAWN_MONSTRO = pygame.USEREVENT + 1

class MonsterManager:
    def __init__(self, all_sprites_group, monster_sprites_group):
        """
        Inicializa o gerenciador. Ele precisa saber em quais grupos do jogo
        deve adicionar os monstros que criar.
        """
        self.all_sprites = all_sprites_group
        self.monster_sprites = monster_sprites_group
        
        self.pontos_de_spawn = [(20, 80), (20, 520), (780, 520), (780, 80)]
        
        self.reset()

    def reset(self):
        """Reseta o estado dos monstros para o início de um novo jogo."""
        self.wave = 1
        self.velocidade_monstro = 100  
        self.velocidade_robot = 130    
        self.spawn_interval = 2000     
        
        for monstro in self.monster_sprites:
            monstro.kill()
        
        pygame.time.set_timer(EVENTO_SPAWN_MONSTRO, self.spawn_interval)

    def spawn_monster(self):
        """O coração do manager: cria um novo monstro."""
        ponto_spawn = random.choice(self.pontos_de_spawn)
        
        if self.wave >= 3 and random.random() < 0.3:
            tipo = 'robot'
            velocidade = self.velocidade_robot
        else:
            tipo = 'monstro'
            velocidade = self.velocidade_monstro
            
        monstro = Monstro(tipo, ponto_spawn, velocidade)
        monstro.aumentar_vida(self.wave)
        
        self.all_sprites.add(monstro)
        self.monster_sprites.add(monstro)

    def update(self):
        """
        Atualiza a lógica de dificuldade. Chamado a cada quadro no jogo.
        """
        if len(self.monster_sprites) >= 10 * self.wave:
            self.wave += 1
            self.velocidade_monstro += 20
            self.velocidade_robot += 20
            
            self.spawn_interval = max(500, self.spawn_interval - 200) 
            pygame.time.set_timer(EVENTO_SPAWN_MONSTRO, self.spawn_interval)