"""
Exercício 7.2 - Test Doubles
3
Escolha um método completo do aplicativo bancário, e
escreva um teste unitário seguindo p padrão AAA e utilizando
pelo menos um Dummy, um Stub e um Mock.
"""

import unittest
from unittest.mock import MagicMock, patch
from main2 import Cliente, PessoaFisica


class TestRealizarTransacaoComDummyStubMock(unittest.TestCase):

    def test_realizar_transacao_chama_registrar_e_adiciona_historico(self):
       
        cliente_dummy = PessoaFisica(
            nome="Dummy Silva",
            cpf="000.000.000-00",
            data_nascimento="1900-01-01",
            endereco="Rua do Dummy, 0"
        )

        conta_stub = MagicMock()
        conta_stub.saldo_atual.return_value = 500.00   # retorno pré-definido
        conta_stub.numero = "STUB-001"

        transacao_mock = MagicMock()

        cliente = PessoaFisica(
            nome="Fernando Teste",
            cpf="123.456.789-00",
            data_nascimento="1990-06-15",
            endereco="Av. Teste, 100"
        )

        # ACT
        cliente.realizar_transacao(conta_stub, transacao_mock)

        # ASSERT 
        transacao_mock.registrar.assert_called_once_with(conta_stub)
        conta_stub.historico.adicionar_transacao.assert_called_once_with(transacao_mock)

    # Caso adicional: stub controla retorno de sacar() para testar branch
    def test_stub_controla_retorno_de_depositar(self):
        """
        Usa Stub para fazer conta.depositar() retornar True,
        garantindo que o caminho de sucesso é percorrido.
        Usa Mock para confirmar que depositar foi chamado com o valor correto.
        """
        cliente_dummy = PessoaFisica("Dummy", "999.999.999-99", "2000-01-01", "Rua X")

        conta_stub = MagicMock()
        conta_stub.depositar.return_value = True   # stub: resposta pré-definida

        def depositar_300(conta):
            conta.depositar(300)

        transacao_mock = MagicMock()
        transacao_mock.registrar.side_effect = depositar_300   # mock com comportamento

        cliente = PessoaFisica("Gisele", "321.654.987-00", "1993-04-22", "Av. G, 7")

        # ACT
        cliente.realizar_transacao(conta_stub, transacao_mock)

        # ASSERT
        conta_stub.depositar.assert_called_once_with(300)       # mock: chamada verificada
        self.assertTrue(conta_stub.depositar.return_value)      # stub: retorno controlado


if __name__ == "__main__":
    unittest.main(verbosity=2)