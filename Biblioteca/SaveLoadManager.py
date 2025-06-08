import json

def salvar_jogo(player, plataforma, save_set='savegame.json'):
    data = {
        'vida': player.vida,
        'amount_honey_coletada': player.amount_honey_coletada,
        'sprite_player': player.sprite,
        'size_x': player.tam_x,
        'size_y': player.tam_y,
            #Cenario
        'current_scene': plataforma.name_background,
        'current_scene_id': plataforma.id_background,
        'current_scene_sprite': plataforma.sprite_background,
        'amount_honey_map': plataforma.amount_honey
    }
    with open(save_set, 'w') as arquivo:
        json.dump(data, arquivo)
    print("Jogo salvo com êxito!")

def carregar_jogo(PlayerClass, PlataformaClass, save_set='savegame.json'):
    with open(save_set, 'r') as arquivo:
        data = json.load(arquivo)

    player = PlayerClass(
        amount_honey_coletada=data['amount_honey_coletada'],
        vida=data['vida'],
        sprite=data['sprite_player'],
        tam_x=data['size_x'],
        tam_y=data['size_y']
    )

    plataforma = PlataformaClass(
        name_background=data['current_scene'],
        id_background=data['current_scene_id'],
        sprite_background=data['current_scene_sprite'],
        amount_honey=data['amount_honey_map']
    )

    print("Jogo carregado com êxito!")
    return player, plataforma
