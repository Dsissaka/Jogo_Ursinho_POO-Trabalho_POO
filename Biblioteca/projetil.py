import pygame

class Projetil:
    def __init__(self, velocidade_projetil, pos_x_projetil, pos_y_projetil, direcao, ativo, largura_proj, altura_proj):
        self.velocidade_projetil = velocidade_projetil
        self.pos_x_projetil = pos_x_projetil
        self.pos_y_projetil = pos_y_projetil
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
                    self.mover()
                    if self.verifica_colisao(outro):
                            outro.vida = outro.vida - 1 #caso atingido, O player perde uma vida
                            self.desativar() #exclui a bala 
                            return
                    if self.pos_x_projetil < 0 or self.pos_x_projetil > largura_tela: #caso saia do mapa
                        self.desativar()

                #(decidir se talvez definir um timeout para chamada da função "atualizar" ou faze quando "verificar_colisão" for true)

        
