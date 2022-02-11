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
            if self.cromossomo[i]=="1":
                nota +=self.valores[i]
                soma_espacos +=self.espacos[i]
            if soma_espacos > self.limite_espacos: # se o tamanho dos produtos levadores forem maiores do que o limite, superou o valor da carga, entao nao eh solucao boa
                nota = 1
            self.nota_avaliacao = nota
            self.espaco_usado = soma_espacos
                
        
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
    #for produto in lista_produtos:
        #print(produto.nome)
    
    espacos = []
    valores = []
    nomes = []
    for produto in lista_produtos:
        espacos.append(produto.espaco)
        valores.append(produto.valor)
        nomes.append(produto.nome)
    limite = 3 # limite de 3 metros cubicos que o caminhão pode carregar
    
    individuo1 = Individuo(espacos, valores, limite) # cria objeto
    
    for i in range(len(lista_produtos)):
        if individuo1.cromossomo[i] == "1": # tá na carga
            print("Nome : %s R$ %s " % (lista_produtos[i].nome, lista_produtos[i].valor))
    