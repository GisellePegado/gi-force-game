# 🔁 Game Loop (Game Loop)

## 💡 O que é

O game loop é o padrão fundamental de arquitetura de jogos em tempo real. Trata-se de um laço infinito que, a cada iteração (chamada de *frame*), executa três etapas: processar entradas do usuário, atualizar o estado do jogo e renderizar a cena na tela.

A frequência com que esse ciclo ocorre é chamada de *frames per second* (FPS). Para garantir que o jogo rode na mesma velocidade em máquinas mais rápidas ou mais lentas, é usado um **clock** que limita o número de iterações por segundo. Sem esse controle, um computador mais potente executaria o jogo em velocidade absurda.

O game loop também precisa lidar com a separação entre atualização de lógica e renderização — em jogos mais avançados, a lógica pode rodar em frequência fixa enquanto a renderização se adapta ao hardware, usando técnicas como *delta time*.

> [!TIP]
> O game loop trabalha em conjunto com a [Máquina de Estados](state-machine.md): o loop chama as funções certas a cada frame, e a máquina de estados decide *quais* funções são essas dependendo do modo atual do jogo.

## ⚙️ Como é usado neste projeto

O método `Jogo.rodar()` implementa o game loop principal. `self.clock.tick(FPS)` bloqueia o loop a 60 frames por segundo. A cada iteração, `_tratar_eventos()` processa inputs de teclado e janela; em seguida, o estado atual determina qual par de métodos `_atualizar_*()` / `_desenhar_*()` é chamado. `pygame.display.flip()` envia o frame renderizado para a tela.

## 🔍 Exemplo do projeto

```python
def rodar(self):
    while True:
        self.clock.tick(FPS)          # 1. limita a 60 FPS
        self._tratar_eventos()        # 2. processa teclado e eventos de janela

        if self.estado == self.ESTADO_MENU:
            self._atualizar_menu()    # 3a. atualiza lógica
            self._desenhar_menu()     # 3b. renderiza
        elif self.estado == self.ESTADO_JOGANDO:
            self._atualizar_jogo()
            self._desenhar_jogo()
        elif self.estado == self.ESTADO_GAME_OVER:
            self._atualizar_game_over()
            self._desenhar_game_over()
        # ... outros estados

        pygame.display.flip()         # 4. envia o frame para a tela
```

## 📚 Recursos para aprofundamento

- [Game Programming Patterns — Game Loop](https://gameprogrammingpatterns.com/game-loop.html) — explicação canônica do padrão com variações (fixed timestep, delta time)
- [pygame.time.Clock — Pygame Docs](https://www.pygame.org/docs/ref/time.html#pygame.time.Clock) — referência do `Clock.tick()` usado no projeto
