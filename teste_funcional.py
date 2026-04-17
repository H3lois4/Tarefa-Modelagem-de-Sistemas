"""
EXERCÍCIO 6.4 — Testes Funcionais
Validam o comportamento do sistema do ponto de vista do usuário final,
percorrendo fluxos completos de ponta a ponta.
"""
import unittest
from main import ContaCorrente, Deposito, Saque, PessoaFisica

class TestFluxoAberturaConta(unittest.TestCase):
    """TF-01: Fluxo completo de criação de cliente e abertura de conta."""

    def test_TF01_abertura_conta_corrente(self):
        """TF-01: Um novo cliente deve conseguir abrir uma conta corrente com saldo zero."""
        # Ação
        cliente = PessoaFisica("Igor", "999.999.999-99", "2001-02-28", "Av. I, 9")
        conta = ContaCorrente("201", cliente)
        cliente.adicionar_conta(conta)

        # Verificações
        self.assertEqual(cliente.nome, "Igor")
        self.assertIn(conta, cliente.contas)
        self.assertEqual(conta.saldo_atual(), 0)
        self.assertEqual(conta.agencia, "0001")


class TestFluxoDeposito(unittest.TestCase):
    """TF-02 a TF-03: Fluxos de depósito."""

    def setUp(self):
        self.cliente = PessoaFisica("Julia", "101.101.101-01", "1999-06-15", "Rua J, 10")
        self.conta = ContaCorrente("202", self.cliente)
        self.cliente.adicionar_conta(self.conta)

    def test_TF02_deposito_bem_sucedido(self):
        """TF-02: Após um depósito válido, saldo deve ser atualizado e histórico registrado."""
        self.cliente.realizar_transacao(self.conta, Deposito(2500))
        self.assertEqual(self.conta.saldo_atual(), 2500)
        self.assertEqual(len(self.conta.historico.transacoes), 1)

    def test_TF03_deposito_invalido_nao_altera_saldo(self):
        """TF-03: Tentativa de depósito com valor zero não deve alterar saldo."""
        self.cliente.realizar_transacao(self.conta, Deposito(0))
        self.assertEqual(self.conta.saldo_atual(), 0)


class TestFluxoSaque(unittest.TestCase):
    """TF-04 a TF-05: Fluxos de saque."""

    def setUp(self):
        self.cliente = PessoaFisica("Lucas", "202.202.202-02", "1996-09-30", "Rua L, 11")
        self.conta = ContaCorrente("203", self.cliente)
        self.cliente.adicionar_conta(self.conta)
        self.cliente.realizar_transacao(self.conta, Deposito(1000))

    def test_TF04_saque_bem_sucedido(self):
        """TF-04: Saque com saldo suficiente deve reduzir saldo e registrar no histórico."""
        self.cliente.realizar_transacao(self.conta, Saque(400))
        self.assertEqual(self.conta.saldo_atual(), 600)
        self.assertEqual(len(self.conta.historico.transacoes), 2)  # 1 depósito + 1 saque

    def test_TF05_saque_sem_saldo(self):
        """TF-05: Tentativa de saque acima do saldo não deve reduzir o saldo."""
        self.cliente.realizar_transacao(self.conta, Saque(5000))
        self.assertEqual(self.conta.saldo_atual(), 1000)


class TestFluxoExtratoCompleto(unittest.TestCase):
    """TF-06: Fluxo completo simulando uso real do sistema bancário."""

    def test_TF06_ciclo_completo_deposito_saque_historico(self):
        """TF-06: Simula um ciclo completo — cliente, conta, depósitos, saques e verificação de extrato."""
        # Criação do cliente e conta
        cliente = PessoaFisica("Marina", "303.303.303-03", "1994-03-12", "Av. M, 12")
        conta = ContaCorrente("204", cliente, limite=1000, limite_saques=5)
        cliente.adicionar_conta(conta)

        # Operações
        cliente.realizar_transacao(conta, Deposito(3000))
        cliente.realizar_transacao(conta, Saque(500))
        cliente.realizar_transacao(conta, Deposito(200))
        cliente.realizar_transacao(conta, Saque(100))

        # Verificações de saldo
        self.assertEqual(conta.saldo_atual(), 2600)

        # Verificações de histórico (extrato)
        self.assertEqual(len(conta.historico.transacoes), 4)

        # Verifica tipos no histórico
        from banco import Deposito as Dep, Saque as Saq
        self.assertIsInstance(conta.historico.transacoes[0], Dep)
        self.assertIsInstance(conta.historico.transacoes[1], Saq)


if __name__ == "__main__":
    unittest.main(verbosity=2)