from random import random # puxa funcao random

class Produto():
    def __init__(self, nome, espaco, valor): # construtor
        self.nome = nome
        self.espaco = espaco
        self.valor = valor
        
class Individuo():
    def __init__(self, espacos, valores, limite_espacos, geracao = 0): # construtor
        self.espacos = espacos # cada produto vai ocupar um espaco
        self.valores = valores
        self.limite_espacos = limite_espacos
        self.nota_avaliacao = 0
        self.geracao = geracao
        self.espaco_usado = 0
        self.cromossomo = [] # ainda sem solucao
        
        for i in range(len(espacos)): # quantidade de espacos no vetor
            if random() < 0.5: # 50% de probabilidade de ser 0 ou 1; numero aleatorio
                self.cromossomo.append("0") # nao vou levar no caminhao
            else:
                self.cromossomo.append("1") # vou levar
                
    def avaliacao(self): # nova funcao na classe; avalia individuos mais apropriados
        nota = 0
        soma_espacos = 0
        for i in range(len(self.cromossomo)):
            if self.cromossomo[i]=="1": # avalia todos os individuos que estao no caminhao
                nota +=self.valores[i]
                soma_espacos +=self.espacos[i]
            if soma_espacos > self.limite_espacos: # se o tamanho dos produtos levados forem maiores do que o limite, superou o valor da carga, entao nao eh solucao boa
                nota = 1 # nota ruim, pq extrapolou limite, porém não ignora esse individuo
            self.nota_avaliacao = nota
            self.espaco_usado = soma_espacos
    
    def crossover(self, outro_individuo):
        corte = round(random() * len(self.cromossomo)) # pega numero aleatorio (entre 0 e 1) e multiplica pelo tamanho do cromossomo (tamanho do dominio)
        
        # ex: se o numero aleatorio for 0.3 e forem 14 produtos, logo seria 4,2, com o round seria 4, então o corte seria até o cromossomo 4
        
        filho1 = outro_individuo.cromossomo[0:corte] + self.cromossomo[corte::]  # :: significa que vai pegar do corte até o final;
        # vai pegar metade (até onde for o corte) dos cromossomos do individuo2 depois a outra metade dos cromossomos do individuo1 (self)
        filho2 = self.cromossomo[0:corte] + outro_individuo.cromossomo[corte::] # contrario do filho1
        
        filhos = [Individuo(self.espacos, self.valores, self.limite_espacos, self.geracao+1), 
                  Individuo(self.espacos, self.valores, self.limite_espacos, self.geracao+1)] # cada filho vai ser um novo membro da classe individuo
        # nova geração por isso + 1
            
        filhos[0].cromossomo = filho1
        filhos[1].cromossomo = filho2
        
        return filhos
    
    # há uma possibilidade, mesmo que pequena, de mutar os genes
    def mutacao(self, taxa_mutacao):
        # print("Antes %s " % self.cromossomo)
        for i in range(len(self.cromossomo)):
            # se random foi maior que taxa_mutacao entao ocorre a mutacao (troca os genes)
            if random() < taxa_mutacao:
                if self.cromossomo[i]=='1':
                    self.cromossomo[i]='0'
                else:
                    self.cromossomo[i]='1'
        # print("Depois %s " % self.cromossomo)            
        return self
    
    
class AlgoritmoGenetico(): # vai armazenar objetos do tipo Individuo
    def __init__(self,tamanho_populacao): # quantos individuos vou criar
        self.tamanho_populacao = tamanho_populacao
        self.populacao = [] # vetor de individuos
        self.geracao = 0
        self.melhor_solucao = 0 # qual dos individuos terá a melhor solucao (maior nota) e que nao extrapole o limite
        
    def inicializa_populacao(self, espacos, valores, limite_espacos):
        for i in range(self.tamanho_populacao):
            self.populacao.append(Individuo(espacos, valores, limite_espacos))
        
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
        print("G:%s -> Valor: %s Espaço: %s Cromossomo: %s" % (self.populacao[0].geracao,
              melhor.nota_avaliacao, melhor.espaco_usado, melhor.cromossomo))
    
    
    def resolver(self, taxa_mutacao, numero_geracoes, espacos, valores, limite_espacos):
        # POPULAÇÃO INICIAL
        self.inicializa_populacao(espacos, valores, limite_espacos) # geração da população
       
        for individuo in self.populacao:
            individuo.avaliacao() #avaliação da população
        
        self.ordena_populacao()
      
        # for i in range(self.tamanho_populacao) :
        #     print("*** INDIVIDUO %s ***\n" % i,
        #       "Espaços = %s\n" % str(ag.populacao[i].espacos),
        #       "Valores = %s\n" % str(ag.populacao[i].valores),
        #       "Cromossomo = %s\n" % str(ag.populacao[i].cromossomo),
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
            
            for individuo in self.populacao:
                individuo.avaliacao()
            
            self.ordena_populacao()
            self.visualiza_geracao()
            
            melhor = self.populacao[0]
            self.melhor_individuo(melhor)
        
        print("\nMelhor solução: G -> %s Valor: %s Espaço: %s Cromossomo: %s" %
              (self.melhor_solucao.geracao, self.melhor_solucao.nota_avaliacao,
              self.melhor_solucao.espaco_usado, self.melhor_solucao.cromossomo))
        
        return self.melhor_solucao.cromossomo # vai retornar o cromossomo da melhor solução
        
if __name__ == '__main__': 
    lista_produtos = [] # inicia lista
    lista_produtos.append(Produto("Geladeira Dako", 0.751, 999.90)) # adiciona na lista
    lista_produtos.append(Produto("Iphone 6", 0.0000899, 2911.12))
    lista_produtos.append(Produto("TV 55", 0.400, 4346.99))
    lista_produtos.append(Produto("TV 50", 0.290, 3999.90))
    lista_produtos.append(Produto("TV 42", 0.200, 2999.00))
    lista_produtos.append(Produto("Notebook Dell", 0.00350, 2499.90))
    lista_produtos.append(Produto("Ventilador Panasonic", 0.496, 199.90))
    lista_produtos.append(Produto("Microondas Electrolux", 0.0424, 308.66))
    lista_produtos.append(Produto("Microondas LG", 0.0544, 429.90))
    lista_produtos.append(Produto("Microondas Panasonic", 0.0319, 299.29))
    lista_produtos.append(Produto("Geladeira Brastemp", 0.635, 849.00))
    lista_produtos.append(Produto("Geladeira Consul", 0.870, 1199.89))
    lista_produtos.append(Produto("Notebook Lenovo", 0.498, 1999.90))
    lista_produtos.append(Produto("Notebook Asus", 0.527, 3999.00))
   
    
    espacos = [] # guarda todos os espaços dos produtos
    valores = [] # guarda todos os valores dos produtos
    nomes = [] # guarda todos os nomes dos produtos
    for produto in lista_produtos:
        espacos.append(produto.espaco)
        valores.append(produto.valor)
        nomes.append(produto.nome)
    limite = 3 # limite de 3 metros cubicos que o caminhão pode carregar
    
    tamanho_populacao = 20  # cria 20 individuos com os mesmos espaços e valores, mas cromossomos e notas diferentes
    taxa_mutacao = 0.01
    numero_geracoes = 100
    
    ag = AlgoritmoGenetico(tamanho_populacao)
    
    resultado = ag.resolver(taxa_mutacao, numero_geracoes, espacos, valores, limite)
    
    # vai listar quais produtos vão fazer parte da carga (cromossomo==1)
    # ex: se resultado for 0 0 1 1 0 e retornar nome de 5 produtos, vc fazer a soma dos valores de cada produto e espaços, vai ver que dá o melhor resultado 
    # (maior valor e menos de 3m ocupados)
    for i in range(len(lista_produtos)):
        if resultado[i]=='1':
            print("Nome: %s R$ %s " % (lista_produtos[i].nome, lista_produtos[i].valor))
   