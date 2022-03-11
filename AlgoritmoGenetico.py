from random import randint

class AlgoritmoGenetico():

    def __init__(self, min, max, populacao, mutacao, crossover, geracoes):

        self.min =  min
        self.max = max
        self.tamPopulacao = populacao
        self.mutacao = mutacao
        self.crossover = crossover
        self.geracoes = geracoes
        # inicializa uma população inviduos vazios
        self.populacao = [[] for i in range(self.tamPopulacao)]
        self.avaliacao = []

        qtdMinBit = self.calculaBits(min)
        qtdMaxBit = self.calculaBits(max)        

        if qtdMaxBit >= qtdMinBit:
            self.numBits = qtdMaxBit 
        else:
            self.numBits = qtdMinBit 
        
        self.geraPopulacao()
    
    def getGeracoes(self):
        return self.geracoes

    def setPopulacao(self, populacao):
        self.populacao = populacao

    ### Calcula os Bits
    def calculaBits(self, qtd):
        return len(bin(qtd).replace('0b', '' if qtd < 0 else '+'))

    ### Gera a População
    def geraPopulacao(self):               
        # preenche a população
        for individuo in self.populacao:

            # para cada individuo da população sorteia números entre "x_min" e "x_max"
            numero = randint(self.min, self.max)

            # converte o número sorteado para formato binário com sinal
            numero_binario = bin(numero).replace('0b', '' if numero < 0 else '+').zfill(self.numBits)

            # transforma o número binário resultante em um vetor
            for bit in numero_binario:
                individuo.append(bit)


    ### Realiza a avaliação do indivíduo
    def avaliar(self):     
        for individuo in self.populacao:
            self.avaliacao.append(self.objetivo(individuo))   


    ### Função para retornar o resultado de f(x) = x*x - 3x + 4
    def objetivo(self, binario):
        # converte o número binário para inteiro
        x = int(''.join(binario), 2)

        # calcula a função x*x - 3x + 4
        return x*x -3*x + 4

    
    def selecaoIndividuo(self):
        # Agrupa os individuos com suas avaliações
        participantes = [self.populacao, self.avaliacao]

        # Escolhe dois individuos aleatoriamente
        individuoA = participantes[randint(0, self.tamPopulacao - 1)]
        individuoB = participantes[randint(0, self.tamPopulacao - 1)]

        # Retorna individuo com a maior avaliação
        return individuoA[0] if individuoB[1] >= individuoB[1] else individuoB[0]

    ### Ajusta o individuo de acordo com limite mais próximo
    def ajustar(self, individuo):

        if int(''.join(individuo), 2) < self.min:
            ajusta = converteBinario(self.min)

            for indice, bit in enumerate(ajusta):
                individuo[indice] = bit

        elif int(''.join(individuo), 2) > self.max:
            # se o individuo é maior que o limite máximo, ele é substituido pelo próprio limite máximo
            ajusta = converteBinario(self.max)
            for indice, bit in enumerate(ajusta):
                individuo[indice] = bit

    ### Busca o individuo com a melhor avaliação
    def filhoApto(self):
        candidatos = zip(self.populacao, self.avaliacao)
        return max(candidatos, key=lambda elemento: elemento[1])                

    ### Realiza a mutação dos bits
    def fazMutacao(self, individuo):
        # cria a tabela com as regras de mutação
        tabelaMutacao = str.maketrans('+-01', '-+10')
        # caso a taxa de mutação seja atingida, ela é realizada em um bit aleatório
        if randint(1,100) <= self.taxa_mutacao:
            bit = randint(0, self.numBits - 1)
            individuo[bit] = individuo[bit].translate(tabelaMutacao)

        # Se o individuo estiver fora dos limites, ele é ajustado de acordo com o limite mais próximo
        self.ajustar(individuo)

    
    ### Crossover
    def fazCrossover(self, pai, mae):
        if randint(1,100) <= self.crossover:
            # caso o crossover seja aplicado os pais trocam suas caldas e com isso geram dois filhos
            corte = randint(1, self.numBits - 1)
            filhoA = pai[:corte] + mae[corte:]
            filhoB = mae[:corte] + pai[corte:]
            # se algum dos filhos estiver fora dos limites de x, ele é ajustado de acordo com o limite mais próximo
            self.ajustar(filhoA)
            self.ajustar(filhoB)    
        else:
            # caso contrário os filhos são cópias exatas dos pais
            filhoA = pai[:]
            filhoB = mae[:]

        # retorna os filhos obtidos pelo crossover
        return (filhoA, filhoB)


def main():

    algoritmoGenetico = AlgoritmoGenetico(-10, 10, 30, 1, 70, 50)

    algoritmoGenetico.avaliar()

    # executa o algoritmo por "num_gerações"
    for i in range(algoritmoGenetico.getGeracoes()):
        # imprime o resultado a cada geração, começando da população original
        print( 'Resultado {}: {}'.format(i, algoritmoGenetico.filhoApto()) )
        # cria uma nova população e a preenche enquanto não estiver completa
        nova_populacao = []
        while len(nova_populacao) < algoritmoGenetico.tamPopulacao:
            # seleciona os pais
            pai = algoritmoGenetico.selecaoIndividuo()
            mae = algoritmoGenetico.selecaoIndividuo()
            # realiza o crossover dos pais para gerar os filhos
            filhoA, filhoB = algoritmoGenetico.fazCrossover(pai, mae)
            # realiza a mutação dos filhos e os adiciona à nova população
            algoritmoGenetico.fazMutacao(filhoA)
            algoritmoGenetico.fazMutacao(filhoB)
            nova_populacao.append(filhoA)
            nova_populacao.append(filhoB)
        # substitui a população antiga pela nova e realiza sua avaliação
        algoritmoGenetico.setPopulacao(nova_populacao)
        algoritmoGenetico.avaliar()

    # procura o filho mais apto dentro da população e exibe o resultado do algoritmo genético
    print( 'Resultado {}: {}'.format(i+1, algoritmoGenetico.filhoApto()) )

    # encerra a execução da função main
    return 0

if __name__ == '__main__':
    main()
