# 🧩 Orientação a Objetos — Classes (Object-Oriented Programming)

## 💡 O que é

A Programação Orientada a Objetos (POO) é um paradigma que organiza o software em torno de **objetos** — entidades que combinam **dados** (atributos) e **comportamentos** (métodos) em uma única unidade chamada classe. Classes funcionam como moldes: cada vez que um objeto é criado a partir delas, chamamos isso de **instanciação**.

Encapsulamento é um dos pilares da POO: ao agrupar estado e lógica dentro da mesma classe, limitamos o impacto de mudanças internas e deixamos o código mais fácil de manter. Em Python, classes são definidas com `class`, o método especial `__init__` é o construtor, e `self` referencia a instância corrente.

## ⚙️ Como é usado neste projeto

O GI-FORCE é estruturado inteiramente em POO. Cada elemento do jogo é uma classe com responsabilidade bem definida:

| Classe | Responsabilidade |
|--------|-----------------|
| `Nave` | Estado e movimentação do jogador |
| `Meteorito` | Lógica de queda, rotação e colisão dos asteroides |
| `Particula` | Efeito visual de explosão com vida útil |
| `CampoEstelar` | Fundo animado com paralaxe de estrelas |
| `Jogo` | Loop principal, estados e coordenação geral |
| `EventManager` | Gerenciamento desacoplado de eventos do jogo |
| `MeteoritoFactory` | Criação centralizada de instâncias de meteoritos |

Objetos são criados dinamicamente durante o jogo — por exemplo, a cada ciclo de spawn um novo `Meteorito` é instanciado, e a cada colisão várias `Particula` são criadas.

## 🔍 Exemplo do projeto

```python
class Nave(EntidadeJogo):
    """Representa a nave do jogador."""

    LARGURA = 72   # atributo de classe (compartilhado por todas as instâncias)
    ALTURA  = 84
    VEL     = 5

    def __init__(self):
        self.x = LARGURA // 2   # atributos de instância (únicos por objeto)
        self.y = ALTURA - 80
        self.vidas = 3
        self.vivo = True

    def sofrer_dano(self):
        if self.invencivel == 0:
            self.vidas -= 1
            self.invencivel = 90

# Instanciação durante o jogo
self.nave = Nave()                         # cria o objeto jogador
self.particulas.append(Particula(x, y, cor))  # cria partículas dinamicamente
```

## 📚 Recursos para aprofundamento

- [Classes — Python Docs](https://docs.python.org/3/tutorial/classes.html) — tutorial oficial sobre POO em Python
- [Object-Oriented Programming in Python — Real Python](https://realpython.com/python3-object-oriented-programming/) — guia completo com exemplos práticos
