from random import random # puxa funcao random
import math
        
class Individuo():
    def __init__(self, espacos, geracao = 0): # construtor
        self.espacos = espacos # cada produto vai ocupar um espaco
        self.nota_final = 0
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
        self.nota_final = F6
           
    
    def crossover(self, outro_individuo, taxa_crossover):
        particiona = round(random() * len(self.cromossomo)) # pega numero aleatorio (entre 0 e 1) e multiplica pelo tamanho do cromossomo (tamanho do dominio)
        
    
        # ex: se o numero aleatorio for 0.3 e forem 14 produtos, logo seria 4,2, com o round seria 4, então o corte seria até o cromossomo 4
        
        filho1 = outro_individuo.cromossomo[0:particiona] + self.cromossomo[particiona::]  # :: significa que vai pegar do corte até o final;
        # vai pegar metade (até onde for o corte) dos cromossomos do individuo2 depois a outra metade dos cromossomos do individuo1 (self)
        filho2 = self.cromossomo[0:particiona] + outro_individuo.cromossomo[particiona::] # contrario do filho1
        
        filhos = [Individuo(self.espacos,  self.geracao+1), 
                  Individuo(self.espacos,  self.geracao+1)] # cada filho vai ser um novo membro da classe individuo
        # nova geração por isso + 1
        if random() < taxa_crossover:  
            filhos[0].cromossomo = filho1
            filhos[1].cromossomo = filho2
        else:
            filhos[0].cromossomo = self.cromossomo
            filhos[1].cromossomo = outro_individuo.cromossomo
        
        return filhos
    
    # há uma possibilidade, mesmo que pequena, de mutar os genes
    def mutacao(self, tx_mutacao):
        
        for i in range(len(self.cromossomoLista)):
            # se random foi maior que tx_mutacao entao ocorre a mutacao (troca os genes)
            if random() < tx_mutacao:
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
    
    
class AG(): # vai armazenar objetos do tipo Individuo
    def __init__(self,pop_size): # quantos individuos vou criar
        self.pop_size = pop_size
        self.populacao = [] # vetor de individuos
        self.geracao = 0
        self.mais_otimizado = 0 # qual dos individuos terá a melhor solucao (maior nota) e que nao extrapole o limite
        
    def inicializa_populacao(self, espacos):
        for i in range(self.pop_size):
            self.populacao.append(Individuo(espacos))
        
        self.mais_otimizado=self.populacao[0] # de primeiro palpite, seta o primeiro individuo como melhor solucao
        
         
    # GUARDA O INDIVIDUO COM MELHOR SOLUÇÃO DENTRE TODAS AS GERAÇÕES
    def individuo_destaque(self, individuo): # checa se a nota do individuo recebido é melhor que a nota da melhor solução
        if individuo.nota_final > self.mais_otimizado.nota_final: # mais_otimizado carrega o objeto do individuo
            self.mais_otimizado = individuo # se for, o individuo da melhor solucao muda
       
    def ordenar(self):
        # ordena baseado na nota_final
        self.populacao = sorted(self.populacao, key = lambda populacao: populacao.nota_final,
                                reverse= True)
    def soma_notas(self): # somatorio de todas avaliações dos individuos (que cromossomo==1)
        soma=0
        for individuo in self.populacao:
            soma += individuo.nota_final # nota_final tem todas as somas dos valores
        
        return soma
    # INDIVIDUOS MAIS APTOS = AVALIAÇÃO MAIOR. Quem tem maior avaliação, tem mais chance de ser selecionado
    
    # roleta viciada, retorna id do individuo selecionado
    def roleta(self, soma_notas): # sorteia o pai baseado no valor_sorteado (roleta)
        pai = -1 # nao selecionou nenhum individuo
        valor_aleatorio = random() * soma_notas
        soma, i =0, 0
       
        while i<len(self.populacao) and soma < valor_aleatorio:
            soma += self.populacao[i].nota_final
            pai+=1
            i += 1
        # ex: se a soma_notas for 50000 e for multiplicado por 0.4, será 20000.
        # depois ele pegará a nota_final de cada individuo nessa populacao e somar
        # quando o valor de soma for maior que o valor sorteado, será escolhido o pai (para o crossover)
        return pai # retorna indice do pai selecionado

    def cromossomo_otimizado(self):# qual espaço e qual cromossomo utilizado
        melhor = self.populacao[0] # vetor ordenado, logo 0 será o melhor
        #print("G:%s -> Cromossomo: %s" % (self.populacao[0].geracao,
              # melhor.cromossomo))
    
    
    def otimizar(self, tx_mutacao, num_ger, espacos, minimo, maximo, total_indiv, taxa_crossover):
        # POPULAÇÃO INICIAL
        self.inicializa_populacao(espacos) # geração da população
       
        # converte binário pra decimal
        for pop in self.populacao:
            # conversão de base
            pop.x = pop.converte_base(int(pop.x))
            pop.y = pop.converte_base(int(pop.y))
            
            # decodificação
            pop.x = minimo + round(pop.x * ((maximo-minimo)/(pow(2,espacos/2)-1)), 4)
            pop.y = minimo + round(pop.y * ((maximo-minimo)/(pow(2,espacos/2)-1)), 4)
            
            pop.avaliacao()
        
        self.ordenar()
      
        # for i in range(self.tamanho_populacao) :
        #      print("*** INDIVIDUO %s ***\n" % i,
        #       "Espaços = %s\n" % str(algoritmo.populacao[i].espacos),
        #       "X = %s\n" % str(algoritmo.populacao[i].x),
        #       "Y = %s\n" % str(algoritmo.populacao[i].y),
        #        "Cromossomo = %s\n" % str(algoritmo.populacao[i].cromossomo),
        #       "Nota = %s\n" % algoritmo.populacao[i].nota_final)
            
        self.cromossomo_otimizado() # pega o melhor individuo de cada populacao(geração) 
        # (escolhe o melhor individuo entre 20 individuos (tamanho_populacao) dessa geração)
        
        # seleciona pais, crossover, mutaçao
        # vai fazer a comparação do individuo_destaque da população inicial com o
        # de todas as outras gerações
        
        for geracao in range(num_ger):
            soma_notas = self.soma_notas()
            nova_populacao = []
            
            for individuos_gerados in range(0, self.pop_size, 2):
                pai_1= self.roleta(soma_notas)
                pai_2= self.roleta(soma_notas)
                
               
                
                filhos = self.populacao[pai_1].crossover(self.populacao[pai_2], taxa_crossover)
                
                    
                nova_populacao.append(filhos[0].mutacao(tx_mutacao))
                nova_populacao.append(filhos[1].mutacao(tx_mutacao))
                
            self.populacao = list(nova_populacao) # sobreescrevi população antiga
            
            for pop in self.populacao:
                
                pop.x = pop.converte_base(int(pop.x))
                pop.y = pop.converte_base(int(pop.y))
                
                pop.x = minimo + round(pop.x * ((maximo-minimo)/(pow(2,espacos/2)-1)), 4)
                pop.y = minimo + round(pop.y * ((maximo-minimo)/(pow(2,espacos/2)-1)), 4)
                
                pop.avaliacao()
            
            self.ordenar()
            self.cromossomo_otimizado()
            
            melhor = self.populacao[0]
            self.individuo_destaque(melhor)
        
        
        return self.mais_otimizado # vai retornar o cromossomo da melhor solução
        
if __name__ == '__main__': 
   
    espacos = 44 # bits
    minimo = -100
    maximo = 100
    pop_size = 100
    tx_mutacao = 0.01
    num_ger = 40
    taxa_crossover = 0.65
    total_ind = pop_size * num_ger
    algoritmo = AG(pop_size)
    
    
    final = algoritmo.otimizar(tx_mutacao, num_ger, espacos, minimo, maximo, total_ind, taxa_crossover)
    
    print("\nMelhor otimização encontrada: Geração -> %s Valor: %s Cromossomo: %s X: %s Y: %s" %
          (final.geracao, final.nota_final,
           final.cromossomo, final.x, final.y))