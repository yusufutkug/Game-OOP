import pygame as pg
from BULLET import *
from Sprites import*
class Heros(Sprite):

    def __init__(self,window,all_sprites,hero_sprite,game):
        super(Heros, self).__init__(hero_sprite,all_sprites)
        self.EUE=game
        self.hero_death=False
        self.cor=(window.get_width()//2-32,window.get_height()//2+32)
        self.image =pg.Surface((32,64))
        self.image.fill((255,0,0))
        self.image_list=[self.image]
        self.current_image=0
        self.image = self.image_list[self.current_image]
        self.rect = self.image.get_rect(center=self.cor)
        self.cooldown_atack=4
        self.cooldown_defense=8
        self.bullet_timer = 1
        self.bullet_time=1
        self.bullet_img=pg.Surface((3,10))
        self.bullet_img.fill((0,255,0))
        self.health=100
        self.max_health=100
        self.screen=window
        self.bullet_damage=15
        self.bullet_vel=(0,-300)
        self.current_animated=0
        self.animated=[pg.Surface((1,1))]
        self.atackSkill=False
        self.defenseSkill=False
        self.laser_sound = pg.mixer.Sound('sound\\shoot.wav')
        self.laser_sound.set_volume(0.3)
        self.amIGhost=False
        self.firex=1
        self.hero_index=0
        self.atack_skillsound=pg.mixer.Sound("sound\\magic-strike-5856.wav")
        self.defense_skillsound=pg.mixer.Sound("sound\\arcade-bleep-sound-6071.wav")
        self.gameoversound=pg.mixer.Sound("sound\\game-over-arcade-6435.wav")

    def update(self, dt):

        if self.health <= 0:
            self.gameoversound.play()
            self.kill()
            self.hero_death=True
        if not self.hero_death:
            objects=self.EUE.HereIsX(enemy_bullets=1)
            hits = self.spritecollide(objects[0])
            for bullet in hits:
                bullet.change_health(self.health)
            self.move()
            self.animation()
            self.fire(dt,self.cor,self.firex)
            self.healthbar(self.screen)
            self.atack_skill(dt)
            self.defense_skill(dt)

    def move(self):

        self.cor=pg.mouse.get_pos()
        self.rect.center = self.cor

    def fire(self,dt,cor,x):

        mouse_pressed = pg.mouse.get_pressed()
        self.bullet_timer -= dt 
        if self.bullet_timer <= 0 and mouse_pressed[0]:
            self.laser_sound.play()
            objects=self.EUE.HereIsX(all_sprites=1,enemies_sprites=1,hero_bullets=1) 
            if x%2==1:             
                Bullet(cor, self.bullet_img,self.bullet_vel,self.bullet_damage, objects[0], objects[1],objects[2])
                if x!=1:
                    self.fire(dt,cor,(x-1))
                else:
                    self.bullet_timer = self.bullet_time
            else:
                distance=self.image.get_width()//x
                k=1/2
                for i in range(1,x+1):
                    i=(i+1)//2
                    Bullet((cor[0]+(i*k*distance),cor[1]), self.bullet_img,self.bullet_vel,self.bullet_damage, objects[0], objects[1],objects[2])
                    self.bullet_timer = self.bullet_time  
                    k*=-1  

    def draw_hero(self,screen,font):

        hero_name = font.render(f"{self.__class__.__name__}", True, (255, 255, 255))
        hero_name_rect = hero_name.get_rect(center=(self.rect.center[0],self.rect.center[1]+128))
        self.rect.center=(screen.get_width() // 2, screen.get_height() // 2+64)
        screen.blit(self.image,self.rect)
        self.animation()
        screen.blit(hero_name,hero_name_rect)

    def animation(self):

        mouse_pressed = pg.mouse.get_pressed()
        image=self.animated[int(self.current_animated)]
        self.current_animated+=0.3
        if mouse_pressed[0]:
            self.current_image+=0.2
        if self.current_animated>=len(self.animated):
            self.current_animated=0
        if self.current_image >= len(self.image_list):
            self.current_image = 0
        rect=image.get_rect(center=(self.rect.center[0],self.rect.center[1]+32))
        self.image=self.image_list[int(self.current_image)]
        if self.amIGhost:
            self.image.set_alpha(150)
        else:
            self.image.set_alpha(255)
        self.screen.blit(image,rect)

    def __get_width(self):

        return self.image.get_width()

    def __get_height(self):

        return self.image.get_height()

    def healthbar(self, window):

            pg.draw.rect(window, (255, 0, 0),(self.rect.x, self.rect.y + self.__get_height() + 20, self.__get_width(), 10))
            pg.draw.rect(window, (0, 255, 0), (self.rect.x, self.rect.y + self.__get_height() + 20, self.__get_width() * (self.health / self.max_health), 10))

    def defense_skill(self,dt):

        pass

    def atack_skill(self,dt):

        pass

    def change_bulletTime(self,value):

        if self.bullet_time>=0.2:
            self.bullet_time-=value

    def change_bulletDamage(self,value):

        self.bullet_damage+=value
    
    def change_Firex(self):

        self.firex+=1
        if self.firex>6:
            self.firex=6

    def change_health(self,value,effect=0):
        if effect==1:
            self.max_health+=value
            self.health=self.max_health
        else: 
            if  not self.amIGhost:   
                self.health-=value

    
    
    def active_defenseSkill(self):
        self.defense_skillsound.play()
        self.defenseSkill=True
    
    def active_atackSkill(self):

        self.atack_skillsound.play()
        self.atackSkill=True
    

    


class Tank(Heros):


    def __init__(self,window, all_sprites, hero_sprites,game):
        super(Tank, self).__init__( window, all_sprites, hero_sprites,game)
        self.image_list =[pg.image.load("image\\hr1.png"),pg.image.load("image\\hr4.png"),pg.image.load("image\\hr1.png"), pg.image.load("image\\hr2.png"), pg.image.load("image\\hr3.png"), pg.image.load("image\\hr2.png"), pg.image.load("image\\hr1.png")]
        self.current_image = 0
        self.image = self.image_list[self.current_image]
        self.rect=self.image.get_rect(center=self.cor)
        self.bullet_time = 0.7
        self.health = 150
        self.max_health = 150
        self.screen = window
        self.bullet_damage = 20
        self.bullet_vel = (0, -500)
        self.cooldown_atack=0
        self.animated=[pg.image.load("image\\Untitled (1).png"),pg.image.load("image\\Untitled (2).png"),pg.image.load("image\\Untitled (3).png")]
        self.bullet_img.fill((255,0,0))
        self.defenseSkill=False
        self.atackSkill=False
        self.amIGhost=False

    def defense_skill(self,dt):
        if self.defenseSkill:
            self.health+=self.health//2
            if self.health>=self.max_health:
                self.health=self.max_health
            self.defenseSkill=False
            

    def atack_skill(self,dt):
        if self.atackSkill:
            cor=pg.mouse.get_pos()
            image_list=[pg.Surface((1,cor[1])),pg.Surface((1,cor[1])),pg.Surface((1,cor[1])),pg.Surface((3,cor[1])),pg.Surface((3,cor[1])),pg.Surface((3,cor[1])),pg.Surface((9,cor[1])),pg.Surface((9,cor[1])),pg.Surface((9,cor[1])),pg.Surface((9,cor[1])),pg.Surface((70,cor[1])),pg.Surface((40,cor[1])),pg.Surface((30,cor[1])),pg.Surface((50,cor[1])),pg.Surface((50,cor[1])),pg.Surface((30,cor[1])),pg.Surface((30,cor[1])),pg.Surface((9,cor[1])),pg.Surface((9,cor[1])),pg.Surface((3,cor[1])),pg.Surface((1,cor[1]))]
            image=image_list[int(self.cooldown_atack)]
            bimage=image.copy()
            bimage.set_alpha(0)
            rect=image.get_rect(midbottom=(cor[0],cor[1]-32))
            objects=self.EUE.HereIsX(all_sprites=1,enemies_sprites=1,hero_bullets=1)           
            Bullet(cor,bimage,(0, -950),99999, objects[0], objects[1],objects[2])
            image.fill((255,0,0))
            self.cooldown_atack+=(dt*40)
            self.screen.blit(image,rect)
            pg.display.update(rect)
            if self.cooldown_atack>=len(image_list)-1:
                self.cooldown_atack=0
                self.atackSkill=False
                


class Ghost(Heros):


    def __init__(self,window, all_sprites,hero_sprites,game):
        super(Ghost, self).__init__( window, all_sprites, hero_sprites,game)
        self.image_list = [pg.image.load("image\\hero1.png"), pg.image.load("image\\hero2.png"), pg.image.load("image\\hero3.png"),
                           pg.image.load("image\\hero4.png"), pg.image.load("image\\hero3.png"), pg.image.load("image\\hero2.png"),
                           pg.image.load("image\\hero1.png")]
        self.current_image = 0
        self.image = self.image_list[self.current_image]
        self.rect=self.image.get_rect(center=self.cor)
        self.bullet_time = 0.5
        self.health = 60
        self.max_health = 60
        self.screen = window
        self.bullet_damage = 25
        self.bullet_vel = (0, -600)
        self.animated=[pg.image.load("image\\Untitled (1).png"),pg.image.load("image\\Untitled (2).png"),pg.image.load("image\\Untitled (3).png")]
        self.cooldown_atack=4
        self.cooldown_defense=8
        self.bullet_img.fill((255,0,0))
        self.defenseSkill=False
        self.atackSkill=False
        self.amIGhost=False

    def defense_skill(self,dt):
        if self.defenseSkill:
            self.cooldown_defense-=dt
            self.amIGhost=True
            if self.cooldown_defense<=0:
                self.defenseSkill=False
                self.amIGhost=False
                self.cooldown_defense=6

    def atack_skill(self,dt):
        if self.atackSkill:
            center=(self.screen.get_width() - self.rect.center[0], self.rect.center[1])
            image=self.image.copy()
            rect = image.get_rect(center=center)
            image.set_alpha(150)
            self.screen.blit(image, rect)
            self.fire(dt,center,self.firex)
            self.cooldown_atack-=dt
            if self.cooldown_atack<=0:
                self.atackSkill=False
                self.cooldown_atack=5


        



