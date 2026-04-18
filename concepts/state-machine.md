# 🔀 Máquina de Estados (State Machine)

## 💡 O que é

Uma máquina de estados é um modelo computacional onde um sistema pode estar em exatamente um de um conjunto finito de _estados_, e transições entre estados ocorrem em resposta a eventos ou condições. Em cada estado, o sistema se comporta de forma diferente — exibe uma tela diferente, processa inputs de forma diferente, ou executa lógica diferente.

Em jogos, a máquina de estados é um padrão quase universal para gerenciar telas e modos de jogo. Ela é preferível a um grande bloco de `if/else` espalhado pelo código porque torna o fluxo explícito, fácil de estender (adicionar um novo estado é adicionar um novo `elif`) e fácil de depurar (o estado atual é uma variável observável).

A implementação mais simples usa uma variável de estado (uma string ou enum) e um bloco condicional no loop principal. Implementações mais sofisticadas usam classes para cada estado com métodos `entrar()`, `atualizar()` e `sair()`.

## ⚙️ Como é usado neste projeto

A classe `Jogo` mantém a variável `self.estado` com seis valores possíveis, definidos como constantes de classe. O game loop em `rodar()` usa esse valor para despachar para os pares corretos de `_atualizar_*()` / `_desenhar_*()`. Transições de estado ocorrem em `_tratar_eventos()` (input do usuário) e em `_atualizar_jogo()` (lógica do jogo, como detecção de game over).

```
menu ──ENTER──▶ jogando ──game over──▶ game_over
  ▲                │                      │
  └──ESC───────────┘◀─────────ESC─────────┘
  │
  ├──▶ comandos ──ESC──▶ menu
  └──▶ sobre    ──ESC──▶ menu
```

## 🔍 Exemplo do projeto

```python
class Jogo:
    ESTADO_MENU      = "menu"
    ESTADO_JOGANDO   = "jogando"
    ESTADO_PAUSADO   = "pausado"
    ESTADO_COMANDOS  = "comandos"
    ESTADO_GAME_OVER = "game_over"
    ESTADO_SOBRE     = "sobre"

    def rodar(self):
        while True:
            self.clock.tick(FPS)
            self._tratar_eventos()

            if self.estado == self.ESTADO_MENU:
                self._atualizar_menu()
                self._desenhar_menu()
            elif self.estado == self.ESTADO_JOGANDO:
                self._atualizar_jogo()
                self._desenhar_jogo()
            elif self.estado == self.ESTADO_PAUSADO:
                self._desenhar_jogo()
                self._desenhar_pausado()
            # ... demais estados

            pygame.display.flip()
```

## 📚 Recursos para aprofundamento

- [Game Programming Patterns — State](https://gameprogrammingpatterns.com/state.html) — o padrão State aplicado a jogos, com exemplos em C++ e Python
- [Real Python — Python State Machine](https://realpython.com/python-finite-state-machine/) — implementações progressivas em Python
