# 🔷 Classes Abstratas com ABC (Abstract Classes)

## 💡 O que é

Uma classe abstrata é uma classe que **não pode ser instanciada diretamente** — ela existe apenas para ser herdada. Seu propósito é definir uma **interface obrigatória**: métodos que toda subclasse concreta *deve* implementar. Se uma subclasse não implementar todos os métodos abstratos, o Python lança um `TypeError` no momento da instanciação.

O módulo `abc` da biblioteca padrão fornece `ABC` (classe base) e o decorator `@abstractmethod` para marcar métodos obrigatórios. Esse mecanismo transforma o contrato de design em uma verificação em tempo de execução, evitando erros sutis causados por subclasses incompletas.

> [!TIP]
> Classes abstratas são especialmente úteis quando diferentes objetos compartilham uma interface comum mas implementações distintas — exatamente o caso de entidades de jogo que precisam de `atualizar()` e `desenhar()`, mas se comportam de formas completamente diferentes.

## ⚙️ Como é usado neste projeto

`EntidadeJogo` é a classe abstrata base de todas as entidades do GI-FORCE. Ela herda de `ABC` e declara dois métodos abstratos: `atualizar()` e `desenhar()`. Qualquer classe que herde de `EntidadeJogo` sem implementar os dois métodos resultará em erro ao ser instanciada — garantindo que o loop principal do jogo possa chamar esses métodos em qualquer entidade com segurança.

As classes `Nave`, `Meteorito`, `Particula` e `CampoEstelar` são as implementações concretas que satisfazem o contrato.

## 🔍 Exemplo do projeto

```python
from abc import ABC, abstractmethod

class EntidadeJogo(ABC):
    """Classe abstrata base para entidades do jogo.
    Toda entidade deve implementar atualizar() e desenhar().
    """

    @abstractmethod
    def atualizar(self):
        """Atualiza o estado da entidade a cada frame."""

    @abstractmethod
    def desenhar(self, tela: pygame.Surface):
        """Desenha a entidade na tela."""


# Implementação concreta obrigatória:
class CampoEstelar(EntidadeJogo):
    def atualizar(self):          # ✅ obrigatório
        for e in self.estrelas:
            e["y"] += e["vel"]

    def desenhar(self, tela):     # ✅ obrigatório
        for e in self.estrelas:
            pygame.draw.circle(tela, ...)

# Tentar instanciar EntidadeJogo diretamente levantaria:
# TypeError: Can't instantiate abstract class EntidadeJogo
# with abstract methods atualizar, desenhar
```

## 📚 Recursos para aprofundamento

- [abc — Python Docs](https://docs.python.org/3/library/abc.html) — documentação oficial do módulo abc
- [Abstract Base Classes in Python — Real Python](https://realpython.com/python-interface/) — guia sobre interfaces e classes abstratas em Python
