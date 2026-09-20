import sys
import pygame


class Player:
    def __init__(self, largura, altura):
        self.pos = pygame.Vector2(largura / 2, altura / 2)
        self.velocidade = 300
        self.raio = 40
        self.largura = largura
        self.altura = altura

        self.spritesheet = pygame.image.load(
            "./assets/images/player3.png"
        ).convert_alpha()

        self.animations = {
            "idle": {
                "speed": 0.2,
                "frames": [
                    (57, 14, 115, 197),
                    (275, 15, 116, 196),
                    (493, 15, 113, 196),
                    (707, 15, 117, 196),
                ],
            },
            "jump": {
                "speed": 0.2,
                "frames": [
                    (55, 256, 138, 182),
                    (265, 231, 156, 189),
                    (468, 249, 164, 184),
                ],
            },
            "walk_right": {
                "speed": 0.25,
                "frames": [
                    (57, 461, 125, 197),
                    (278, 461, 113, 195),
                    (491, 461, 121, 196),
                    (710, 460, 118, 196),
                ],
            },
            "walk_left": {
                "speed": 0.25,
                "frames": [
                    (54, 684, 124, 196),
                    (284, 684, 111, 194),
                    (508, 683, 101, 198),
                    (715, 684, 119, 197),
                ],
            },
            "walk_back": {
                "speed": 0.25,
                "frames": [
                    (56, 905, 123, 197),
                    (277, 904, 120, 197),
                    (494, 904, 118, 198),
                    (710, 904, 122, 198),
                ],
            },
            "attack": {
                "speed": 0.08,
                "frames": [
                    (45, 1130, 164, 193),
                    (254, 1122, 149, 198),
                    (464, 1135, 198, 186),
                    (677, 1149, 205, 171),
                ],
            },
            "pickup": {
                "speed": 0.12,
                "frames": [
                    (42, 1388, 138, 147),
                    (267, 1380, 134, 155),
                    (504, 1363, 106, 178),
                    (721, 1344, 100, 197),
                ],
            },
            "hurt": {
                "speed": 0.10,
                "frames": [
                    (55, 1558, 154, 204),
                    (270, 1605, 133, 152),
                    (495, 1580, 111, 177),
                ],
            },
        }

        self.current_animation = "idle"
        self.current_frame = 0
        self.animation_timer = 0

        self.direction = "right"

        self.is_jumping = False
        self.velocity_y = 0
        self.gravity = 800
        self.jump_power = 500
        self.is_grounded = True

        self.display_height = 160
        self.extract_frames()

        self.width = 160
        self.height = 160

    def extract_frames(self):
        self.frames = {}

        for anim_name, anim_data in self.animations.items():
            self.frames[anim_name] = []

            for x, y, w, h in anim_data["frames"]:
                frame = self.spritesheet.subsurface(pygame.Rect(x, y, w, h)).copy()
                escala = self.display_height / h
                nova_largura = int(w * escala)
                frame = pygame.transform.scale(frame, (nova_largura, self.display_height))
                self.frames[anim_name].append(frame)

    def set_animation(self, animation_name):
        if animation_name != self.current_animation:
            self.current_animation = animation_name
            self.current_frame = 0
            self.animation_timer = 0

    def handle_input(self, keys, dt):
        moving = False

        if keys[pygame.K_w]:
            self.pos.y -= self.velocidade * dt
            self.set_animation("walk_back")
            moving = True
        elif keys[pygame.K_s]:
            self.pos.y += self.velocidade * dt
            self.set_animation("idle")
            moving = True
        elif keys[pygame.K_a]:
            self.pos.x -= self.velocidade * dt
            self.direction = "left"
            self.set_animation("walk_left")
            moving = True
        elif keys[pygame.K_d]:
            self.pos.x += self.velocidade * dt
            self.direction = "right"
            self.set_animation("walk_right")
            moving = True

        if not moving and not self.is_jumping:
            self.set_animation("idle")

        self.pos.x = max(self.raio, min(self.largura - self.raio, self.pos.x))
        self.pos.y = max(self.raio, min(self.altura - self.raio, self.pos.y))
        
    def update(self, dt):
        if self.is_jumping:
            self.velocity_y += self.gravity * dt
            self.pos.y += self.velocity_y * dt

            if self.pos.y >= self.altura - self.height / 2:
                self.pos.y = self.altura - self.height / 2
                self.is_jumping = False
                self.is_grounded = True
                self.velocity_y = 0

        anim_data = self.animations[self.current_animation]
        self.animation_timer += dt

        if self.animation_timer >= anim_data["speed"]:
            self.current_frame += 1
            self.animation_timer = 0

            if self.current_frame >= len(anim_data["frames"]):
                self.current_frame = 0

    def draw(self, screen):
        frame = self.frames[self.current_animation][self.current_frame]
        if (self.direction == "left" and self.current_animation != "walk_left"):
            frame = pygame.transform.flip(frame, True, False)

        rect = frame.get_rect(center=(int(self.pos.x),int(self.pos.y)))

        screen.blit(frame, rect)


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("./assets/sounds/excuse.mp3")
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(-1)

        info = pygame.display.Info()
        self.largura = info.current_w
        self.altura = info.current_h
        print(f"Resolução: {self.largura}x{self.altura}")

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Mine 2D")
        self.fonte = pygame.font.SysFont("Arial", 48)
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load("./assets/images/back.jpg").convert()
        self.home = pygame.image.load("./assets/images/home.png").convert()
        self.background = pygame.transform.scale(self.background, (self.largura, self.altura))
        self.home = pygame.transform.scale(self.home, (self.largura, self.altura))
        self.player = Player(self.largura, self.altura)

        self.criar_botoes()

        self.running = True
        self.init_game = False

    def criar_botoes(self):
        """Cria os retângulos dos botões do menu"""
        self.init_text = self.fonte.render("Iniciar Jogo", True, (255, 255, 255))
        self.options_text = self.fonte.render("Opções", True, (255, 255, 255))
        self.credits_text = self.fonte.render("Créditos", True, (255, 255, 255))
        self.exit_text = self.fonte.render("Sair", True, (255, 255, 255))

        centro_x = self.largura // 2
        self.button_init = self.init_text.get_rect(center=(centro_x, self.altura * 0.40))
        self.button_options = self.options_text.get_rect(center=(centro_x, self.altura * 0.50))
        self.button_credits = self.credits_text.get_rect(center=(centro_x, self.altura * 0.60))
        self.button_exit = self.exit_text.get_rect(center=(centro_x, self.altura * 0.70))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.init_game:
                        self.init_game = False  # Voltar ao menu
                    else:
                        self.running = False  # Sair do jogo
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.init_game:
                    self.handle_menu_click(event.pos)

    def handle_menu_click(self, pos):
        if self.button_init.collidepoint(pos):
            print("Iniciando o jogo...")
            self.init_game = True
        elif self.button_options.collidepoint(pos):
            print("Opções")
        elif self.button_credits.collidepoint(pos):
            print("Créditos")
        elif self.button_exit.collidepoint(pos):
            print("Saindo...")
            self.running = False

    def update(self, dt):
        if self.init_game:
            keys = pygame.key.get_pressed()
            self.player.handle_input(keys, dt)
            self.player.update(dt)

    def draw(self):
        if self.init_game:
            self.screen.blit(self.background, (0, 0))
            self.player.draw(self.screen)
        else:
            self.screen.blit(self.home, (0, 0))
            self.screen.blit(self.init_text, self.button_init)
            self.screen.blit(self.options_text, self.button_options)
            self.screen.blit(self.credits_text, self.button_credits)
            self.screen.blit(self.exit_text, self.button_exit)

        pygame.display.flip()

    def loop(self):
        while self.running:
            dt = self.clock.tick(60) / 1000  # Delta time em segundos

            self.handle_events()
            self.update(dt)
            self.draw()

    def quit(self):
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.loop()
    game.quit()
