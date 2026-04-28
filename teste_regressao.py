"""
EXERCÍCIO 6.5 — Testes de Regressão + Nova Funcionalidade (Poupança)

Estratégia:
  1. Os testes originais (TU, TI, TF) são reexecutados contra banco_v2.py
     para garantir que a nova funcionalidade não quebrou nada existente.
  2. Novos casos de teste (TP) cobrem ContaPoupanca e Rendimento.
"""
import unittest
from main2 import (
    Conta, ContaCorrente, ContaPoupanca,
    Deposito, Saque, Rendimento,
    Historico, PessoaFisica
)
# REGRESSÃO — Testes Unitários originais (main2)

class TestRegressao_Deposito(unittest.TestCase):
    def setUp(self):
        self.cliente = PessoaFisica("Ana", "111.111.111-11", "1990-01-01", "Rua A, 1")
        self.conta = Conta("001", self.cliente)

    def test_TU01_deposito_valor_valido(self):
        Deposito(200).registrar(self.conta)
        self.assertEqual(self.conta.saldo, 200)

    def test_TU02_deposito_valor_zero(self):
        Deposito(0).registrar(self.conta)
        self.assertEqual(self.conta.saldo, 0)

    def test_TU03_deposito_valor_negativo(self):
        Deposito(-50).registrar(self.conta)
        self.assertEqual(self.conta.saldo, 0)


class TestRegressao_Saque(unittest.TestCase):
    def setUp(self):
        self.cliente = PessoaFisica("Bruno", "222.222.222-22", "1985-05-10", "Rua B, 2")
        self.conta = Conta("002", self.cliente)
        self.conta.saldo = 500

    def test_TU04_saque_saldo_suficiente(self):
        Saque(200).registrar(self.conta)
        self.assertEqual(self.conta.saldo, 300)

    def test_TU05_saque_saldo_exato(self):
        Saque(500).registrar(self.conta)
        self.assertEqual(self.conta.saldo, 0)

    def test_TU06_saque_saldo_insuficiente(self):
        Saque(600).registrar(self.conta)
        self.assertEqual(self.conta.saldo, 500)


class TestRegressao_Historico(unittest.TestCase):
    def test_TU07_historico_inicialmente_vazio(self):
        self.assertEqual(len(Historico().transacoes), 0)

    def test_TU08_historico_adiciona_transacao(self):
        h = Historico()
        dep = Deposito(100)
        h.adicionar_transacao(dep)
        self.assertIs(h.transacoes[0], dep)


class TestRegressao_PessoaFisica(unittest.TestCase):
    def test_TU09_atributos_pessoa_fisica(self):
        p = PessoaFisica("Carlos", "333.333.333-33", "2000-12-31", "Av. C, 3")
        self.assertEqual(p.nome, "Carlos")
        self.assertEqual(p.cpf, "333.333.333-33")

    def test_TU10_lista_contas_inicialmente_vazia(self):
        p = PessoaFisica("Diana", "444.444.444-44", "1995-07-20", "Rua D, 4")
        self.assertEqual(p.contas, [])


class TestRegressao_ContaCorrente(unittest.TestCase):
    def test_TU11_valores_padrao_conta_corrente(self):
        cli = PessoaFisica("Eduardo", "555.555.555-55", "1988-03-15", "Rua E, 5")
        cc = ContaCorrente("003", cli)
        self.assertEqual(cc.limite, 500)
        self.assertEqual(cc.limite_saques, 3)
        self.assertEqual(cc.saldo, 0)


class TestRegressao_IntegracaoClienteConta(unittest.TestCase):
    def test_TI01_adicionar_conta_ao_cliente(self):
        cli = PessoaFisica("Fernanda", "666.666.666-66", "1993-08-22", "Rua F, 6")
        cc = ContaCorrente("101", cli)
        cli.adicionar_conta(cc)
        self.assertIn(cc, cli.contas)

    def test_TI06_multiplas_transacoes_historico_completo(self):
        cli = PessoaFisica("Helena", "888.888.888-88", "1987-04-18", "Rua H, 8")
        conta = ContaCorrente("104", cli)
        cli.adicionar_conta(conta)
        cli.realizar_transacao(conta, Deposito(500))
        cli.realizar_transacao(conta, Deposito(300))
        cli.realizar_transacao(conta, Saque(100))
        self.assertEqual(len(conta.historico.transacoes), 3)
        self.assertEqual(conta.saldo_atual(), 700)


class TestRegressao_Funcional(unittest.TestCase):
    def test_TF06_ciclo_completo(self):
        cliente = PessoaFisica("Marina", "303.303.303-03", "1994-03-12", "Av. M, 12")
        conta = ContaCorrente("204", cliente)
        cliente.adicionar_conta(conta)
        cliente.realizar_transacao(conta, Deposito(3000))
        cliente.realizar_transacao(conta, Saque(500))
        cliente.realizar_transacao(conta, Deposito(200))
        cliente.realizar_transacao(conta, Saque(100))
        self.assertEqual(conta.saldo_atual(), 2600)
        self.assertEqual(len(conta.historico.transacoes), 4)

# NOVOS TESTES — ContaPoupanca e Rendimento
class TestContaPoupanca(unittest.TestCase):
    """TP-01 a TP-06: Testa a nova funcionalidade de poupança."""

    def setUp(self):
        self.cliente = PessoaFisica("Nadia", "010.101.010-10", "1992-02-14", "Rua N, 13")
        self.poupanca = ContaPoupanca("301", self.cliente)
        self.cliente.adicionar_conta(self.poupanca)

    def test_TP01_taxa_padrao(self):
        """TP-01: ContaPoupanca deve usar taxa padrão de 0,5% ao mês."""
        self.assertAlmostEqual(self.poupanca.taxa_mensal, 0.005)

    def test_TP02_taxa_customizada(self):
        """TP-02: ContaPoupanca deve aceitar taxa mensal customizada."""
        p = ContaPoupanca("302", self.cliente, taxa_mensal=0.01)
        self.assertAlmostEqual(p.taxa_mensal, 0.01)

    def test_TP03_taxa_negativa_levanta_erro(self):
        """TP-03: Criar ContaPoupanca com taxa negativa deve lançar ValueError."""
        with self.assertRaises(ValueError):
            ContaPoupanca("303", self.cliente, taxa_mensal=-0.01)

    def test_TP04_rendimento_calculado_corretamente(self):
        """TP-04: aplicar_rendimento() deve creditar 0,5% sobre o saldo."""
        self.cliente.realizar_transacao(self.poupanca, Deposito(1000))
        saldo_antes = self.poupanca.saldo_atual()
        self.poupanca.aplicar_rendimento()
        saldo_esperado = round(saldo_antes * 1.005, 2)
        self.assertAlmostEqual(self.poupanca.saldo_atual(), saldo_esperado, places=2)

    def test_TP05_rendimento_registrado_no_historico(self):
        """TP-05: Após aplicar_rendimento(), histórico deve ter mais uma entrada."""
        self.cliente.realizar_transacao(self.poupanca, Deposito(2000))
        qtd_antes = len(self.poupanca.historico.transacoes)
        self.poupanca.aplicar_rendimento()
        self.assertEqual(len(self.poupanca.historico.transacoes), qtd_antes + 1)

    def test_TP06_rendimento_saldo_zero(self):
        """TP-06: Aplicar rendimento com saldo zero não deve alterar o saldo."""
        self.assertEqual(self.poupanca.saldo_atual(), 0)
        self.poupanca.aplicar_rendimento()
        self.assertEqual(self.poupanca.saldo_atual(), 0)

    def test_TP07_multiplos_rendimentos_acumulam(self):
        """TP-07: Dois rendimentos aplicados devem acumular corretamente (juros compostos)."""
        self.cliente.realizar_transacao(self.poupanca, Deposito(1000))
        self.poupanca.aplicar_rendimento()  # mês 1
        self.poupanca.aplicar_rendimento()  # mês 2
        esperado = round(1000 * (1.005 ** 2), 2)
        self.assertAlmostEqual(self.poupanca.saldo_atual(), esperado, places=1)

    def test_TP08_poupanca_herda_deposito_e_saque(self):
        """TP-08: ContaPoupanca deve aceitar depósitos e saques normalmente (herança)."""
        self.cliente.realizar_transacao(self.poupanca, Deposito(500))
        self.cliente.realizar_transacao(self.poupanca, Saque(200))
        self.assertEqual(self.poupanca.saldo_atual(), 300)


class TestRendimento(unittest.TestCase):
    """TP-09 a TP-10: Testa a classe Rendimento isoladamente."""

    def setUp(self):
        self.cliente = PessoaFisica("Otavio", "020.202.020-20", "1990-10-10", "Rua O, 14")
        self.poupanca = ContaPoupanca("304", self.cliente)
        self.poupanca.saldo = 1000

    def test_TP09_rendimento_registra_valor_correto(self):
        """TP-09: Rendimento.registrar() deve aumentar o saldo pelo valor da taxa."""
        r = Rendimento(0.005)
        r.registrar(self.poupanca)
        self.assertAlmostEqual(self.poupanca.saldo, 1005.0, places=2)

    def test_TP10_rendimento_taxa_zero_nao_altera_saldo(self):
        """TP-10: Rendimento com taxa 0% não deve alterar o saldo (juro zero não deposita)."""
        r = Rendimento(0.0)
        r.registrar(self.poupanca)
        # taxa=0 → rendimento=0 → depositar(0) → valor inválido, saldo não muda
        self.assertEqual(self.poupanca.saldo, 1000)


if __name__ == "__main__":
    unittest.main(verbosity=2)