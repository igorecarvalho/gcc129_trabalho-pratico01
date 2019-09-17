import time
from socket import *
import os

#IP do servidor e a porta utilizada para conexção
ip_servidor = '127.0.0.1'
porta_servidorUDP = 4242
porta_servidorUDPTP = 4343
porta_servidorTCP = 5005

#IP do cliente e a porta do cliente
ip_cliente = '127.0.0.1'

#Criação do socket UDP
clienteUDP = socket(AF_INET, SOCK_DGRAM)
#clienteUDP.bind((ip_servidor, porta_servidorUDP))

#Criação do socket UDP - Taxa de Perda
clienteUDPerda = socket(AF_INET, SOCK_DGRAM)

#Criação do socket TCP
clienteTCP = socket(AF_INET, SOCK_STREAM)
clienteTCP.connect((ip_servidor, porta_servidorTCP))
path = 'hue.txt'

def receber_mensagem():
	mensagem = clienteUDP.recvfrom(1024)
	return mensagem

def enviar_mensagem(mensagem):
	clienteUDP.sendto(mensagem.encode(), ((ip_servidor, porta_servidorUDP)))
	return receber_mensagem()

def calculaRTT(mensagem, num_ping = 10):
	cont = 0
	rtt_medio = 0
	while num_ping > cont:

		tempo_inicio = time.time()
		msg_recebida = enviar_mensagem(mensagem)
		tempo_fim = time.time()
		rtt_medio = rtt_medio + (tempo_fim - tempo_inicio)
		cont = cont+1
	clienteUDP.close()
	return str(rtt_medio/num_ping)

def calculaVazao():
	arquivo = open(path, 'rb')

	for i in arquivo.readlines():
		clienteTCP.send(i)
		print('enviando..')
	saida = 'SAI'
	clienteTCP.send(saida.encode())

	arquivo.close()
	print('saiu aqui tbm')
	tempo_gasto = clienteTCP.recv(1024)
	clienteTCP.close()
	return tempo_gasto.decode()

def calculaPerda(mensagem, num_pcts = 10000):

	for i in range(num_pcts):
		clienteUDPerda.sendto(mensagem.encode(), (ip_servidor, porta_servidorUDPTP))
	mensagem = 'SAI'
	clienteUDPerda.sendto(mensagem.encode(), (ip_servidor, porta_servidorUDPTP))

	mensagem, addr = clienteUDPerda.recvfrom(1024)
	clienteUDPerda.close()
	return mensagem.decode()


def main():
    menu = True
    while(menu):
        saida = '1 - RTT. \n2 - Vazão. \n3 - Taxa de perda de pacotes. \n4 - Sair \n'
        opcao = input(saida)
        if opcao == '1':
            print('Teste de RTT')
            mensagem = input("Digite a msg para envio: ")
            print('Tempo gasto: ', calculaRTT(mensagem), 's')

        elif(opcao == '2'):
        	print('Teste Vazão')
        	statinfo = os.stat(path)
        	print('Tamanho do arquivo: ', statinfo.st_size, 'bytes')

        	tempo = calculaVazao()
        	print('Tempo gasto para recebimento: ', tempo, 's')

        	print('Vazão: ', float(statinfo.st_size)/float(tempo), 'b/s')

        elif(opcao == '3'):
            print('Teste de taxa de perda\n')

            mensagem = input("Digite a msg para envio: ")
            num_pct_recv = calculaPerda(mensagem)
            print('Numero de pcts recebidos: ', num_pct_recv)
            print('Taxa de Perda: ', int(num_pct_recv)/10000, '%')

        elif(opcao == '4'):
            menu = False
        else:
            print('entrada invalida:\n')
main()