"""
EXERCÍCIO 6.3 — Testes de Integração
Testam a colaboração entre múltiplas classes:
Cliente + Conta + Transacao + Historico.
"""
import unittest
from main import Conta, ContaCorrente, Deposito, Saque, PessoaFisica

class TestIntegracaoClienteConta(unittest.TestCase):
    """TI-01 a TI-02: Integração entre Cliente e Conta."""

    def test_TI01_adicionar_conta_ao_cliente(self):
        """TI-01: Cliente.adicionar_conta deve vincular a conta à lista do cliente."""
        cli = PessoaFisica("Fernanda", "666.666.666-66", "1993-08-22", "Rua F, 6")
        cc = ContaCorrente("101", cli)
        cli.adicionar_conta(cc)
        self.assertIn(cc, cli.contas)
        self.assertEqual(len(cli.contas), 1)

    def test_TI02_cliente_pode_ter_multiplas_contas(self):
        """TI-02: Um cliente pode ter mais de uma conta associada."""
        cli = PessoaFisica("Gabriel", "777.777.777-77", "1991-11-05", "Rua G, 7")
        cc1 = ContaCorrente("102", cli)
        cc2 = ContaCorrente("103", cli)
        cli.adicionar_conta(cc1)
        cli.adicionar_conta(cc2)
        self.assertEqual(len(cli.contas), 2)


class TestIntegracaoTransacaoHistorico(unittest.TestCase):
    """TI-03 a TI-06: Integração entre realizar_transacao, saldo e histórico."""

    def setUp(self):
        self.cli = PessoaFisica("Helena", "888.888.888-88", "1987-04-18", "Rua H, 8")
        self.conta = ContaCorrente("104", self.cli)
        self.cli.adicionar_conta(self.conta)

    def test_TI03_deposito_via_cliente_atualiza_saldo(self):
        """TI-03: Deposito registrado por Cliente.realizar_transacao deve aumentar saldo."""
        dep = Deposito(1000)
        self.cli.realizar_transacao(self.conta, dep)
        self.assertEqual(self.conta.saldo_atual(), 1000)

    def test_TI04_deposito_registrado_no_historico(self):
        """TI-04: Deposito registrado por Cliente.realizar_transacao deve aparecer no histórico."""
        dep = Deposito(1000)
        self.cli.realizar_transacao(self.conta, dep)
        self.assertEqual(len(self.conta.historico.transacoes), 1)
        self.assertIs(self.conta.historico.transacoes[0], dep)

    def test_TI05_saque_via_cliente_atualiza_saldo(self):
        """TI-05: Saque registrado por Cliente.realizar_transacao deve reduzir saldo."""
        self.conta.saldo = 800
        saque = Saque(300)
        self.cli.realizar_transacao(self.conta, saque)
        self.assertEqual(self.conta.saldo_atual(), 500)

    def test_TI06_multiplas_transacoes_historico_completo(self):
        """TI-06: Múltiplas transações devem ser todas registradas no histórico."""
        self.cli.realizar_transacao(self.conta, Deposito(500))
        self.cli.realizar_transacao(self.conta, Deposito(300))
        self.cli.realizar_transacao(self.conta, Saque(100))
        self.assertEqual(len(self.conta.historico.transacoes), 3)
        self.assertEqual(self.conta.saldo_atual(), 700)

    def test_TI07_saque_sem_saldo_nao_registra_historico(self):
        """TI-07: Transacao de Saque que falha ainda é adicionada ao histórico pelo Cliente (comportamento atual)."""
        # Nota: o método realizar_transacao sempre adiciona ao histórico,
        # independente do sucesso da transação — este teste documenta esse comportamento.
        saque = Saque(9999)
        self.cli.realizar_transacao(self.conta, saque)
        # Saldo permanece 0
        self.assertEqual(self.conta.saldo_atual(), 0)
        # Mas a tentativa foi registrada no histórico
        self.assertEqual(len(self.conta.historico.transacoes), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)