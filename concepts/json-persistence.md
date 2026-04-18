# 💾 Persistência com JSON (JSON Persistence)

## 💡 O que é

JSON (_JavaScript Object Notation_) é um formato de texto leve para representar dados estruturados como pares chave-valor, listas e objetos aninhados. Por ser legível por humanos e suportado nativamente em quase todas as linguagens de programação, tornou-se o padrão mais comum para armazenar e trocar dados simples.

No Python, o módulo `json` da biblioteca padrão oferece as funções `json.load()` / `json.dump()` para ler e escrever arquivos JSON, e `json.loads()` / `json.dumps()` para manipular strings. Ao usar JSON para persistência local, o dado sobrevive ao encerramento do programa — o que é ideal para configurações, rankings e preferências do usuário.

## ⚙️ Como é usado neste projeto

O GI-FORCE usa JSON para persistir o recorde entre sessões. O arquivo `scores.json` é gerado na mesma pasta do executável e armazena um único campo `"recorde"`. As funções `carregar_recorde()` e `salvar_recorde()` encapsulam toda a leitura e escrita, tratando erros como arquivo inexistente ou JSON corrompido com segurança.

> [!NOTE]
> O caminho do arquivo é resolvido por `caminho_recorde()`, que detecta se o programa roda como script Python normal ou como `.exe` compilado pelo PyInstaller — garantindo que o `scores.json` sempre seja salvo ao lado do executável.

## 🔍 Exemplo do projeto

```python
# scores.json gerado em disco:
{"recorde": 1500}

# Leitura — carregar_recorde()
def carregar_recorde() -> int:
    try:
        with open(caminho_recorde(), "r") as f:
            return json.load(f).get("recorde", 0)
    except (FileNotFoundError, ValueError, KeyError):
        return 0   # valor seguro se o arquivo não existir ou estiver corrompido

# Escrita — salvar_recorde() (protegida pelo decorator @validar_positivo)
@validar_positivo
def salvar_recorde(pontuacao: int) -> None:
    with open(caminho_recorde(), "w") as f:
        json.dump({"recorde": pontuacao}, f)
```

## 📚 Recursos para aprofundamento

- [json — Python Docs](https://docs.python.org/3/library/json.html) — documentação oficial do módulo json
- [Working With JSON Data in Python — Real Python](https://realpython.com/python-json/) — guia prático de leitura, escrita e validação de JSON
