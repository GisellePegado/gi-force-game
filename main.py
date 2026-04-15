"""
=============================================================
  GI-FORCE - Demo de Jogo 2D
  Desenvolvido com Python + Pygame
  Disciplina: Linguagem de Programação Aplicada - UNINTER
=============================================================

Conteúdos aplicados:
  - POO: Classes Nave, Meteorito, Particula, Jogo, CampoEstelar
  - Herança: MeteoritoPequeno, MeteoritoMedio, MeteoritoGrande (herdam de Meteorito)
  - ABC: EntidadeJogo como classe abstrata base (atualizar/desenhar)
  - Design Pattern: Observer (EventManager — sistema de eventos)
  - Design Pattern: Factory (MeteoritoFactory — criação de meteoritos)
  - Design Pattern: Singleton (@singleton aplicado ao EventManager)
  - Decorator: @singleton (classe), @validar_positivo (função)
  - List Comprehension: geração de estrelas e partículas
  - Manipulação de JSON: salvar/carregar recorde (scores.json)
  - Bibliotecas: pygame, random, math, abc, json
"""

import pygame
import random
import math
import sys
import os
import json
from abc import ABC, abstractmethod


def caminho_som(arquivo: str) -> str:
    """Retorna o caminho absoluto para um arquivo dentro da pasta 'assets/sounds/'.
    Funciona tanto ao rodar main.py diretamente quanto ao usar o .exe compilado.
    """
    if getattr(sys, 'frozen', False):
        # Rodando como executável compilado pelo PyInstaller
        base = os.path.dirname(sys.executable)
    else:
        # Rodando como script Python normal
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "assets", "sounds", arquivo)


def caminho_recorde() -> str:
    """Retorna o caminho absoluto para o arquivo de recorde (scores.json)."""
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "scores.json")


def carregar_recorde() -> int:
    """Lê o maior recorde salvo no scores.json. Retorna 0 se não existir."""
    try:
        with open(caminho_recorde(), "r") as f:
            return json.load(f).get("recorde", 0)
    except (FileNotFoundError, ValueError, KeyError):
        return 0


def validar_positivo(func):
    """Decorator de função: garante que a pontuação seja não-negativa antes de salvar."""
    def wrapper(pontuacao: int):
        if pontuacao < 0:
            pontuacao = 0
        return func(pontuacao)
    return wrapper


@validar_positivo
def salvar_recorde(pontuacao: int) -> None:
    """Salva a pontuação como novo recorde no scores.json."""
    with open(caminho_recorde(), "w") as f:
        json.dump({"recorde": pontuacao}, f)


def caminho_fonte(arquivo: str) -> str:
    """Retorna o caminho absoluto para um arquivo dentro da pasta 'assets/fonts/'."""
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "assets", "fonts", arquivo)


def caminho_imagem(arquivo: str) -> str:
    """Retorna o caminho absoluto para um arquivo dentro da pasta 'assets/images/'.
    Funciona tanto ao rodar main.py diretamente quanto ao usar o .exe compilado.
    """
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "assets", "images", arquivo)

# ===========================================================
#  CONSTANTES
# ===========================================================
LARGURA = 800
ALTURA = 600
FPS = 60
TITULO = "GI-FORCE"

# Paleta de cores (tema espacial escuro)
PRETO       = (0,   0,   0)
BRANCO      = (255, 255, 255)
AZUL_NEON   = (0,   200, 255)
ROXO_NEON   = (180,  50, 255)
MAGENTA_NEON = (255, 45,   155)
LARANJA     = (255, 140,   0)
VERMELHO    = (220,  40,  40)
CINZA_ESCURO= (20,  20,  35)
AMARELO     = (255, 230,  50)
VERDE_NEON  = (50,  255, 120)


def singleton(cls):
    """Decorator de classe: garante que apenas uma instância seja criada (Singleton)."""
    _instancias = {}
    def _obter(*args, **kwargs):
        if cls not in _instancias:
            _instancias[cls] = cls(*args, **kwargs)
        return _instancias[cls]
    return _obter


# ===========================================================
#  DESIGN PATTERN: OBSERVER
#  Permite que objetos "assinem" eventos e sejam notificados
# ===========================================================
@singleton
class EventManager:
    """Gerenciador de eventos (padrão Observer)."""

    def __init__(self):
        self._assinantes: dict = {}

    def assinar(self, evento: str, callback):
        """Registra um callback para um tipo de evento."""
        if evento not in self._assinantes:
            self._assinantes[evento] = []
        self._assinantes[evento].append(callback)

    def publicar(self, evento: str, dados=None):
        """Notifica todos os assinantes de um evento."""
        for cb in self._assinantes.get(evento, []):
            cb(dados)


# Instância global do gerenciador de eventos
event_manager = EventManager()


# ===========================================================
#  CLASSE ABSTRATA BASE: EntidadeJogo (ABC)
#  Define a interface comum para todas as entidades do jogo
# ===========================================================
class EntidadeJogo(ABC):
    """Classe abstrata base para entidades do jogo.
    Toda entidade deve implementar atualizar() e desenhar().
    """

    @abstractmethod
    def atualizar(self):
        """Atualiza o estado da entidade a cada frame."""

    @abstractmethod
    def desenhar(self, tela: pygame.Surface):
        """Desenha a entidade na tela."""


# ===========================================================
#  DESIGN PATTERN: FACTORY
#  Fábrica que cria meteoros com variações aleatórias
# ===========================================================
class MeteoritoFactory:
    """Fábrica de meteoros (padrão Factory)."""

    TIPOS = ["pequeno", "medio", "grande"]

    @staticmethod
    def criar(nivel: int = 1) -> "Meteorito":
        """Cria a subclasse de meteorito correspondente ao tipo sorteado."""
        tipo = random.choice(MeteoritoFactory.TIPOS)
        velocidade_base = 2 + nivel * 0.5
        classes = {
            "pequeno": MeteoritoPequeno,
            "medio":   MeteoritoMedio,
            "grande":  MeteoritoGrande,
        }
        return classes[tipo](velocidade_base=velocidade_base)


# ===========================================================
#  CLASSE: PARTÍCULA (efeito visual de explosão)
# ===========================================================
class Particula(EntidadeJogo):
    """Representa uma partícula de explosão."""

    def __init__(self, x: float, y: float, cor: tuple):
        self.x = x
        self.y = y
        self.cor = cor
        angulo = random.uniform(0, 2 * math.pi)
        velocidade = random.uniform(1, 5)
        self.vx = math.cos(angulo) * velocidade
        self.vy = math.sin(angulo) * velocidade
        self.vida = random.randint(20, 50)
        self.vida_max = self.vida
        self.raio = random.randint(2, 5)

    def atualizar(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1  # gravidade leve
        self.vida -= 1

    def desenhar(self, tela: pygame.Surface):
        alpha = int(255 * (self.vida / self.vida_max))
        cor = (*self.cor[:3], alpha)
        surf = pygame.Surface((self.raio * 2, self.raio * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, cor, (self.raio, self.raio), self.raio)
        tela.blit(surf, (int(self.x - self.raio), int(self.y - self.raio)))

    @property
    def vivo(self) -> bool:
        return self.vida > 0


# ===========================================================
#  CLASSE: METEORITO
# ===========================================================
class Meteorito(EntidadeJogo):
    """Representa um meteorito que cai pela tela."""

    CONFIGS = {
        "pequeno": {"raio": 15, "pontos": 10, "cor": (180, 120, 60),  "vel_rot": 4, "arquivo": "asteroid-small.png"},
        "medio":   {"raio": 25, "pontos": 5,  "cor": (140,  90, 40),  "vel_rot": 2, "arquivo": "asteroid-medium.png"},
        "grande":  {"raio": 40, "pontos": 2,  "cor": (100,  70, 30),  "vel_rot": 1, "arquivo": "asteroid-large.png"},
    }
    
    # Cache de imagens para não carregar múltiplas vezes
    _cache_imagens = {}

    @staticmethod
    def _carregar_imagem(tipo: str):
        """Carrega e cacheia a imagem do meteorito."""
        if tipo in Meteorito._cache_imagens:
            return Meteorito._cache_imagens[tipo]
        
        arquivo = Meteorito.CONFIGS[tipo]["arquivo"]
        caminho = caminho_imagem(arquivo)
        
        try:
            img = pygame.image.load(caminho).convert_alpha()
            Meteorito._cache_imagens[tipo] = img
            return img
        except pygame.error:
            print(f"[AVISO] Imagem '{caminho}' não encontrada. Usando desenho padrão.")
            return None

    def __init__(self, tipo: str, velocidade_base: float):
        self.tipo = tipo
        cfg = self.CONFIGS[tipo]
        self.raio: int       = cfg["raio"]
        self.pontos: int     = cfg["pontos"]
        self.cor: tuple      = cfg["cor"]
        self.vel_rot: float  = cfg["vel_rot"] * random.choice([-1, 1])
        self.angulo: float   = 0.0

        self.x = random.randint(self.raio, LARGURA - self.raio)
        self.y = -self.raio
        self.vy = velocidade_base + random.uniform(-0.5, 1.5)
        self.vx = random.uniform(-1.2, 1.2)

        # Carrega a imagem
        self.imagem = self._carregar_imagem(tipo)
        self.imagem_original = self.imagem

        # Gera forma irregular com list comprehension (usada só para colisão)
        self.pontos_forma = [
            (
                self.raio * random.uniform(0.7, 1.0) * math.cos(i * 2 * math.pi / 8),
                self.raio * random.uniform(0.7, 1.0) * math.sin(i * 2 * math.pi / 8),
            )
            for i in range(8)
        ]

    def atualizar(self):
        self.y += self.vy
        self.x += self.vx
        self.angulo += self.vel_rot
        # Rebate nas bordas laterais
        if self.x < self.raio or self.x > LARGURA - self.raio:
            self.vx *= -1

    def desenhar(self, tela: pygame.Surface):
        if self.imagem:
            # Rotaciona e desenha a imagem
            imagem_rotacionada = pygame.transform.rotate(self.imagem, -self.angulo)
            rect = imagem_rotacionada.get_rect(center=(int(self.x), int(self.y)))
            tela.blit(imagem_rotacionada, rect)
        else:
            # Fallback: desenho padrão com polígonos
            rad = math.radians(self.angulo)
            cos_a, sin_a = math.cos(rad), math.sin(rad)
            pontos_rot = [
                (
                    int(self.x + px * cos_a - py * sin_a),
                    int(self.y + px * sin_a + py * cos_a),
                )
                for px, py in self.pontos_forma
            ]
            pygame.draw.polygon(tela, self.cor, pontos_rot)
            # Borda brilhante
            cor_borda = tuple(min(255, c + 60) for c in self.cor)
            pygame.draw.polygon(tela, cor_borda, pontos_rot, 2)

    def colidiu_com(self, outro_rect: pygame.Rect) -> bool:
        dist = math.hypot(self.x - outro_rect.centerx, self.y - outro_rect.centery)
        return dist < self.raio + max(outro_rect.width, outro_rect.height) // 2

    @property
    def fora_da_tela(self) -> bool:
        return self.y > ALTURA + self.raio


# ===========================================================
#  HERANÇA: Subclasses de Meteorito
#  Cada tipo especializa o comportamento da classe base
# ===========================================================
class MeteoritoPequeno(Meteorito):
    """Meteorito pequeno — rápido e vale mais pontos."""

    def __init__(self, velocidade_base: float):
        super().__init__(tipo="pequeno", velocidade_base=velocidade_base)


class MeteoritoMedio(Meteorito):
    """Meteorito médio — equilíbrio entre velocidade e pontos."""

    def __init__(self, velocidade_base: float):
        super().__init__(tipo="medio", velocidade_base=velocidade_base)


class MeteoritoGrande(Meteorito):
    """Meteorito grande — lento e vale menos pontos."""

    def __init__(self, velocidade_base: float):
        super().__init__(tipo="grande", velocidade_base=velocidade_base)


# ===========================================================
#  CLASSE: NAVE (jogador)
# ===========================================================
class Nave(EntidadeJogo):
    """Representa a nave do jogador."""

    LARGURA = 72
    ALTURA  = 84
    VEL     = 5

    def __init__(self):
        self.x = LARGURA // 2
        self.y = ALTURA - 80
        self.rect = pygame.Rect(
            self.x - self.LARGURA // 2,
            self.y - self.ALTURA // 2,
            self.LARGURA,
            self.ALTURA,
        )
        self.vivo = True
        self.invencivel = 0   # frames de invencibilidade após dano
        self.vidas = 3
        self.trail: list[dict] = []  # rastro de fogo
        self.direcao = 1  # 1 = direita/centro, -1 = esquerda

        try:
            img = pygame.image.load(caminho_imagem("spaceship.png")).convert_alpha()
            self.imagem = pygame.transform.scale(img, (self.LARGURA, self.ALTURA))
        except (pygame.error, FileNotFoundError):
            self.imagem = None

    def atualizar(self, teclas):
        # Movimento horizontal e vertical
        if teclas[pygame.K_LEFT]  or teclas[pygame.K_a]:
            self.x -= self.VEL
            self.direcao = -1
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.x += self.VEL
            self.direcao = 1
        if teclas[pygame.K_UP]    or teclas[pygame.K_w]: self.y -= self.VEL
        if teclas[pygame.K_DOWN]  or teclas[pygame.K_s]: self.y += self.VEL

        # Limita à tela
        self.x = max(self.LARGURA // 2, min(LARGURA - self.LARGURA // 2, self.x))
        self.y = max(self.ALTURA  // 2, min(ALTURA  - self.ALTURA  // 2, self.y))

        self.rect.center = (self.x, self.y)

        if self.invencivel > 0:
            self.invencivel -= 1

        # Atualiza rastro
        self.trail.append({"x": self.x, "y": self.y + self.ALTURA // 2, "vida": 15})
        self.trail = [p for p in self.trail if p["vida"] > 0]
        for p in self.trail:
            p["vida"] -= 1

    def sofrer_dano(self):
        if self.invencivel == 0:
            self.vidas -= 1
            self.invencivel = 90  # 1.5 segundos
            event_manager.publicar("dano", self.vidas)
            if self.vidas <= 0:
                self.vivo = False
                event_manager.publicar("game_over", None)

    def desenhar(self, tela: pygame.Surface):
        # Rastro de fogo
        for p in self.trail:
            alpha = int(200 * p["vida"] / 15)
            cor = (255, random.randint(80, 180), 0, alpha)
            surf = pygame.Surface((8, 8), pygame.SRCALPHA)
            pygame.draw.circle(surf, cor, (4, 4), random.randint(2, 4))
            tela.blit(surf, (int(p["x"]) - 4 + random.randint(-3, 3), int(p["y"])))

        # Pisca se invencível
        if self.invencivel > 0 and (self.invencivel // 6) % 2 == 0:
            return

        if self.imagem:
            img = pygame.transform.flip(self.imagem, self.direcao == -1, False)
            rect = img.get_rect(center=(int(self.x), int(self.y)))
            tela.blit(img, rect)
        else:
            cx, cy = self.x, self.y
            corpo = [
                (cx,      cy - 26),
                (cx + 20, cy + 10),
                (cx + 12, cy + 18),
                (cx,      cy + 12),
                (cx - 12, cy + 18),
                (cx - 20, cy + 10),
            ]
            pygame.draw.polygon(tela, AZUL_NEON, corpo)
            pygame.draw.polygon(tela, BRANCO, corpo, 2)
            asa_dir = [(cx+12, cy+4), (cx+30, cy+20), (cx+14, cy+20)]
            asa_esq = [(cx-12, cy+4), (cx-30, cy+20), (cx-14, cy+20)]
            pygame.draw.polygon(tela, ROXO_NEON, asa_dir)
            pygame.draw.polygon(tela, ROXO_NEON, asa_esq)
            pygame.draw.ellipse(tela, (150, 230, 255), (cx - 8, cy - 12, 16, 18))
            pygame.draw.circle(tela, LARANJA, (cx, cy + 16), 5)
            pygame.draw.circle(tela, AMARELO, (cx, cy + 16), 3)


# ===========================================================
#  CLASSE: ESTRELAS (fundo animado)
# ===========================================================
class CampoEstelar(EntidadeJogo):
    """Fundo com estrelas em paralaxe."""

    def __init__(self, quantidade: int = 150):
        # List comprehension para gerar estrelas  ← List Comprehension aplicada
        self.estrelas = [
            {
                "x": random.randint(0, LARGURA),
                "y": random.randint(0, ALTURA),
                "vel": random.uniform(0.3, 2.5),
                "raio": random.choice([1, 1, 1, 2, 2, 3]),
                "brilho": random.randint(100, 255),
            }
            for _ in range(quantidade)
        ]

    def atualizar(self):
        for e in self.estrelas:
            e["y"] += e["vel"]
            if e["y"] > ALTURA:
                e["y"] = 0
                e["x"] = random.randint(0, LARGURA)

    def desenhar(self, tela: pygame.Surface):
        for e in self.estrelas:
            b = e["brilho"]
            pygame.draw.circle(tela, (b, b, b), (int(e["x"]), int(e["y"])), e["raio"])


# ===========================================================
#  CLASSE PRINCIPAL: JOGO
# ===========================================================
class Jogo:
    """Controla o loop principal e os estados do jogo."""

    ESTADO_MENU      = "menu"
    ESTADO_JOGANDO   = "jogando"
    ESTADO_PAUSADO   = "pausado"
    ESTADO_COMANDOS  = "comandos"
    ESTADO_GAME_OVER = "game_over"
    ESTADO_SOBRE     = "sobre"

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        icone = pygame.image.load(caminho_imagem("spaceship.png"))
        pygame.display.set_icon(icone)
        pygame.display.set_caption(TITULO)
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        self.clock = pygame.time.Clock()

        # Fontes — Press Start 2P (estilo arcade retro)
        _ttf = caminho_fonte("PressStart2P-Regular.ttf")
        self.fonte_titulo = pygame.font.Font(_ttf, 36)
        self.fonte_grande = pygame.font.Font(_ttf, 20)
        self.fonte_media  = pygame.font.Font(_ttf, 14)
        self.fonte_minima = pygame.font.Font(_ttf, 12)
        self.fonte_pequena= pygame.font.Font(_ttf, 10)

        self.estado = self.ESTADO_MENU
        self.opcao_menu = 0  # 0 = Iniciar Jogo, 1 = Comandos
        self.pontuacao = 0
        self.nivel = 1
        self.melhor_pontuacao = carregar_recorde()
        self.particulas: list[Particula] = []
        self.campo_estelar = CampoEstelar()
        self.tempo_spawn = 0
        self.intervalo_spawn = 90
        self.inicio_game_over = 0

        # Nave demo do menu (persistente para manter trail animado)
        self.nave_demo = Nave()
        self.nave_demo.y = 185

        # Miniatura da nave para o HUD de vidas
        try:
            img = pygame.image.load(caminho_imagem("spaceship.png")).convert_alpha()
            self.nave_miniatura = pygame.transform.scale(img, (24, 28))
        except (pygame.error, FileNotFoundError):
            self.nave_miniatura = None

        # --- ÁUDIO ---
        # Guarda o caminho da música principal para poder recarregá-la depois
        self._musica_principal = caminho_som("musica_menu.mp3")

        # Música de fundo em loop (buscada em sounds/ ao lado do executável)
        try:
            pygame.mixer.music.load(self._musica_principal)
            pygame.mixer.music.set_volume(1.0)           # volume cheio no menu
            pygame.mixer.music.play(-1)                   # -1 = loop infinito
        except pygame.error:
            print("[AVISO] Arquivo 'sounds/musica_menu.mp3' não encontrado. Continuando sem música.")

        # Música de Game Over (canal separado via Sound para não conflitar)
        try:
            self.som_game_over = pygame.mixer.Sound(caminho_som("game_over.mp3"))
            self.som_game_over.set_volume(1.0)
        except pygame.error:
            print("[AVISO] Arquivo 'sounds/game_over.mp3' não encontrado. Continuando sem música de game over.")
            self.som_game_over = None

        # Efeito sonoro de colisão
        try:
            self.som_colisao = pygame.mixer.Sound(caminho_som("colisao.wav"))  # aceita .wav ou .ogg
            self.som_colisao.set_volume(0.7)
        except pygame.error:
            print("[AVISO] Arquivo 'sounds/colisao.wav' não encontrado. Continuando sem efeito sonoro.")
            self.som_colisao = None

        # Efeito sonoro de navegação no menu
        try:
            self.som_select = pygame.mixer.Sound(caminho_som("select.wav"))
            self.som_select.set_volume(0.5)
        except pygame.error:
            print("[AVISO] Arquivo 'sounds/select.wav' não encontrado. Continuando sem som de navegação.")
            self.som_select = None

        # Efeito sonoro de saída de tela (ESC → menu)
        try:
            self.som_leave = pygame.mixer.Sound(caminho_som("leave.wav"))
            self.som_leave.set_volume(0.5)
        except pygame.error:
            print("[AVISO] Arquivo 'sounds/leave.wav' não encontrado. Continuando sem som de saída.")
            self.som_leave = None

        # Efeito sonoro de encerramento do jogo (ESC no menu principal)
        try:
            self.som_byebye = pygame.mixer.Sound(caminho_som("byebye.wav"))
            self.som_byebye.set_volume(0.8)
        except pygame.error:
            print("[AVISO] Arquivo 'sounds/byebye.wav' não encontrado. Continuando sem som de encerramento.")
            self.som_byebye = None

        # Efeito sonoro de game over sem recorde
        try:
            self.som_dead = pygame.mixer.Sound(caminho_som("dead.wav"))
            self.som_dead.set_volume(0.8)
        except pygame.error:
            print("[AVISO] Arquivo 'sounds/dead.wav' não encontrado. Continuando sem som de derrota.")
            self.som_dead = None

        # Efeito sonoro de novo recorde
        try:
            self.som_hallelujah = pygame.mixer.Sound(caminho_som("hallelujah.wav"))
            self.som_hallelujah.set_volume(0.8)
        except pygame.error:
            print("[AVISO] Arquivo 'sounds/hallelujah.wav' não encontrado. Continuando sem som de recorde.")
            self.som_hallelujah = None

        # Observer: escuta eventos do jogo
        event_manager.assinar("dano",     self._ao_sofrer_dano)
        event_manager.assinar("game_over",self._ao_game_over)

        self._iniciar_jogo()

    def _retomar_musica_principal(self, volume: float = 1.0):
        """Para qualquer música tocando e retoma a música principal no volume indicado."""
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self._musica_principal)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)
        except pygame.error:
            pass

    def _iniciar_jogo(self):
        self.nave = Nave()
        self.meteoritos: list[Meteorito] = []
        self.pontuacao = 0
        self.nivel = 1
        self.tempo_spawn = 0
        self.intervalo_spawn = 90
        self.particulas = []
        self.novo_recorde = False
        self.som_resultado_tocado = False
        # Abaixa o volume da música durante o jogo
        pygame.mixer.music.set_volume(0.3)

    def _ao_sofrer_dano(self, vidas):
        """Callback chamado quando a nave leva dano."""
        # Explode partículas laranjas
        for _ in range(20):
            self.particulas.append(Particula(self.nave.x, self.nave.y, LARANJA))

    def _ao_game_over(self, _):
        """Callback chamado quando o jogador perde."""
        self.novo_recorde = self.pontuacao > self.melhor_pontuacao
        if self.novo_recorde:
            self.melhor_pontuacao = self.pontuacao
            salvar_recorde(self.melhor_pontuacao)
        # Grande explosão final
        for _ in range(60):
            self.particulas.append(
                Particula(self.nave.x, self.nave.y,
                          random.choice([LARANJA, VERMELHO, AMARELO]))
            )
        # Marca o instante do game over para animações
        self.inicio_game_over = pygame.time.get_ticks()
        self.som_resultado_tocado = False  # será disparado após a contagem
        # Para a música principal e toca a de game over
        pygame.mixer.music.stop()
        if self.som_game_over:
            self.som_game_over.play()

    # ----------------------------------------------------------
    #  LOOP PRINCIPAL
    # ----------------------------------------------------------
    def rodar(self):
        while True:
            self.clock.tick(FPS)
            self._tratar_eventos()

            if self.estado == self.ESTADO_MENU:
                self._atualizar_menu()
                self._desenhar_menu()
            elif self.estado == self.ESTADO_COMANDOS:
                self._atualizar_menu()
                self._desenhar_comandos()
            elif self.estado == self.ESTADO_SOBRE:
                self._atualizar_menu()
                self._desenhar_sobre()
            elif self.estado == self.ESTADO_JOGANDO:
                self._atualizar_jogo()
                self._desenhar_jogo()
            elif self.estado == self.ESTADO_PAUSADO:
                self._desenhar_jogo()
                self._desenhar_pausado()
            elif self.estado == self.ESTADO_GAME_OVER:
                self._atualizar_game_over()
                self._desenhar_game_over()

            pygame.display.flip()

    def _tratar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                # --- MENU ---
                if self.estado == self.ESTADO_MENU:
                    if evento.key == pygame.K_ESCAPE:
                        if self.som_byebye:
                            self.som_byebye.play()
                            pygame.time.wait(int(self.som_byebye.get_length() * 1000))
                        pygame.quit()
                        sys.exit()
                    elif evento.key in (pygame.K_UP, pygame.K_w):
                        self.opcao_menu = (self.opcao_menu - 1) % 3
                        if self.som_select:
                            self.som_select.play()
                    elif evento.key in (pygame.K_DOWN, pygame.K_s):
                        self.opcao_menu = (self.opcao_menu + 1) % 3
                        if self.som_select:
                            self.som_select.play()
                    elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        if self.opcao_menu == 0:
                            self._iniciar_jogo()
                            self.estado = self.ESTADO_JOGANDO
                        elif self.opcao_menu == 1:
                            self.estado = self.ESTADO_COMANDOS
                        elif self.opcao_menu == 2:
                            self.estado = self.ESTADO_SOBRE

                # --- COMANDOS ---
                elif self.estado == self.ESTADO_COMANDOS:
                    if evento.key == pygame.K_ESCAPE:
                        if self.som_leave:
                            self.som_leave.play()
                        self.estado = self.ESTADO_MENU

                # --- SOBRE O JOGO ---
                elif self.estado == self.ESTADO_SOBRE:
                    if evento.key == pygame.K_ESCAPE:
                        if self.som_leave:
                            self.som_leave.play()
                        self.estado = self.ESTADO_MENU

                # --- JOGANDO ---
                elif self.estado == self.ESTADO_JOGANDO:
                    if evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        self.estado = self.ESTADO_PAUSADO

                # --- PAUSADO ---
                elif self.estado == self.ESTADO_PAUSADO:
                    if evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        self.estado = self.ESTADO_JOGANDO

                # --- GAME OVER ---
                elif self.estado == self.ESTADO_GAME_OVER:
                    if evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        if self.som_game_over:
                            self.som_game_over.stop()
                        self._retomar_musica_principal(volume=0.3)
                        self._iniciar_jogo()
                        self.estado = self.ESTADO_JOGANDO
                    elif evento.key == pygame.K_ESCAPE:
                        if self.som_game_over:
                            self.som_game_over.stop()
                        if self.som_leave:
                            self.som_leave.play()
                        self._retomar_musica_principal(volume=1.0)
                        self.estado = self.ESTADO_MENU

    # ----------------------------------------------------------
    #  ESTADO: MENU
    # ----------------------------------------------------------
    def _atualizar_menu(self):
        self.campo_estelar.atualizar()

        # Movimenta a nave demo com oscilação senoidal suave
        tick = pygame.time.get_ticks()
        amplitude = 150
        self.nave_demo.x = LARGURA // 2 + int(amplitude * math.sin(tick / 700))
        self.nave_demo.direcao = 1 if math.cos(tick / 700) >= 0 else -1
        self.nave_demo.rect.center = (self.nave_demo.x, self.nave_demo.y)

        # Atualiza rastro de fogo
        self.nave_demo.trail.append({
            "x": self.nave_demo.x,
            "y": self.nave_demo.y + Nave.ALTURA // 2,
            "vida": 15,
        })
        self.nave_demo.trail = [p for p in self.nave_demo.trail if p["vida"] > 0]
        for p in self.nave_demo.trail:
            p["vida"] -= 1

    def _desenhar_trofeu(self, x, y, cor):
        """Desenha um troféu pixel-art com pygame.draw. (x, y) = canto superior esquerdo."""
        s = 2
        # Copo (trapézio)
        copo = [
            (x + 2*s, y),
            (x + 8*s, y),
            (x + 10*s, y + 3*s),
            (x + 7*s, y + 7*s),
            (x + 3*s, y + 7*s),
            (x,       y + 3*s),
        ]
        pygame.draw.polygon(self.tela, cor, copo)
        pygame.draw.polygon(self.tela, BRANCO, copo, 1)
        # Alças laterais
        pygame.draw.rect(self.tela, cor,   (x - s,      y + 2*s, s,    3*s))
        pygame.draw.rect(self.tela, BRANCO,(x - s,      y + 2*s, s,    3*s), 1)
        pygame.draw.rect(self.tela, cor,   (x + 10*s,   y + 2*s, s,    3*s))
        pygame.draw.rect(self.tela, BRANCO,(x + 10*s,   y + 2*s, s,    3*s), 1)
        # Haste
        pygame.draw.rect(self.tela, cor,   (x + 4*s,    y + 7*s, 2*s,  3*s))
        # Base
        pygame.draw.rect(self.tela, cor,   (x + 2*s,    y + 10*s, 6*s, 2*s))
        pygame.draw.rect(self.tela, BRANCO,(x + 2*s,    y + 10*s, 6*s, 2*s), 1)

    def _desenhar_menu(self):
        self.tela.fill(CINZA_ESCURO)
        self.campo_estelar.desenhar(self.tela)

        tick = pygame.time.get_ticks()

        # Gradiente decorativo no topo
        for i in range(100):
            alpha = int(160 * (1 - i / 100))
            cor = (*ROXO_NEON[:3], alpha)
            surf = pygame.Surface((LARGURA, 1), pygame.SRCALPHA)
            surf.fill(cor)
            self.tela.blit(surf, (0, i))

        # Título com sombra pulsante
        pulso = abs(math.sin(tick / 800)) * 30
        cor_titulo = (int(AZUL_NEON[0]), int(AZUL_NEON[1]), min(255, int(AZUL_NEON[2] + pulso)))
        sombra = self.fonte_titulo.render(TITULO, True, ROXO_NEON)
        titulo  = self.fonte_titulo.render(TITULO, True, cor_titulo)
        self.tela.blit(sombra, (LARGURA // 2 - sombra.get_width() // 2 + 3, 33))
        self.tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 30))

        # Linha decorativa sob o título
        pygame.draw.line(self.tela, ROXO_NEON, (80, 105), (LARGURA - 80, 105), 1)

        # Nave decorativa animada
        self.nave_demo.desenhar(self.tela)

        # Linha decorativa acima das opções
        pygame.draw.line(self.tela, ROXO_NEON, (80, 270), (LARGURA - 80, 270), 1)

        # Opções no estilo arcade — cursor ">" na selecionada
        opcoes = ["INICIAR JOGO", "COMANDOS DE CONTROLE", "SOBRE O JOGO"]
        for i, texto in enumerate(opcoes):
            selecionado = (i == self.opcao_menu)

            cor_texto = BRANCO if selecionado else (80, 80, 130)

            y = 295 + i * 65
            t = self.fonte_grande.render(texto, True, cor_texto)
            x_texto = LARGURA // 2 - t.get_width() // 2
            self.tela.blit(t, (x_texto, y))

            if selecionado:
                cores_cursor = [AZUL_NEON, ROXO_NEON, MAGENTA_NEON]
                cor_cursor = cores_cursor[(tick // 350) % 3]
                cursor = self.fonte_grande.render(">", True, cor_cursor)
                self.tela.blit(cursor, (x_texto - cursor.get_width() - 14, y))

        # Linha decorativa acima do rodapé
        pygame.draw.line(self.tela, ROXO_NEON, (80, ALTURA - 130), (LARGURA - 80, ALTURA - 130), 1)

        # Recorde (sempre visível)
        valor_rec = str(self.melhor_pontuacao) if self.melhor_pontuacao > 0 else "---"
        mp = self.fonte_media.render(f"RECORDE: {valor_rec}", True, AMARELO)
        tx = LARGURA // 2 - mp.get_width() // 2
        ty = ALTURA - 90
        self.tela.blit(mp, (tx, ty))
        self._desenhar_trofeu(tx - 32, ty - 4, AMARELO)

        # Dica de navegação
        dica = self.fonte_pequena.render("W/S ou CIMA/BAIXO: Navegar  |  ENTER: Confirmar  |  ESC: Sair", True, (100, 100, 150))
        self.tela.blit(dica, (LARGURA // 2 - dica.get_width() // 2, ALTURA - 30))

    # ----------------------------------------------------------
    #  ESTADO: COMANDOS
    # ----------------------------------------------------------
    def _desenhar_comandos(self):
        self.tela.fill(CINZA_ESCURO)
        self.campo_estelar.desenhar(self.tela)

        titulo = self.fonte_grande.render("COMANDOS DE CONTROLE", True, ROXO_NEON)
        self.tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 50))
        pygame.draw.line(self.tela, AZUL_NEON, (100, 95), (LARGURA - 100, 95), 1)

        linhas = [
            ("Mover a nave",       "SETAS  ou  W A S D"),
            ("Pausar / Continuar", "ENTER"),
            ("Voltar ao menu", "ESC"),
        ]
        y = 130
        for acao, tecla in linhas:
            t_acao = self.fonte_media.render(acao, True, BRANCO)
            t_tecla = self.fonte_media.render(tecla, True, MAGENTA_NEON)
            self.tela.blit(t_acao,  (130, y))
            self.tela.blit(t_tecla, (LARGURA - 130 - t_tecla.get_width(), y))
            pygame.draw.line(self.tela, (50, 50, 80), (130, y + 34), (LARGURA - 130, y + 34), 1)
            y += 55

        voltar = self.fonte_media.render("ESC  -  Voltar ao menu", True, (120, 120, 160))
        self.tela.blit(voltar, (LARGURA // 2 - voltar.get_width() // 2, ALTURA - 60))

    # ----------------------------------------------------------
    #  ESTADO: SOBRE O JOGO
    # ----------------------------------------------------------
    def _desenhar_sobre(self):
        self.tela.fill(CINZA_ESCURO)
        self.campo_estelar.desenhar(self.tela)

        tick = pygame.time.get_ticks()

        # Gradiente decorativo no topo (mesmo do menu)
        for i in range(80):
            alpha = int(140 * (1 - i / 80))
            surf = pygame.Surface((LARGURA, 1), pygame.SRCALPHA)
            surf.fill((*ROXO_NEON[:3], alpha))
            self.tela.blit(surf, (0, i))

        # Titulo com pulso
        pulso = abs(math.sin(tick / 800)) * 30
        cor_titulo = (int(AZUL_NEON[0]), int(AZUL_NEON[1]), min(255, int(AZUL_NEON[2] + pulso)))
        titulo = self.fonte_grande.render("SOBRE O JOGO", True, cor_titulo)
        sombra = self.fonte_grande.render("SOBRE O JOGO", True, ROXO_NEON)
        self.tela.blit(sombra, (LARGURA // 2 - sombra.get_width() // 2 + 2, 27))
        self.tela.blit(titulo,  (LARGURA // 2 - titulo.get_width()  // 2,     25))

        pygame.draw.line(self.tela, ROXO_NEON, (80, 55), (LARGURA - 80, 55), 1)

        # ---- SECAO: O NOME ----  (sep=55, label=72, subsep=96, lines=108,130,152, sep=182)
        label_nome = self.fonte_media.render("O NOME", True, AZUL_NEON)
        self.tela.blit(label_nome, (80, 72))
        pygame.draw.line(self.tela, (60, 60, 100), (80, 96), (LARGURA - 80, 96), 1)

        COR_BASE  = (200, 200, 230)
        COR_CIANO = (148, 210, 242)  # cinza puxado para ciano
        COR_ROXO  = (200, 152, 240)  # cinza puxado para roxo
        COR_MAG   = (238, 160, 215)  # cinza puxado para magenta

        def render_rich(partes, cor_base, cor_dest, x, y):
            cx = x
            for texto, destaque in partes:
                s = self.fonte_minima.render(texto, True, cor_dest if destaque else cor_base)
                self.tela.blit(s, (cx, y))
                cx += s.get_width()

        linhas_nome = [
            [("GI-FORCE", True), (" e um trocadilho entre", False)],
            [("G-Force", True), (" (forca gravitacional)", False)],
            [("e ", False), ("Gi", True), (", apelido da desenvolvedora.", False)],
        ]
        y = 108
        for partes in linhas_nome:
            render_rich(partes, COR_BASE, COR_CIANO, 80, y)
            y += 22

        pygame.draw.line(self.tela, ROXO_NEON, (80, 182), (LARGURA - 80, 182), 1)

        # ---- SECAO: A HISTORIA ----  (sep=182, label=199, subsep=223, lines=235..345, sep=375)
        label_hist = self.fonte_media.render("A HISTORIA", True, ROXO_NEON)
        self.tela.blit(label_hist, (80, 199))
        pygame.draw.line(self.tela, (60, 60, 100), (80, 223), (LARGURA - 80, 223), 1)

        linhas_hist = [
            [("A Terra se tornou inabitavel pelo lixo e poluicao.", False)],
            [("A astrofisica ", False), ("Giselle Pegado", True), (" descobriu um planeta", False)],
            [("em uma galaxia distante e o batizou de ", False), ("GI-FORCE", True), (".", False)],
            [("Os ultimos sobreviventes partem rumo ao novo lar,", False)],
            [("mas uma chuva de meteoros bloqueia o caminho.", False)],
            [("Voce pilota a nave. Desvie e nos leve para casa!", True)],
        ]
        y = 235
        for partes in linhas_hist:
            render_rich(partes, COR_BASE, COR_ROXO, 80, y)
            y += 22

        pygame.draw.line(self.tela, ROXO_NEON, (80, 375), (LARGURA - 80, 375), 1)

        # ---- SECAO: O PROJETO ----  (sep=375, label=392, subsep=416, lines=428..500, sep=530)
        label_proj = self.fonte_media.render("O PROJETO", True, MAGENTA_NEON)
        self.tela.blit(label_proj, (80, 392))
        pygame.draw.line(self.tela, (60, 60, 100), (80, 416), (LARGURA - 80, 416), 1)

        dados_proj = [
            ("Desenvolvido por:", "Giselle Pegado",                       COR_MAG),
            ("RU:",               "5052104",                               COR_MAG),
            ("Disciplina:",       "Linguagem de Programacao Aplicada",     COR_MAG),
            ("Instituicao:",      "UNINTER  -  2026",                      COR_MAG),
        ]
        y = 428
        for label, valor, cor_val in dados_proj:
            t_label = self.fonte_minima.render(label, True, (160, 160, 200))
            t_valor = self.fonte_minima.render(valor, True, cor_val)
            self.tela.blit(t_label, (80,  y))
            self.tela.blit(t_valor, (310, y))
            y += 24

        pygame.draw.line(self.tela, ROXO_NEON, (80, ALTURA - 70), (LARGURA - 80, ALTURA - 70), 1)

        # Rodape
        voltar = self.fonte_media.render("ESC  -  Voltar ao menu", True, (100, 100, 150))
        self.tela.blit(voltar, (LARGURA // 2 - voltar.get_width() // 2, ALTURA - 50))

    # ----------------------------------------------------------
    #  ESTADO: PAUSADO
    # ----------------------------------------------------------
    def _desenhar_pausado(self):
        # Overlay escuro sobre o jogo
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.tela.blit(overlay, (0, 0))

        # Dimensões do painel
        pw, ph = 420, 200
        px = LARGURA // 2 - pw // 2
        py = ALTURA  // 2 - ph // 2

        # Fundo do painel
        panel = pygame.Surface((pw, ph), pygame.SRCALPHA)
        panel.fill((10, 10, 30, 220))
        self.tela.blit(panel, (px, py))

        # Borda dupla estilo RPG
        pygame.draw.rect(self.tela, ROXO_NEON, (px,     py,     pw,     ph    ), 2)
        pygame.draw.rect(self.tela, AZUL_NEON,  (px + 6, py + 6, pw - 12, ph - 12), 1)

        # Cantos ornamentados com losangos
        s = 7
        cantos = [
            (px + 1,      py + 1     ),  # topo-esquerda
            (px + pw - 2, py + 1     ),  # topo-direita
            (px + 1,      py + ph - 2),  # baixo-esquerda
            (px + pw - 2, py + ph - 2),  # baixo-direita
        ]
        for cx_c, cy_c in cantos:
            pygame.draw.polygon(self.tela, AMARELO, [
                (cx_c,     cy_c - s),
                (cx_c + s, cy_c    ),
                (cx_c,     cy_c + s),
                (cx_c - s, cy_c    ),
            ])

        # Título centralizado no painel
        titulo = self.fonte_titulo.render("PAUSADO", True, AMARELO)
        titulo_y = py + ph // 2 - titulo.get_height() // 2 - 18
        self.tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, titulo_y))

        # Linha separadora acima da dica
        pygame.draw.line(self.tela, ROXO_NEON, (px + 18, py + ph - 52), (px + pw - 18, py + ph - 52), 1)

        # Dica piscante
        tick = pygame.time.get_ticks()
        if (tick // 500) % 2 == 0:
            dica = self.fonte_media.render("ENTER - continuar", True, BRANCO)
            self.tela.blit(dica, (LARGURA // 2 - dica.get_width() // 2, py + ph - 38))

    # ----------------------------------------------------------
    #  ESTADO: JOGANDO
    # ----------------------------------------------------------
    def _atualizar_jogo(self):
        if not self.nave.vivo:
            self.estado = self.ESTADO_GAME_OVER
            return

        teclas = pygame.key.get_pressed()
        self.campo_estelar.atualizar()
        self.nave.atualizar(teclas)

        # Spawn de meteoritos via Factory
        self.tempo_spawn += 1
        if self.tempo_spawn >= self.intervalo_spawn:
            self.tempo_spawn = 0
            self.meteoritos.append(MeteoritoFactory.criar(self.nivel))

        # Atualiza meteoritos
        for m in self.meteoritos:
            m.atualizar()

        # Colisões
        for m in self.meteoritos[:]:
            if m.colidiu_com(self.nave.rect):
                # Explosão
                for _ in range(30):
                    self.particulas.append(
                        Particula(m.x, m.y, random.choice([LARANJA, VERMELHO, AMARELO]))
                    )
                self.meteoritos.remove(m)
                self.nave.sofrer_dano()
                # Som de colisão
                if self.som_colisao:
                    self.som_colisao.play()

        # Remove meteoritos fora da tela e pontua
        antes = len(self.meteoritos)
        self.meteoritos = [m for m in self.meteoritos if not m.fora_da_tela]
        desviados = antes - len(self.meteoritos)
        self.pontuacao += desviados * 1

        # Atualiza partículas
        for p in self.particulas:
            p.atualizar()
        self.particulas = [p for p in self.particulas if p.vivo]

        # Aumenta nível a cada 50 pontos
        novo_nivel = 1 + self.pontuacao // 50
        if novo_nivel != self.nivel:
            self.nivel = novo_nivel
            self.intervalo_spawn = max(20, 90 - self.nivel * 8)

    def _desenhar_jogo(self):
        self.tela.fill(CINZA_ESCURO)
        self.campo_estelar.desenhar(self.tela)

        for m in self.meteoritos:
            m.desenhar(self.tela)

        for p in self.particulas:
            p.desenhar(self.tela)

        self.nave.desenhar(self.tela)
        self._desenhar_hud()

    def _desenhar_hud(self):
        # Pontuação
        pts = self.fonte_grande.render(f"{self.pontuacao:05d}", True, BRANCO)
        self.tela.blit(pts, (LARGURA // 2 - pts.get_width() // 2, 10))

        # Nível
        nv = self.fonte_media.render(f"NIVEL {self.nivel}", True, AZUL_NEON)
        self.tela.blit(nv, (10, 10))

        # Barra de progresso do nível
        barra_x, barra_y, barra_w, barra_h = 10, 36, 120, 8
        progresso = (self.pontuacao % 50) / 50
        preenchido = int(barra_w * progresso)
        pygame.draw.rect(self.tela, (40, 40, 80),  (barra_x, barra_y, barra_w, barra_h), border_radius=4)
        if preenchido > 0:
            pygame.draw.rect(self.tela, AZUL_NEON, (barra_x, barra_y, preenchido, barra_h), border_radius=4)
        pygame.draw.rect(self.tela, AZUL_NEON,     (barra_x, barra_y, barra_w, barra_h), 1, border_radius=4)
        prox = self.fonte_pequena.render(f"proximo: {50 - self.pontuacao % 50}", True, (100, 100, 160))
        self.tela.blit(prox, (barra_x, barra_y + barra_h + 3))

        # Vidas (miniaturas da nave)
        for i in range(self.nave.vidas):
            x = LARGURA - 34 - i * 32
            if self.nave_miniatura:
                self.tela.blit(self.nave_miniatura, (x, 6))
            else:
                pygame.draw.polygon(self.tela, VERMELHO, [
                    (x + 8, 6), (x + 16, 14), (x + 8, 22), (x, 14)
                ])

        # Barra inferior
        pygame.draw.line(self.tela, AZUL_NEON, (0, ALTURA - 30), (LARGURA, ALTURA - 30), 1)
        dica = self.fonte_pequena.render(
            "SETAS / WASD: Mover   |   ENTER: Pausar", True, (120, 120, 160)
        )
        self.tela.blit(dica, (LARGURA // 2 - dica.get_width() // 2, ALTURA - 22))

    # ----------------------------------------------------------
    #  ESTADO: GAME OVER
    # ----------------------------------------------------------
    def _atualizar_game_over(self):
        self.campo_estelar.atualizar()
        for p in self.particulas:
            p.atualizar()
        self.particulas = [p for p in self.particulas if p.vivo]

        # Dispara o som de resultado uma única vez ao fim da contagem (1800ms)
        if not self.som_resultado_tocado:
            elapsed = pygame.time.get_ticks() - self.inicio_game_over
            if elapsed >= 1800:
                self.som_resultado_tocado = True
                if self.novo_recorde:
                    if self.som_hallelujah:
                        self.som_hallelujah.play()
                else:
                    if self.som_dead:
                        self.som_dead.play()

    def _desenhar_game_over(self):
        self.tela.fill(CINZA_ESCURO)
        self.campo_estelar.desenhar(self.tela)

        for p in self.particulas:
            p.desenhar(self.tela)

        # Overlay escuro
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.tela.blit(overlay, (0, 0))

        tick = pygame.time.get_ticks()
        cx = LARGURA // 2
        go_y = 130

        # --- GAME OVER com efeito glitch ---
        go_base = self.fonte_titulo.render("GAME OVER", True, BRANCO)
        go_w = go_base.get_width()

        # Alterna entre ciano e roxo a cada ~200ms
        cor_glitch = (0, 255, 255) if (tick // 200) % 2 == 0 else ROXO_NEON

        offset_c = random.randint(2, 7)
        go_layer1 = self.fonte_titulo.render("GAME OVER", True, cor_glitch)
        go_layer1.set_alpha(130)
        self.tela.blit(go_layer1, (cx - go_w // 2 + offset_c, go_y))

        offset_r = random.randint(2, 6)
        go_layer2 = self.fonte_titulo.render("GAME OVER", True, cor_glitch)
        go_layer2.set_alpha(80)
        self.tela.blit(go_layer2, (cx - go_w // 2 - offset_r, go_y))

        # Texto principal por cima
        self.tela.blit(go_base, (cx - go_w // 2, go_y))

        # --- Animação de contagem (dura 1800ms) ---
        elapsed = tick - self.inicio_game_over
        t = min(1.0, elapsed / 1800)
        pts_exibidos = int(self.pontuacao * t)
        rec_exibidos = int(self.melhor_pontuacao * t)

        pts = self.fonte_grande.render(f"PONTOS: {pts_exibidos:05d}", True, BRANCO)
        self.tela.blit(pts, (cx - pts.get_width() // 2, 230))

        mp = self.fonte_media.render(f"RECORDE: {rec_exibidos:05d}", True, AMARELO)
        self.tela.blit(mp, (cx - mp.get_width() // 2, 300))

        # Mensagem de novo recorde (só após a contagem terminar)
        if t >= 1.0 and self.pontuacao > 0 and self.pontuacao == self.melhor_pontuacao:
            if (tick // 400) % 2 == 0:
                novo = self.fonte_media.render("NOVO RECORDE!", True, AMARELO)
                self.tela.blit(novo, (cx - novo.get_width() // 2, 345))

        # Ações (só aparecem após a contagem terminar)
        if t >= 1.0:
            if (tick // 500) % 2 == 0:
                reiniciar = self.fonte_grande.render("ENTER - Jogar Novamente", True, VERDE_NEON)
                self.tela.blit(reiniciar, (cx - reiniciar.get_width() // 2, 420))
            voltar = self.fonte_media.render("ESC - Voltar ao Menu", True, (160, 160, 200))
            self.tela.blit(voltar, (cx - voltar.get_width() // 2, 480))


# ===========================================================
#  ENTRY POINT
# ===========================================================
if __name__ == "__main__":
    jogo = Jogo()
    jogo.rodar()
