import json

def salvar_jogo(Player, save_Set = 'savegame.json'):
    date = {
        'vida': Player.vida,
        'amount_honey_coletada' : Player.amount_honey_coletada,
                #cenario atual
        #'current_scene': Plataforma.name_background,
        #'current_scene_id': Plataforma.id_background,
        #'current_scene_sprite': Plataforma.sprite_background
    }
    with open(save_Set, 'w') as arquivo:
        json.dump(date,arquivo)
    print (f"Jogo salvo com exito!!")


def carregar_jogo(save_Set = 'savegame.json'):
    with open(save_Set,'r') as arquivo:
        date = json.load(arquivo)

    Player = Player(
        amount_honey_coletada = date['amount_honey_coletada'],
        vida = date['vida'],
    )

    # Plataforma = Plataforma(
    #     name_background = date['current_scene'],
    #     id_background = date['current_scene_id'],
    #     sprite_background = date['current_scene_sprite']
    # )
    
    print(f"Jogo carregado com exito!!")
    return Player
