"""
Exercício 7.5 - TDD
Aplique o método TDD para escrever um teste unitário e
desenvolver uma nova funcionalidade de cálculo de
rendimentos e atualização do saldo da poupança.
O rendimento deve ser de 0.5% sobre o saldo atual. O teste
deve validar se o saldo foi atualizado corretamente após a
chamada do método.
"""

import unittest
import sys
from main2 import ContaPoupanca, PessoaFisica

# TESTES TDD — escritos ANTES da implementação (etapa RED)

class TestCalcularRendimentoTDD(unittest.TestCase):
    def setUp(self):
        self.cliente = PessoaFisica(
            nome="Helena TDD",
            cpf="700.700.700-70",
            data_nascimento="1991-08-18",
            endereco="Rua TDD, 42"
        )
        self.poupanca = ContaPoupanca("TDD-001", self.cliente, taxa_mensal=0.005)
        self.poupanca.saldo = 1000.00   # saldo inicial: R$ 1000,00

    # Teste 1: saldo é atualizado corretamente
    def test_tdd1_saldo_atualizado_apos_calcular_rendimento(self):
        """
        RED  → AttributeError: 'ContaPoupanca' object has no attribute 'calcular_rendimento'
        GREEN → passa: saldo deve ser 1005,00 após 0,5% de rendimento
        """
        # ARRANGE (complementar ao setUp)
        saldo_esperado = 1005.00   # 1000 * 1.005

        # ACT
        self.poupanca.calcular_rendimento()

        # ASSERT
        self.assertAlmostEqual(self.poupanca.saldo_atual(), saldo_esperado, places=2)

    # Teste 2: método retorna o valor do rendimento creditado 
    def test_tdd2_retorna_valor_do_rendimento(self):
        """
        GREEN → calcular_rendimento() deve retornar R$ 5,00 (0,5% de 1000)
        """
        # ARRANGE
        rendimento_esperado = 5.00

        # ACT
        rendimento_retornado = self.poupanca.calcular_rendimento()

        # ASSERT
        self.assertAlmostEqual(rendimento_retornado, rendimento_esperado, places=2)

    # Teste 3: histórico registra a operação
    def test_tdd3_historico_registra_operacao(self):
        """
        GREEN → após calcular_rendimento(), histórico deve ter 1 transação
        """
        # ARRANGE
        qtd_inicial = len(self.poupanca.historico.transacoes)

        # ACT
        self.poupanca.calcular_rendimento()

        # ASSERT
        self.assertEqual(len(self.poupanca.historico.transacoes), qtd_inicial + 1)

    # Teste 4: saldo zero não gera rendimento
    def test_tdd4_saldo_zero_nao_gera_rendimento(self):
        """
        GREEN → com saldo 0, calcular_rendimento() retorna 0 e saldo permanece 0
        """
        # ARRANGE
        self.poupanca.saldo = 0.00

        # ACT
        rendimento = self.poupanca.calcular_rendimento()

        # ASSERT
        self.assertEqual(self.poupanca.saldo_atual(), 0.00)
        self.assertEqual(rendimento, 0.00)

    # Teste 5: chamadas múltiplas aplicam juros compostos
    def test_tdd5_multiplas_chamadas_juros_compostos(self):
        """
        GREEN → 3 chamadas devem acumular 0,5% ao mês (juros compostos)
        """
        # ARRANGE
        saldo_esperado = round(1000.00 * (1.005 ** 3), 2)  # R$ 1015,08

        # ACT
        self.poupanca.calcular_rendimento()
        self.poupanca.calcular_rendimento()
        self.poupanca.calcular_rendimento()

        # ASSERT
        self.assertAlmostEqual(self.poupanca.saldo_atual(), saldo_esperado, places=1)


# =============================================================================
# IMPLEMENTAÇÃO — adicionada na etapa GREEN do TDD
# Normalmente estaria em banco_v2.py; está aqui para ilustrar o ciclo completo.
# =============================================================================

def _calcular_rendimento(self):
    """
    Calcula 0,5% sobre o saldo atual, credita o rendimento e
    registra a operação no histórico.
    Retorna o valor do rendimento creditado (0.0 se saldo for zero).
    """
    valor_rendimento = round(self.saldo_atual() * self.taxa_mensal, 2)
    if valor_rendimento > 0:
        self.depositar(valor_rendimento)
        # Registra no histórico reutilizando a classe Rendimento existente
        from banco_v2 import Rendimento
        self.historico.adicionar_transacao(Rendimento(self.taxa_mensal))
    return valor_rendimento

# Injeção do método na classe (monkey-patch para fins didáticos do TDD)
# Em produção, o método seria adicionado diretamente em banco_v2.py
ContaPoupanca.calcular_rendimento = _calcular_rendimento


# =============================================================================
# Execução
# =============================================================================

if __name__ == "__main__":
    # Remove o argumento customizado antes de repassar ao unittest
    argv = [a for a in sys.argv if not a.startswith("--etapa")]
    unittest.main(argv=argv, verbosity=2)