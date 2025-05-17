from settings import *
from entities.player import Player
from entities.platform import Platform
from entities.collectible import Collectible
from entities.spikes import Spike
from entities.interactible import *
from griding import *
from entities.button import Button
from draw_method import circle, rect, polygon, font
from draw_platforms import draw_platform


pg.init()


class Game:
    def __init__(self):
        pg.display.set_caption("Platformer")

        self.player = Player(PLAYER_WIDTH, PLAYER_HEIGHT)
        self.platforms = []
        # Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50), Platform(800, 550, 250, 20), Platform(0, 0, 20, SCREEN_HEIGHT)
        self.collectibles = []
        # Collectible(800, 600, 20)
        self.spikes = []
        # Spike(400, 620, 50, 60)
        self.checkpoints = []
        # Checkpoint(500, 620, 40, 60)
        self.jump_orbs = []

        self.clock = pg.time.Clock()

        self.score = 0

    def setup_map(self):
        level = read_map(MAP_FILENAME)
        for y, row in enumerate(level):
            for x, item in enumerate(row):
                self.place_item(item, x, y)

    def group_platforms(self, level, tile_size):
        rows = len(level)
        cols = len(level[0])
        visited = [[False for _ in range(cols)] for _ in range(rows)]

        for y in range(rows):
            for x in range(cols):
                if level[y][x] == '#' and not visited[y][x]:
                    max_w = 0
                    while x + max_w < cols and level[y][x + max_w] == '#' and not visited[y][x + max_w]:
                        max_w += 1

                    max_h = 1
                    done = False
                    while y + max_h < rows and not done:
                        for dx in range(max_w):
                            if level[y + max_h][x + dx] != '#' or visited[y + max_h][x + dx]:
                                done = True
                                break
                        if not done:
                            max_h += 1

                    for dy in range(max_h):
                        for dx in range(max_w):
                            visited[y + dy][x + dx] = True

                    platform = Platform(
                        x * tile_size,
                        y * tile_size,
                        max_w * tile_size,
                        max_h * tile_size
                    )
                    self.platforms.append(platform)

    def place_item(self, item, x, y):
        x *= TILE_SIZE
        y *= TILE_SIZE
        w, h = TILE_SIZE, TILE_SIZE
        item_dict = {'.': None, '#': Platform(x, y, w, h), '<': Spike(x, y, w, h), '@': Checkpoint(x, y, w, h), 'o': Collectible(x, y, TILE_SIZE*0.5), '0': JumpOrb(x, y, TILE_SIZE*0.3)}
        match item:
            case '<':
                self.spikes.append(item_dict[item])
            case '@':
                self.checkpoints.append(item_dict[item])
            case 'o':
                self.collectibles.append(item_dict[item])
            case '0':
                self.jump_orbs.append(item_dict[item])
            case _:
                return

    def setup(self):
        self.group_platforms(read_map(MAP_FILENAME), TILE_SIZE)
        self.setup_map()

    def loop(self):
        run = True
        while run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pause = Pause()
                        pause.loop()

            SCREEN.fill((50, 50, 50))

            self.update()
            self.draw()
            font(f"score: {self.score}", pg.Color("white"), (10, 10))

            pg.display.update()
            self.clock.tick(FPS)

    def update(self):
        if not self.player.isDead:
            self.player.move_y()
            self.player_floor_collision()
            self.player_wall_collision()
            self.player.apply_friction()
            self.death_condition()
            self.player_collectible_collision()
            self.player_checkpoint_collision()
            self.player_orb_collision()
            self.input()

        for collectible in self.collectibles:
            collectible.animation()

        for orb in self.jump_orbs:
            orb.animation()

    def draw(self):
        for collectible in self.collectibles:
            if not collectible.isAnimationDone:
                circle((255, 215, 0, 255), collectible.return_circle_info())
        rect(pg.Color('red'), self.player.return_rect())
        for idx, platform in enumerate(self.platforms):
            rect(pg.Color('blue'), platform)
        for spike in self.spikes:
            polygon(pg.Color('black'), spike.return_poly_info())
        for checkpoint in self.checkpoints:
            if checkpoint.isOn:
                polygon((0, 200, 0, 255), checkpoint.return_diamond_points())
            else:
                polygon((80, 105, 0, 200), checkpoint.return_diamond_points())
        for orb in self.jump_orbs:
            circle((255, 215, 0, 255), orb.return_circle_info())
            circle((255, 255, 100, 100), orb.animation_circle())

    def player_floor_collision(self):
        self.player.isColliding = False
        self.player.canJump = False
        player_rect = self.player.return_rect()

        for platform in self.platforms:
            plat_rect = platform.return_rect()

            if player_rect.colliderect(plat_rect):
                if self.player.speedY > 0 and player_rect.bottom - self.player.speedY <= plat_rect.top:
                    self.player.y = plat_rect.top - self.player.height
                    self.player.rect.y = self.player.y
                    self.player.speedY = 0
                    self.player.isColliding = True
                    self.player.canJump = True

                elif self.player.speedY < 0 and player_rect.top - self.player.speedY >= plat_rect.bottom:
                    self.player.y = plat_rect.bottom
                    self.player.rect.y = self.player.y
                    self.player.speedY = 0

    def player_wall_collision(self):
        player_rect = self.player.return_rect()

        for platform in self.platforms:
            plat_rect = platform.return_rect()

            if player_rect.colliderect(plat_rect):
                if self.player.speedX > 0 and player_rect.right > plat_rect.left > player_rect.left:
                    self.player.x = plat_rect.left - self.player.width
                    self.player.rect.x = self.player.x
                    self.player.speedX = 0
                    return

                elif self.player.speedX < 0 and player_rect.left < plat_rect.right < player_rect.right:
                    self.player.x = plat_rect.right
                    self.player.rect.x = self.player.x
                    self.player.speedX = 0
                    return

    def player_collectible_collision(self):
        for collectible in self.collectibles:
            if not collectible.isCollected and self.player.rect.colliderect(collectible.return_rect()):
                collectible.isCollected = True
                self.score += 1
                collectible.start_animation()

    def player_spike_collision(self):
        player_rect = self.player.return_rect()
        for spike in self.spikes:
            if player_rect.colliderect(spike.return_rect(hitbox_len=30)):
                if not self.player.isDead:
                    return True

    def player_checkpoint_collision(self):
        player_rect = self.player.return_rect()
        for checkpoint in self.checkpoints:
            if player_rect.colliderect(checkpoint.return_rect()) and not checkpoint.isOn:
                for i in self.checkpoints:
                    i.isOn = False
                checkpoint.isOn = True
                self.player.respawn_point = [checkpoint.x, checkpoint.y]

    def player_orb_collision(self):
        player_rect = self.player.return_rect()
        for orb in self.jump_orbs:
            if player_rect.colliderect(orb.return_hitbox(TILE_SIZE)) and not self.player.canJump:
                self.player.canJump = True
                orb.activate()

    def player_fell_void(self):
        y = self.player.y
        if y > SCREEN_HEIGHT + 500:
            return True

    def death_condition(self):
        if self.player.isDead:
            return

        conditions = [self.player_spike_collision(), self.player_fell_void()]
        if any(conditions):
            self.player.on_death()

    def input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.player.move_x(-2)
        if keys[pg.K_RIGHT]:
            self.player.move_x(2)
        if keys[pg.K_SPACE] and self.player.canJump:
            self.player.speedY = -13


def get_font(size):
    return pg.font.Font("assets/fonts/font.ttf", size)


class Menu:
    def __init__(self):
        pg.display.set_caption("Menu")

    def setup(self):
        pass

    def loop(self):
        run = True

        while run:
            play_button = Button(image=None, pos=(SCREEN_WIDTH//2, 100),
                                 text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
            options_button = Button(image=None, pos=(SCREEN_WIDTH//2, 300),
                                    text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
            exit_button = Button(image=None, pos=(SCREEN_WIDTH//2, 500),
                                 text_input="EXIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    run = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if play_button.check_for_input(pg.mouse.get_pos()):
                        game = Game()
                        game.setup()
                        game.loop()
                    if options_button.check_for_input(pg.mouse.get_pos()):
                        options = Options()
                        options.loop()
                    if exit_button.check_for_input(pg.mouse.get_pos()):
                        pg.quit()
                        run = False

            SCREEN.fill(pg.Color('gray35'))

            for button in [play_button, options_button, exit_button]:
                button.change_color(pg.mouse.get_pos())
                button.update(SCREEN)

            pg.display.update()


class Options:
    def __init__(self):
        pg.display.set_caption("Options")

    def loop(self):
        run = True

        while run:
            return_button = Button(image=None, pos=(SCREEN_WIDTH//2, 530),
                                 text_input="RETURN", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    run = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if return_button.check_for_input(pg.mouse.get_pos()):
                        menu = Menu()
                        menu.loop()

            SCREEN.fill(pg.Color('gray30'))

            return_button.change_color(pg.mouse.get_pos())
            return_button.update(SCREEN)

            pg.display.update()


class Pause:
    def __init__(self):
        pg.display.set_caption("Game Paused")

    def loop(self):
        run = True

        resume_button = Button(image=None, pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100),
                               text_input="RESUME", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        menu_button = Button(image=None, pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100),
                             text_input="MENU", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        while run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    run = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if resume_button.check_for_input(pg.mouse.get_pos()):
                        game = Game()
                        game.loop()
                    if menu_button.check_for_input(pg.mouse.get_pos()):
                        menu = Menu()
                        menu.loop()

            sc_rect = pg.Rect(0, 0, SCREEN.get_size()[0], SCREEN.get_size()[1])
            rect((50, 50, 50, 100), sc_rect)

            for button in [resume_button, menu_button]:
                button.change_color(pg.mouse.get_pos())
                button.update(SCREEN)

            pg.display.update()
