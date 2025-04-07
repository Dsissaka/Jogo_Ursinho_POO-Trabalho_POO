# Ursinho-POO

## Objetivo
Fazer um jogode plataforma do ursinho pooh, onde o ursinho pega busca pegar uma quantidade limitada de potes de mel,<br> e como principais inimigos/antagonistas tais como: abelhas e ursos.

## Personagens

### Player
* Ursinho Pooh
### NPC
* Leitão
### Inimigos
* Abelhas (Movimentação Vertical);
* Ursos(Movimento Horizontal)
* Boss(Abelha Rainha que seria um inimigo com projetil)

### Funcionamento
O ursinho pooh deve coletar os mels enquanto evito os inimigos. Ele possui 3 corações que são perdidos caso ocorra contato com os inimigos (os corações não são recuperaveis), após todos os mels serem coletados a Abelha Rainha aparecerá e ela poderá lançar uma quantidade de ferroes dos quais o player deverá desviar após essa quantidade ela entrará em cooldown por um certo periodo de tempo, e nesse momento poderemos ativar uma manguira que causa um dano de um coração de vida da Abelha. Assim que ela é derrotada o player ganha o jogo.

### Ideias
* Classes
```
Uma Classe p jogo (classe Pai);
{
  Uma Classe para o personagem;
  {
    Um obj para o Player;
    Um obj para os inimigos;
    Um obj para o NPC;
  }
  Uma Classe para o cenario.
}
```
