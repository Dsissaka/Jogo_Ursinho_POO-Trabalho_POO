from abc import ABC, abstractmethod
import pygame

ALTURA_TELA = 1080
COMPRIMENTO_TELA = 1920
GRAVIDADE = 1

class Jogo:
    def __init__(self, id_game, status):
        self.id_game = id_game # pode ser usado para recuperar logs de sessões passadas
                                #podemos usar escrita em arquivos para isso
        self.status= status #0 = parado/ 1 = rodando/ 2 = segundo plano

class Background(Jogo):
    def __init__(self, id_game, amount_honey, status, id_background, name_background, sprite_background):
        super().__init__(id_game, status)
        self.name_background = name_background #nome do mapa
        self.amount_honey= amount_honey #quantiade de méis disponiveis pelo mapa
        self.id_background = id_background #usado para identificar possiveis variações para um mesmo cenário (ex:versão noite e versão dia)
        self.sprite_background = sprite_background

class Plataforma(Background):
    def __init__(self, id_game, amount_honey, status,id_background, id_plataforma, name_background, sprite_background, posx_plataforma, posy_plataforma, largura, altura):
        super().__init__(id_game, amount_honey, status, id_background, name_background, sprite_background)
        self.id_plataforma =  id_plataforma #id especifico para pré-definicação e uma plataforma
        self.posx_plataforma =  posx_plataforma # posicionamento no eixo X da plataforma responsavel pela ilusao de movimento
        self.posy_plataforma = posy_plataforma # posicionamento no eixo Y da plataforma
        self.largura = largura #comprimento da plataforma
        self.altura = altura #altura da plataforma

class Honey(Background):
    def __init__(self, id_game, amount_honey, status, id_background, name_background, sprite_background,posx_honey, posy_honey, tam_x, tam_y, ativo):
        super().__init__(id_game, amount_honey, status, id_background, name_background, sprite_background)
        self.posx_honey= posx_honey #posicao no eixo X do mel
        self.posy_honey= posy_honey #posicao no eixo Y do mel
        self.tam_x=tam_x
        self.tam_y=tam_y
        self.ativo = ativo

    def desavitar(self):
        self.ativo= False

    def verifica_colisao(self, outro):
        hitbox_mel = pygame.Rect(self.posx_honey, self.posy_honey, self.tam_x, self.tam_y)
        hitbox_outro = pygame.Rect(outro.pos_x, outro.pos_y, outro.tam_x, outro.tam_y)
        return hitbox_mel.colliderect(hitbox_outro)

    def coleta_mel(self):
        self.amount_honey= self.amount_honey - 1
        self.desavitar()


class Personagens(Jogo):
    def __init__(self, id_game, status, id_character, sprite,  name_character, pos_x, pos_y, vida, tam_x, tam_y):
        super().__init__(id_game, status)
        self.id_character= id_character #id de identificação do personagem
        self.sprite= sprite #biblioteca responsavel por armazenar as sprites dos personagens
        self.name_character= name_character #nome do personagem
        self.pos_x = pos_x #posicao no eixo X do personagem em relação ao mapa
        self.pos_y= pos_y #posicao no eixo Y do personagem em relação ao mapa
        self.vida = vida #contador de vida do personagem
        self.tam_x = tam_x #altura do personagem
        self.tam_y = tam_y # largura do personagem

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

class Npc(Personagens, ABC):
    def __init__(self, id_game, name_character, status, id_character, sprite, pos_x, pos_y, text_box, vida, tam_x, tam_y):
        super().__init__(id_game, status, id_character, sprite,  name_character, pos_x, pos_y, vida, tam_x, tam_y)
        self.text_box=text_box #frase dita pelo npc ao haver colisão com o personagem principal

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
    
class Player(Personagens, ABC):
    def __init__ (self, id_game, name_character, status, id_character, sprite, pos_x, pos_y, vida, tam_x, tam_y, speed, no_chao, speed_jump, amount_honey_coletada):
        super().__init__(id_game, status, id_character, sprite, name_character, pos_x, pos_y, vida, tam_x, tam_y)
        self.amount_honey_coletada = amount_honey_coletada #quantidade de mel coletada pelo personagem
        self.speed = speed #velocidade de movimento do personagem
        self.no_chao = no_chao #variável para definir o contato do poo com o chão
        self.speed_jump = speed_jump

    def verifica_colisao(self, outro):
        hitbox_player = pygame.Rect(self.pos_x, self.pos_y, self.tam_x, self.tam_y)
        hitbox_outro = pygame.Rect(outro.pos_x, outro.pos_y, outro.tam_x, outro.tam_y)
        return hitbox_player.colliderect(hitbox_outro)

       
    def movimento(self):
        self.speed_jump = 3
        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_LEFT]:
            self.pos_x -= self.speed
        if tecla[pygame.K_RIGHT]:
            self.pos_x += self.speed
        if tecla[pygame.K_UP]:
            self.pos_y += self.speed
            while self.no_chao == False: 
                self.speed_jump= self.speed -1
            self.no_chao = True



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

class Inimigo(Personagens, ABC):
    def __init__(self, id_game, name_character, status, id_character, sprite, pos_x, pos_y, text_box, vida, tam_x, tam_y, speed, inimigo_ativo, ativo):
        super().__init__(id_game, status, id_character, sprite,  name_character, pos_x, pos_y, vida, tam_x, tam_y)
        self.ativo = ativo
        self.inimigo_ativo= inimigo_ativo
        self.text_box= text_box
        self.speed= speed 

    def verifica_colisao(self, outro):
        hitbox_inimigo = pygame.Rect(self.pos_x, self.pos_y, self.tam_x, self.tam_y)
        hitbox_outro = pygame.Rect(outro.pos_x, outro.pos_y, outro.tam_x, outro.tam_y)
        return hitbox_inimigo.colliderect(hitbox_outro)


    def dispara_projetil(self, outro, largura_tela):
        velocidade = None   # definir posteriormente
        direcao = None      # definir posteriormente
        distancia_disparo = None #distancia minima para o inimigo atirar contra poo
        proj_ativo =True    
        largura_proj = None # definir posteriormente
        altura_proj = None  # definir posteriormente
        if (self.pos_x - outro.pos_x) <= distancia_disparo :
                projetil = Projetil(
                    velocidade_projetil= velocidade,
                    pos_x_projetil=self.pos_x, #por estar na classe inimigo, o puxam-se os dados de posicao e assim o ferrao parte da posicao do inimigo
                    pos_y_projetil=self.pos_y, #por estar na classe inimigo, o puxam-se os dados de posicao e assim o ferrao parte da posicao do inimigo
                    direcao= direcao,
                    ativo = proj_ativo,
                    largura_proj = largura_proj,
                    altura_proj = altura_proj
        )
        
        while projetil.ativo:
            projetil.atualizar(outro, largura_tela)

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
        
class Projetil:
    def __init__(self, velocidade_projetil, pos_x_projetil, pos_y_projetil, hitbox_projetil, direcao, ativo, largura_proj, altura_proj):
        self.velocidade_projetil = velocidade_projetil
        self.pos_x_projetil = pos_x_projetil
        self.pos_y_projetil = pos_y_projetil
        self.hitbox_projetil = hitbox_projetil
        self.direcao = direcao #1 para direita/ -1 para esquerda
        self.ativo = ativo 
        self.altura_proj = altura_proj
        self.largura_proj = largura_proj

    def desativar(self):
        #função para causar a exclusão da bala após ela sair do mapa ou após acertar o jogador
        self.ativo = False
        #terminar implementar posteriormente

    def mover(self):
        self.pos_x_projetil = self.pos_x_projetil + (self.velocidade_projetil*self.direcao)

    def verifica_colisao(self, outro):
        hitbox_projetil = pygame.Rect(self.pos_x_projetil, self.pos_y_projetil, self.largura_proj, self.altura_proj)
        hitbox_outro = pygame.Rect(outro.pos_x, outro.pos_y, outro.tam_x, outro.tam_y)
        return hitbox_projetil.colliderect(hitbox_outro)


    def atualizar(self, outro, largura_tela):
        while self.ativo:
            self.mover()
            if self.verifica_colisao(outro):
                outro.vida = outro.vida - 1 #caso atingido, O player perde uma vida
                self.desativar() #exclui a bala 
                return
            if self.pos_x_projetil < 0 or self.pos_x_projetil > largura_tela: #caso saia do mapa
                self.desativar()
                return
                #(decidir se talvez definir um timeout para chamada da função "atualizar" ou faze quando "verificar_colisão" for true)


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
    status=1,
    id_character=0,
    sprite=sprite_poo,
    pos_x= None,
    pos_y= None,
    text_box="",
    vida=10,
    tam_x=50,
    tam_y=70,
    speed=5,
    no_chao=True,
    speed_jump=10
)


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    tela.fill((0, 0, 0))
    pygame.display.flip()
    clock.tick(60)
    pygame.quit()

if "__main__" == __name__:
    main()
