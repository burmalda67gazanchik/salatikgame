#Создай собственный Шутер!



from pygame import*
from random import randint
img_hero = 'панда.png'
img_enemy = 'апельсин.png'
img_bullet = 'колобок.png'

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image),(size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def update (self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        
    def fire(self):
        bullet = Bullet(img_bullet,self.rect.centerx,self.rect.top,200,200,-15)
        bullets.add(bullet)

lost = 0
score = 0
win_width = 700
win_height = 500

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        global win_height
        global win_width
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):

    def update(self):
        self.rect.y += self.speed

        if self.rect.y < 0:
            self.kill()


window = display.set_mode((700, 500))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))

ship = Player(img_hero,5,win_height - 100,80,100,10)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80,win_width-80),-40, 80, 50, randint(1, 5))
    monsters.add(monster)
    

bullets = sprite.Group()

finish = False



mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
clock = time.Clock()
font.init()
font2 = font.SysFont('Arial',36)
FPS = 60
run = True
finish = False
while run:




    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire +1                  
                    fire_sound.play()
                    ship.fire()

                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

            
    if not finish:
        window.blit(background,(0,0))
        text = font2.render("Счет:"+str(score),1,(255,255,255))
        window.blit(text,(10,20))

        text_lose = font2.render("Пропущено:"+ str(lost), 1,(255,255,255))
        window.blit(text_lose,(10,50))
        sprites_list = sprite.groupcollide(monsters,bullet,True,True)
        for c in sprites_list:
            score += 1

            monster = Enemy(img_enemy,randint(80,win_width - 80),40,80,50,randint(1, 5))
            monster.add(monster)
            if sprite.spritecollide(ship,monsters,False):
                hits += 1

            if real_time == True:
                now_time = timer()
                if now_time - last_time < 3:
                    reload = font2.render('Перезарядка',1,(150,0,0))
                    window.blit(reload,(260,460))
            else:
                num_fire = 0
                real_time = False

            if score >= 10:
                finish = True
                text = font2.render('Win',1,(255,255,255))
                window.blit(text,(100,100))

                if lost >= 3:
                    finish = True
                    text_lose = font2.render('Lose',1,(255,255,255))
                    window.blit(text_lose,(100,100))
                    if hits >= 3:
                        finish = True
                        text_lose = font2.render('Lose',1,(255,255,255))
                        if real_time == True:
                            now_time = timer()
        if now_time - last_time < 3:
            reload = font2.render('Перезарядка',1,(150,0,0))
            window.blit(reload,(260,460))
        else:
            num_fire = 0
            real_time = False
            if real_time == True:
                now_time = timer()
        if now_time - last_time < 3:
            reload = font2.render('Перезарядка',1,(150,0,0))
            window.blit(reload,(260,460))
        else:
            num_fire = 0
            real_time = False

        if sprite.spritecollide(ship,asterodis,False):
            hits += 1
        if sprite.spritecollide(ship,monsters,False):
            hits += 1
        
        if score >= 10:
            finish = True
            text = font2.render('Win',1,(255,255,255))
            if real_time == True:
                now_time = timer()
        if now_time - last_time < 3:
            reload = font2.render('Перезарядка',1,(150,0,0))
            window.blit(reload,(260,460))
        else:
            num_fire = 0
            real_time = False
            
            if lost >= 3:
                finish = True
                text_lose = font2.render('Lose',1,(255,255,255))


        ship.update()
        monsters.update()
        bullets.update()

        ship.reset()

        monsters.draw(window)
        bullets.draw(window)

        time.delay(50)
        display.update()
        clock.tick(FPS)








