# 📡 Padrão de Projeto Observer (Observer Pattern)

## 💡 O que é

O Observer é um padrão de projeto **comportamental** que define uma relação de dependência um-para-muitos entre objetos: quando um objeto (o **publicador**) muda de estado, todos os objetos que se registraram para receber notificações (os **assinantes**) são avisados automaticamente.

Esse padrão é a base de sistemas de eventos em jogos, frameworks de UI e arquiteturas orientadas a eventos. Ele promove o **baixo acoplamento**: o publicador não precisa conhecer quem são os assinantes — apenas publica o evento e a infraestrutura cuida do resto.

Os componentes essenciais são:
- **Publicador (subject):** mantém a lista de assinantes e emite eventos
- **Assinante (observer):** registra um callback que será chamado quando o evento ocorrer

## ⚙️ Como é usado neste projeto

O `EventManager` implementa o Observer no GI-FORCE. A classe `Nave` publica eventos como `"dano"` e `"game_over"` quando o jogador é atingido ou perde todas as vidas. A classe `Jogo` assina esses eventos no construtor e define os callbacks `_ao_sofrer_dano()` e `_ao_game_over()`. Dessa forma, `Nave` não precisa conhecer `Jogo` — ela simplesmente avisa que algo aconteceu.

## 🔍 Exemplo do projeto

```python
@singleton
class EventManager:
    def __init__(self):
        self._assinantes: dict = {}

    def assinar(self, evento: str, callback):
        """Registra um callback para um tipo de evento."""
        if evento not in self._assinantes:
            self._assinantes[evento] = []
        self._assinantes[evento].append(callback)

    def publicar(self, evento: str, dados=None):
        """Notifica todos os assinantes de um evento."""
        for cb in self._assinantes.get(evento, []):
            cb(dados)


# Em Jogo.__init__() — assinatura dos eventos:
event_manager.assinar("dano",      self._ao_sofrer_dano)
event_manager.assinar("game_over", self._ao_game_over)

# Em Nave.sofrer_dano() — publicação do evento:
def sofrer_dano(self):
    if self.invencivel == 0:
        self.vidas -= 1
        event_manager.publicar("dano", self.vidas)      # avisa os assinantes
        if self.vidas <= 0:
            event_manager.publicar("game_over", None)   # avisa os assinantes
```

## 📚 Recursos para aprofundamento

- [Observer — Refactoring Guru](https://refactoring.guru/design-patterns/observer) — explicação visual com exemplos em Python
- [The Observer Pattern in Python — Real Python](https://realpython.com/python-observer-pattern/) — implementação passo a passo do padrão Observer
