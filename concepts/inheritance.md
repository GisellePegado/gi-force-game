# 🧬 Herança (Inheritance)

## 💡 O que é

Herança é o mecanismo da POO que permite criar uma nova classe (subclasse) a partir de uma classe existente (superclasse), reaproveitando e especializando seu comportamento. A subclasse herda todos os atributos e métodos da superclasse e pode sobrescrevê-los ou estendê-los conforme necessário.

Em Python, a herança é declarada colocando a superclasse entre parênteses no cabeçalho da classe: `class Filha(Pai)`. A função `super()` é usada para chamar o construtor ou métodos da classe pai sem precisar nomear explicitamente a superclasse — o que facilita a manutenção quando a hierarquia muda.

Herança promove o princípio **DRY** (_Don't Repeat Yourself_): comportamento comum fica na superclasse, enquanto variações específicas ficam nas subclasses.

## ⚙️ Como é usado neste projeto

O GI-FORCE usa herança em dois níveis:

**Nível 1 — `EntidadeJogo` como raiz de todas as entidades:**  
`Nave`, `Meteorito`, `Particula` e `CampoEstelar` herdam de `EntidadeJogo`, garantindo que toda entidade implemente `atualizar()` e `desenhar()`.

**Nível 2 — Especialização de `Meteorito`:**  
`MeteoritoPequeno`, `MeteoritoMedio` e `MeteoritoGrande` herdam de `Meteorito`. Cada subclasse apenas chama `super().__init__()` passando seu tipo fixo — todo o comportamento de movimento, colisão e renderização já está implementado na superclasse.

```
EntidadeJogo (ABC)
├── Nave
├── CampoEstelar
├── Particula
└── Meteorito
    ├── MeteoritoPequeno
    ├── MeteoritoMedio
    └── MeteoritoGrande
```

## 🔍 Exemplo do projeto

```python
class Meteorito(EntidadeJogo):
    """Superclasse com toda a lógica de um meteorito."""
    CONFIGS = {
        "pequeno": {"raio": 15, "pontos": 10, "vel_rot": 4, ...},
        "medio":   {"raio": 25, "pontos": 5,  "vel_rot": 2, ...},
        "grande":  {"raio": 40, "pontos": 2,  "vel_rot": 1, ...},
    }

    def __init__(self, tipo: str, velocidade_base: float):
        cfg = self.CONFIGS[tipo]
        self.raio = cfg["raio"]
        self.pontos = cfg["pontos"]
        # ... demais atributos


class MeteoritoPequeno(Meteorito):
    """Subclasse que fixa o tipo 'pequeno' — rápido e vale mais pontos."""
    def __init__(self, velocidade_base: float):
        super().__init__(tipo="pequeno", velocidade_base=velocidade_base)


class MeteoritoGrande(Meteorito):
    """Subclasse que fixa o tipo 'grande' — lento e vale menos pontos."""
    def __init__(self, velocidade_base: float):
        super().__init__(tipo="grande", velocidade_base=velocidade_base)
```

## 📚 Recursos para aprofundamento

- [Inheritance — Python Docs](https://docs.python.org/3/tutorial/classes.html#inheritance) — documentação oficial sobre herança em Python
- [Inheritance and Composition — Real Python](https://realpython.com/inheritance-composition-python/) — guia completo comparando herança e composição
