# 🏭 Padrão de Projeto Factory (Factory Pattern)

## 💡 O que é

O Factory (ou Factory Method) é um padrão de projeto **criacional** que centraliza a lógica de criação de objetos em um único lugar, desacoplando o código que usa os objetos do código que os instancia. Em vez de chamar `MinhaClasse()` diretamente em vários lugares, o código cliente chama um método de fábrica que decide qual classe instanciar e como configurá-la.

As principais vantagens são: facilidade de adicionar novos tipos sem alterar o código cliente, possibilidade de encapsular lógica complexa de inicialização, e centralização de regras de criação para facilitar testes e manutenção. É especialmente útil quando o tipo exato do objeto a ser criado só é conhecido em tempo de execução.

## ⚙️ Como é usado neste projeto

`MeteoritoFactory` é a fábrica de meteoritos do GI-FORCE. Seu método estático `criar()` sorteia aleatoriamente o tipo (`"pequeno"`, `"medio"` ou `"grande"`), calcula a velocidade com base no nível atual do jogo, e instancia a subclasse correta de `Meteorito`. O código do loop principal simplesmente chama `MeteoritoFactory.criar(self.nivel)` — sem precisar conhecer as três subclasses.

Isso garante que, caso um novo tipo de meteorito seja adicionado, basta atualizar a factory sem tocar no loop do jogo.

## 🔍 Exemplo do projeto

```python
class MeteoritoFactory:
    """Fábrica de meteoros (padrão Factory)."""

    TIPOS = ["pequeno", "medio", "grande"]

    @staticmethod
    def criar(nivel: int = 1) -> "Meteorito":
        """Cria a subclasse de meteorito correspondente ao tipo sorteado."""
        tipo = random.choice(MeteoritoFactory.TIPOS)
        velocidade_base = 2 + nivel * 0.5
        classes = {
            "pequeno": MeteoritoPequeno,
            "medio":   MeteoritoMedio,
            "grande":  MeteoritoGrande,
        }
        return classes[tipo](velocidade_base=velocidade_base)


# Uso no loop do jogo — o cliente não precisa conhecer as subclasses:
self.meteoritos.append(MeteoritoFactory.criar(self.nivel))
```

## 📚 Recursos para aprofundamento

- [Factory Method — Refactoring Guru](https://refactoring.guru/design-patterns/factory-method) — explicação visual do padrão com exemplos em Python
- [The Factory Method Pattern in Python — Real Python](https://realpython.com/factory-method-python/) — implementação detalhada e casos de uso reais
