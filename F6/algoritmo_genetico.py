from random import random # puxa funcao random
import math
        
class Individuo():
    def __init__(self, espacos, geracao = 0): # construtor
        self.espacos = espacos # cada produto vai ocupar um espaco
        self.nota_avaliacao = 0
        self.geracao = geracao
        self.x = 0
        self.y = 0
        self.cromossomoLista = []
        self.cromossomo = '' # ainda sem solucao
        
        for i in range(espacos): # quantidade de espacos no vetor
            if random() < 0.5: # 50% de probabilidade de ser 0 ou 1; numero aleatorio
                self.cromossomo+="0" # nao vou levar no caminhao
                self.cromossomoLista.append("0")
            else:
                self.cromossomo+="1" # vou levar
                self.cromossomoLista.append("1")
                
        corte = round(espacos/2)
        self.x = self.cromossomo[0:corte] 
        self.y = self.cromossomo[corte::]
        
       
        
    def avaliacao(self): # nova funcao na classe; avalia individuos mais apropriados
        F6 = 0
        
        F6 = 0.5 - ((pow(math.sin(math.sqrt(pow(self.x,2) + pow(self.y,2))),2)-0.5)/pow(1 + 0.001*(pow(self.x,2) + pow(self.y,2)),2))
        self.nota_avaliacao = F6
           
    
    def crossover(self, outro_individuo):
        corte = round(random() * len(self.cromossomo)) # pega numero aleatorio (entre 0 e 1) e multiplica pelo tamanho do cromossomo (tamanho do dominio)
        
    
        # ex: se o numero aleatorio for 0.3 e forem 14 produtos, logo seria 4,2, com o round seria 4, então o corte seria até o cromossomo 4
        
        filho1 = outro_individuo.cromossomo[0:corte] + self.cromossomo[corte::]  # :: significa que vai pegar do corte até o final;
        # vai pegar metade (até onde for o corte) dos cromossomos do individuo2 depois a outra metade dos cromossomos do individuo1 (self)
        filho2 = self.cromossomo[0:corte] + outro_individuo.cromossomo[corte::] # contrario do filho1
        
        filhos = [Individuo(self.espacos,  self.geracao+1), 
                  Individuo(self.espacos,  self.geracao+1)] # cada filho vai ser um novo membro da classe individuo
        # nova geração por isso + 1
            
        filhos[0].cromossomo = filho1
        filhos[1].cromossomo = filho2
        
        return filhos
    
    # há uma possibilidade, mesmo que pequena, de mutar os genes
    def mutacao(self, taxa_mutacao):
        
        for i in range(len(self.cromossomoLista)):
            # se random foi maior que taxa_mutacao entao ocorre a mutacao (troca os genes)
            if random() < taxa_mutacao:
                if self.cromossomoLista[i]=='1':
                    self.cromossomoLista[i]='0'
                else:
                    self.cromossomoLista[i]='1'
                   
        return self
    
    def converte_base(self, binario): 
        decimal, i = 0, 0
        while(binario != 0): 
            dec = binario % 10
            decimal = decimal + dec * pow(2, i) 
            binario = binario//10
            i += 1
        return decimal
    
    
class AlgoritmoGenetico(): # vai armazenar objetos do tipo Individuo
    def __init__(self,tamanho_populacao): # quantos individuos vou criar
        self.tamanho_populacao = tamanho_populacao
        self.populacao = [] # vetor de individuos
        self.geracao = 0
        self.melhor_solucao = 0 # qual dos individuos terá a melhor solucao (maior nota) e que nao extrapole o limite
        
    def inicializa_populacao(self, espacos):
        for i in range(self.tamanho_populacao):
            self.populacao.append(Individuo(espacos))
        
        self.melhor_solucao=self.populacao[0] # de primeiro palpite, seta o primeiro individuo como melhor solucao
        
      
    def ordena_populacao(self):
        # ordena baseado na nota_avaliacao
        self.populacao = sorted(self.populacao, key = lambda populacao: populacao.nota_avaliacao,
                                reverse= True)
         
    # GUARDA O INDIVIDUO COM MELHOR SOLUÇÃO DENTRE TODAS AS GERAÇÕES
    def melhor_individuo(self, individuo): # checa se a nota do individuo recebido é melhor que a nota da melhor solução
        if individuo.nota_avaliacao > self.melhor_solucao.nota_avaliacao: # melhor_solucao carrega o objeto do individuo
            self.melhor_solucao = individuo # se for, o individuo da melhor solucao muda
       
    def soma_avaliacoes(self): # somatorio de todas avaliações dos individuos (que cromossomo==1)
        soma=0
        for individuo in self.populacao:
            soma += individuo.nota_avaliacao # nota_avaliacao tem todas as somas dos valores
        
        return soma
    # INDIVIDUOS MAIS APTOS = AVALIAÇÃO MAIOR. Quem tem maior avaliação, tem mais chance de ser selecionado
    
    # roleta viciada, retorna id do individuo selecionado
    def seleciona_pai(self, soma_avaliacao): # sorteia o pai baseado no valor_sorteado (roleta)
        pai = -1 # nao selecionou nenhum individuo
        valor_sorteado = random() * soma_avaliacao
        soma=0
        i =0
        while i<len(self.populacao) and soma < valor_sorteado:
            soma += self.populacao[i].nota_avaliacao
            pai+=1
            i += 1
        # ex: se a soma_avaliacao for 50000 e for multiplicado por 0.4, será 20000.
        # depois ele pegará a nota_avaliacao de cada individuo nessa populacao e somar
        # quando o valor de soma for maior que o valor sorteado, será escolhido o pai (para o crossover)
        return pai # retorna indice do pai selecionado

    def visualiza_geracao(self):# qual espaço e qual cromossomo utilizado
        melhor = self.populacao[0] # vetor ordenado, logo 0 será o melhor
        #print("G:%s -> Cromossomo: %s" % (self.populacao[0].geracao,
              # melhor.cromossomo))
    
    
    def resolver(self, taxa_mutacao, numero_geracoes, espacos, minimo, maximo):
        # POPULAÇÃO INICIAL
        self.inicializa_populacao(espacos) # geração da população
        
        # converte binário pra decimal
        for pop in self.populacao:
            
            pop.x = pop.converte_base(int(pop.x))
            pop.y = pop.converte_base(int(pop.y))
            
            pop.x = minimo + round(pop.x * (self.tamanho_populacao/(pow(2,espacos/2)-1)), 5)
            pop.y = maximo + round(pop.y * (self.tamanho_populacao/(pow(2,espacos/2)-1)), 5)
            
            pop.avaliacao()
        
        self.ordena_populacao()
      
        # for i in range(self.tamanho_populacao) :
        #      print("*** INDIVIDUO %s ***\n" % i,
        #       "Espaços = %s\n" % str(ag.populacao[i].espacos),
        #       "X = %s\n" % str(ag.populacao[i].x),
        #       "Y = %s\n" % str(ag.populacao[i].y),
        #        "Cromossomo = %s\n" % str(ag.populacao[i].cromossomo),
        #       "Nota = %s\n" % ag.populacao[i].nota_avaliacao)
            
        self.visualiza_geracao() # pega o melhor individuo de cada populacao(geração) 
        # (escolhe o melhor individuo entre 20 individuos (tamanho_populacao) dessa geração)
        
        # seleciona pais, crossover, mutaçao
        # vai fazer a comparação do melhor_individuo da população inicial com o
        # de todas as outras gerações
        
        for geracao in range(numero_geracoes):
            soma_avaliacao = self.soma_avaliacoes()
            nova_populacao = []
            
            for individuos_gerados in range(0, self.tamanho_populacao, 2):
                pai1= self.seleciona_pai(soma_avaliacao)
                pai2= self.seleciona_pai(soma_avaliacao)
                
                filhos = self.populacao[pai1].crossover(self.populacao[pai2])
                
                nova_populacao.append(filhos[0].mutacao(taxa_mutacao))
                nova_populacao.append(filhos[1].mutacao(taxa_mutacao))
                
            self.populacao = list(nova_populacao) #sobreescrevi população antiga
            
            for pop in self.populacao:
                
                pop.x = pop.converte_base(int(pop.x))
                pop.y = pop.converte_base(int(pop.y))
                
                pop.x = minimo + round(pop.x * (self.tamanho_populacao/(pow(2,espacos/2)-1)), 5)
                pop.y = maximo + round(pop.y * (self.tamanho_populacao/(pow(2,espacos/2)-1)), 5)
                
                pop.avaliacao()
            
            self.ordena_populacao()
            self.visualiza_geracao()
            
            melhor = self.populacao[0]
            self.melhor_individuo(melhor)
        
        print("\nMelhor solução: G -> %s Valor: %s Cromossomo: %s" %
              (self.melhor_solucao.geracao, self.melhor_solucao.nota_avaliacao,
               self.melhor_solucao.cromossomo))
        
        return self.melhor_solucao.cromossomo # vai retornar o cromossomo da melhor solução
        
if __name__ == '__main__': 
   
    espacos = 44 # guarda todos os espaços dos produtos
    minimo = -100
    maximo = 100
    tamanho_populacao = maximo - minimo  # cria 20 individuos com os mesmos espaços e valores, mas cromossomos e notas diferentes
    taxa_mutacao = 0.01
    numero_geracoes = 40
    
    ag = AlgoritmoGenetico(tamanho_populacao)
    
    
    resultado = ag.resolver(taxa_mutacao, numero_geracoes, espacos, minimo, maximo)
    
    