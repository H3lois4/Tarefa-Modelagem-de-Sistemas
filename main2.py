from abc import ABC, abstractmethod

# Interface e classes base (inalteradas)
class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

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

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
        conta.historico.adicionar_transacao(transacao)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        conta.depositar(self.valor)

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        conta.sacar(self.valor)

# NOVA FUNCIONALIDADE: Investimento em Poupança
class Rendimento(Transacao):
    """
    Transacao de rendimento mensal da poupança.
    Aplica a taxa sobre o saldo atual e credita o resultado.
    """
    def __init__(self, taxa_mensal: float):
        if taxa_mensal < 0:
            raise ValueError("Taxa de rendimento não pode ser negativa.")
        self.taxa_mensal = taxa_mensal

    def registrar(self, conta):
        valor_rendimento = round(conta.saldo_atual() * self.taxa_mensal, 2)
        conta.depositar(valor_rendimento)


class ContaPoupanca(Conta):
    """
    Conta Poupança com taxa de rendimento mensal configurável.
    Herda de Conta e adiciona a lógica de aplicar_rendimento().
    Taxa padrão: 0,5% ao mês (referência poupança brasileira).
    """
    TAXA_PADRAO = 0.005

    def __init__(self, numero, cliente, taxa_mensal=TAXA_PADRAO):
        super().__init__(numero, cliente)
        if taxa_mensal < 0:
            raise ValueError("Taxa de rendimento não pode ser negativa.")
        self.taxa_mensal = taxa_mensal

    def aplicar_rendimento(self):
        """
        Calcula e credita o rendimento mensal sobre o saldo atual.
        Registra a operação no histórico da conta.
        """
        rendimento = Rendimento(self.taxa_mensal)
        rendimento.registrar(self)
        self.historico.adicionar_transacao(rendimento)