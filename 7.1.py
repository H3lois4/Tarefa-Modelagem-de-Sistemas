"""
Exercício 7.1 - Teste Unitário
Para o sistema bancário implementado nas aulas anteriores,
escreva um teste unitário para a última funcionalidade de
investimento em poupança, seguindo o padrão AAA.
"""

import unittest
from main2 import ContaPoupanca, PessoaFisica, Deposito, Rendimento


class TestAplicarRendimentoAAA(unittest.TestCase):

    # Caso 1: rendimento credita o valor correto no saldo
    def test_rendimento_atualiza_saldo_corretamente(self):
        # ARRANGE
        cliente = PessoaFisica("Ana", "111.111.111-11", "1990-01-01", "Rua A, 1")
        poupanca = ContaPoupanca("001", cliente, taxa_mensal=0.005)
        poupanca.saldo = 1000.00   

        # ACT
        poupanca.aplicar_rendimento()

        # ASSERT
        self.assertAlmostEqual(poupanca.saldo_atual(), 1005.00, places=2)

    # Caso 2: rendimento é registrado no histórico
    def test_rendimento_registrado_no_historico(self):
        # ARRANGE
        cliente = PessoaFisica("Bruno", "222.222.222-22", "1985-05-10", "Rua B, 2")
        poupanca = ContaPoupanca("002", cliente, taxa_mensal=0.005)
        poupanca.saldo = 2000.00

        # ACT
        poupanca.aplicar_rendimento()

        # ASSERT
        self.assertEqual(len(poupanca.historico.transacoes), 1)
        self.assertIsInstance(poupanca.historico.transacoes[0], Rendimento)

    # Caso 3: rendimento com saldo zero não altera saldo
    def test_rendimento_sobre_saldo_zero_nao_altera_saldo(self):
        # ARRANGE
        cliente = PessoaFisica("Carla", "333.333.333-33", "2000-07-20", "Rua C, 3")
        poupanca = ContaPoupanca("003", cliente, taxa_mensal=0.005)

        # ACT
        poupanca.aplicar_rendimento()

        # ASSERT
        self.assertEqual(poupanca.saldo_atual(), 0)

    # Caso 4: dois rendimentos acumulam (juros compostos)
    def test_dois_rendimentos_acumulam_juros_compostos(self):
        # ARRANGE
        cliente = PessoaFisica("Diego", "444.444.444-44", "1995-11-30", "Rua D, 4")
        poupanca = ContaPoupanca("004", cliente, taxa_mensal=0.005)
        poupanca.saldo = 1000.00
        saldo_esperado = round(1000.00 * (1.005 ** 2), 2) 

        # ACT
        poupanca.aplicar_rendimento() 
        poupanca.aplicar_rendimento() 

        # ASSERT
        self.assertAlmostEqual(poupanca.saldo_atual(), saldo_esperado, places=1)

    # Caso 5: taxa negativa lança ValueError
    def test_taxa_negativa_levanta_valor_error(self):
        # ARRANGE
        cliente = PessoaFisica("Eva", "555.555.555-55", "1988-03-12", "Rua E, 5")

        # ACT + ASSERT (exceção esperada na criação)
        with self.assertRaises(ValueError):
            ContaPoupanca("005", cliente, taxa_mensal=-0.01)


if __name__ == "__main__":
    unittest.main(verbosity=2)