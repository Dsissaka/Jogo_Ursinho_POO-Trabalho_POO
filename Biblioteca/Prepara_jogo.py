from Biblioteca import Animacao as Am  

ALTURA_TELA = 840
COMPRIMENTO_TELA = 480

class Jogo():
    def __init__(self, id_game):
        self._id_game = id_game

    def load_sprites_geral(self):
        sprite_inimigo_urso = {
            "urso_movimento_D_sprites": Am.pega_sprite_na_pasta("Assets/Urso/Direita"),
            "urso_movimento_E_sprites": Am.pega_sprite_na_pasta("Assets/Urso/Esquerda"),
            "urso_idle_sprites": Am.pega_sprite_na_pasta("Assets/Urso/Idle")
        }
        sprite_poo = {
            "pooh_idle_sprites": Am.pega_sprite_na_pasta("Assets/Poo/Idle"),
            "pooh_movimento_D_sprites": Am.pega_sprite_na_pasta("Assets/Poo/Direita"),
            "pooh_movimento_E_sprites": Am.pega_sprite_na_pasta("Assets/Poo/Esquerda"),
            "pooh_morte_poo": Am.pega_sprite_na_pasta("Assets/Poo/Morte")
        }
        sprite_leitao = {
            "npc_idle_sprites": Am.pega_sprite_na_pasta("Assets/Npc")
        }
        sprite_honey = {
            "honey_sprites": Am.pega_sprite_na_pasta("Assets/Mel")
        }
        sprite_boss = {
            "boss_idle_sprites": Am.pega_sprite_na_pasta("Assets/Boss")
        }
        sprite_inimigo_abelha = {
            "abelha_idle_sprites": Am.pega_sprite_na_pasta("Assets/Abelha/idle"),
        }
        sprite_mapa = {
            "mapa_original_sprite": Am.pega_sprite_na_pasta("Assets/Mapas/Mapa_original"),
            "mapa_boss_sprites": Am.pega_sprite_na_pasta("") # Verifique o caminho
        }
        sprite_projetil = {
            "projetil": Am.pega_sprite_na_pasta("Assets/Ferrao")
        }
        return sprite_inimigo_urso, sprite_poo, sprite_leitao, sprite_honey, \
               sprite_boss, sprite_inimigo_abelha, sprite_mapa, sprite_projetil

    def setup_level(self, all_sprites, plataforms_group, honey_group, enemies_group,
                    boss_group, stingers_group, water_group, player,
                    platform_map, honey_map, enemy_map, game_sprites,
                     PlataformClass, HoneyClass, InimigoClass):
        
        all_sprites.empty()
        plataforms_group.empty()
        honey_group.empty()
        enemies_group.empty()
        boss_group.empty()
        stingers_group.empty()
        water_group.empty()

        all_sprites.add(player)
        player.rect.x = player._pos_x
        player.rect.y = player._pos_y

        player.vida = 3
        player.invincible = False
        player._speed_y = 0

        for data in platform_map:
            plat = PlataformClass(*data)
            all_sprites.add(plat)
            plataforms_group.add(plat)
        
        for data in honey_map:
            honey = HoneyClass(data[0], data[1], game_sprites['sprite_honey'])
            all_sprites.add(honey)
            honey_group.add(honey)

        for data in enemy_map:
            enemy = InimigoClass(*data)
            all_sprites.add(enemy)
            enemies_group.add(enemy)
        

        return len(honey_map)
    
    def setup_boss_level(self, all_sprites, plataforms_group, honey_group,
                         enemies_group, stingers_group, water_group, boss_group,
                         player, game_sprites, BossClass):
        
        all_sprites.empty()
        plataforms_group.empty()
        honey_group.empty()
        enemies_group.empty()
        stingers_group.empty()
        water_group.empty()
        boss_group.empty() # Garante que o grupo do boss esteja limpo

        all_sprites.add(player)
        boss = BossClass(
            id_character=4,
            name_character="Boss",
            sprite=game_sprites['sprite_boss'], 
            pos_x=COMPRIMENTO_TELA / 2,
            pos_y=80,
            tam_x=80,
            tam_y=80
        )
        all_sprites.add(boss)
        boss_group.add(boss)
        
        player.rect.x = player._pos_x
        player.rect.y = player._pos_y
        player._speed_y = 0
        
        return boss 
