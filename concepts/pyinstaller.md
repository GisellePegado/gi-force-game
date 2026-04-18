# 📦 Geração de Executável com PyInstaller (PyInstaller)

## 💡 O que é

PyInstaller é uma ferramenta que empacota um projeto Python — scripts, dependências e assets — em um **executável standalone**. O usuário final pode rodar o programa sem ter Python instalado: tudo que ele precisa está dentro do `.exe` (Windows), do binário (Linux) ou do `.app` (macOS).

O processo funciona em duas etapas: primeiro, o PyInstaller analisa o código e descobre todas as importações; depois, gera um diretório `dist/` com o executável e os arquivos de suporte. A configuração avançada é feita via arquivo `.spec` — um script Python gerado automaticamente na primeira execução que pode ser editado para incluir arquivos extras (como `assets/`), definir ícone, ajustar modo console/janela e muito mais.

Um detalhe importante ao usar PyInstaller com arquivos de recurso (imagens, sons, fontes): o diretório de trabalho muda quando o programa é empacotado, então o código precisa detectar se está rodando como script normal ou como executável compilado para montar os caminhos corretamente.

## ⚙️ Como é usado neste projeto

O GI-FORCE usa PyInstaller para gerar um executável Windows do jogo. A configuração está em `GiForce.spec`, que instrui o empacotador a incluir as pastas `assets/` (imagens, fontes e sons) no bundle. O `build.bat` automatiza o processo com um único duplo-clique.

Todo o código de resolução de caminhos usa `getattr(sys, 'frozen', False)` para distinguir os dois modos de execução:

> [!IMPORTANT]
> Sem a detecção de `sys.frozen`, o executável gerado não encontraria os arquivos de assets — o diretório de trabalho muda quando o PyInstaller empacota o programa e os caminhos relativos deixam de funcionar.

## 🔍 Exemplo do projeto

```bat
:: build.bat — gera o executável com um duplo clique
pyinstaller GiForce.spec
pause
```

```python
# Detecção do modo de execução — padrão usado em todas as funções de caminho:
def caminho_som(arquivo: str) -> str:
    if getattr(sys, 'frozen', False):
        # Rodando como .exe compilado pelo PyInstaller
        base = os.path.dirname(sys.executable)
    else:
        # Rodando como script Python normal
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "assets", "sounds", arquivo)
```

## 📚 Recursos para aprofundamento

- [PyInstaller Manual](https://pyinstaller.org/en/stable/) — documentação oficial completa
- [Using PyInstaller to Easily Distribute Python Applications — Real Python](https://realpython.com/pyinstaller-python/) — guia prático com exemplos de `.spec` e assets
