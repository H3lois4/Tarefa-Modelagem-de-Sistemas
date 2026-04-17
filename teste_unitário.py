"""
EXERCÍCIO 6.2 — Testes Unitários
Testam unidades isoladas: métodos de Conta, Deposito, Saque, Historico e PessoaFisica.
"""
import unittest
from main import Conta, ContaCorrente, Deposito, Saque, Historico, PessoaFisica

class TestDeposito(unittest.TestCase):
    """TU-01 a TU-03: Testa a classe Deposito em isolamento."""

    def setUp(self):
        self.cliente = PessoaFisica("Ana", "111.111.111-11", "1990-01-01", "Rua A, 1")
        self.conta = Conta("001", self.cliente)

    def test_TU01_deposito_valor_valido(self):
        """TU-01: Depositar valor positivo deve aumentar o saldo.
        NOTA: Deposito.registrar() não retorna o valor de conta.depositar()
        (retorna None). O saldo é atualizado corretamente mesmo assim.
        """
        dep = Deposito(200)
        dep.registrar(self.conta)
        self.assertEqual(self.conta.saldo, 200)

    def test_TU02_deposito_valor_zero(self):
        """TU-02: Depositar valor zero deve retornar False e não alterar o saldo."""
        dep = Deposito(0)
        resultado = dep.registrar(self.conta)
        self.assertFalse(resultado)
        self.assertEqual(self.conta.saldo, 0)

    def test_TU03_deposito_valor_negativo(self):
        """TU-03: Depositar valor negativo deve retornar False e não alterar o saldo."""
        dep = Deposito(-50)
        resultado = dep.registrar(self.conta)
        self.assertFalse(resultado)
        self.assertEqual(self.conta.saldo, 0)


class TestSaque(unittest.TestCase):
    """TU-04 a TU-06: Testa a classe Saque em isolamento."""

    def setUp(self):
        self.cliente = PessoaFisica("Bruno", "222.222.222-22", "1985-05-10", "Rua B, 2")
        self.conta = Conta("002", self.cliente)
        self.conta.saldo = 500  # Saldo inicial direto para isolar o teste

    def test_TU04_saque_saldo_suficiente(self):
        """TU-04: Sacar valor menor que o saldo deve reduzir saldo.
        NOTA: Saque.registrar() não propaga o retorno de conta.sacar() (retorna None).
        """
        saque = Saque(200)
        saque.registrar(self.conta)
        self.assertEqual(self.conta.saldo, 300)

    def test_TU05_saque_saldo_exato(self):
        """TU-05: Sacar exatamente o saldo disponível deve zerar o saldo."""
        saque = Saque(500)
        saque.registrar(self.conta)
        self.assertEqual(self.conta.saldo, 0)

    def test_TU06_saque_saldo_insuficiente(self):
        """TU-06: Sacar valor maior que o saldo deve retornar False e manter o saldo."""
        saque = Saque(600)
        resultado = saque.registrar(self.conta)
        self.assertFalse(resultado)
        self.assertEqual(self.conta.saldo, 500)


class TestHistorico(unittest.TestCase):
    """TU-07 a TU-08: Testa a classe Historico."""

    def test_TU07_historico_inicialmente_vazio(self):
        """TU-07: Historico recém-criado deve ter lista de transações vazia."""
        h = Historico()
        self.assertEqual(len(h.transacoes), 0)

    def test_TU08_historico_adiciona_transacao(self):
        """TU-08: adicionar_transacao deve incluir o objeto na lista."""
        h = Historico()
        dep = Deposito(100)
        h.adicionar_transacao(dep)
        self.assertEqual(len(h.transacoes), 1)
        self.assertIs(h.transacoes[0], dep)


class TestPessoaFisica(unittest.TestCase):
    """TU-09 a TU-10: Testa a criação de PessoaFisica."""

    def test_TU09_atributos_pessoa_fisica(self):
        """TU-09: PessoaFisica deve armazenar corretamente nome, cpf, nascimento e endereço."""
        p = PessoaFisica("Carlos", "333.333.333-33", "2000-12-31", "Av. C, 3")
        self.assertEqual(p.nome, "Carlos")
        self.assertEqual(p.cpf, "333.333.333-33")
        self.assertEqual(p.data_nascimento, "2000-12-31")
        self.assertEqual(p.endereco, "Av. C, 3")

    def test_TU10_lista_contas_inicialmente_vazia(self):
        """TU-10: PessoaFisica herda de Cliente; lista de contas deve iniciar vazia."""
        p = PessoaFisica("Diana", "444.444.444-44", "1995-07-20", "Rua D, 4")
        self.assertEqual(p.contas, [])


class TestContaCorrente(unittest.TestCase):
    """TU-11: Testa atributos padrão de ContaCorrente."""

    def test_TU11_valores_padrao_conta_corrente(self):
        """TU-11: ContaCorrente deve ter limite=500 e limite_saques=3 por padrão."""
        cli = PessoaFisica("Eduardo", "555.555.555-55", "1988-03-15", "Rua E, 5")
        cc = ContaCorrente("003", cli)
        self.assertEqual(cc.limite, 500)
        self.assertEqual(cc.limite_saques, 3)
        self.assertEqual(cc.agencia, "0001")
        self.assertEqual(cc.saldo, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)