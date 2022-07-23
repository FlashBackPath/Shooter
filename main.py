from pygame import *
from random import randint

window = display.set_mode((700, 500))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))
font.init()
lost = 0
score = 0
font1 = font.Font(None, 36)
font2 = font.Font(None, 150)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_speed, x, y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        if player_image == "bullet.png":
            self.image = transform.scale(image.load(player_image), (15, 20))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 695:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", 15, self.rect.centerx - 7, self.rect.top)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 495:
            lost += 1
            self.rect.y = 0
            self.rect.x = randint(70, 630)


monsters = sprite.Group()
bullets = sprite.Group()

for i in range(1, 6):
   monster = Enemy("ufo.png", randint(1, 5), randint(80, 620), 40)
   monsters.add(monster)

ship = Player("rocket.png", 8, 10, 400)

while True:
    # переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
    finish = False
    # Основной цикл игры:
    run = True  # флаг сбрасывается кнопкой закрытия окна
    while run:
        # событие нажатия на кнопку “Закрыть”
        for e in event.get():
            if e.type == QUIT:
                run = False
            elif e.type == KEYDOWN:
                if e.key == K_SPACE:
                    ship.fire()

        if not finish:
            sprites_list = sprite.groupcollide(monsters, bullets, True, True)
            for i in sprites_list:
                monster = Enemy("ufo.png", randint(1, 5), randint(80, 620), 40)
                monsters.add(monster)
                score += 1

            window.blit(background, (0, 0))

            text = font1.render("Счет: " + str(score), 1, (255, 255, 255))
            window.blit(text, (10, 20))

            text_lose = font1.render("Пропущено: " + str(lost), 1, (255, 255, 255))
            window.blit(text_lose, (10, 50))

            ship.update()
            monsters.update()
            bullets.update()
            ship.reset()
            monsters.draw(window)
            bullets.draw(window)

            if score >= 30:
                window.blit(font2.render("YOU WON", 1, (255, 0, 0)), (100, 100))
                finish = True
            if lost >= 3:
                window.blit(font2.render("YOU LOST", 1 ,(255, 0, 0)), (100, 100))
                finish = True
            display.update()
        time.delay(50)

