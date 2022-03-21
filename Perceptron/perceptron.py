
import random
import matplotlib as plt
import numpy as np
import pandas as pd


class Perceptron():
    def __init__(self, aprendizagem): # taxa de aprendizado 
        self.aprendizagem=aprendizagem
        self.pesos = [0,0,0]
        self.bias=1
        self.inicio=0
    
        self.dataset=np.array([
            [0,0,0], [0,1,0], [1,0,1], [1,1,1]
            ])
       
    
    # funcao que checa se o valor calculado dos pesos e dos elementos, dá o valor esperado
    def prever (self, net_input,pesos): # net_input é a cada "elemento" do vetor dataset
        ativacao = self.pesos[0]
       
        for i in range(len(net_input)):
            # 1 elemento da soma é a somatoria do bias e do primeiro peso
            if i==0:
                ativacao+= self.bias*self.pesos[i]
                # wi*ni, wi sendo o peso na posição i
            else:
                ativacao+=self.pesos[i] * net_input[i-1]
        return 1.0 if ativacao > 0.0 else 0.0 
    
    
    def ajustaPeso(self):
       # elemento aleatorio do dataset escolhido para montarmos o peso
        valor_escolhido = random.randint(0,3)
      
        # passa a coluna escolhida e o peso
        previsao = self.prever(self.dataset[valor_escolhido], self.pesos)
        # retorna o erro; se erro for 0, os pesos se permanecem
        erro = self.dataset[valor_escolhido][-1] - previsao
     
        self.pesos[0] =self.pesos[0] + self.aprendizagem * erro
    	
        for i in range(len(self.dataset[valor_escolhido])-1):
          self.pesos[i + 1] = self.pesos[i + 1] + (self.aprendizagem * erro * self.dataset[valor_escolhido][i])
        
             
    def resolver(self):
        while self.inicio<len(self.dataset):
            self.inicio=0 # caso o peso nao tenha batido com todos os resultados esperados
            # reinicia o inicio pra tentar achar outro peso que bata
            for row in self.dataset:
                previsao = self.prever(row, self.pesos)
                if row[-1]-previsao!=0: # erro diferente de 0, logo o valor
                # recebido e o esperado são diferentes
                    self.ajustaPeso()
                else:
                    self.inicio= self.inicio+1
                    
        for row in self.dataset:
            previsao = self.prever(row, self.pesos)
            print("Valor esperado = %d, Valor recebido = %d"% (row[-1], previsao))
        
        print("Pesos finais")
        print(self.pesos)
        
if __name__ == '__main__':
    taxa_aprendizagem = 0.1
   
    
    perc = Perceptron(taxa_aprendizagem)
    perc.resolver()
    