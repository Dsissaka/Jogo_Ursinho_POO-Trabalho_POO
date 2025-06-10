from abc import ABC, abstractmethod
import pygame
import json
import os
from Biblioteca import Projetil as Pj # IMPORTA A CLASSE PROJETIL
from Biblioteca import Animacao as Am #Importa a classe animacao
from Biblioteca import SaveLoadManager as Slm


#para testes, to assumindo que o chão é em 100 e o topo em 400

ALTURA_TELA = 600
COMPRIMENTO_TELA = 800
GRAVIDADE = 1
INTERVALO_DISPARO = 3000 # 1.5 segundos

class Jogo():
    def __init__(self, id_game):
        self._id_game = id_game # pode ser usado para recuperar logs de sessões passadas
                                #podemos usar escrita em arquivos para isso
                    
        #talvez mover "load_sprites_geral" para cá

class Background(Jogo):
    def __init__(self, id_game, amount_honey, status, id_background, name_background, sprite_background):
        super().__init__(id_game)
        self._status= status #0 = parado/ 1 = rodando/ 2 = segundo plano
        self._name_background = name_background #nome do mapa
        self._amount_honey= amount_honey #quantiade de méis disponiveis pelo mapa
        self._id_background = id_background #usado para identificar possiveis variações para um mesmo cenário (ex:versão noite e versão dia)
        self._sprite_background = sprite_background

class Plataforma(Background):
    #classe responsável pela enquadramento visivel do jogo, onde o jogador se encontra

    def __init__(self, id_game, amount_honey, status,id_background, id_plataforma, name_background, sprite_background, posx_plataforma, posy_plataforma, largura, altura):
        super().__init__(id_game, amount_honey, status, id_background, name_background, sprite_background)
        self._id_plataforma =  id_plataforma #id especifico para pré-definicação e uma plataforma
        self._posx_plataforma =  posx_plataforma # posicionamento no eixo X da plataforma responsavel pela ilusao de movimento
        self._posy_plataforma = posy_plataforma # posicionamento no eixo Y da plataforma
        self._largura = largura #comprimento da plataforma
        self._altura = altura #altura da plataforma

#ID_plamatorma = 1 para mapa original e 2 para mapa do boss
class Honey(Background):
    def __init__(self, id_game, amount_honey, status, id_background, name_background, sprite_background,posx_honey, posy_honey, tam_x, tam_y, ativo):
        super().__init__(id_game, amount_honey, status, id_background, name_background, sprite_background)
        self.__posx_honey= posx_honey #posicao no eixo X do mel
        self.__posy_honey= posy_honey #posicao no eixo Y do mel
        self.__tam_x=tam_x
        self.__tam_y=tam_y
        self._ativo = ativo

    def desativar(self):
        self._ativo= False

    def verifica_colisao(self, outro):
        hitbox_mel = pygame.Rect(self.__posx_honey, self.__posy_honey, self.__tam_x, self.__tam_y)
        hitbox_outro = pygame.Rect(outro._pos_x, outro._pos_y, outro._tam_x, outro._tam_y)
        return hitbox_mel.colliderect(hitbox_outro)

    def coleta_mel(self):
        self._amount_honey= self._amount_honey - 1
        self.desativar()


class Personagens(Jogo, ABC):
    def __init__(self, id_game, id_character,  name_character, pos_x, pos_y, vida, tam_x, tam_y, sprite):
        super().__init__(id_game)
        self._id_character= id_character #id de identificação do personagem
        self._name_character= name_character #nome do personagem
        self._pos_x = pos_x #posicao no eixo X do personagem em relação ao mapa
        self._pos_y= pos_y #posicao no eixo Y do personagem em relação ao mapa
        self._vida = vida #contador de vida do personagem
        self._tam_x = tam_x #altura do personagem
        self._tam_y = tam_y # largura do personagem
        self._sprite = sprite

        #ID DE PERSONAGEM
        #0 = POOH
        #1 = ABELHA
        #2 = NPC
        #3= BOSS



    @abstractmethod
    def fazer_animacao(self, tipo):
        #será utilizado a variavel "self.id_character" para identificar qual personagem 
        # e a variavel tipo para identificar o tipo da animação
        pass

    @abstractmethod
    def verifica_colisao(self, outro):
        #verifica se a posição do objeto self coincide com a do objeto outro. Assim permitindo intereção do POOH com NPC, além do ataque 
        # e hit de projeteis inimigos. Utiliza a variavel "outro" para identificar como calcular a colisão
        pass

    @abstractmethod
    def movimento(self):
        # possui implementações diferenes para cada personagem.
        # Inimigo possui implimentação de forma randômica ou a vir pra cima do personagem (a definir)
        # Player possui movimentação baseada nas entradas do teclado
        pass

class Npc(Personagens):
    def __init__(self, id_game, name_character, id_character, sprite, pos_x, pos_y, vida, tam_x, tam_y,):
        super().__init__(id_game, id_character,  name_character, pos_x, pos_y, vida, tam_x, tam_y, sprite)
        self.animacao = Am.Animacao(sprite,"npc_idle_sprites", 100)


    def comentario(self):
        text_box = "Cuidado com as abelhas" #frase dita pelo npc ao haver colisão com o personagem principal
        print(text_box) #ainda definir como fazer isto aparecer na tela e não no terminal

    def fazer_animacao(self, tipo):
        self.animacao.definir_estado(tipo)

    def movimento(self):
        estado = "npc_idle_sprites"
        self.fazer_animacao(estado)

    def verifica_colisao(self, outro):
        hitbox_npc = pygame.Rect(self._pos_x, self._pos_y, self._tam_x, self._tam_y)
        hitbox_outro = pygame.Rect(outro._pos_x, outro._pos_y, outro._tam_x, outro._tam_y)
        return hitbox_npc.colliderect(hitbox_outro)
    
class Player(Personagens):
    def __init__ (self, id_game, name_character, id_character, sprite, pos_x, pos_y, vida, tam_x, tam_y, speed_x, speed_y, amount_honey_coletada,):
        super().__init__(id_game, id_character, name_character, pos_x, pos_y, vida, tam_x, tam_y, sprite)
        self._amount_honey_coletada = amount_honey_coletada #quantidade de mel coletada pelo personagem
        self._speed_x = speed_x
        self._speed_y = speed_y #velocidade de movimento do personagem
        self._no_chao = True #variável para definir o contato do poo com o chão
        self.animacao = Am.Animacao(sprite, "pooh_idle_sprites", 100)
        self.speed_jump = -15

    def verifica_colisao(self, outro):
        hitbox_player = pygame.Rect(self._pos_x, self._pos_y, self._tam_x, self._tam_y)
        hitbox_outro = pygame.Rect(outro._pos_x, outro._pos_y, outro._tam_x, outro._tam_y)
        return hitbox_player.colliderect(hitbox_outro)


    def fazer_animacao(self, tipo):
        self.animacao.definir_estado(tipo)

    def movimento(self):
        animacao = "pooh_idle_sprites"
        tecla = pygame.key.get_pressed()

        if tecla[pygame.K_LEFT]:
            self._pos_x -= self._speed_x
            animacao = "pooh_movimento_E_sprites"
        elif tecla[pygame.K_RIGHT]:
            self._pos_x += self._speed_x
            animacao = "pooh_movimento_D_sprites"
        elif tecla[pygame.K_UP] and self._no_chao:
            self._speed_y = self.speed_jump
            self._no_chao = False 
            animacao = "pooh_movimento_U_sprites"

        self._speed_y += GRAVIDADE
        self._pos_y += self._speed_y

        if self._pos_y >= 401:  #definir posteriormente onde vai ser o chão 
            self._pos_y = 400
            self._speed_y = 0
            self._no_chao = True 

        self.fazer_animacao(animacao)

class Inimigo(Personagens):
    def __init__(self, id_game, name_character,  id_character, sprite, pos_x, pos_y, vida, tam_x, tam_y, speed):
        super().__init__(id_game, id_character,  name_character, pos_x, pos_y, vida, tam_x, tam_y, sprite)
        self.inimigo_ativo= True
        self.speed= speed
        self.lim_sup = 400
        self.lim_inf = 100
        self.dir = 1 #supoe-se que a abelha ja nasce no ar

        if self._id_character ==1:
            self.animacao = Am.Animacao(sprite, "abelha_idle_sprites", 100)
        elif self._id_character == 3:
            self.animacao = Am.Animacao(sprite, "inimigo_idle_sprites", 100)
        self.lim_sup = 400 #definir posteriormente
        self.lim_inf = 100 #definir posteriormente

    def verifica_colisao(self, outro):
        hitbox_inimigo = pygame.Rect(self._pos_x, self._pos_y, self._tam_x, self._tam_y)
        hitbox_outro = pygame.Rect(outro._pos_x, outro._pos_y, outro._tam_x, outro._tam_y)
        return hitbox_inimigo.colliderect(hitbox_outro)

    def movimento(self):
        self._pos_y += self.speed * self.dir
        if self._pos_y <= self.lim_sup:
            self._pos_y = self.lim_sup # Garante que não passe do limite
            self.dir = 1 # Muda para baixo
        elif self._pos_y >= self.lim_inf:
            self._pos_y = self.lim_inf # Garante que não passe do limite
            self.dir = -1 # Muda para cima 
        if self._id_character == 1:
            self.fazer_animacao("abelha_idle_sprites")
        else:
            self.fazer_animacao("boss_idle_sprites")
                

    def fazer_animacao(self, tipo):
        self.animacao.definir_estado(tipo)

    
    def dispara_projetil(self, outro):
        velocidade = 10   # definir posteriormente
        direcao = -1 if self._pos_x > outro._pos_x else 1
        distancia_disparo = 10 #distancia minima para o inimigo atirar contra poo
                               #definir posteriormente
        proj_ativo =True    
        largura_proj = 5 # definir posteriormente
        altura_proj = 2  # definir posteriormente
        sprite_proj = Am.pega_sprite_na_pasta("Assets/Projetil")
        if abs(self._pos_x - outro._pos_x) <= distancia_disparo :
                projetil = Pj(
                    velocidade_projetil= velocidade,
                    pos_x_projetil=self._pos_x, #por estar na classe inimigo, o puxam-se os dados de posicao e assim o ferrao parte da posicao do inimigo
                    pos_y_projetil=self._pos_y, #por estar na classe inimigo, o puxam-se os dados de posicao e assim o ferrao parte da posicao do inimigo
                    direcao= direcao,
                    ativo = proj_ativo,
                    largura_proj = largura_proj,
                    altura_proj = altura_proj,
                    sprite = sprite_proj
        )
        return projetil
    
class gerenciaSave:
    def __init__(self, arquivo_save='savegame.json'):
        self.arquivo_save = arquivo_save

    def salvar_jogo(self, player, plataforma, versao=1):
        try:
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
            with open(self.arquivo_save, 'w') as arquivo:
                json.dump(data, arquivo)
            print("Jogo salvo com êxito!")
        except Exception as e:
            print(f"Erro ao salvar o jogo: {e}")

    def carregar_jogo(self, PlayerClass, PlataformaClass):
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

        except Exception as e:
            print(f"Erro ao carregar o jogo: {e}")
            return None, None
            
#inicio da parte de declaração e preenchimento de sprites    
def load_sprites_geral():
        sprite_poo = {
        "pooh_idle_sprites": Am.pega_sprite_na_pasta("Assets/Poo/Idle"),
        "pooh_movimento_D_sprites": Am.pega_sprite_na_pasta("Assets/Poo/Direita"),
        "pooh_movimento_E_sprites": Am.pega_sprite_na_pasta("Assets/Poo/Esquerda"),
        "pooh_movimento_U_sprites": Am.pega_sprite_na_pasta("Assets/Poo/Pulo"),
        "pooh_morte_poo": Am.pega_sprite_na_pasta("Assets/Poo/Morte")
        }

        sprite_boss = {
        "boss_idle_sprites": Am.pega_sprite_na_pasta("Assets/Boss/idle")

        }

        sprite_inimigo = {
        "abelha_idle_sprites": Am.pega_sprite_na_pasta("Assets/Abelha/idle"),
        }

        sprite_leitao = {
        "npc_idle_sprites": Am.pega_sprite_na_pasta("Assets/Npc")
        }
        sprite_mapa= {
        "mapa_original_sprite": Am.pega_sprite_na_pasta("Assets/Mapas/Mapa_original")
        }
        return sprite_poo, sprite_boss, sprite_inimigo, sprite_leitao, sprite_mapa
#fim da parte de declaração e preenchimento de sprites

def main():
    pygame.init()
    tela = pygame.display.set_mode((COMPRIMENTO_TELA,ALTURA_TELA))
    pygame.display.set_caption("jogo poo")
    relogio = pygame.time.Clock()
    running = True
    sprite_poo, sprite_boss, sprite_inimigo, sprite_leitao, sprite_mapa = load_sprites_geral()


#inicio da parte de declaração e preenchimento de objetos
    #ainda definir como esse dialogo ocorrerá dentro da tela dojogo, e não no terminal
    resp = int(input("Deseja utilizar o seu último save?")) #1 para sim e 0 para não
    if resp == 1:
        poo, frontground= Slm.carregar_jogo(Player, Plataforma)
    
    else:
        poo = Player(
        id_game=1,
        amount_honey_coletada= 0,
        name_character="Pooh",
        id_character=0,
        sprite=sprite_poo,
        pos_x= 1,    #definir quando o mapa ficar pronto
        pos_y= 100,   #definir quando o mapa ficar pronto
        vida=10,
        tam_x=50,   #a definir conforme a sprite
        tam_y=70,   #a definir conforme a sprite
        speed_x=5,
        speed_y=3
    )
        
    frontground = Plataforma(
        id_game=1,
        amount_honey=10,
        status=1,
        id_background=1,     #a definir
        id_plataforma= 1,    #a definir
        name_background= "mapa_original",
        sprite_background= sprite_mapa,
        posx_plataforma= 400,  #a definir
        posy_plataforma= 300,  #a definir
        largura= 0,          #a definir
        altura= 0            #a definir
    )

    leitao = Npc(
        id_game =1,
        name_character= "Leitao",
        id_character= 2,
        sprite = sprite_leitao,
        pos_x= 50,    #definir quando o mapa ficar pronto
        pos_y= 100,    #definir quando o mapa ficar pronto
        vida = 9999,    #npc não morre
        tam_x= 30,    #definir conforme a sprite
        tam_y= 20,    #definir conforme a sprite
    )

    abelha = Inimigo(
        id_game=1,
        name_character= "Abelha",
        id_character=1,
        sprite = sprite_inimigo,
        pos_x= 300,
        pos_y= 250,
        vida=10,
        tam_x=30,
        tam_y= 30,
        speed=10,
 )
    boss = Inimigo(
                id_game=1,
                name_character= "Boss",
                id_character=3,
                sprite = sprite_boss,
                pos_x=300,
                pos_y= 250,
                vida=10,
                tam_x=30,     #a definir
                tam_y= 30,    #a definir
                speed=10,
)

#inicio da parte de declaração e preenchimento de objetos
    projeteis_ativos = []
    ultimo_disparo_boss = pygame.time.get_ticks()

    while running:
        tela.fill((0, 0, 0))  # Limpa a tela
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                Slm.salvar_jogo(poo, frontground)
                running = False

        dt = relogio.tick(60)
        poo.movimento()
        poo.animacao.atualiza(dt)
        tela.blit(frontground._sprite_background["mapa_original_sprite"][0], (frontground._posy_plataforma, frontground._posy_plataforma))

        
        if abelha.inimigo_ativo:
            abelha.movimento()
            abelha.animacao.atualiza(dt)

        if boss.inimigo_ativo:
            boss.movimento() # Definir posteriormente como é o movimento do boss
            boss.animacao.atualiza(dt)
            #inicio parte do codigo referente a projetil do chefão#
        
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - ultimo_disparo_boss > INTERVALO_DISPARO:
                novo_proj = boss.dispara_projetil(poo) 
                if novo_proj: 
                    projeteis_ativos.append(novo_proj)
                    ultimo_disparo_boss = tempo_atual
        projeteis_a_remover = []
        for proj in projeteis_ativos:
            if proj.ativo:
                proj.atualizar(poo, frontground._largura)
                tela.blit(proj.sprite, (proj.pos_x, proj.pos_y))
            else:
                projeteis_a_remover.append(proj)
        for proj_removido in projeteis_a_remover:
            projeteis_ativos.remove(proj_removido)
        #fim da parte do codigo referente a projetil do chefão

        if leitao._pos_x is not None and poo._pos_x is not None:
            if (leitao and abs(poo._pos_x - leitao._pos_x)<20) or leitao.verifica_colisao(poo): #20 pixels de distancia entre leitão e player
                leitao.comentario()

#inicio da parte de desenho na tela
        leitao.animacao.atualiza(dt)

        tela.blit(poo.animacao.pega_sprite_atual(), (poo._pos_x, poo._pos_y))
        tela.blit(leitao.animacao.pega_sprite_atual(), (leitao._pos_x, leitao._pos_y))
        tela.blit(abelha.animacao.pega_sprite_atual(), (abelha._pos_x, abelha._pos_y))
        tela.blit(boss.animacao.pega_sprite_atual(), (boss._pos_x, boss._pos_y))
        pygame.display.flip()
#fim da parte de desenho na tela

    pygame.quit()

if  __name__== "__main__": 
    main()
