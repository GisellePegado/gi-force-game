# ✅ Casos de Teste

> Todos os casos estão implementados em `test_giforce.py` e executados com `python -m unittest test_giforce -v`.

---

## Grupo 1 — Persistência de Recorde (JSON)

### 🧪 CT-001 — Carregar recorde com arquivo ausente

| Campo | Valor |
|-------|-------|
| **Pré-condição** | Caminho de recorde aponta para arquivo inexistente |
| **Entrada** | `/nao/existe.json` (via `patch`) |
| **Passos** | Chamar `main.carregar_recorde()` |
| **Resultado esperado** | Retorna `0` sem lançar exceção |
| **Resultado obtido** | ✅ Aprovado |

### 🧪 CT-002 — Salvar e carregar preserva valor

| Campo | Valor |
|-------|-------|
| **Pré-condição** | Arquivo temporário criado via `tempfile` |
| **Entrada** | `pontuacao = 1500` |
| **Passos** | `salvar_recorde(1500)` → `carregar_recorde()` |
| **Resultado esperado** | Retorna `1500` |
| **Resultado obtido** | ✅ Aprovado |

### 🧪 CT-003 — Salvar zero

| Campo | Valor |
|-------|-------|
| **Entrada** | `pontuacao = 0` |
| **Passos** | `salvar_recorde(0)` → `carregar_recorde()` |
| **Resultado esperado** | Retorna `0` |
| **Resultado obtido** | ✅ Aprovado |

### 🧪 CT-004 — Arquivo JSON corrompido

| Campo | Valor |
|-------|-------|
| **Pré-condição** | Arquivo contém `"conteudo_invalido!!!"` |
| **Passos** | Chamar `carregar_recorde()` |
| **Resultado esperado** | Retorna `0` sem lançar exceção |
| **Resultado obtido** | ✅ Aprovado |

### 🧪 CT-005 — Sobrescrever recorde existente

| Campo | Valor |
|-------|-------|
| **Passos** | `salvar_recorde(100)` → `salvar_recorde(900)` → `carregar_recorde()` |
| **Resultado esperado** | Retorna `900` (valor mais recente) |
| **Resultado obtido** | ✅ Aprovado |

---

## Grupo 2 — Decorator `@validar_positivo`

### 🧪 CT-006 — Pontuação negativa é corrigida

| Campo | Valor |
|-------|-------|
| **Entrada** | `pontuacao = -500` |
| **Passos** | `salvar_recorde(-500)` → `carregar_recorde()` |
| **Resultado esperado** | Retorna `0` (decorator corrigiu para zero) |
| **Resultado obtido** | ✅ Aprovado |

### 🧪 CT-007 — Pontuação positiva não é alterada

| Campo | Valor |
|-------|-------|
| **Entrada** | `pontuacao = 750` |
| **Passos** | `salvar_recorde(750)` → `carregar_recorde()` |
| **Resultado esperado** | Retorna `750` sem modificação |
| **Resultado obtido** | ✅ Aprovado |

---

## Grupo 3 — Cálculo de Nível

### 🧪 CT-008 — Nível inicial é 1

| Campo | Valor |
|-------|-------|
| **Entrada** | `pontuacao = 0` |
| **Resultado esperado** | `1 + 0 // 50 = 1` |
| **Resultado obtido** | ✅ Aprovado |

### 🧪 CT-009 — Nível sobe exatamente aos 50 pontos

| Campo | Valor |
|-------|-------|
| **Entrada** | `pontuacao = 49` e `pontuacao = 50` |
| **Resultado esperado** | 49 → nível 1; 50 → nível 2 |
| **Resultado obtido** | ✅ Aprovado |

### 🧪 CT-010 — Progressão de múltiplos níveis

| Campo | Valor |
|-------|-------|
| **Entrada** | `{0:1, 50:2, 100:3, 150:4, 450:10}` (via `subTest`) |
| **Resultado esperado** | Cada pontuação mapeia ao nível correto |
| **Resultado obtido** | ✅ Aprovado |

---

## Grupo 4 — ABC `EntidadeJogo`

### 🧪 CT-011 — Instanciação direta lança TypeError

| Campo | Valor |
|-------|-------|
| **Passos** | `EntidadeJogo()` |
| **Resultado esperado** | `TypeError` (classe abstrata) |
| **Resultado obtido** | ✅ Aprovado |

### 🧪 CT-012 — Subclasse sem `desenhar()` lança TypeError

| Campo | Valor |
|-------|-------|
| **Passos** | Criar `Incompleta(EntidadeJogo)` apenas com `atualizar()`; instanciar |
| **Resultado esperado** | `TypeError` |
| **Resultado obtido** | ✅ Aprovado |

### 🧪 CT-013 — Subclasse sem `atualizar()` lança TypeError

| Campo | Valor |
|-------|-------|
| **Passos** | Criar `Incompleta(EntidadeJogo)` apenas com `desenhar()`; instanciar |
| **Resultado esperado** | `TypeError` |
| **Resultado obtido** | ✅ Aprovado |

### 🧪 CT-014 — Subclasse completa instancia com sucesso

| Campo | Valor |
|-------|-------|
| **Passos** | Criar `Completa(EntidadeJogo)` com ambos os métodos; instanciar |
| **Resultado esperado** | Instância criada; `isinstance(obj, EntidadeJogo)` é `True` |
| **Resultado obtido** | ✅ Aprovado |

---

## Grupo 5 — Hierarquia de Herança

### 🧪 CT-015 a CT-017 — Subclasses herdam de Meteorito

| Campo | Valor |
|-------|-------|
| **Entrada** | `MeteoritoPequeno`, `MeteoritoMedio`, `MeteoritoGrande` (via `subTest`) |
| **Resultado esperado** | `issubclass(cls, Meteorito)` é `True` para cada um |
| **Resultado obtido** | ✅ Aprovado (3 sub-testes) |

### 🧪 CT-018 — Nave herda de EntidadeJogo

| Campo | Valor |
|-------|-------|
| **Resultado esperado** | `issubclass(Nave, EntidadeJogo)` é `True` |
| **Resultado obtido** | ✅ Aprovado |

### 🧪 CT-019 — Particula e CampoEstelar herdam de EntidadeJogo

| Campo | Valor |
|-------|-------|
| **Resultado esperado** | `issubclass` retorna `True` para ambas |
| **Resultado obtido** | ✅ Aprovado |

---

## Grupo 6 — Singleton do EventManager

### 🧪 CT-020 — Duas chamadas retornam a mesma instância

| Campo | Valor |
|-------|-------|
| **Passos** | `instancia1 = EventManager()` → `instancia2 = EventManager()` |
| **Resultado esperado** | `instancia1 is instancia2` |
| **Resultado obtido** | ✅ Aprovado |

### 🧪 CT-021 — Variável global é a mesma instância

| Campo | Valor |
|-------|-------|
| **Passos** | `event_manager is EventManager()` |
| **Resultado esperado** | `True` |
| **Resultado obtido** | ✅ Aprovado |
