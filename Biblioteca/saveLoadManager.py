import json
import os

class gerenciaSave:
    def __init__(self, arquivo_save='savegame.json'):
        self.arquivo_save = arquivo_save #construtor

    #função para salvar
    def salvar_jogo(self, player,honey_score,game_state, versao=1):
        try:

            #Escolhe as cenas para salvar e salva
            cenas_para_salvar = {'level_1', 'boss_level'}
            if game_state in cenas_para_salvar:
                'current_scene' = game_state
            # else:
            #     'current_scene' = None

            #seta os dados a serem salvos
            data = {
                # Dados do player
                'id_C': player._id_character,
                'name_C': player._name_character,
                'sprite_path_player': player.rect,
                'position_x': player._pos_x,
                'position_y': player._pos_y,
                'size_x': player._tam_x,
                'size_y': player._tam_y,
                'spd_x': player._speed_x,
                'spd_y': player._speed_y,

                # Salva quantidade de méis coletados
                'amount_honey_coletada': honey_score,

                # Salva a vida atual do player
                'Health': player.vida,

                # Versão do jogo
                'versao': versao
            }

            #escrita no arquivo
            with open(self.arquivo_save, 'w') as arquivo:
                json.dump(data, arquivo)
            print("Jogo salvo com êxito!")

        #tratamento de exceção
        except Exception as e:
            print(f"Erro ao salvar o jogo: {e}")

    #função que carrega o jogo
    def carregar_jogo(self, PlayerClass, honey_score, game_state):
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
                id_character=data['id_C'],
                name_character=data['name_C'],
                sprite=data['sprite_path_player'],
                pos_x=data['position_x'],
                pos_y=data['position_y'],
                tam_x=data['size_x'],
                tam_y=data['size_y'],
                speed_x=data['spd_x'],
                speed_y=data['spd_y'],
            )

            #carrega o mapa que parou
            cenas_para_carregar = {'level_1', 'boss_level'}
            if game_state in cenas_para_carregar:
                game_state = data['current_scene'],
            
            #carrega a quantidade de mel
            honey_score = data['amount_honey_coletada'],

            #carrega a quantidade de vida
            player.vida = data['Health'],
            
            print("Jogo carregado com êxito!")
            return player, honey_score

        except Exception as e:
            print(f"Erro ao carregar o jogo: {e}")
            return None, None
  