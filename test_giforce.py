"""
=============================================================
  GI-FORCE — Testes Unitários
  Disciplina: Linguagem de Programação Aplicada - UNINTER
=============================================================

Execução:
    python test_giforce.py
    python -m unittest test_giforce -v
"""

import unittest
import os
import sys
import tempfile
from unittest.mock import MagicMock, patch

# ─── Mock do pygame antes de importar main ────────────────
# Necessário pois main.py importa pygame, mas os testes
# não precisam de janela gráfica.
_pygame = MagicMock()
_pygame.Surface = MagicMock
_pygame.Rect    = MagicMock
_pygame.SRCALPHA = 0
sys.modules['pygame']          = _pygame
sys.modules['pygame.mixer']    = _pygame.mixer
sys.modules['pygame.font']     = _pygame.font
sys.modules['pygame.image']    = _pygame.image
sys.modules['pygame.draw']     = _pygame.draw
sys.modules['pygame.transform'] = _pygame.transform
# ─────────────────────────────────────────────────────────

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import main  # noqa: E402


# =============================================================
#  1. TESTES: salvar e carregar recorde (JSON)
# =============================================================
class TestRecorde(unittest.TestCase):
    """Testa as funções de persistência do recorde em JSON."""

    def setUp(self):
        self._tmp = tempfile.NamedTemporaryFile(
            mode='w', suffix='.json', delete=False
        )
        self._tmp.close()
        self._patch = patch('main.caminho_recorde', return_value=self._tmp.name)
        self._patch.start()

    def tearDown(self):
        self._patch.stop()
        os.unlink(self._tmp.name)

    def test_carregar_sem_arquivo_retorna_zero(self):
        """carregar_recorde() deve retornar 0 quando o arquivo não existe."""
        with patch('main.caminho_recorde', return_value='/nao/existe.json'):
            self.assertEqual(main.carregar_recorde(), 0)

    def test_salvar_e_carregar_preserva_valor(self):
        """Valor salvo deve ser idêntico ao carregado."""
        main.salvar_recorde(1500)
        self.assertEqual(main.carregar_recorde(), 1500)

    def test_salvar_zero(self):
        """Deve salvar e recuperar zero corretamente."""
        main.salvar_recorde(0)
        self.assertEqual(main.carregar_recorde(), 0)

    def test_arquivo_corrompido_retorna_zero(self):
        """JSON inválido deve ser tratado retornando 0."""
        with open(self._tmp.name, 'w') as f:
            f.write("conteudo_invalido!!!")
        self.assertEqual(main.carregar_recorde(), 0)

    def test_sobrescrever_recorde(self):
        """Salvar duas vezes deve manter o valor mais recente."""
        main.salvar_recorde(100)
        main.salvar_recorde(900)
        self.assertEqual(main.carregar_recorde(), 900)


# =============================================================
#  2. TESTES: Decorator @validar_positivo
# =============================================================
class TestValidarPositivo(unittest.TestCase):
    """Testa o decorator de função @validar_positivo."""

    def setUp(self):
        self._tmp = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
        self._tmp.close()
        self._patch = patch('main.caminho_recorde', return_value=self._tmp.name)
        self._patch.start()

    def tearDown(self):
        self._patch.stop()
        os.unlink(self._tmp.name)

    def test_pontuacao_negativa_e_corrigida_para_zero(self):
        """Decorator deve converter pontuação negativa em 0."""
        main.salvar_recorde(-500)
        self.assertEqual(main.carregar_recorde(), 0)

    def test_pontuacao_positiva_nao_e_alterada(self):
        """Decorator não deve modificar valores positivos."""
        main.salvar_recorde(750)
        self.assertEqual(main.carregar_recorde(), 750)


# =============================================================
#  3. TESTES: Lógica de cálculo de nível
# =============================================================
class TestCalculoNivel(unittest.TestCase):
    """Testa a fórmula de progressão de nível do jogo."""

    @staticmethod
    def _calcular_nivel(pontuacao: int) -> int:
        """Replica a fórmula usada em _atualizar_jogo(): 1 + pontuacao // 50."""
        return 1 + pontuacao // 50

    def test_nivel_inicial_e_um(self):
        self.assertEqual(self._calcular_nivel(0), 1)

    def test_nivel_sobe_exatamente_aos_50_pontos(self):
        self.assertEqual(self._calcular_nivel(49), 1)
        self.assertEqual(self._calcular_nivel(50), 2)

    def test_progressao_de_niveis(self):
        esperado = {0: 1, 50: 2, 100: 3, 150: 4, 450: 10}
        for pontos, nivel in esperado.items():
            with self.subTest(pontos=pontos):
                self.assertEqual(self._calcular_nivel(pontos), nivel)


# =============================================================
#  4. TESTES: Classe abstrata EntidadeJogo (ABC)
# =============================================================
class TestEntidadeJogoABC(unittest.TestCase):
    """Testa que EntidadeJogo impõe a implementação dos métodos abstratos."""

    def test_nao_instancia_diretamente(self):
        """EntidadeJogo não pode ser instanciada diretamente."""
        with self.assertRaises(TypeError):
            main.EntidadeJogo()

    def test_subclasse_sem_desenhar_falha(self):
        """Subclasse que não implementa desenhar() deve lançar TypeError."""
        class Incompleta(main.EntidadeJogo):
            def atualizar(self):
                pass

        with self.assertRaises(TypeError):
            Incompleta()

    def test_subclasse_sem_atualizar_falha(self):
        """Subclasse que não implementa atualizar() deve lançar TypeError."""
        class Incompleta(main.EntidadeJogo):
            def desenhar(self, tela):
                pass

        with self.assertRaises(TypeError):
            Incompleta()

    def test_subclasse_completa_instancia_com_sucesso(self):
        """Subclasse com todos os métodos implementados deve instanciar."""
        class Completa(main.EntidadeJogo):
            def atualizar(self):
                pass
            def desenhar(self, tela):
                pass

        obj = Completa()
        self.assertIsInstance(obj, main.EntidadeJogo)


# =============================================================
#  5. TESTES: Hierarquia de herança dos meteoritos
# =============================================================
class TestHerancaMeteorito(unittest.TestCase):
    """Testa a hierarquia de herança das subclasses de Meteorito."""

    def test_subclasses_herdam_de_meteorito(self):
        for cls in (main.MeteoritoPequeno, main.MeteoritoMedio, main.MeteoritoGrande):
            with self.subTest(cls=cls.__name__):
                self.assertTrue(issubclass(cls, main.Meteorito))

    def test_subclasses_herdam_de_entidade_jogo(self):
        for cls in (main.MeteoritoPequeno, main.MeteoritoMedio, main.MeteoritoGrande):
            with self.subTest(cls=cls.__name__):
                self.assertTrue(issubclass(cls, main.EntidadeJogo))

    def test_nave_herda_de_entidade_jogo(self):
        self.assertTrue(issubclass(main.Nave, main.EntidadeJogo))

    def test_particula_herda_de_entidade_jogo(self):
        self.assertTrue(issubclass(main.Particula, main.EntidadeJogo))

    def test_campo_estelar_herda_de_entidade_jogo(self):
        self.assertTrue(issubclass(main.CampoEstelar, main.EntidadeJogo))


# =============================================================
#  6. TESTES: Singleton do EventManager
# =============================================================
class TestSingleton(unittest.TestCase):
    """Testa que @singleton garante instância única do EventManager."""

    def test_duas_chamadas_retornam_mesma_instancia(self):
        """EventManager() chamado duas vezes deve retornar o mesmo objeto."""
        instancia1 = main.EventManager()
        instancia2 = main.EventManager()
        self.assertIs(instancia1, instancia2)

    def test_event_manager_global_e_a_mesma_instancia(self):
        """event_manager global deve ser a mesma instância de EventManager()."""
        self.assertIs(main.event_manager, main.EventManager())


if __name__ == "__main__":
    unittest.main(verbosity=2)
