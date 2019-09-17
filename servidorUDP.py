from socket import *
import time
import threading

#IP do servidor e a porta utilizada para conexção
ip_servidor = '127.0.0.1'
porta_servidorUDP = 4242
porta_servidorUDPTP = 4343

#IP do cliente e a porta do cliente
ip_cliente = '127.0.0.1'
porta_clienteTCP = 5005

#Criação do socket UDP - RTT
servidorUDP = socket(AF_INET, SOCK_DGRAM)
servidorUDP.bind((ip_servidor, porta_servidorUDP))

#Criação do socket UDP - Taxa de Perda
servidorUDPerda = socket(AF_INET, SOCK_DGRAM)
servidorUDPerda.bind((ip_servidor, porta_servidorUDPTP))

#Criação do socket TCP - VAZAO
servidorTCP = socket(AF_INET, SOCK_STREAM)
servidorTCP.bind((ip_cliente, porta_clienteTCP))
servidorTCP.listen(5)
path = 'hue-copy.txt'

def devolver(msg, addr):
	servidorUDP.sendto(msg, addr)

def calculaRTT():
	while True:
		mensagem_frag, addr = servidorUDP.recvfrom(10)
		print("mensagem recebida:", mensagem_frag.decode())
		devolver(mensagem_frag, addr)
	
	servidorUDP.close()

def calculaVazao():

	tempo_inicio = time.time()

	conexao, endereco = servidorTCP.accept()

	arquivo = open(path, 'wb')

	flag = True
	while flag:
		#print('vem dado')
		dados = conexao.recv(1024)
		if dados.decode() == 'SAICODE':
			flag = False
		else:
			arquivo.write(dados)

	arquivo.close()
	#print('saiu do for')
	tempo_fim = time.time()

	tempo_gasto = str(tempo_fim - tempo_inicio)

	conexao.send(tempo_gasto.encode())

	servidorTCP.close()

def calculaPerda():
	while True:
		cont = 0
		mensagem_frag, addr = servidorUDPerda.recvfrom(1024)
		
		flag = True
		while flag:
			mensagem = mensagem_frag.decode()
			if mensagem == 'SAICODE':
				flag = False
			else:
				cont = cont + 1
				mensagem_frag, addr = servidorUDPerda.recvfrom(1024)
		
		print(cont)
		servidorUDPerda.sendto(str(cont).encode(), addr)

	servidorUDPerda.close()

def main():
	print('Iniciado!')
	threadRTT = threading.Thread(target=calculaRTT)
	threadRTT.start()

	threadVazao = threading.Thread(target=calculaVazao)
	threadVazao.start()

	threadPerda = threading.Thread(target=calculaPerda)
	threadPerda.start()

main()