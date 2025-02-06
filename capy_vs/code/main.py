from settings import *
from player import *
from sprites import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites
from button import *

from random import randint, choice

class Game:
    def __init__(self):
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Capy's Christmas Nightmare")
        self.clock = pygame.time.Clock()
        self.running = True

        # groups 
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        # gun timers
        self.can_shoot = True
        self.shoot_time = 0 
        self.gun_cooldown = 300

        # enemy timer 
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 500)
        self.spawn_positions = []
        
        # audio 
        self.shoot_sound = pygame.mixer.Sound('audio/shoot.wav')
        self.hit_sound = pygame.mixer.Sound(join('audio', 'hit.wav'))
        self.hit_sound.set_volume(0.5)
        self.shoot_sound.set_volume(0.2)
        self.impact_sound = pygame.mixer.Sound(join('audio', 'impact.ogg'))
        self.music = pygame.mixer.Sound(join('audio', 'music.wav'))
        self.music.set_volume(0.4)
        self.music.play(loops = -1)

        # health bar
        self.health_bar = HealthBar(50, 650, 300, 40, 100)
        self.health_bar.hp = 100
        self.heart = pygame.image.load(join('images', 'player', 'heart.png')).convert_alpha()
        self.heart_size = self.heart.get_size()
        self.heart = pygame.transform.scale(self.heart, (float(self.heart_size[0] / 15), float(self.heart_size[1] / 15)))

        # score
        self.score = 0

        # setup
        self.load_images()
        self.setup()

    def load_images(self):
        self.bullet_surf = pygame.image.load(join('images', 'gun', 'bullet.png')).convert_alpha()
        self.bullet_size = self.bullet_surf.get_size()
        self.bullet_surf = pygame.transform.scale(self.bullet_surf, (float(self.bullet_size[0]*2.5), float(self.bullet_size[1]*2.5)))

        folders = list(walk(join('images', 'enemies')))[0][1]
        self.enemy_frames = {}
        for folder in folders:
            for folder_path, _, file_names in walk(join('images', 'enemies', folder)):
                self.enemy_frames[folder] = []
                for file_name in sorted(file_names, key = lambda name: int(name.split('.')[0])):
                    full_path = join(folder_path, file_name)
                    self.enemy_img = pygame.image.load(full_path).convert_alpha()
                    self.enemy_size = self.enemy_img.get_size()
                    surf = pygame.transform.scale(self.enemy_img, (float(self.enemy_size[0]*2), float(self.enemy_size[1]*2)))
                    self.enemy_frames[folder].append(surf)

    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            self.shoot_sound.play()
            pos = self.gun.rect.center + self.gun.player_direction * 50
            Bullet(self.bullet_surf, pos, self.gun.player_direction, (self.all_sprites, self.bullet_sprites))
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.gun_cooldown:
                self.can_shoot = True

    def bullet_collision(self):
        if self.bullet_sprites:
            for bullet in self.bullet_sprites:
                collision_sprites = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False, pygame.sprite.collide_mask)
                if collision_sprites:
                    self.impact_sound.play()
                    self.score += 1
                    for sprite in collision_sprites:
                        sprite.destroy()
                    bullet.kill()
                    
    def setup(self):
        map = load_pygame(join('data', 'maps', 'world.tmx'))

        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE,y * TILE_SIZE), image, self.all_sprites)
        
        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
        
        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x,obj.y), self.all_sprites, self.collision_sprites)
                self.gun = Gun(self.player, self.all_sprites)
            else:
                self.spawn_positions.append((obj.x, obj.y))

    #add health system
    def player_collision(self):
        if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
            self.health_bar.hp -= 0.5
            self.hit_sound.play()
            if self.health_bar.hp <= 0:
                self.running = False

    def run(self):
        pygame.display.init()
        self.health_bar.hp = 100
        while self.running:
            # dt 
            dt = self.clock.tick() / 1000

            # event loop 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == self.enemy_event:
                    Enemy(choice(self.spawn_positions), choice(list(self.enemy_frames.values())), (self.all_sprites, self.enemy_sprites), self.player, self.collision_sprites)

            # update 
            self.gun_timer()
            self.input()
            self.all_sprites.update(dt)
            self.bullet_collision()
            self.player_collision()

            # draw
            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            
            self.health_bar.draw(self.display_surface)
            self.display_surface.blit(self.heart, (10, 640))

            font = pygame.font.Font("data/menu/font.ttf", 35)
            SCORE_TEXT = font.render(f"SCORE: {self.score}", True, "#7315d4")
            self.display_surface.blit(SCORE_TEXT, (950, 650))
            pygame.display.update()

        game.game_over()


    def main_menu(self):
        pygame.display.init()
        BG = pygame.image.load("images/start.png")
        while True:
            self.display_surface.blit(BG, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()
            font = pygame.font.Font("data/menu/font.ttf", 60)

            MENU_TEXT = font.render("CAPY'S CHRISTMAS", True, "#eabf34")
            MENU_TEXT2 = font.render("NIGHTMARE", True, "#ac1211")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
            MENU_RECT2 = MENU_TEXT2.get_rect(center=(640, 175))

            PLAY_BUTTON = Button(image=pygame.image.load("data/menu/Play Rect.png"), pos=(640, 300), 
                                    text_input="PLAY", font=pygame.font.Font("data/menu/font.ttf", 75), base_color="#d7fcd4", hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("data/menu/Quit Rect.png"), pos=(640, 450), 
                                    text_input="QUIT", font=pygame.font.Font("data/menu/font.ttf", 75), base_color="#d7fcd4", hovering_color="White")

            self.display_surface.blit(MENU_TEXT, MENU_RECT)
            self.display_surface.blit(MENU_TEXT2, MENU_RECT2)

            for button in [PLAY_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.display_surface)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        game.run()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()

            pygame.display.update()
    
    def game_over(self):
        pygame.display.init()
        BG = pygame.image.load("images/end.png")

        self.music.stop()
        self.music = pygame.mixer.Sound(join('audio', 'game_over.mp3'))
        self.music.set_volume(0.7)
        self.music.play()

        while True:
            self.display_surface.blit(BG, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()
            font = pygame.font.Font("data/menu/font.ttf", 60)

            MENU_TEXT = font.render("GAME OVER", True, "#eabf34")
            font = pygame.font.Font("data/menu/font.ttf", 50)
            MENU_TEXT2 = font.render(f"FINAL SCORE: {self.score}", True, "#ac1211")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
            MENU_RECT2 = MENU_TEXT2.get_rect(center=(640, 175))

            QUIT_BUTTON = Button(image=pygame.image.load("data/menu/Quit Rect.png"), pos=(640, 300), 
                                    text_input="QUIT", font=pygame.font.Font("data/menu/font.ttf", 70), base_color="#d7fcd4", hovering_color="White")

            self.display_surface.blit(MENU_TEXT, MENU_RECT)
            self.display_surface.blit(MENU_TEXT2, MENU_RECT2)

            for button in [QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.display_surface)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()

            pygame.display.update()

if __name__ == '__main__':
    pygame.display.init()
    game = Game()
    game.main_menu()