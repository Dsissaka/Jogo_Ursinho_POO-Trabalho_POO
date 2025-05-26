from abc import ABC, abstractmethod
import pygame
from Biblioteca import Projetil as pj # IMPORTA A CLASSE PROJETIL

ALTURA_TELA = 1080
COMPRIMENTO_TELA = 1920
GRAVIDADE = 1

class Jogo():
    def __init__(self, id_game):
        self._id_game = id_game # pode ser usado para recuperar logs de sessões passadas
                                #podemos usar escrita em arquivos para isso


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



class Honey(Background):
    def __init__(self, id_game, amount_honey, status, id_background, name_background, sprite_background,posx_honey, posy_honey, tam_x, tam_y, ativo):
        super().__init__(id_game, amount_honey, status, id_background, name_background, sprite_background)
        self.__posx_honey= posx_honey #posicao no eixo X do mel
        self.__posy_honey= posy_honey #posicao no eixo Y do mel
        self.__tam_x=tam_x
        self.__tam_y=tam_y
        self._ativo = ativo

    def desavitar(self):
        self._ativo= False

    def verifica_colisao(self, outro):
        hitbox_mel = pygame.Rect(self.__posx_honey, self.__posy_honey, self.__tam_x, self.__tam_y)
        hitbox_outro = pygame.Rect(outro.pos_x, outro.pos_y, outro.tam_x, outro.tam_y)
        return hitbox_mel.colliderect(hitbox_outro)

    def coleta_mel(self):
        self._amount_honey= self._amount_honey - 1
        self.desavitar()


class Personagens(Jogo):
    def __init__(self, id_game, id_character, sprite,  name_character, pos_x, pos_y, vida, tam_x, tam_y):
        super().__init__(id_game)
        self._id_character= id_character #id de identificação do personagem
        self._sprite= sprite #biblioteca responsavel por armazenar as sprites dos personagens
        self._name_character= name_character #nome do personagem
        self._pos_x = pos_x #posicao no eixo X do personagem em relação ao mapa
        self._pos_y= pos_y #posicao no eixo Y do personagem em relação ao mapa
        self._vida = vida #contador de vida do personagem
        self._tam_x = tam_x #altura do personagem
        self._tam_y = tam_y # largura do personagem

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
        # e hit de projeteis inimigos. Utiliza a variavel "outro.character_id" para identificar como calcular a colisão
        pass

    @abstractmethod
    def movimento(self):
        # possui implementações diferenes para cada personagem.
        # Inimigo possui implimentação de forma randômica ou a vir pra cima do personagem (a definir)
        # Player possui movimentação baseada nas entradas do teclado
        pass

class Npc(Personagens):
    def __init__(self, id_game, name_character, id_character, sprite, pos_x, pos_y, text_box, vida, tam_x, tam_y):
        super().__init__(id_game, id_character, sprite,  name_character, pos_x, pos_y, vida, tam_x, tam_y)
        self.__text_box=text_box #frase dita pelo npc ao haver colisão com o personagem principal

    def comentario(self):
        print(self.__text_box)

    def movimento(self):
        #NPC possui return por ser um ser estático
        return 
    
    def fazer_animacao(self, tipo):
        if tipo == "idle":
            #(terminar de implementar posteriormente)
            pass

    def verifica_colisao(self, outro):
        hitbox_npc = pygame.Rect(self.pos_x, self.pos_y, self.tam_x, self.tam_y)
        hitbox_outro = pygame.Rect(outro.pos_x, outro.pos_y, outro.tam_x, outro.tam_y)
        return hitbox_npc.colliderect(hitbox_outro)
    
class Player(Personagens):
    def __init__ (self, id_game, name_character, id_character, sprite, pos_x, pos_y, vida, tam_x, tam_y, speed, no_chao, speed_jump, amount_honey_coletada):
        super().__init__(id_game, id_character, sprite, name_character, pos_x, pos_y, vida, tam_x, tam_y)
        self._amount_honey_coletada = amount_honey_coletada #quantidade de mel coletada pelo personagem
        self._speed = speed #velocidade de movimento do personagem
        self._no_chao = no_chao #variável para definir o contato do poo com o chão
        self._speed_jump = speed_jump

    def verifica_colisao(self, outro):
        hitbox_player = pygame.Rect(self.pos_x, self.pos_y, self.tam_x, self.tam_y)
        hitbox_outro = pygame.Rect(outro.pos_x, outro.pos_y, outro.tam_x, outro.tam_y)
        return hitbox_player.colliderect(hitbox_outro)

       
    def movimento(self):
        self._speed_jump = 3
        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_LEFT]:
            self._pos_x -= self.speed
        if tecla[pygame.K_RIGHT]:
            self._pos_x += self.speed
        if tecla[pygame.K_UP]:
            self._pos_y += self.speed
            while self._no_chao == False: 
                self._speed_jump= self.speed -1
            self._no_chao = True



    def fazer_animacao(self, tipo):
        if tipo == "idle":
            #(terminar)
            pass

        if tipo == "morte_poo":
            #(terminar)
            pass

        if tipo == "deslocamento":
            #(terminar)
            pass


    def ataque(self, outro):
        if self.verifica_colisao(outro):
            if self.pos_y > (outro.pos_y + (outro.tam_y/1.1)):
                dano_ataque=3
                outro.vida = outro.vida-dano_ataque
                #poo mata quicando 
                if outro.vida == 0:
                    outro.fazer_animacao("morte_enemy")
                    outro.ativo= False
            #talvez definir um sistema de knockback

class Inimigo(Personagens):
    def __init__(self, id_game, name_character,  id_character, sprite, pos_x, pos_y, text_box, vida, tam_x, tam_y, speed, inimigo_ativo):
        super().__init__(id_game, id_character, sprite,  name_character, pos_x, pos_y, vida, tam_x, tam_y)
        self.inimigo_ativo= inimigo_ativo
        self.text_box= text_box
        self.speed= speed 

    def verifica_colisao(self, outro):
        hitbox_inimigo = pygame.Rect(self.pos_x, self.pos_y, self.tam_x, self.tam_y)
        hitbox_outro = pygame.Rect(outro.pos_x, outro.pos_y, outro.tam_x, outro.tam_y)
        return hitbox_inimigo.colliderect(hitbox_outro)

    def movimento(self):
        # terminar posteriormente
        pass

    def fazer_animacao(self, tipo):
        if tipo == "idle":
            #(terminar)
            pass

        if tipo == "morte_enemy":
            #(terminar)
            pass

        if tipo == "deslocamento":
            #(terminar)
            pass
    
    def dispara_projetil(self, outro):
        velocidade = 10   # definir posteriormente
        direcao = -1 if self.pos_x > outro.pos_x else 1
        distancia_disparo = 10 #distancia minima para o inimigo atirar contra poo
                               #definir posteriormente
        proj_ativo =True    
        largura_proj = 10 # definir posteriormente
        altura_proj = 10  # definir posteriormente
        if (self.pos_x - outro.pos_x) <= distancia_disparo :
                projetil = pj(
                    velocidade_projetil= velocidade,
                    pos_x_projetil=self.pos_x, #por estar na classe inimigo, o puxam-se os dados de posicao e assim o ferrao parte da posicao do inimigo
                    pos_y_projetil=self.pos_y, #por estar na classe inimigo, o puxam-se os dados de posicao e assim o ferrao parte da posicao do inimigo
                    direcao= direcao,
                    ativo = proj_ativo,
                    largura_proj = largura_proj,
                    altura_proj = altura_proj
        )
        return projetil
        

def main():
    pygame.init()
    tela = pygame.display.set_mode((COMPRIMENTO_TELA,ALTURA_TELA))
    pygame.display.set_caption("jogo poo")
    clock = pygame.time.Clock()
    running = True

    sprite_poo = {
    "pooh_idle_sprites": [],
    "pooh_movimento_D_sprites": [],
    "pooh_movimento_E_sprites": [],
    "pooh_movimento_U_sprites": [] 
    }

    poo = Player(
    id_game=1,
    amount_honey_coletada= None,
    name_character="Pooh",
    id_character=0,
    sprite=sprite_poo,
    pos_x= None,    #definir quando o mapa ficar pronto
    pos_y= None,   #definir quando o mapa ficar pronto
    vida=10,
    tam_x=50,   #a definir conforme a sprite
    tam_y=70,   #a definir conforme a sprite
    speed=5,
    no_chao=True,
    speed_jump=10
    )
    sprite_leitao = {
    "leitao_idle_sprites": []
    }

    leitao = Npc(
        id_game =1,
        name_character= "Leitao",
        id_character= 2,
        sprite = sprite_leitao,
        pos_x= None,    #definir quando o mapa ficar pront
        pos_y= None,    #definir quando o mapa ficar pront
        text_box= "",   #definir a frase do npc
        vida = None,    #npc não morre
        tam_x= None,    #definir conforme a sprite
        tam_y= None,    #definir conforme a sprite
    )

    sprite_inimigo = {
    "inimigo_idle_sprites": [],
    #como a abelha apenas sobe e desce, é necessário somente a sprite dela em idle

    }

    abelha = Inimigo(
        id_game=1,
        name_character= "Abelha",
        id_character=1,
        sprite = sprite_inimigo,
        vida=10,
        tam_x=None,
        tam_y= None,
        speed=10,
        inimigo_ativo= True,
 )
    sprite_boss = {
    "boss_idle_sprites": [],
    "boss_movimento_D_sprites": [],
    "boss_movimento_E_sprites": [],
    "boss_movimento_U_sprites": [],

    }

    boss = Inimigo(
        id_game=1,
        name_character= "Boss",
        id_character=3,
        sprite = sprite_boss,
        vida=10,
        tam_x=None,
        tam_y= None,
        speed=10,
        inimigo_ativo= True,
    )

    projeteis_ativos = []

    ultimo_disparo_abelha = pygame.time.get_ticks()
    intervalo_disparo = 1500 # 1.5 segundos

    while running:
        for event in pygame.event.get():
                    if event.type == pygame.QUIT:

                        running = False
        poo.movimento()
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - ultimo_disparo_abelha > intervalo_disparo:
                        # A abelha dispara um projétil
            novo_proj = boss.dispara_projetil(poo)
            if novo_proj.ativo == True:
                projeteis_ativos.append(novo_proj)
                ultimo_disparo_abelha = tempo_atual
                while novo_proj.ativo == True:
                    novo_proj.atualizar()           

    tela.fill((0, 0, 0))
    pygame.display.flip()
    clock.tick(60)
    pygame.quit()

if "__main__" == __name__:
    main()
