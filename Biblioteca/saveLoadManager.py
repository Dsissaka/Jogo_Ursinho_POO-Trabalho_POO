import json
import os

class gerenciaSave:
    def __init__(self, arquivo_save='savegame.json'):
        self.arquivo_save = arquivo_save

    def salvar_jogo(self, player, plataforma, versao=1):
        try:
            data = {
                'id_G': player._id_game,
                'amount_honey_coletada': player._amount_honey_coletada,
                'name_C': player._name_character,
                'id_C': player._id_character,
                'sprite_path_player': 'Assets/Poo/Idle',
                'position_x': player._pos_x,
                'position_y': player._pos_y,
                'life': player._vida,
                'size_x': player._tam_x,
                'size_y': player._tam_y,
                'spd_x': player._speed_x,
                'spd_y': player._speed_y,
                'current_scene': plataforma.name_background,
                'current_scene_id': plataforma.id_background,
                'amount_honey_map': plataforma.amount_honey,
                'versao': versao
                }
            with open(self.arquivo_save, 'w') as arquivo:
                json.dump(data, arquivo)
            print("Jogo salvo com êxito!")
        except Exception as e:
            print(f"Erro ao salvar o jogo: {e}")

    def carregar_jogo(self, PlayerClass, PlataformaClass, sprite_poo, sprite_mapa):
        if not os.path.exists(self.arquivo_save):
            print("Arquivo de save não encontrado.")
            return None, None

        try:
            with open(self.arquivo_save, 'r') as arquivo:
                data = json.load(arquivo)

            if data.get('versao') != 1:
                print("Versão de save incompatível.")
                return None, None

            player = PlayerClass(
                id_game=data['id_G'],
                name_character=data['name_C'],
                id_character=data['id_C'],
                sprite=sprite_poo,
                pos_x=data['position_x'],
                pos_y=data['position_y'],
                vida=data['life'],
                tam_x=data['size_x'],
                tam_y=data['size_y'],
                speed_x=data['spd_x'],
                speed_y=data['spd_y'],
                amount_honey_coletada=data['amount_honey_coletada']
            )


            plataforma = PlataformaClass(
                id_game=1,
                amount_honey=data['amount_honey_map'],
                status=1,
                id_background=data['current_scene_id'],
                id_plataforma=1,
                name_background=data['current_scene'],
                sprite_background=sprite_mapa,
                posx_plataforma=400,
                posy_plataforma=300,
                largura=0,
                altura=0
            )


            print("Jogo carregado com êxito!")
            return player, plataforma

        except Exception as e:
            print(f"Erro ao carregar o jogo: {e}")
            return None, None
  