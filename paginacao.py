import numpy as np

class TLB():
	def __init__(self, tam):
		self.size = tam #Tamanho do TLB
		self.vetorP = np.empty(tam) #Vetor número de página
		self.vetorF = np.empty(tam) #Vetor frame
		self.vetorB = np.zeros(tam) #Vetor bit de validade
		self.filaBit = [] #Bit de verificação para segunda chance
		self.filaP = [] #PseudoFila no modo segunda chance, PseudoPilha no LRU
	def popa(self, i): #Retira elemento do das filas ou pilhas
		if len(self.filaBit):
			self.filaBit.pop(i)
			aux = self.filaP.pop(i)
			#print('Popado: ', aux)
			return aux
		return -1
	def appenda(self, p): #Coloca elementos nas filas ou pilhas
		self.filaBit.append(0) #Com o bit de verificação 0
		self.filaP.append(p)
		return
	def __str__(self):
		a = []
		for i in range(len(myTLB.vetorP)):
			a.append(myTLB.vetorP[i])
		return str(a)

class tabelaPagina():
	def __init__(self):
		self.size = 1048576 #Tamanho da tabela, 2^n, n=20
		self.vetorF = np.empty(1048576) #Vetor de frames
		self.vetorB = np.zeros(1048576) #Vetor de validade

myTLB = TLB(3) #Objeto TLB
myPag = tabelaPagina() #Objeto tabela de pagina
tlbHit = 0 #Numero de hits
tlbMiss = 0 #Numero de miss

def segundaChance(p, f): #Algoritmo segunda chance
	for i in range(len(myTLB.filaBit)): #Dentro do range da fila
		if myTLB.filaBit[i] == 0: #Se o bit de verificação for 0, ja teve chance
			if i>=len(myTLB.filaP):
				print('ERRO')
			aux = myTLB.popa(i) #Pop elemento i, sai da fila
			for j in range(myTLB.size): #Procura posição no vetor do popado
				if aux == myTLB.vetorP[j]:
					myTLB.vetorF[j] = f
					myTLB.vetorP[j] = p
					myTLB.vetorB[j] = 1 #E seta o bit de validação para 0
					myTLB.appenda(p)
					return
		else: #Seta elementos que tiveram segunda chance
			myTLB.filaBit[i] = 0

	#Se nenhum elemento foi ja teve uma segunda chance, FIFO
	aux = myTLB.popa(0) #Popa primeiro
	for k in range(myTLB.size):
		if aux == myTLB.vetorP[k]:
			myTLB.vetorF[k] = f
			myTLB.vetorP[k] = p
			myTLB.vetorB[k] = 1 #E seta o bit de validação para 1
			myTLB.appenda(p)
			return	
	
	print('Problema-----------------') #Caso ocorra algum problema
	return

def LRU(p, f):
	#Se chegou aqui, não hitou, e não existe na pilha, entao
	aux = myTLB.popa(0) #Popa base
	for k in range(myTLB.size): #Acha a posição do popado no vetor
		if aux == myTLB.vetorP[k]:
			myTLB.vetorF[k] = f
			myTLB.vetorP[k] = p
			myTLB.vetorB[k] = 1 #E seta o bit de validação para 0
			myTLB.appenda(p)
			return
	return
def leTrace(arq): #Le linha do arquivo
	aux = arq.readline()
	if(aux):
		linha = aux

	return linha
def separaPD(linha): #Separa pagina do deslocamento
	p = linha[0:5]
	d = linha[5:8]

	return [p,d]
def traduzEndereco(p, d): #Passa p e d para decimal
	return [int(str(p), 16), int(str(d), 16)]
def padroniza(p): #Passa p para o dominio dos frames
	decimal = int(str(p), 16)
	padronizado = (decimal/(4*4096))-(decimal%(4*4096))
	return padronizado
def atualizaTLB(p, f): #Atualiza TLB
	for i in range(myTLB.size): #Se tiver espaço na tabela
		if not(myTLB.vetorB[i]): # Se o bit de validação é zero
			myTLB.vetorF[i] = f # Atribui o frame
			myTLB.vetorP[i] = p # Atribui o numero da pagina
			myTLB.vetorB[i] = 1
			myTLB.appenda(p)
			#print('TLB atualizado')
			return
	#Se não tiver espaço, subtituir pagina
	#Segunda chance
	segundaChance(p, f)
	#LRU
	# LRU(p, f)
	return
def buscaTabelaPagina(p, f): #Busca na tabela de pagina
	#Vai até posicao p do vetor, se for valido atualiza TLB
	if myPag.vetorB[p]: #Verifica bit valido
		#print('Acertou pagina')
		atualizaTLB(p, myPag.vetorF[p])
	else: #Senão, falha de pagina, incluir pagina e atualizar TLB
		#print('Falha de pagina')
		#Falha de pagina, incluir na tabela de pag
		myPag.vetorF[p] = f
		myPag.vetorB[p] = 1
		atualizaTLB(p, f)

	return

def buscaTLB(p, f): #Busca no TLB
	global tlbHit
	global tlbMiss
	for i in range(myTLB.size): #Procura no TBL
		if p == myTLB.vetorP[i]: #Se achou, entao HIT
			#print('TLB HIT')
			tlbHit = tlbHit + 1
			########Segunda chance############
			# Reseta a segunda chance caso tenha um hit
			for j in range(len(myTLB.filaP)): #Procura posição do elemento na fila 
				if p == myTLB.filaP[j]:
					# aux = myTLB.popa(j)
					# myTLB.appenda(aux) #Popa e empilha
					myTLB.filaBit[j] = 1
					return
			print('Problema----------')
			#return
			##############LRU#################################
			# for j in range(len(myTLB.filaP)): #Procura posição do elemento na pilha 
			# 	if p == myTLB.filaP[j]:
			# 		aux = myTLB.popa(j)
			# 		myTLB.appenda(aux) #Popa e empilha
			# 		# myTLB.filaBit[j] = 0
			# 		return

	#print('TLB MISS') #Se não achou, MISS
	tlbMiss = tlbMiss + 1
	buscaTabelaPagina(p, f) #E busca na tabela de pagina
	return 

def dotoTrace(trace):
	arq = open(trace, "r") #Abre arquivo com traces
	for i in range(1000000): #Numero de traces
		#print('TAM ', i)
		linha = leTrace(arq) #Linha contendo o endereço lógico
		PD = separaPD(linha) #PD, p e d separados
		pEd = traduzEndereco(PD[0], PD[1]) #p e d em decimal
		f = padroniza(pEd[0]) #frame=f=p padronizado
		buscaTLB(pEd[0], f) #Inicia busca no TLB

	print('HITS', tlbHit) #Mostra o numero total de hits
	print('MISSES', tlbMiss) #Mostra o numero total de miss

	arq.close()
	return

def dotoVector(vec):
	for i in range(len(vec)):
		buscaTLB(vec[i], 0)
		print(myTLB)
	print('HITS: ', tlbHit)
	print('MISSES: ', tlbMiss)
	return

def main():
	op = input('1 - Arquivo trace, 2 - Input: ')
	if op == '1':
		print('Trace file')
		dotoTrace("bzip.trace")
		print(myTLB)
	else:
		print('Vetor')
		vec = [2,5,10,1,2,2,6,9,1,2,10,2,6,1,2,1,6,9,5,1]
		dotoVector(vec)
		print(myTLB)

	return

if __name__ == '__main__':
	main()