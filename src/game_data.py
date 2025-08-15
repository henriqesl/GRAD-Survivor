PLAYER_DATA = {
    'speed': 220,
    'max_lives': 3,
    'invincibility_duration': 1500,
    'shoot_delay': 300,
    'sprite_paths': {
        'left': 'assets/images/sprite_2_resized.png',
        'right': 'assets/images/sprite_3_resized.png',
        'up': 'assets/images/sprite_4_resized.png',
        'down': 'assets/images/sprite_1_resized.png'
    }
}

ENEMY_DATA = {
    'monstro': {
        'speed': 100,
        'health': 1,
        'sprite_paths': {
            'left': 'assets/images/monstro sprite_esquerda.png',
            'right': 'assets/images/monstro_sprite_direita.png',
            'up': 'assets/images/monstro_sprite_costas.png',
            'down': 'assets/images/monstro_sprite.png'
        }
    },
    'robo': {
        'speed': 130,
        'health': 2,
        'sprite_paths': {
            'left': 'assets/images/robo_esquerda_sprite.png',
            'right': 'assets/images/robo_direita_sprite.png',
            'up': 'assets/images/robo_costas_sprite.png',
            'down': 'assets/images/robo_frente_sprite.png'
        }
    }
}

GAME_SETUP = {
    'monsters_per_wave': 10,
    'max_waves': 10,
    'wave_speed_increase': 20,
    'initial_spawn_interval': 2000,
    'spawn_interval_reduction': 200,
    'min_spawn_interval': 500,
    'spawn_points': [(35, 85), (35, 525), (765
    , 525), (765, 85)],
    'robot_spawn_wave_start': 3,
    'robot_spawn_chance': 0.3
}

ITEM_DATA = {
    'cracha': {
        'image_path': 'assets/images/cracha.png',
        'drop_chance': 10,  # Chance em %
        'duration': 3000    # Duração em milissegundos
    },
    'redbull': {
        'image_path': 'assets/images/redbull.png',
        'drop_chance': 10,
        'duration': 3000
    },
    'subway': {
        'image_path': 'assets/images/subway.png',
        'drop_chance': 10,
        # Sem 'duration' pois o efeito é instantâneo
    }
}

ASSET_PATHS = {
    'caption': "GRAD-Survivor",
    'map': 'assets/images/mapa1.0.png',
    'music': 'assets/sounds/interstellar.mp3',
    'heart_full': 'assets/images/coracao.png',
    'heart_empty': 'assets/images/coracao_apagado.png',
    'projectile': 'assets/images/mouse.png',
    'initial_screen_bg': 'assets/images/inicio.png',
    'initial_screen_button': 'assets/images/play.png'
}