# ⚖️ Decisões de Arquitetura (ADRs)

## 🏛️ ADR-001 — Uso do Pygame como engine de jogo

**📅 Data:** 2026
**🚦 Status:** ✅ Aceita

### 💡 Contexto

O projeto precisava de uma biblioteca que fornecesse janela gráfica, loop de eventos, renderização 2D, reprodução de áudio e detecção de input de teclado, com suporte nativo a Python e curva de aprendizado adequada a uma disciplina universitária.

### 🚀 Decisão

Adotar o `pygame` (versão 2.5.2) como única dependência de runtime, declarada em `requirements.txt`.

### 📈 Consequências

**✅ Vantagens:**
- API estável e bem documentada, com suporte a sprites, áudio, fontes e eventos de janela em uma única biblioteca.
- Facilidade de compilar para `.exe` via PyInstaller sem dependências adicionais.

**⚠️ Desvantagens/Riscos:**
- Sem aceleração de hardware por padrão; API mais verbosa que engines modernas.
- Os testes unitários exigem mockar o módulo inteiro para evitar dependência de janela gráfica.

---

## 🏛️ ADR-002 — Classe abstrata `EntidadeJogo` como contrato de interface

**📅 Data:** 2026
**🚦 Status:** ✅ Aceita

### 💡 Contexto

O sistema possui vários tipos de objetos visuais que participam do loop do jogo (`Nave`, `Meteorito`, `Particula`, `CampoEstelar`). Era necessário garantir que todos implementassem `atualizar()` e `desenhar()`, evitando erros silenciosos de objeto com método faltando.

### 🚀 Decisão

Criar `EntidadeJogo(ABC)` com `@abstractmethod` para `atualizar()` e `desenhar()`. Toda entidade do jogo herda dessa classe.

### 📈 Consequências

**✅ Vantagens:**
- Erro detectado na criação do objeto (`TypeError`), não em tempo de execução.
- Facilita a adição de novas entidades com garantia de contrato.

**⚠️ Desvantagens/Riscos:**
- Pequena rigidez — entidades que não precisem de ambos os métodos ainda são obrigadas a implementá-los (ainda que como passthrough).

---

## 🏛️ ADR-003 — Padrão Observer para comunicação entre `Nave` e `Jogo`

**📅 Data:** 2026
**🚦 Status:** ✅ Aceita

### 💡 Contexto

A `Nave` precisa notificar o `Jogo` quando sofre dano ou perde todas as vidas. Uma chamada direta (`jogo.ao_sofrer_dano()`) criaria acoplamento forte entre as classes.

### 🚀 Decisão

Implementar o `EventManager` como despachante de eventos (Observer), com `assinar()` e `publicar()`. `Nave` publica eventos; `Jogo` os assina.

### 📈 Consequências

**✅ Vantagens:**
- `Nave` não conhece `Jogo`. Novos assinantes podem ser adicionados sem modificar `Nave`.

**⚠️ Desvantagens/Riscos:**
- Fluxo de controle menos óbvio para leitores do código — a reação ao evento está deslocada da sua origem.

---

## 🏛️ ADR-004 — Singleton para o `EventManager`

**📅 Data:** 2026
**🚦 Status:** ✅ Aceita

### 💡 Contexto

O `EventManager` é um recurso compartilhado globalmente — qualquer entidade pode publicar eventos, e `Jogo` precisa assinar a mesma instância que `Nave` usa para publicar.

### 🚀 Decisão

Implementar o decorator `@singleton` e aplicá-lo a `EventManager`, garantindo que `EventManager()` retorne sempre o mesmo objeto.

### 📈 Consequências

**✅ Vantagens:**
- Elimina a necessidade de passar a instância do gerenciador por parâmetro em todo o código.
- Simples de implementar com decorator em Python.

**⚠️ Desvantagens/Riscos:**
- Introduz estado global, o que os testes de `TestSingleton` precisam considerar (a instância persiste entre casos de teste).

---

## 🏛️ ADR-005 — Compilação para executável Windows via PyInstaller

**📅 Data:** 2026
**🚦 Status:** ✅ Aceita

### 💡 Contexto

O projeto precisava ser distribuído como executável sem exigir que o usuário instale Python ou dependências manualmente.

### 🚀 Decisão

Usar PyInstaller com `GiForce.spec` para empacotar `main.py` e todos os assets (`assets/fonts/`, `assets/images/`, `assets/sounds/`). O script `build.bat` automatiza o processo no Windows.

### 📈 Consequências

**✅ Vantagens:**
- Distribuição simples via `.exe`; o usuário final não precisa configurar ambiente Python.

**⚠️ Desvantagens/Riscos:**
- Binário resultante é volumoso (inclui Python runtime). Requer ambiente Windows para build.
- As funções `caminho_imagem()` e similares precisam tratar o caso `sys.frozen` para localizar assets corretamente dentro do executável.
