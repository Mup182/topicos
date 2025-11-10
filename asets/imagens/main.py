import pygame
import sys

# --------------------- CONFIGURAÇÕES INICIAIS ---------------------
pygame.init()
LARGURA, ALTURA = 1280, 720
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Ecos do Passado")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Fontes
fonte_titulo = pygame.font.Font(None, 100)
fonte_botao = pygame.font.Font(None, 50)
fonte_creditos = pygame.font.Font(None, 30)

# Fundo
fundo = pygame.image.load("fundo_menu.jpg")
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))

# --------------------- FUNÇÕES ---------------------
def novo_jogo():
    print("Novo jogo iniciado!")  # Aqui você vai chamar a próxima tela depois

def carregar_jogo():
    print("Função em desenvolvimento.")

def configuracoes():
    configurando = True

    volume_musica = 5
    volume_efeitos = 5
    tela_cheia = False
    idioma = "Português"

    while configurando:
        tela.blit(fundo, (0, 0))

        # Título
        titulo = fonte_titulo.render("Configurações", True, BRANCO)
        tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 80))

        # Opções
        opcoes = [
            f"Volume da música: {volume_musica}",
            f"Volume dos efeitos sonoros: {volume_efeitos}",
            f"Tela cheia: {'Ativada' if tela_cheia else 'Janela'}",
            f"Idioma: {idioma}",
            "Voltar ao menu principal"
        ]

        # Renderizar opções
        for i, texto in enumerate(opcoes):
            texto_render = fonte_botao.render(texto, True, BRANCO)
            rect = texto_render.get_rect(center=(LARGURA // 2, 270 + i * 80))
            tela.blit(texto_render, rect)

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE or evento.key == pygame.K_RETURN:
                    configurando = False
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                x, y = evento.pos
                for i, texto in enumerate(opcoes):
                    texto_render = fonte_botao.render(texto, True, BRANCO)
                    rect = texto_render.get_rect(center=(LARGURA // 2, 270 + i * 80))
                    if rect.collidepoint(x, y):
                        if i == 0:
                            volume_musica = (volume_musica + 1) % 11
                        elif i == 1:
                            volume_efeitos = (volume_efeitos + 1) % 11
                        elif i == 2:
                            tela_cheia = not tela_cheia
                            if tela_cheia:
                                pygame.display.set_mode((LARGURA, ALTURA), pygame.FULLSCREEN)
                            else:
                                pygame.display.set_mode((LARGURA, ALTURA))
                        elif i == 3:
                            idioma = "Inglês" if idioma == "Português" else "Português"
                        elif i == 4:
                            configurando = False

        pygame.display.flip()

def sair():
    pygame.quit()
    sys.exit()

# --------------------- CLASSE BOTÃO ---------------------
class Botao:
    def __init__(self, texto, y, acao):
        self.texto = texto
        self.y = y
        self.acao = acao
        self.rect = None
        self.hover = False

    def desenhar(self, superficie):
        # Render do texto
        texto_render = fonte_botao.render(self.texto, True, PRETO if self.hover else BRANCO)
        largura_texto = texto_render.get_width() + 40
        altura_texto = texto_render.get_height() + 20
        x = (LARGURA - largura_texto) // 2

        # Fundo do botão com transparência
        s = pygame.Surface((largura_texto, altura_texto), pygame.SRCALPHA)
        cor_fundo = (255, 255, 255, 100) if not self.hover else (255, 255, 255, 200)
        pygame.draw.rect(s, cor_fundo, (0, 0, largura_texto, altura_texto), border_radius=12)
        pygame.draw.rect(s, BRANCO, (0, 0, largura_texto, altura_texto), 2, border_radius=12)
        superficie.blit(s, (x, self.y))

        # Texto
        superficie.blit(texto_render, (x + 20, self.y + 10))

        # Atualiza o rect para hover/click
        self.rect = pygame.Rect(x, self.y, largura_texto, altura_texto)

    def checar_clique(self, pos):
        if self.rect and self.rect.collidepoint(pos):
            self.acao()

# --------------------- BOTÕES ---------------------
botoes = [
    ("Novo Jogo", novo_jogo),
    ("Carregar Jogo", carregar_jogo),
    ("Configurações", configuracoes),
    ("Sair", sair)
]

objetos_botoes = []
y_inicial = 320
espacamento = 80
for i, (texto, acao) in enumerate(botoes):
    objetos_botoes.append(Botao(texto, y_inicial + i * espacamento, acao))

# --------------------- LOOP PRINCIPAL ---------------------
rodando = True
while rodando:
    tela.blit(fundo, (0, 0))

    # Título com sombra
    titulo = fonte_titulo.render("Ecos do Passado", True, BRANCO)
    sombra = fonte_titulo.render("Ecos do Passado", True, PRETO)
    tela.blit(sombra, (LARGURA // 2 - titulo.get_width() // 2 + 3, 103))
    tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 100))

    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for botao in objetos_botoes:
                botao.checar_clique(evento.pos)

    # Hover
    mouse_pos = pygame.mouse.get_pos()
    for botao in objetos_botoes:
        botao.hover = botao.rect.collidepoint(mouse_pos) if botao.rect else False
        botao.desenhar(tela)

    # Créditos
    creditos = fonte_creditos.render("© Equipe: Murilo, Júlia, Izadora e Maria", True, BRANCO)
    tela.blit(creditos, (LARGURA // 2 - creditos.get_width() // 2, ALTURA - 40))

    pygame.display.flip()

pygame.quit()
