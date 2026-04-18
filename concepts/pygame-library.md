# 🎮 Biblioteca Pygame (Pygame Library)

## 💡 O que é

Pygame é uma biblioteca Python de código aberto criada para o desenvolvimento de jogos e aplicações multimídia 2D. Ela fornece uma camada de abstração sobre a SDL (_Simple DirectMedia Layer_), permitindo criar janelas gráficas, capturar eventos de teclado e mouse, desenhar formas e imagens, reproduzir áudio e controlar o tempo de execução — tudo em Python puro.

A biblioteca é organizada em módulos: `pygame.display` controla a janela, `pygame.event` captura entradas do usuário, `pygame.draw` renderiza primitivas geométricas, `pygame.image` carrega texturas, e `pygame.mixer` gerencia áudio. O loop principal de um jogo Pygame segue um ciclo fixo: processar eventos → atualizar estado → desenhar tela → sincronizar FPS.

## ⚙️ Como é usado neste projeto

O GI-FORCE usa o Pygame como infraestrutura completa do jogo. A classe `Jogo` inicializa o subsistema com `pygame.init()` e `pygame.mixer.init()`, cria a janela com `pygame.display.set_mode()`, e executa o loop principal via `self.clock.tick(FPS)` a 60 FPS. Cada entidade do jogo (`Nave`, `Meteorito`, `Particula`, `CampoEstelar`) usa `pygame.draw` e `pygame.Surface` para renderização. O áudio é gerenciado com `pygame.mixer.music` para música de fundo e `pygame.mixer.Sound` para efeitos sonoros independentes.

## 🔍 Exemplo do projeto

```python
# Inicialização em Jogo.__init__()
pygame.init()
pygame.mixer.init()
self.tela = pygame.display.set_mode((LARGURA, ALTURA))   # 800×600
self.clock = pygame.time.Clock()

# Loop principal em Jogo.rodar()
def rodar(self):
    while True:
        self.clock.tick(FPS)          # limita a 60 frames/s
        self._tratar_eventos()        # captura teclado/fechar janela
        self._atualizar_jogo()        # lógica do estado atual
        self._desenhar_jogo()         # renderiza na tela
        pygame.display.flip()         # envia o frame para a tela
```

## 📚 Recursos para aprofundamento

- [Documentação oficial do Pygame](https://www.pygame.org/docs/) — referência completa de todos os módulos
- [Pygame Tutorial — Real Python](https://realpython.com/pygame-a-primer/) — introdução prática à criação de jogos com Pygame
