# ⌨️ Eventos de Teclado (Keyboard Events)

## 💡 O que é

Em jogos e aplicações interativas, a entrada do usuário é capturada através de um sistema de **eventos**: o sistema operacional gera um evento sempre que uma tecla é pressionada ou liberada, e o programa processa esses eventos em seu loop principal.

O Pygame distingue dois modelos de leitura de teclado:

- **Eventos pontuais** (`pygame.KEYDOWN` / `pygame.KEYUP`): disparam uma única vez quando a tecla é pressionada ou solta — ideal para ações discretas como confirmar, pausar ou navegar em menus.
- **Estado contínuo** (`pygame.key.get_pressed()`): retorna um dicionário com o estado atual de todas as teclas — ideal para movimento suave enquanto a tecla é mantida pressionada.

## ⚙️ Como é usado neste projeto

O GI-FORCE usa os dois modelos. Em `_tratar_eventos()`, o loop de eventos captura `pygame.KEYDOWN` para ações discretas: navegar no menu (↑/↓), confirmar (ENTER), pausar, voltar (ESC) e fechar o jogo. Já em `Nave.atualizar()`, `pygame.key.get_pressed()` é usado para movimento contínuo da nave enquanto as teclas direcionais ou WASD estão pressionadas.

## 🔍 Exemplo do projeto

```python
# Modelo 1 — eventos pontuais (ações discretas no menu):
def _tratar_eventos(self):
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        if evento.type == pygame.KEYDOWN:
            if self.estado == self.ESTADO_MENU:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                elif evento.key in (pygame.K_UP, pygame.K_w):
                    self.opcao_menu = (self.opcao_menu - 1) % 3
                elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    self._iniciar_jogo()
                    self.estado = self.ESTADO_JOGANDO


# Modelo 2 — estado contínuo (movimento suave da nave):
def atualizar(self, teclas):
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        self.x -= self.VEL
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        self.x += self.VEL
    if teclas[pygame.K_UP] or teclas[pygame.K_w]:
        self.y -= self.VEL
    if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
        self.y += self.VEL
```

## 📚 Recursos para aprofundamento

- [pygame.event — Pygame Docs](https://www.pygame.org/docs/ref/event.html) — referência completa do sistema de eventos
- [pygame.key — Pygame Docs](https://www.pygame.org/docs/ref/key.html) — referência de `get_pressed()` e constantes de tecla
