import pygame
import sys

# Inicializa o Pygame
pygame.init()

# Configurações da janela
LARGURA, ALTURA = 1280, 720
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Ecos do Passado - Menu")

# Cores
COR_TEXTO = (240, 240, 240)
COR_BOTAO = (50, 50, 50)
COR_HOVER = (200, 180, 150)
COR_FUNDO_JOGO = (60, 50, 40)

# Fonte moderna
pygame.font.init()
try:
    fonte = pygame.font.Font("Montserrat-Bold.ttf", 48)  # substitui pelo arquivo da fonte
except:
    fonte = pygame.font.SysFont("Arial", 48, bold=True)

# Fundo
fundo = pygame.image.load("fundo_menu.jpg")
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))

# Classe para botões
class Botao:
    def __init__(self, texto, x, y, largura, altura, acao=None):
        self.texto = texto
        self.rect = pygame.Rect(x, y, largura, altura)
        self.acao = acao

    def desenhar(self, tela, mouse_pos):
        # Muda cor se estiver sobre o mouse
        cor = COR_HOVER if self.rect.collidepoint(mouse_pos) else COR_BOTAO
        pygame.draw.rect(tela, cor, self.rect, border_radius=12)

        # Sombra do texto
        texto_render = fonte.render(self.texto, True, COR_TEXTO)
        texto_sombra = fonte.render(self.texto, True, (30,30,30))
        texto_rect = texto_render.get_rect(center=self.rect.center)
        tela.blit(texto_sombra, texto_rect.move(2,2))
        tela.blit(texto_render, texto_rect)

    def clicado(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# Criação dos botões
botoes = [
    Botao("Novo Jogo", LARGURA//2 - 150, 400, 300, 70, acao="novo"),
    Botao("Carregar", LARGURA//2 - 150, 500, 300, 70, acao="carregar"),
    Botao("Sair", LARGURA//2 - 150, 600, 300, 70, acao="sair")
]

# Função da tela de jogo
def tela_jogo():
    jogando = True
    fade_in = 255
    while jogando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                jogando = False

        tela.fill(COR_FUNDO_JOGO)
        texto = fonte.render("Capítulo 1 - Brasília, 1964", True, (255, 230, 200))
        texto_rect = texto.get_rect(center=(LARGURA//2, ALTURA//2))
        tela.blit(texto, texto_rect)

        # Fade-in simples
        if fade_in > 0:
            fade_surface = pygame.Surface((LARGURA, ALTURA))
            fade_surface.set_alpha(fade_in)
            fade_surface.fill((0,0,0))
            tela.blit(fade_surface, (0,0))
            fade_in -= 10

        pygame.display.flip()
        pygame.time.Clock().tick(60)

# Loop principal
rodando = True
while rodando:
    mouse_pos = pygame.mouse.get_pos()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.MOUSEBUTTONDOWN:
            for botao in botoes:
                if botao.clicado(mouse_pos):
                    if botao.acao == "novo":
                        tela_jogo()
                    elif botao.acao == "carregar":
                        print("Função de carregar ainda em desenvolvimento!")
                    elif botao.acao == "sair":
                        rodando = False

    # Desenha menu
    tela.blit(fundo, (0,0))
    for botao in botoes:
        botao.desenhar(tela, mouse_pos)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
