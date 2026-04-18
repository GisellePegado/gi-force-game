# 🧪 Testes Unitários (Unit Testing)

## 💡 O que é

Testes unitários verificam o comportamento de **unidades isoladas** do código — funções, métodos ou classes — de forma automática e repetível. A ideia central é testar cada peça separadamente, simulando as entradas e verificando se a saída corresponde ao esperado, sem depender de componentes externos como banco de dados, rede ou interface gráfica.

Em Python, o módulo `unittest` da biblioteca padrão fornece a estrutura para criar e executar testes. Cada grupo de testes é uma classe que herda de `unittest.TestCase`, e cada método que começa com `test_` é um caso de teste individual. O módulo `unittest.mock` permite substituir dependências reais por objetos simulados (**mocks**), essencial quando o código depende de recursos externos.

As principais vantagens: detectar regressões cedo, documentar o comportamento esperado e dar confiança para refatorar sem medo de quebrar funcionalidades existentes.

## ⚙️ Como é usado neste projeto

`test_giforce.py` contém 21 testes organizados em 6 grupos, cobrindo as partes testáveis do jogo sem precisar de janela gráfica. Como `main.py` importa Pygame — que exige display — os testes usam `unittest.mock.MagicMock` para substituir todo o módulo `pygame` por um mock antes da importação.

| Grupo | Classe de Teste | O que verifica |
|-------|----------------|----------------|
| 1 | `TestRecorde` | Salvar e carregar recorde em JSON |
| 2 | `TestValidarPositivo` | Decorator `@validar_positivo` |
| 3 | `TestSingleton` | Padrão Singleton no `EventManager` |
| 4 | `TestEventManager` | `assinar()` e `publicar()` do Observer |
| 5 | `TestMeteoritoFactory` | Criação de tipos corretos pela Factory |
| 6 | `TestMeteoritoHeranca` | Atributos herdados das subclasses |

## 🔍 Exemplo do projeto

```python
import unittest
from unittest.mock import patch

class TestRecorde(unittest.TestCase):
    """Testa as funções de persistência do recorde em JSON."""

    def setUp(self):
        # Cria um arquivo temporário para não sujar o scores.json real
        self._tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self._tmp.close()
        self._patch = patch('main.caminho_recorde', return_value=self._tmp.name)
        self._patch.start()

    def tearDown(self):
        self._patch.stop()
        os.unlink(self._tmp.name)

    def test_salvar_e_carregar_preserva_valor(self):
        """Valor salvo deve ser idêntico ao carregado."""
        main.salvar_recorde(1500)
        self.assertEqual(main.carregar_recorde(), 1500)

    def test_arquivo_corrompido_retorna_zero(self):
        """JSON inválido deve ser tratado retornando 0."""
        with open(self._tmp.name, 'w') as f:
            f.write("conteudo_invalido!!!")
        self.assertEqual(main.carregar_recorde(), 0)
```

```bash
# Execução dos testes:
python -m unittest test_giforce -v
```

## 📚 Recursos para aprofundamento

- [unittest — Python Docs](https://docs.python.org/3/library/unittest.html) — documentação oficial do módulo de testes
- [unittest.mock — Python Docs](https://docs.python.org/3/library/unittest.mock.html) — guia completo sobre mocks em Python
- [Getting Started With Testing in Python — Real Python](https://realpython.com/python-testing/) — introdução prática a testes unitários
