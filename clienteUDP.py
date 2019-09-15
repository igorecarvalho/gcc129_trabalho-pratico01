import time
from socket import *
import os

path = '/run/media/igorecarvalho/Documentos/UFLA/2019.02/SD/cliente.py'

#IP do servidor e a porta utilizada para conexção
ip_servidor = '127.0.0.1'
porta_servidorUDP = 4242
porta_servidorTCP = 5005

#IP do cliente e a porta do cliente
ip_cliente = '127.0.0.1'

#Criação do socket UDP
clienteUDP = socket(AF_INET, SOCK_DGRAM)
#clienteUDP.bind((ip_servidor, porta_servidorUDP))

#Criação do socket TCP
clienteTCP = socket(AF_INET, SOCK_STREAM)
clienteTCP.connect((ip_servidor, porta_servidorTCP))

def receber_mensagem():
	mensagem = clienteUDP.recvfrom(512)
	return mensagem

def enviar_mensagem(mensagem):
	clienteUDP.sendto(mensagem.encode(), ((ip_servidor, porta_servidorUDP)))
	return receber_mensagem()

def calculaRTT():
	#numero de vezes pra ping
	pingNumero = 10
	cont = 0

	rtt_medio = 0

	mensagem = 'teste'

	while pingNumero > cont:

		tempo_inicio = time.time()
		msg_recebida = enviar_mensagem(mensagem)
		tempo_fim = time.time()
		rtt_medio = rtt_medio + (tempo_fim - tempo_inicio)
		cont = cont+1
	
	return str(rtt_medio/pingNumero)

def calculaVazao():

	arquivo = open(path, 'rb')

	for i in arquivo.readlines():
		clienteTCP.send(i)
		#print('enviando..')

	clienteTCP.send('SAICARAI'.encode())

	arquivo.close()
	#print('saiu aqui tbm')
	tempo_gasto = clienteTCP.recv(1024)
	clienteTCP.close()
	return tempo_gasto.decode()

def main():
    menu = True
    while(menu):
        saida = '1 - RTT. \n2 - Vazão. \n3 - Taxa de perda de pacotes. \n4 - Sair \n'
        opcao = input(saida)
        if opcao == '1':
            print('Teste de RTT')
            print('Tempo gasto: ', calculaRTT(), 's')
        elif(opcao == '2'):
        	print('Teste Vazão')
        	statinfo = os.stat(path)
        	print('Tamanho do arquivo: ', statinfo.st_size, 'bytes')

        	tempo = calculaVazao()
        	print('Tempo gasto para recebimento: ', tempo, 's')

        	print('Vazão: ', float(statinfo.st_size)/float(tempo), 'b/s')
        elif(opcao == '3'):
            print('Iniciando teste de taxa de perda de pacotes')
        elif(opcao == '4'):
            menu = False
        else:
            print('entrada invalida:\n')
main()