from main import *

cliente = Cliente("Rua A")

conta = Conta(numero=1, cliente=cliente)

cliente.adicionar_conta(conta)

deposito = Deposito(1000)
cliente.realizar_transacao(conta, deposito)

saque = Saque(200)
cliente.realizar_transacao(conta, saque)

print("Saldo final:", conta.saldo_atual())