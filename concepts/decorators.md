# 🎀 Decorators (Decorators)

## 💡 O que é

Um decorator é uma função (ou classe) que **envolve outra função ou classe** para modificar ou estender seu comportamento sem alterar seu código original. Em Python, decorators são aplicados com a sintaxe `@nome_decorator` logo acima da definição da função ou classe.

Decorators exploram o fato de que funções são objetos de primeira classe em Python: podem ser passadas como argumentos, retornadas de outras funções e armazenadas em variáveis. O padrão geral é:

```
decorator(funcao_original) → funcao_nova_com_comportamento_extra
```

Existem dois usos principais no projeto:
- **Decorator de função:** modifica o comportamento de uma função específica (validação, logging, cache, etc.)
- **Decorator de classe:** transforma a própria classe — pode interceptar a criação de instâncias, como faz o Singleton.

## ⚙️ Como é usado neste projeto

O GI-FORCE usa dois decorators distintos:

**`@validar_positivo` (decorator de função):** garante que a pontuação passada a `salvar_recorde()` nunca seja negativa. Se o valor recebido for menor que zero, ele é corrigido para zero antes de a função executar. Isso protege o `scores.json` de valores inválidos sem poluir a lógica de negócio da função original.

**`@singleton` (decorator de classe):** aplicado ao `EventManager`, garante que apenas uma instância seja criada (veja o conceito [Padrão Singleton](singleton-pattern.md)).

## 🔍 Exemplo do projeto

```python
# Decorator de função — validação de entrada:
def validar_positivo(func):
    """Garante que a pontuação seja não-negativa antes de salvar."""
    def wrapper(pontuacao: int):
        if pontuacao < 0:
            pontuacao = 0       # corrige silenciosamente
        return func(pontuacao)  # chama a função original com o valor corrigido
    return wrapper


@validar_positivo
def salvar_recorde(pontuacao: int) -> None:
    """Salva a pontuação como novo recorde no scores.json."""
    with open(caminho_recorde(), "w") as f:
        json.dump({"recorde": pontuacao}, f)


# Uso — o decorator age de forma transparente:
salvar_recorde(-50)   # internamente salva 0, não -50
salvar_recorde(1500)  # salva 1500 normalmente
```

> [!TIP]
> O decorator `wrapper` recebe os mesmos parâmetros da função original e os repassa após a validação — esse é o padrão mais comum para decorators de função em Python.

## 📚 Recursos para aprofundamento

- [Primer on Python Decorators — Real Python](https://realpython.com/primer-on-python-decorators/) — guia completo sobre decorators de função e classe
- [functools.wraps — Python Docs](https://docs.python.org/3/library/functools.html#functools.wraps) — como preservar o nome e docstring da função decorada
