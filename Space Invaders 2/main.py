import pygame
import time
import random

pygame.init()
pygame.font.init()

BLUE_SPACE_SHIP = pygame.image.load("/Users/dunura/Desktop/Programming Projects/Space Invaders 2/assets/pixel_ship_blue_small.png")
GREEN_SPACE_SHIP = pygame.image.load("/Users/dunura/Desktop/Programming Projects/Space Invaders 2/assets/pixel_ship_green_small.png")
RED_SPACE_SHIP = pygame.image.load("/Users/dunura/Desktop/Programming Projects/Space Invaders 2/assets/pixel_ship_red_small.png")
YELLOW_SPACE_SHIP = pygame.image.load("/Users/dunura/Desktop/Programming Projects/Space Invaders 2/assets/pixel_ship_yellow.png")

BLUE_LASER = pygame.image.load("/Users/dunura/Desktop/Programming Projects/Space Invaders 2/assets/pixel_laser_blue.png")
GREEN_LASER = pygame.image.load("/Users/dunura/Desktop/Programming Projects/Space Invaders 2/assets/pixel_laser_green.png")
RED_LASER = pygame.image.load("/Users/dunura/Desktop/Programming Projects/Space Invaders 2/assets/pixel_laser_red.png")
YELLOW_LASER = pygame.image.load("/Users/dunura/Desktop/Programming Projects/Space Invaders 2/assets/pixel_laser_yellow.png")

WIDTH = 750
HEIGHT = 750


def collide(obj1, obj2):
    offset_x = obj2.x-obj1.x
    offset_y = obj2.y-obj1.y
    return obj1.mask.overlap(obj2.mask,(offset_x,offset_y)) != None




class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    
    def draw(self, window):
        window.blit(self.img, (self.x,self.y))
    
    def move(self, vel):
        self.y += vel
    
    def off_screen(self,height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(obj,self)



class Ship:
    COOLDOWN = 30

    def __init__(self, window, x, y,health=100,):
        self.window = window

        self.x = x
        self.y = y

        self.x_vel = 0
        self.y_vel = 0

        self.health = health

        self.ship_img = None
        self.laser_img = None

        self.lasers = []

        self.cool_down_counter = 0
        

    def draw(self): 
        self.window.blit(self.ship_img, (self.x, self.y))

        self.x+=self.x_vel
        self.y+=self.y_vel

        for laser in self.lasers:
            laser.draw(self.window)
    
    def move_lasers(self,vel,obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)



    
    def cooldown(self):
        if self.cool_down_counter >= 30:
            self.cool_down_counter = 0
        
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x,self.y,self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
    
    def get_width(self):
        return self.ship_img.get_width()
    
    def get_height(self):
        return self.ship_img.get_height()





 
class Player(Ship):
    def __init__(self, window, x,y,health=100): 
        super().__init__(window, x, y, health)

        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        
        self.mask = pygame.mask.from_surface(self.ship_img)  
        self.max_health = health

    

    def draw(self):
        super().draw()
        self.health_bar()

    def move_lasers(self,vel,objs):
            self.cooldown()
            for laser in self.lasers:
                laser.move(vel)
                if laser.off_screen(HEIGHT):
                    self.lasers.remove(laser)
                
                else:
                    for obj in objs:
                        if laser.collision(obj):
                            objs.remove(obj)
                            if laser in self.lasers:
                                self.lasers.remove(laser)

    def health_bar(self):
        pygame.draw.rect(self.window, (255,0,0), (self.x,self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(self.window, (0,255,0), (self.x,self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))





class Enemy(Ship):

    # CLASS VARAIBLES

    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER)

    }


    def __init__(self, window,x,y,color, health=100):
        super().__init__(window,x,y,health)

        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)



    def move(self,vel):
        self.y+=vel


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<GAME>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

class Game:

    laser_vel = 5
    enemy_vel = 1
    def __init__(self):

        
        # WINDOW 
    
        self.width, self.height = 750, 750
        self.window = pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption("Space Invaders 2")

        # FONTS

        self.font = pygame.font.SysFont("comicsans", 50)
        self.lost_font = pygame.font.SysFont("comicsans", 60)
        self.title_font = pygame.font.SysFont("comicsans",  50)

        # FRAME RATE 
        self.FPS = 60
        self.clock = pygame.time.Clock()

        # LEVEL AND LIVES
        self.level = 0
        self.lives = 5

        self.lives_label = ""
        self.level_label = ""

        # SCORE
        self.score = 0

        # BACKGROUND
        self.BG = pygame.transform.scale(pygame.image.load("/Users/dunura/Desktop/Programming Projects/Space Invaders 2/assets/background-black.png"), (self.width,self.height))


        # ENEMIES

        self.enemies = []
        self.wave_length = 0

       

        # PLAYER SHIP
        self.player_ship = Player(self.window, 300, 630)
        
        
        self.lost = False
        self.lost_count = 0


        # OTHER VARIABLES



    def play(self):
        self.window.blit(self.BG,(0,0))
        self.lives_label = self.font.render(f"Lives: {self.lives}", True, (255,255,255))
        self.level_label = self.font.render(f"Level: {self.level}", True, (255,255,255))

        self.window.blit(self.lives_label, (10,10))
        self.window.blit(self.level_label, (self.width - self.level_label.get_width() - 10, 10))

        
        for enemy in self.enemies:
            enemy.draw()


        # ENEMY MOVEMENT

        for enemy in self.enemies[:]:
            enemy.move(self.enemy_vel)
            enemy.move_lasers(self.laser_vel, self.player_ship)

            if random.randrange(0,2*60) == 1:
                enemy.shoot()

            if collide(enemy, self.player_ship):
                self.player_ship.health -= 10
                self.enemies.remove(enemy)


            if enemy.y + enemy.get_height() > self.height:
                self.lives-=1
                self.enemies.remove(enemy)
            
            
        

        
        self.player_ship.draw()

        self.player_ship.move_lasers(-self.laser_vel, self.enemies)

        # PLAYER BOUNDARIES

        if self.player_ship.y >= self.height - self.player_ship.get_height() - 30:
            self.player_ship.y = self.height - self.player_ship.get_height() - 30
        
        if self.player_ship.y <= 0:
            self.player_ship.y = 0
        
        if self.player_ship.x >= self.width - self.player_ship.get_width():
            self.player_ship.x = self.width-self.player_ship.get_width()
        
        if self.player_ship.x <= 0:
            self.player_ship.x = 0

        
        if self.lost:
            lost_label = self.lost_font.render("GAME OVER", True, (255,255,255))
            self.window.blit(lost_label, (self.width/2 - lost_label.get_width()/2, 350))
    
        

    def main_menu(self):
        run = True
        while run:
            self.window.blit(self.BG, (0,0))
            title_label = self.title_font.render("Press the mouse to begin", True, (255,255,255))
            self.window.blit(title_label, (self.width/2 - title_label.get_width()/2, 350))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.player_ship.health = 100
                    self.level = 0
                    self.lives = 5
                    self.wave_length = 0
                    self.lost = False
                    self.enemies = []
                    
                    self.run()
                    
                    
            
        pygame.quit()



    def run(self):

        running = True
        while running:
            self.clock.tick(self.FPS)
            self.play()

            # LOST CHECK
            if self.lives == 0 or self.player_ship.health<= 0:
                self.lost = True
                self.lost_count +=1
            
            
            # GAME OVER FREEZE SCREEN LOGIC

            if self.lost:
                if self.lost_count > self.FPS*5:
                    running = False

            
            
            # ENEMY WAVE LOGIC
            if len(self.enemies) == 0:
                self.level+=1
                self.wave_length+=5
                for i in range(self.wave_length):
                    enemy = Enemy(self.window, random.randrange(50,self.width-100), random.randrange(-1500+self.level*100,-100), random.choice(["red","blue","green"]))
                    self.enemies.append(enemy)



            # WINDOW EVENTS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player_ship.x_vel = -5

                    if event.key == pygame.K_RIGHT:
                        self.player_ship.x_vel = 5
                    
                    if event.key == pygame.K_UP:
                        self.player_ship.y_vel = -5
                    
                    if event.key == pygame.K_DOWN:
                        self.player_ship.y_vel = 5
                
                    if event.key == pygame.K_SPACE:
                        self.player_ship.shoot()
                
                
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.player_ship.x_vel = 0
                    
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        self.player_ship.y_vel = 0
                    
                    
            



            

            
            pygame.display.update()



if __name__ == "__main__":
    game = Game()
    game.main_menu()