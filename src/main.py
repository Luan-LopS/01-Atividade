import sys
import pygame

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("./assets/sounds/excuse.mp3")
pygame.mixer.music.set_volume(0.25)
pygame.mixer.music.play(-1)

info = pygame.display.Info()
largura = info.current_w
altura = info.current_h

print(f"Resolução: {largura}x{altura}")

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Mine 2D")
fonte = pygame.font.SysFont("Arial", 48)
background = pygame.image.load("./assets/images/back.jpg").convert()
home = pygame.image.load("./assets/images/home.png").convert()

background = pygame.transform.scale(background, (largura, altura))
home = pygame.transform.scale(home, (largura, altura))

clock = pygame.time.Clock()
player_pos = pygame.Vector2(largura / 2, altura / 2)
velocidade = 300

init_text = fonte.render("Iniciar Jogo", True, (255, 255, 255))
options_text = fonte.render("Opções", True, (255, 255, 255))
credits_text = fonte.render("Créditos", True, (255, 255, 255))
exit_text = fonte.render("Sair", True, (255, 255, 255))

centro_x = largura // 2
button_init = init_text.get_rect(center=(centro_x, altura * 0.40))
button_options = options_text.get_rect(center=(centro_x, altura * 0.50))
button_credits = credits_text.get_rect(center=(centro_x, altura * 0.60))
button_exit = exit_text.get_rect(center=(centro_x, altura * 0.70))

running = True
init_game = False

while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not init_game:
                if button_init.collidepoint(event.pos):
                    print("Iniciando o jogo...")
                    init_game = True
                elif button_options.collidepoint(event.pos):
                    print("Opções")
                elif button_credits.collidepoint(event.pos):
                    print("Créditos")
                elif button_exit.collidepoint(event.pos):
                    print("Saindo...")
                    running = False

    if init_game:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_pos.y -= velocidade * dt
        if keys[pygame.K_s]:
            player_pos.y += velocidade * dt
        if keys[pygame.K_a]:
            player_pos.x -= velocidade * dt
        if keys[pygame.K_d]:
            player_pos.x += velocidade * dt

        player_pos.x = max(40, min(largura - 40, player_pos.x))
        player_pos.y = max(40, min(altura - 40, player_pos.y))

        screen.blit(background, (0, 0))
        pygame.draw.circle(screen, "red", player_pos, 40)
    else:
        screen.blit(home, (0, 0))
        screen.blit(init_text, button_init)
        screen.blit(options_text, button_options)
        screen.blit(credits_text, button_credits)
        screen.blit(exit_text, button_exit)

    pygame.display.flip()


pygame.quit()
sys.exit()
