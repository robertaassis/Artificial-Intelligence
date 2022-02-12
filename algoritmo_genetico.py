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
                nota = 1 # nota ruim, pq extrapolou limite
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
    
    def mutacao(self, taxa_mutacao):
        print("Antes %s " % self.cromossomo)
        for i in range(len(self.cromossomo)):
            # se random foi maior que taxa_mutacao entao ocorre a mutacao (troca os genes)
            if random() < taxa_mutacao:
                if self.cromossomo[i]=='1':
                    self.cromossomo[i]='0'
                else:
                    self.cromossomo[i]='1'
        print("Depois %s " % self.cromossomo)            
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
    
    tamanho_populacao = 20
    ag = AlgoritmoGenetico(tamanho_populacao)
    ag.inicializa_populacao(espacos, valores, limite)
    
    for individuo in ag.populacao: # pega cada individuo da populacao e o submete a avaliacao
        individuo.avaliacao()
        
    ag.ordena_populacao()
    for i in range(ag.tamanho_populacao) :
        print("*** INDIVIDUO %s ***\n" % i,
              "Espaços = %s\n" % str(ag.populacao[i].espacos),
              "Valores = %s\n" % str(ag.populacao[i].valores),
              "Cromossomo = %s\n" % str(ag.populacao[i].cromossomo),
              "Nota = %s\n" % ag.populacao[i].nota_avaliacao)
