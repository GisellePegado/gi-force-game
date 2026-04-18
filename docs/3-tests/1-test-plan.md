# 🧪 Plano de Testes

## 🎯 Escopo

**Dentro do escopo:** lógica de negócio pura — persistência de recorde (JSON), decorator `@validar_positivo`, cálculo de progressão de nível, contrato da ABC `EntidadeJogo`, hierarquia de herança das entidades e unicidade do Singleton `EventManager`.

**Fora do escopo:** renderização gráfica (dependente de janela pygame), reprodução de áudio, eventos de teclado em tempo real e comportamento visual de partículas — esses elementos requerem inspeção manual ou testes de integração com display.

## 🛠️ Tipos de teste

| Tipo | Ferramenta | Cobertura |
|------|------------|-----------|
| Unitário | `unittest` (stdlib) | Funções de negócio, decorators, hierarquia de classes, Singleton |
| Mocking | `unittest.mock.MagicMock`, `patch` | Isola pygame e sistema de arquivos dos testes |
| Manual | Execução do jogo | Renderização, áudio, inputs, transições de estado |

## Estratégia de isolamento

Como `main.py` importa `pygame` no topo do arquivo e pygame requer display gráfico, todos os submódulos de pygame são substituídos por `MagicMock` **antes** do `import main`. Isso permite testar a lógica pura sem janela gráfica:

```bash
python test_giforce.py
# ou
python -m unittest test_giforce -v
```

## Grupos de teste implementados

| Classe de teste | O que verifica | Qtd. |
|-----------------|----------------|:----:|
| `TestRecorde` | Persistência JSON: salvar, carregar, arquivo corrompido, sobrescrever | 5 |
| `TestValidarPositivo` | Decorator corrige negativos e preserva positivos | 2 |
| `TestCalculoNivel` | Fórmula `1 + pontuacao // 50` em múltiplos cenários | 3 |
| `TestEntidadeJogoABC` | ABC impõe contrato: `TypeError` para subclasses incompletas | 4 |
| `TestHerancaMeteorito` | Hierarquia: subclasses herdam de `Meteorito` e `EntidadeJogo` | 5 |
| `TestSingleton` | `EventManager()` retorna sempre a mesma instância | 2 |
| **Total** | | **21** |

## ✅ Critérios de aceite (Quality Gates)

| Critério | Meta |
|----------|------|
| Todos os testes unitários passam | 21/21 ✅ |
| Nenhum teste depende de display pygame | Garantido via mocking |
| Testes são independentes entre si | `setUp()`/`tearDown()` isolam estado de arquivo |
| Tempo de execução total | < 1 segundo |
