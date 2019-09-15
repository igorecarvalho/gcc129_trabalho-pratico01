from socket import *
import time
import threading

#IP do servidor e a porta utilizada para conexção
ip_servidor = '127.0.0.1'
porta_servidorUDP = 4242

#IP do cliente e a porta do cliente
ip_cliente = '127.0.0.1'
porta_clienteUDP = 4242
porta_clienteTCP = 5005

#Criação do socket UDP
servidorUDP = socket(AF_INET, SOCK_DGRAM)
servidorUDP.bind((ip_servidor, porta_servidorUDP))

#Criação do socket TCP
servidorTCP = socket(AF_INET, SOCK_STREAM)
servidorTCP.bind((ip_cliente, porta_clienteTCP))
servidorTCP.listen(5)

def devolver(msg, addr):
	servidorUDP.sendto(msg, addr)

def calculaRTT():
	while True:
		mensagem_frag, addr = servidorUDP.recvfrom(10)
		print("mensagem recebida:", mensagem_frag.decode())
		devolver(mensagem_frag, addr)

def calculaVazao():

	tempo_inicio = time.time()

	conexao, endereco = servidorTCP.accept()

	path = '/run/media/igorecarvalho/Documentos/UFLA/2019.02/SD/clienteCOPY.py'

	arquivo = open(path, 'wb')

	flag = True
	while flag:
		print('vem dado')
		dados = conexao.recv(1024)
		if dados.decode() == 'SAICARAI':
			flag = False
		else:
			arquivo.write(dados)

	arquivo.close()
	print('saiu do for')
	tempo_fim = time.time()

	tempo_gasto = str(tempo_fim - tempo_inicio)

	conexao.send(tempo_gasto.encode())

def main():
	print('Iniciado!')
	threadRTT = threading.Thread(target=calculaRTT)
	threadRTT.start()

	threadVazao = threading.Thread(target=calculaVazao)
	threadVazao.start()

main()