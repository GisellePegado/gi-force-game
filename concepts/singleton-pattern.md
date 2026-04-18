# 🔒 Padrão de Projeto Singleton (Singleton Pattern)

## 💡 O que é

O Singleton é um padrão de projeto **criacional** que garante que uma classe tenha **apenas uma instância** durante toda a execução do programa, e fornece um ponto de acesso global a essa instância. É útil quando exatamente um objeto é necessário para coordenar ações em todo o sistema — como um gerenciador de eventos, um pool de conexões ou um logger.

Em Python, o Singleton pode ser implementado de várias formas. Uma abordagem elegante é criar um **decorator de classe**: uma função que envolve a classe alvo e intercepta cada chamada de criação, retornando a instância existente se ela já tiver sido criada.

> [!NOTE]
> Embora o Singleton seja amplamente conhecido, ele deve ser usado com cuidado: torna o estado global implícito e pode dificultar testes unitários. No contexto de um gerenciador de eventos centralizado em um jogo, ele é uma escolha justificada.

## ⚙️ Como é usado neste projeto

O `@singleton` é um decorator de classe definido em `main.py` e aplicado ao `EventManager`. Isso garante que todos os subsistemas do jogo que obtêm uma referência ao `EventManager` estejam sempre falando com o mesmo objeto — fundamental para que publicações e assinaturas de eventos funcionem de forma coerente.

## 🔍 Exemplo do projeto

```python
def singleton(cls):
    """Decorator de classe: garante que apenas uma instância seja criada."""
    _instancias = {}

    def _obter(*args, **kwargs):
        if cls not in _instancias:
            _instancias[cls] = cls(*args, **kwargs)
        return _instancias[cls]

    return _obter


@singleton
class EventManager:
    """Gerenciador de eventos — existe apenas uma instância no jogo."""

    def __init__(self):
        self._assinantes: dict = {}

    def assinar(self, evento: str, callback):
        ...

    def publicar(self, evento: str, dados=None):
        ...


# Chamadas posteriores retornam sempre o mesmo objeto:
em1 = EventManager()
em2 = EventManager()
assert em1 is em2  # True — mesma instância
```

## 📚 Recursos para aprofundamento

- [Singleton — Refactoring Guru](https://refactoring.guru/design-patterns/singleton) — visão geral do padrão com diagramas e exemplos em Python
- [Implementing Singleton in Python](https://python-patterns.guide/gang-of-four/singleton/) — comparação de abordagens de implementação em Python
