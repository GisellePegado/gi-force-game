# 📋 List Comprehension (List Comprehension)

## 💡 O que é

List comprehension é uma sintaxe concisa do Python para criar listas a partir de iteráveis existentes, com filtragem e transformação opcionais — tudo em uma única expressão. A forma geral é:

```python
[expressão for item in iterável if condição]
```

Além de mais legível que um loop `for` equivalente, list comprehensions tendem a ser mais rápidas porque o Python as otimiza internamente. Elas expressam **o que** se quer obter, em vez de **como** iterar — o que aproxima o código de uma linguagem declarativa.

O mesmo padrão se aplica a **dict comprehensions** (`{chave: valor for ...}`) e **set comprehensions** (`{valor for ...}`).

## ⚙️ Como é usado neste projeto

O GI-FORCE usa list comprehensions em três contextos distintos:

| Uso | Onde | Propósito |
|-----|------|-----------|
| **Geração** | `CampoEstelar.__init__()` | Cria 150 estrelas com atributos aleatórios |
| **Filtragem** | `Nave.atualizar()` | Remove pontos do rastro de fogo que esgotaram a vida |
| **Filtragem** | `Jogo._atualizar_jogo()` | Remove meteoritos fora da tela e partículas extintas |

## 🔍 Exemplo do projeto

```python
# Geração — cria 150 dicionários de estrelas de uma vez:
self.estrelas = [
    {
        "x":      random.randint(0, LARGURA),
        "y":      random.randint(0, ALTURA),
        "vel":    random.uniform(0.3, 2.5),
        "raio":   random.choice([1, 1, 1, 2, 2, 3]),
        "brilho": random.randint(100, 255),
    }
    for _ in range(quantidade)   # _ indica que o índice não é usado
]

# Filtragem — mantém apenas partículas ainda vivas:
self.particulas = [p for p in self.particulas if p.vivo]

# Filtragem — mantém apenas meteoritos ainda na tela:
self.meteoritos = [m for m in self.meteoritos if not m.fora_da_tela]

# Filtragem no rastro da nave — remove pontos com vida <= 0:
self.trail = [p for p in self.trail if p["vida"] > 0]
```

## 📚 Recursos para aprofundamento

- [List Comprehensions — Python Docs](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions) — documentação oficial com exemplos
- [When to Use a List Comprehension in Python — Real Python](https://realpython.com/list-comprehension-python/) — guia sobre quando usar (e quando evitar) list comprehensions
