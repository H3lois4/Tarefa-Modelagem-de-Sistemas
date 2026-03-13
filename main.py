from abc import ABC, abstractmethod

# Interface Transacao
class Transacao(ABC):

    @abstractmethod
    def registrar(self, conta):
        pass

# Classe Deposito
class Deposito(Transacao):

    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        conta.depositar(self.valor)

# Classe Saque
class Saque(Transacao):

    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        conta.sacar(self.valor)

# Classe Historico
class Historico:

    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

# Classe Conta
class Conta:

    def __init__(self, numero, cliente):
        self.saldo = 0
        self.numero = numero
        self.agencia = "0001"
        self.cliente = cliente
        self.historico = Historico()

    def saldo_atual(self):
        return self.saldo

    def sacar(self, valor):

        if valor > self.saldo:
            print("Saldo insuficiente")
            return False

        self.saldo -= valor
        return True

    def depositar(self, valor):

        if valor <= 0:
            print("Valor inválido")
            return False

        self.saldo += valor
        return True

# ContaCorrente (herança)
class ContaCorrente(Conta):

    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

# Classe Cliente
class Cliente:

    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
        conta.historico.adicionar_transacao(transacao)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

# PessoaFisica (herança)
class PessoaFisica(Cliente):

    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento