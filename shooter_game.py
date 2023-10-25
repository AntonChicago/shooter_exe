from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        key_result = key.get_pressed()
        if key_result [K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if key_result [K_d] and self.rect.x < win_w - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', player.rect.x + 28, player.rect.y - 15, 10, 30, 9)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= win_h:
            self.rect.y = 0
            self.rect.x = randint(80, win_w - 80)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 5:
            self.kill() 


font.init()
font2 = font.SysFont('Arial', 36)

score = 0
lost = 0
goal = 10
max_lost = 5

win_w = 700
win_h = 500

lose = font2.render('Вы проиграли', True, (255, 255, 255))
win = font2.render('Вы выиграли', True, (255, 255, 255))

window = display.set_mode((win_w, win_h))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (win_w, win_h))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')

game = True
finish = False
clock = time.Clock()
FPS = 120

player = Player('rocket.png', 350, 410, 65, 65, 7)
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()

for i in range(1, 6):
    monster = Enemy('ufo.png', randint(80, win_w - 80), -40, 65, 65, 1)
    monsters.add(monster)

for q in range(1, 3):
    asteroid = Enemy('asteroid.png', randint(80, win_w -80), -40, 70, 70, 2)
    asteroids.add(asteroid) 

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()

    if not finish:
        window.blit(background, (0, 0))
        
        text = font2.render("Счёт: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 40))

        player.reset()
        player.update()
        #monsters.reset()
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)
        bullets.update()
        bullets.draw(window)
         
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy('ufo.png', randint(80, win_w - 80), -40, 65, 65, randint(1, 3))
            monsters.add(monster)

        if sprite.spritecollide(player, monsters, False) or lost > max_lost or sprite.spritecollide(player, asteroids, False):
            finish = True
            window.blit(lose, (200, 200))

        if score > goal:
            finish = True
            window.blit(win, (200, 200))

        display.update()
        clock.tick(FPS)
        
time.delay(50)