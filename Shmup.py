# Shmup
# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3
# Art from Kenny.nl
import sys, pygame, random, os
from os import path
WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000

# Create color objects
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)

# setup assests folders and directory
game_dir = os.path.dirname(__file__)
snd_dir = os.path.dirname(__file__)
img_folder = os.path.join(game_dir, "PyGameSprites\Shmup")
snd_folder = os.path.join(snd_dir, "PyGameSounds")
# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()
font_name = pygame.font.match_font('arial')

# Text draw function
def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    # True refers to anti-aliasing. True is anti-aliasing, false is no anti-aliasing
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)
def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
def draw_shield_bar(surface, x, y, percent):
    if percent < 0:
        percent = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (percent / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill_rect)
    # 2 is the width of the outline
    pygame.draw.rect(surface, WHITE, outline_rect, 2)
def draw_lives(surface, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surface.blit(img, img_rect)
def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "SHMUP!", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Arrow keys move, Space to fire", 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
                
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .8 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_timer = pygame.time.get_ticks()

    def update(self):
        # timeout for powerups
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power = 1
            self.power_time = pygame.time.get_ticks()
        # unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        # Key event listener
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if keystate[pygame.K_UP]:
            self.speedy = -5
        if keystate[pygame.K_DOWN]:
            self.speedy = 5
        if keystate[pygame.K_SPACE]:
            self.shoot()
        # Collision on borders
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if not self.hidden and self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullets(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            else:
                bullet = Bullets(self.rect.left, self.rect.centery)
                bullet2 = Bullets(self.rect.right, self.rect.centery)
                all_sprites.add(bullet)
                all_sprites.add(bullet2)
                bullets.add(bullet)
                bullets.add(bullet2)
                shoot_sound.play()

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()
        
    def hide(self):
        # hide the player on death
        self.lives -= 1
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(2, 10)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()
        
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            
    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 5)

class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # Kill if moves off top of screen
        if self.rect.bottom < 0:
            self.kill()
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_animation[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_animation[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
class Powerups(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        # Kill if moves off top of screen
        if self.rect.top > HEIGHT:
            self.kill()
# load all graphics and sounds
background = pygame.image.load(path.join(img_folder, "SpaceBackground.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_folder, "PlayerShip1_blue.png")).convert()
player_lives_img = pygame.transform.scale(player_img, (25, 19))
player_lives_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(path.join(img_folder, "laserRed01.png")).convert()
meteor_images = []
meteor_list = ['meteorBrown_small1.png', 'meteorBrown_med1.png', 'meteorBrown_big1.png']

for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_folder, img)).convert())
explosion_animation = {}
explosion_animation['lg'] = []
explosion_animation['sm'] = []
explosion_animation['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_folder, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_animation['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_animation['sm'].append(img_sm)

    filename_player = 'sonicExplosion0{}.png'.format(i)
    player_explosion_img = pygame.image.load(path.join(img_folder, filename_player)).convert()
    player_explosion_img.set_colorkey(BLACK)
    explosion_animation['player'].append(player_explosion_img)
    
shoot_sound = pygame.mixer.Sound(path.join(snd_folder, 'Laser_2.wav'))
shoot_sound.set_volume(0.05)

power_shield_sound = pygame.mixer.Sound(path.join(snd_folder, 'Powerup.wav'))
power_shield_sound.set_volume(0.05)
power_gun_sound = pygame.mixer.Sound(path.join(snd_folder, 'Powerup2.wav'))
power_gun_sound.set_volume(0.05)

player_hit_sound = pygame.mixer.Sound(path.join(snd_folder, 'Hit_2.wav'))
player_hit_sound.set_volume(0.15)
explosion_sounds = []
for snd in ['Explosion.wav', 'Explosion2.wav', 'Explosion3.wav', 'Explosion4.wav']:
    explosion = pygame.mixer.Sound(path.join(snd_folder, snd))
    explosion.set_volume(0.05)
    explosion_sounds.append(explosion)
player_death_sound = pygame.mixer.Sound(path.join(snd_folder, 'rumble1.ogg'))
player_death_sound.set_volume(0.15)
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_folder, 'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_folder, 'bolt_gold.png')).convert()
pygame.mixer.music.load(path.join(snd_folder, 'maxstack-through-space.ogg'))
pygame.mixer.music.set_volume(0.05)

# Sprite Groups           
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()

# Sprite Creation and Group addition
player = Player()
all_sprites.add(player)
for i in range(8):
    newmob()
score = 0
pygame.mixer.music.play(loops=-1)
# game loop

# While running is true do this
# 1) Process input (events)
# 2) Update
# 3) Render
game_over = True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        # Sprite Groups           
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()

        # Sprite Creation and Group addition
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            newmob()
        score = 0
    # keep loop running at FPS. Pause for 1/60 second
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window  
        if event.type == pygame.QUIT:
            running = False
    # Update
    all_sprites.update()

    # Collison List between Mob and Player
    # Checks individual sprite against group (sprite, group) with boolean to control deletion. True means remove, false means keep
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player_hit_sound.play()
        player.shield -= hit.radius * 2
        explosion = Explosion(hit.rect.center, 'sm')
        all_sprites.add(explosion)
        newmob()
        if player.shield <= 0:
            death_explosion = Explosion(player.rect.center, 'player')
            player_death_sound.play()
            all_sprites.add(death_explosion)
            player.hide()
            if player.lives == 0:
                player.shield = 0
            else:
                player.shield = 100
    if player.lives == 0 and not death_explosion.alive():
        game_over = True
    # Collision for player and powerup
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += 25
            power_shield_sound.play()
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            power_gun_sound.play()
            player.powerup()
            # running = False
    # Collison List between Bullet and Mob
    # Checks Group of Bullets against Groups of Mobs
    bullet_hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in bullet_hits:
        score += 50 - hit.radius
        random.choice(explosion_sounds).play()
        explosion = Explosion(hit.rect.center, 'lg')
        all_sprites.add(explosion)
        if random.random() > 0.9:
            pow = Powerups(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()
        
    # Draw section
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_lives_img)
    # Always do this last after drawing everything
    pygame.display.flip()
    
pygame.quit()
