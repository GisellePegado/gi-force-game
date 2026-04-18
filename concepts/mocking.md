# 🎭 Mocking em Testes (Mocking)

## 💡 O que é

Mocking é uma técnica de teste em que dependências externas de um componente são substituídas por objetos falsos (*mocks*) que simulam o comportamento esperado sem executar o código real. O objetivo é isolar o código sob teste: se um teste falha, você sabe que o problema está na lógica testada, não em uma dependência de rede, arquivo ou biblioteca gráfica.

Em Python, o módulo `unittest.mock` (padrão da linguagem) fornece `MagicMock`, um objeto que aceita qualquer acesso a atributos e chamadas de método sem lançar erros, retornando outros mocks. `patch()` é um context manager/decorator que substitui temporariamente um nome no namespace alvo por um mock — e restaura o original ao sair do bloco.

Mocking é essencial sempre que o código depende de I/O de arquivos, conexões de rede, APIs externas, interfaces gráficas, relógio do sistema, ou qualquer recurso que torne os testes lentos, não determinísticos ou difíceis de configurar.

> [!NOTE]
> Mocking complementa os [Testes Unitários](unit-testing.md): sem mocks, testar `main.py` exigiria uma janela gráfica aberta e hardware de áudio — o que tornaria os testes impossíveis em servidores de CI/CD.

## ⚙️ Como é usado neste projeto

`main.py` depende de `pygame`, que requer display gráfico e áudio. Para testar a lógica do jogo sem abrir uma janela, `test_giforce.py` substitui todo o módulo `pygame` por um `MagicMock()` antes de importá-lo. Além disso, `patch('main.caminho_recorde', ...)` redireciona o caminho do arquivo de recorde para um arquivo temporário em cada teste, isolando escritas do sistema de arquivos real.

## 🔍 Exemplo do projeto

```python
from unittest.mock import MagicMock, patch

# Mock do pygame substituído ANTES de importar main —
# evita que a importação tente inicializar janela ou áudio
_pygame = MagicMock()
_pygame.Surface = MagicMock
_pygame.Rect    = MagicMock
sys.modules['pygame']          = _pygame
sys.modules['pygame.mixer']    = _pygame.mixer

import main  # agora importa sem precisar de janela gráfica


class TestRecorde(unittest.TestCase):
    def setUp(self):
        # Redireciona scores.json para um arquivo temporário por teste
        self._tmp = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
        self._tmp.close()
        self._patch = patch('main.caminho_recorde', return_value=self._tmp.name)
        self._patch.start()

    def tearDown(self):
        self._patch.stop()
        os.unlink(self._tmp.name)   # limpa o arquivo temporário após cada teste
```

## 📚 Recursos para aprofundamento

- [unittest.mock — Python Docs](https://docs.python.org/3/library/unittest.mock.html) — referência completa de `MagicMock`, `patch` e `call`
- [Understanding the Python Mock Library — Real Python](https://realpython.com/python-mock-library/) — guia prático com exemplos progressivos
