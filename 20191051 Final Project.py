
import pygame
import random
from time import sleep
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 400
HEIGHT = 700
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("20191051 김명지 Final Project")
clock = pygame.time.Clock()

background = pygame.image.load(path.join(img_dir, "메인.png")).convert()
background = pygame.transform.scale(background, (400, 711))
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "뒤집개.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "뒤집개.png")).convert()
egg_img = pygame.image.load(path.join(img_dir, "계란수정3.png")).convert()
chick_img = pygame.image.load(path.join(img_dir, "병아리수정3.png")).convert()
s_fri_img = pygame.image.load(path.join(img_dir, "계란후라이.png")).convert()
fri_images = []
fri_list = ['계란후라이0.png', '계란후라이1.png', '계란후라이2.png', '계란후라이3.png', '계란후라이4.png', '계란후라이5.png']
for i in fri_list:
    img = pygame.image.load(path.join(img_dir, i)).convert()
    img.set_colorkey(BLACK)
    fri_images.append(img)
score_img = pygame.image.load(path.join(img_dir, "스코어.png")).convert()
score_img = pygame.transform.scale(score_img, (38, 25))
score_img.set_colorkey(BLACK)
miss_img = pygame.image.load(path.join(img_dir, "미스.png")).convert()
miss_img = pygame.transform.scale(miss_img, (43, 37))
miss_img.set_colorkey(BLACK)

success_snd = pygame.mixer.Sound(path.join(snd_dir, '정답+후라이_편집.mp3'))
fail_snd = pygame.mixer.Sound(path.join(snd_dir, '오답_편집.mp3'))
kill_snd = pygame.mixer.Sound(path.join(snd_dir, '놀람+병아리_편집.mp3'))
click_snd = pygame.mixer.Sound(path.join(snd_dir, '클릭_편집.mp3'))
bgm1 = pygame.mixer.Sound(path.join(snd_dir, '브금1.mp3'))
bgm2 = pygame.mixer.Sound(path.join(snd_dir, '브금2.mp3'))

pygame.mixer.music.load(path.join(snd_dir, '브금2.mp3'))
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(loops=-1)


font_name = pygame.font.match_font('210카툰스토리B')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (20, 87))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect() 
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 3
        self.speedx = 0
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.x, self.rect.y)
            all_sprites.add(bullet)
            bullets.add(bullet)
            #shoot_sound.play()

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)        
        self.image = egg_img
        self.image = pygame.transform.scale(egg_img, (50, 35))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.bottom = random.randrange(-80, -20)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        #self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -100 or self.rect.right > WIDTH + 100:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

class BossMob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)        
        self.image = pygame.transform.scale(chick_img, (50, 35))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.bottom = random.randrange(-80, -20)
        self.speedy = random.randrange(1, 3)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        #self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -100 or self.rect.right > WIDTH + 100:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (20, 87))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

class Check(pygame.sprite.Sprite):
    def __init__(self,):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(s_fri_img, (260, 260))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2 + 20)

class FriedEgg(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        fri_img = pygame.transform.scale(fri_images[0], (70, 70))
        self.image = fri_img
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
            if self.frame == len(fri_list):
                self.kill()
            else:
                center = self.rect.center
                self.image = pygame.transform.scale(fri_images[self.frame], (70, 70)) 
                print(self.frame)
                self.rect = self.image.get_rect()
                self.rect.center = center

class Fail(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        fail_img = pygame.image.load(path.join(img_dir, "실패최종.png")).convert()
        fail_img = pygame.transform.scale(fail_img, (75, 50))
        self.image = fail_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 600

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            self.kill()

class Blood(pygame.sprite.Sprite):
    def __init__(self, x, y ):
        pygame.sprite.Sprite.__init__(self)
        blood_img = pygame.image.load(path.join(img_dir, "피1.png")).convert()
        blood_img = pygame.transform.scale(blood_img, (90, 90))
        self.image = blood_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 1500

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            self.kill()

def show_go_screen():
    img = pygame.image.load(path.join(img_dir, "시작.png")).convert()
    img = pygame.transform.scale(img, (400, 711))
    screen.blit(img, (0, 0))
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                click_snd.play()
                waiting = False

def show_finish_screen_noegg():
    img = pygame.image.load(path.join(img_dir, "엔딩2.png")).convert()
    img = pygame.transform.scale(img, (400, 711))
    screen.blit(img, (0, 0))
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                click_snd.play()
                waiting = False

def show_finish_screen_killchick():
    img = pygame.image.load(path.join(img_dir, "엔딩1.png")).convert()
    img = pygame.transform.scale(img, (400, 711))
    screen.blit(img, (0, 0))
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                click_snd.play()
                waiting = False


# Game loop
game_over = True
running = True
first = True

while running:
    if first:
        show_go_screen()
        first = False

    if game_over:
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bossmobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        fris = pygame.sprite.Group()
        checks = pygame.sprite.Group()

        player = Player()
        check = Check()

        checks.add(check)
        all_sprites.add(player)
        for i in range(8):
            newmob()

        for i in range(1):
            bossmob = BossMob()
            bossmobs.add(bossmob)
            all_sprites.add(bossmob)
        score = 0
        miss = 0

    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # 총알-몹
    for mob in mobs:
        for bullet in bullets:
            if pygame.sprite.collide_rect(mob, bullet):
                if pygame.sprite.collide_circle(check, mob):
                    success_snd.play()
                    fri = FriedEgg(mob.rect.center)
                    all_sprites.add(fri)
                    mob.kill()
                    bullet.kill()
                    score += 1
                    newmob()
                    
                else:
                    fail_snd.play()
                    fail = Fail(mob.rect.center)
                    all_sprites.add(fail)
                    mob.kill()
                    bullet.kill()
                    newmob()
                    miss += 1
                    

    # 플레이어-몹
    hits = pygame.sprite.spritecollide(player, mobs, True)
    for hit in hits:
        fail_snd.play()
        fail = Fail(hit.rect.center)
        all_sprites.add(fail)
        newmob()
        miss += 1

    # 총알-보스몹
    hits = pygame.sprite.groupcollide(bullets, bossmobs, True, True)
    for hit in hits:
        kill_snd.play()
        blood = Blood(hit.rect.x, (hit.rect.y - 5))
        all_sprites.add(blood)
        all_sprites.draw(screen)
        pygame.display.flip()
        sleep(.5)
        show_finish_screen_killchick()
        game_over = True

    #플레이어-보스몹
    hits = pygame.sprite.spritecollide(player, bossmobs, True)
    for hit in hits:
        kill_snd.play()
        blood = Blood(hit.rect.x, (hit.rect.y - 5))
        all_sprites.add(blood)
        all_sprites.draw(screen)
        pygame.display.flip()
        sleep(.5)
        show_finish_screen_killchick()
        game_over = True
        
    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, (0, -5))
    screen.blit(score_img, (WIDTH-90, 35))
    screen.blit(miss_img,(WIDTH-92, 67))
    #checks.draw(screen)
    all_sprites.draw(screen)
    draw_text(screen, 'x  ' + str(score), 18, WIDTH - 30, 40)
    draw_text(screen, 'x  ' + str(miss), 18, WIDTH - 30, 77)

    if miss >= 10:
        show_finish_screen_noegg()
        game_over = True

    pygame.display.flip()


pygame.quit()
