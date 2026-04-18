# 🚀 Implantação

## 📋 Requisitos de ambiente

| Dependência | Versão mínima | Instalação |
|-------------|---------------|------------|
| Python | 3.8+ | [python.org/downloads](https://www.python.org/downloads/) |
| pygame | 2.5.2 | `pip install -r requirements.txt` |
| PyInstaller | qualquer | `pip install pyinstaller` (apenas para build) |

## 🔑 Variáveis de ambiente

Nenhuma variável de ambiente é necessária. O jogo usa caminhos relativos ao diretório do executável ou do script.

## 💻 Execução local

```bash
# 1. Clone o repositório
git clone https://github.com/GisellePegado/gi-force-game.git
cd gi-force-game

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute o jogo
python main.py
```

## Resolução de caminhos (assets)

O projeto resolve caminhos de assets de forma compatível tanto com execução direta quanto com o executável compilado. O mesmo padrão é aplicado em `caminho_som()`, `caminho_fonte()` e `caminho_recorde()`:

```python
def caminho_imagem(arquivo: str) -> str:
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)   # executável PyInstaller
    else:
        base = os.path.dirname(os.path.abspath(__file__))  # script Python
    return os.path.join(base, "assets", "images", arquivo)
```

> [!IMPORTANT]
> Todos os assets de áudio e imagem são carregados com `try/except pygame.error`, permitindo que o jogo rode mesmo com arquivos ausentes — exibindo avisos no console em vez de travar.

## 🏗️ Build do executável Windows

```bash
# 1. Instale o PyInstaller
pip install pyinstaller

# 2. Execute o build via spec (recomendado)
pyinstaller GiForce.spec

# 3. Ou use o script batch (Windows)
build.bat
```

O executável gerado estará em `dist/GiForce/GiForce.exe`, com todos os assets incluídos.

## Estrutura de assets necessária

```
gi-force-game/
├── main.py
├── requirements.txt
└── assets/
    ├── fonts/
    │   └── PressStart2P-Regular.ttf
    ├── images/
    │   ├── spaceship.png
    │   ├── spaceship.ico
    │   ├── asteroid-small.png
    │   ├── asteroid-medium.png
    │   └── asteroid-large.png
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
