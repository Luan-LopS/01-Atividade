import pygame
import sys

# Inicializa o Pygame
pygame.init()

# Configurações da tela
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Home do Jogo")

# Carrega a imagem de fundo (ex: background.png)
try:
    background = pygame.image.load('./images/back.jpg')
    background = pygame.transform.scale(background, (largura, altura))
except pygame.error as e:
    print(f"Erro ao carregar a imagem: {e}")
    sys.exit()

# Fonte para texto
fonte = pygame.font.SysFont("Arial", 48)

# Botão "Iniciar Jogo"
botao_texto = fonte.render("Iniciar Jogo", True, (255, 255, 255))
botao_rect = botao_texto.get_rect(center=(largura // 2, altura // 2))

# Loop principal da tela de "home"
rodando = True
while rodando:
    tela.blit(background, (0, 0))  # Desenha o fundo

    # Desenha o botão
    tela.blit(botao_texto, botao_rect)

    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
            pygame.quit()
            sys.exit()

        # Verifica clique no botão
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if botao_rect.collidepoint(evento.pos):
                print("Iniciando o jogo...")
                # Aqui você pode adicionar código para iniciar o jogo principal
                # Exemplo: chamar a função principal do jogo
                # game_loop()

    # Atualiza a tela
    pygame.display.flip()

# Finaliza o Pygame
pygame.quit()
sys.exit()
