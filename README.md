# GI-FORCE

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-2.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Descrição

GI-FORCE é um jogo 2D de esquiva desenvolvido em Python com Pygame. Pilote uma nave espacial e desvire de meteoritos que caem em velocidade crescente. A dificuldade aumenta automaticamente a cada 50 pontos.

## Screenshots

![Menu Principal](assets/screenshots/menu.png)
![Jogo em Ação](assets/screenshots/gameplay.png)
![Game Over](assets/screenshots/gameover.png)

No século XXIII, a exploração desenfreada tornou a Terra inabitável e quase extinguiu a humanidade. A astrofísica Giselle Pegado descobriu um planeta distante com gravidade semelhante à da Terra e o batizou de **Gi-Force**. Com os últimos sobreviventes a bordo, a nave parte rumo ao novo lar — mas uma implacável chuva de meteoros ameaça encerrar de vez a história da humanidade. Desviar é a única chance de sobrevivência.

## Funcionalidades

- Jogo 2D com janela gráfica
- Menu principal navegável
- Sistema de vidas com invencibilidade temporária
- Pontuação com recorde salvo
- Progressão automática de dificuldade
- Efeitos visuais: partículas, rastro de fogo, fundo estrelado
- Áudio: música de fundo e efeitos sonoros
- Pause e Game Over
- Executável Windows via PyInstaller

## Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip

### Passos

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/gi-force.git
   cd gi-force
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Como Jogar

Execute o jogo:

```bash
python main.py
```

### Controles

| Tecla                     | Ação                           |
| ------------------------- | ------------------------------ |
| `← → ↑ ↓` ou `W A S D`    | Mover a nave                   |
| `ENTER` ou `ENTER (num.)` | Confirmar / Pausar / Continuar |
| `ESC`                     | Voltar ao menu / Fechar        |

## Desenvolvimento

### Estrutura do Projeto

```
├── main.py              # Código principal do jogo
├── test_giforce.py      # Testes unitários
├── requirements.txt     # Dependências Python
├── build.bat            # Script para gerar .exe (Windows)
├── GiForce.spec         # Configuração PyInstaller
├── README.md            # Este arquivo
├── scores.json          # Arquivo de recordes
└── assets/
    ├── fonts/
    │   └── PressStart2P-Regular.ttf
    ├── images/
    │   ├── asteroid-small.png
    │   ├── asteroid-medium.png
    │   ├── asteroid-large.png
    │   ├── spaceship.png
    │   └── spaceship.ico
    └── sounds/
        ├── musica_menu.mp3
        ├── game_over.mp3
        ├── colisao.wav
        ├── select.wav
        ├── leave.wav
        ├── byebye.wav
        ├── dead.wav
        └── hallelujah.wav
```

### Testes

Execute os testes unitários:

```bash
python -m unittest test_giforce -v
```

### Build

Para gerar o executável Windows:

1. Instale PyInstaller:

   ```bash
   pip install pyinstaller
   ```

2. Execute o build:
   ```bash
   pyinstaller GiForce.spec
   ```
   Ou use `build.bat`.

## Conteúdos da Disciplina Aplicados

### Aula 1 — Bibliotecas Python

| Conteúdo   | Aplicação                                                   |
| ---------- | ----------------------------------------------------------- |
| **Pygame** | Base do jogo: janela, eventos, desenho 2D, colisões, áudio  |
| **JSON**   | `carregar_recorde()` e `salvar_recorde()` via `scores.json` |

### Aula 2 — POO e UML

| Conteúdo                | Aplicação                                                                                                                  |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| **Classes**             | `Nave`, `Meteorito`, `Particula`, `CampoEstelar`, `Jogo`, `EventManager`, `MeteoritoFactory`                               |
| **Atributos e métodos** | Encapsulamento em todas as classes                                                                                         |
| **Instanciação**        | Objetos criados dinamicamente durante o jogo                                                                               |
| **Herança**             | `MeteoritoPequeno`, `MeteoritoMedio`, `MeteoritoGrande` herdam de `Meteorito`; todas as entidades herdam de `EntidadeJogo` |

### Aula 3 — Módulos e Design Patterns Criacionais

| Conteúdo                    | Aplicação                                                            |
| --------------------------- | -------------------------------------------------------------------- |
| **Módulos**                 | `pygame`, `math`, `random`, `sys`, `os`, `json`, `abc`               |
| **ABC (Classes Abstratas)** | `EntidadeJogo(ABC)` com `@abstractmethod atualizar()` e `desenhar()` |
| **Design Pattern Factory**  | `MeteoritoFactory.criar()` instancia a subclasse correta por tipo    |

### Aula 4 — Eventos, Decorators, List Comprehension e Design Patterns Comportamentais

| Conteúdo                    | Aplicação                                                                      |
| --------------------------- | ------------------------------------------------------------------------------ |
| **Eventos de teclado**      | `pygame.KEYDOWN` tratado em `_tratar_eventos()`                                |
| **Decorator de classe**     | `@singleton` aplicado ao `EventManager`                                        |
| **Decorator de função**     | `@validar_positivo` aplicado ao `salvar_recorde()`                             |
| **List Comprehension**      | Geração de estrelas, filtragem de partículas e meteoritos                      |
| **Design Pattern Observer** | `EventManager` com `assinar()` e `publicar()` para eventos de dano e game over |

### Aula 5 — Banco de Dados e Design Patterns Estruturais

| Conteúdo | Aplicação                                             |
| -------- | ----------------------------------------------------- |
| **JSON** | Persistência do recorde entre sessões (`scores.json`) |

### Aula 6 — Ferramentas e Testes

| Conteúdo                  | Aplicação                                              |
| ------------------------- | ------------------------------------------------------ |
| **Testes Unitários**      | `test_giforce.py` com 21 testes em 6 grupos (unittest) |
| **Geração de Executável** | PyInstaller via `GiForce.spec` e `build.bat`           |

## Contribuição

Contribuições são bem-vindas! Por favor, veja [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes.

## Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Autor

- **Giselle Pegado** - RU: 5052104 - [GitHub](https://github.com/seu-usuario)

---

_Projeto desenvolvido como atividade prática para a disciplina Linguagem de Programação Aplicada - UNINTER_
