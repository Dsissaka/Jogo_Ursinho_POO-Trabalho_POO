import json
import os

class gerenciaSave:
    def __init__(self, arquivo_save='savegame.json'):
        self.arquivo_save = arquivo_save  # Construtor

    def salvar_jogo(self, player, honey_score, game_state, versao=1):
        try:
            # Escolhe as cenas para salvar
            cenas_para_salvar = {'level_1', 'boss_level'}

    # Define os dados a serem salvos
            data = {
                'position_x':player.rect.x,
                'position_y':player.rect.y,
                'speed':player.speed,
                'falling_y':player.velocity_y,
                'gravity':player.gravity,
                'jump_str':player.jump_strength,
                'ground':player.on_ground,
                'Health': player.health,
                'hurt':player.hurt_time,
                'knockback':player.knockback_strength,
                'amount_honey_coletada': honey_score,
                'versao': versao
            }


            # Adiciona `current_scene` se necessário
            if game_state in cenas_para_salvar:
                data['current_scene'] = game_state

            # Escrita no arquivo JSON
            with open(self.arquivo_save, 'w') as arquivo:
                json.dump(data, arquivo)

            print("Jogo salvo com êxito!")

        except Exception as e:
            print(f"Erro ao salvar o jogo: {e}")

    def carregar_jogo(self, player):
        if not os.path.exists(self.arquivo_save):
            print("Arquivo de save não encontrado.")
            return False, 0  # Retorna `False` e um valor padrão para honey_score

        try:
            with open(self.arquivo_save, 'r') as arquivo:
                data = json.load(arquivo)

            # Verifica se a versão do save é compatível
            if data.get('versao') != 1:
                print("Versão de save incompatível.")
                return False, 0

            # Restaurando os atributos do player
            player.rect.x = data.get('position_x', player.rect.x)
            player.rect.y = data.get('position_y', player.rect.y)
            player.speed = data.get('speed', player.speed)
            player.velocity_y = data.get('falling_y', player.velocity_y)
            player.gravity = data.get('gravity', player.gravity)
            player.jump_strength = data.get('jump_str', player.jump_strength)
            player.on_ground = data.get('ground', player.on_ground)
            player.health = data.get('Health', player.health)
            player.hurt_time = data.get('hurt', player.hurt_time)
            player.knockback_strength = data.get('knockback', player.knockback_strength)
            honey_score = data.get('amount_honey_coletada', 0)  # Define um padrão
            
            print("Jogo carregado com êxito!")
            return True, honey_score  # Retorna sucesso e o honey_score carregado

        except Exception as e:
            print(f"Erro ao carregar o jogo: {e}")
            return False, 0