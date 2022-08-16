import pygame 
from pygame.locals import *
import os 
import time
import random 



window_x = 1000
window_y = 800

PLAYER_SHIP  = pygame.image.load("resources/player_spaceship.png")
ENEMY_SHIPV1 = pygame.image.load("resources/spaceship_enemyv1.png")
ENEMY_SHIPV1 = pygame.transform.scale(ENEMY_SHIPV1, (60,60))
ENEMY_SHIPV2 = pygame.image.load("resources/spaceship_enemyv2.png")
ENEMY_SHIPV2 = pygame.transform.scale(ENEMY_SHIPV2, (75, 75))
SPIDER_ENEMY = pygame.image.load("resources/spider_enemy.png")
SPIDER_ENEMY = pygame.transform.scale(SPIDER_ENEMY, (50,50))

RED_LASER = pygame.image.load("resources/red_laser.png")
RED_LASER = pygame.transform.scale(RED_LASER , (25,25))

BLUE_LASER = pygame.image.load("resources/blue_laser.png")
BLUE_LASER = pygame.transform.scale(BLUE_LASER ,(40,40))

GREEN_LASER = pygame.image.load("resources/green_laser.png")
GREEN_LASER = pygame.transform.scale(GREEN_LASER, (25,25))

YELLOW_LASER =pygame.image.load("resources/yellow_laser.png")

BG = pygame.image.load("resources/space_background.jpg")

RECT = pygame.image.load("resources/Rect.png")
RECT = pygame.transform.scale(RECT, (400,100))

class Button():
    def __init__(self, image , pos , text_input, font, base_color, hovering_color) :
            self.image = image
            self.x_pos = pos[0]
            self.y_pos = pos[1]
            self.font = font
            self.base_color, self.hovering_color = base_color, hovering_color
            self.text_input = text_input
            self.text = self.font.render(self.text_input, True, self.base_color)

            if self.image is None:
                self.image = self.text
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
            self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
            if self.image is not None:
                screen.blit(self.image, self.rect)
            screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
                return True
            return False

    def changeColor(self, position):
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
                self.text = self.font.render(self.text_input, True, self.hovering_color)
            else:
                self.text = self.font.render(self.text_input, True, self.base_color)

class Laser():
    def __init__(self,x,y,img):
        self.x = x 
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self,game_surface):
        game_surface.blit(self.img ,(self.x,self.y))

    def move(self,speed):
        self.y += speed

    def off_screen(self,height):
        return not(self.y <= height and self.y >= 0)

    def collision(self,obj):
        return collide(self,obj)

    

class Live():
    def __init__(self,game_surface, live):
        self.game_surface = game_surface
        self.live = live 
        self.heart = pygame.image.load("resources/heart.png")
        self.heart = pygame.transform.scale(self.heart,(40,40))
        self.x = [960]*live
        self.y = [25]*live
        for i in range (self.live):
            if i <= self.live - 1:
                self.x[i] -= 40*i

    def lose_live(self):
        
        if self.live == 0:
            return 0 

        self.live -= 1

        self.x.pop()
        self.y.pop()  
    
    def update_live(self, value):
        self.live = value 

    def draw(self):
        for i in range(self.live):
            self.game_surface.blit(self.heart, (self.x[i],self.y[i]))   
                   
          
class Player():
    COOLDOWN = 30
    def __init__(self, game_surface,live):
        self.game_surface = game_surface
        self.ship = PLAYER_SHIP
        self.ship = pygame.transform.scale(self.ship, (60,60))
        self.x = 500
        self.y = 700
        self.laser_img = YELLOW_LASER
        self.laser_img = pygame.transform.scale(self.laser_img, (25,25))
        self.lasers = []
        self.cool_down_counter = 0
        self.mask = pygame.mask.from_surface(self.ship)
        self.damaged = False
        self.live = live 
        self.score = 0      

    def moveUp(self):
        if self.y > 0:
            self.y -= 10
            self.draw()
    
    def moveDown(self):
        if self.y < 750:
            self.y += 10
            self.draw()
        
    def moveRight(self):
        if self.x < 950:
            self.x += 10
            self.draw()

    def moveLeft(self):
        if self.x > 0:
            self.x -= 10
            self.draw()


    def draw(self):
        self.game_surface.blit(self.ship, (self.x,self.y))
        for laser in self.lasers:
            laser.draw(self.game_surface)

    def move_laser(self,vel,objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(window_y):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        obj.live -= 1
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                        else:
                            pass
                        if obj.is_death():
                            self.score += obj.points
                            sound = pygame.mixer.Sound("resources/8_bit explosion.mp3")
                            pygame.mixer.Sound.play(sound)
                            objs.remove(obj)
                            


    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0: 
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0 :
            laser = Laser(self.x+15,self.y, self.laser_img) 
            self.lasers.append(laser)
            laser_sound = pygame.mixer.Sound("resources/Laser_sound_effect.mp3")
            pygame.mixer.Sound.play(laser_sound)
            self.cool_down_counter = 1

    def new_live(self):
        if self.live < 5:
            self.live += 1
        else:
            pass

    def get_live(self):
        return self.live

    def get_score(self):
        return self.score

    def level_up(self, value):
        if value >= 3 and value < 5:
            self.COOLDOWN = 20
        if value >= 5:
            self.COOLDOWN = 10

         
class Enemy():
        COOLDOWN = 30

        enemy_type = { 
                        "spider":(SPIDER_ENEMY, RED_LASER, 1 , 5) ,
                        "shipv1":(ENEMY_SHIPV1, GREEN_LASER, 2 , 10) ,
                        "shipv2":(ENEMY_SHIPV2 , BLUE_LASER, 4 , 20)

                                                }
        def __init__(self,x,y,type,game_surface,DIRECTION):
            self.game_surface = game_surface
            self.type = type
            self.enemy_img , self.enemy_laser,self.live, self.points = self.enemy_type[type]
            self.mask = pygame.mask.from_surface(self.enemy_img)
            self.x = x
            self.y = y
            self.direction = DIRECTION
            self.lasers= []
            self.cool_down_counter = 0
            self.score = 0
            
            
         
        def draw(self): 
            self.game_surface.blit(self.enemy_img, (self.x,self.y))
            for laser in self.lasers:
                laser.draw(self.game_surface)

        def move(self , speed):
            if self.direction == "vertical":
                self.y += 2 + speed*0.2
            if self.direction == "left":
                self.x -= 2 + speed*0.2
            if self.direction == "right":
                self.x += 2 + speed*0.2

        def shoot(self):
            if self.cool_down_counter == 0 :
                laser = Laser(self.x+10,self.y, self.enemy_laser) 
                self.lasers.append(laser)
                self.cool_down_counter = 1

        def move_laser(self,vel,obj):
            self.cooldown()
            for laser in self.lasers:
                laser.move(vel)

                if laser.off_screen(window_y):
                    self.lasers.remove(laser)

                elif laser.collision(obj):
                    sound = pygame.mixer.Sound("resources/get_hit_sound_effect.mp3")
                    pygame.mixer.Sound.play(sound)
                    self.lasers.remove(laser)
                    obj.live -= 1
                    

        def cooldown(self):
            if self.cool_down_counter >= self.COOLDOWN:
                self.cool_down_counter = 0
            elif self.cool_down_counter > 0: 
                self.cool_down_counter += 1

        def is_death(self):
            if self.live == 0:
                return True

                
        

class Game():
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.play_menu_music()
        pygame.display.set_caption("Khoi Nguyen Space Invader")
        self.surface = pygame.display.set_mode((window_x,window_y))
        self.live = 5
        self.player = Player(self.surface,self.live)
        self.heart = Live(self.surface , self.live)
        self.level = 0
        self.enemies = []
        self.wave_length = 0
        self.score = 0
        
    def render_background(self):
        self.surface.blit(BG, (0,0))

    def play_background_music(self):
        pygame.mixer.music.load("resources/game_background.mp3")
        pygame.mixer.music.play(-1)

    def play_menu_music(self):
        pygame.mixer.music.load("resources/menu_music.mp3")
        # pygame.mixer.music.set_volume()
        pygame.mixer.music.play(-1)

    def play(self):
        self.render_background()
        for self.enemy in self.enemies:
            self.enemy.draw()

        self.player.draw()
        self.info_display()
        self.heart.draw()
        self.show_score()
        pygame.display.flip()
        self.check_live()
        

    def info_display(self):
        font = pygame.font.SysFont("comicsans" , 40, bold = True)
        level = font.render(f"Level: {self.level}", True, (255,255,255))
        self.surface.blit(level, (830,50))

    def check_live(self):
        remain = self.player.get_live()
        self.heart.update_live(remain)
        if remain <= 0:
            raise "Game Over"

    def show_score(self):
        font = pygame.font.SysFont('Amarone',40)
        self.score = self.player.get_score()
        display_score = font.render(f"Score: {self.score}", True , (255, 255, 255))
        self.surface.blit(display_score, (10,25))

    def instruction(self):
        run = True
        while run:
            RULES_MOUSE_POS = pygame.mouse.get_pos()

            self.surface.blit(BG, (0,0))

            instruction_font = pygame.font.SysFont("Arial" , 30)
            title_font = pygame.font.SysFont("Arial" , 50 , bold= True)

            line0 = title_font.render("HOW TO MOVE", True, "Red")
            self.surface.blit(line0, (340,50))
            line1 = instruction_font.render("Press W to move up", True, (219, 180, 7))
            self.surface.blit(line1, (370,120))
            line2 = instruction_font.render("Press S to move down", True, (219, 180, 7))
            self.surface.blit(line2, (370,160))
            line3 = instruction_font.render("Press A to move left", True, (219, 180, 7))
            self.surface.blit(line3, (370,200))
            line4 = instruction_font.render("Press D to move right", True, (219, 180, 7))
            self.surface.blit(line4, (370,240))
            line5 = title_font.render("OTHER BUTTONS", True, "Red")
            self.surface.blit(line5, (340,400))
            line6 = instruction_font.render("Press Space to shoot", True, (219, 180, 7))
            self.surface.blit(line6, (370,470))
            line7 = instruction_font.render("Press P to pause the game" , True , (219, 180, 7))
            self.surface.blit(line7, (370,510))


            back_font = pygame.font.SysFont("Arial" , 50, bold = True)
            BACK = Button(image=None, pos=(100, 700), 
                                text_input="BACK", font= back_font, base_color=(18, 119, 201), hovering_color="white")

            BACK.changeColor(RULES_MOUSE_POS)
            BACK.update(self.surface)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK.checkForInput(RULES_MOUSE_POS):
                        self.main_menu()

            pygame.display.flip()

        pygame.quit()
        quit()

    def credit(self):
        run = True
        while run:
            RULES_MOUSE_POS = pygame.mouse.get_pos()

            self.surface.fill((0,0,0))
            
            font = pygame.font.SysFont("Arial" , 40 )
            line1 = font.render("This game is made by Khoi Nguyen", True, (227, 93, 16))
            self.surface.blit(line1, (250,220))
            line2 = font.render("Great thanks to Tech With Tim and BaralTech's tutorials", True, (227, 93, 16))
            self.surface.blit(line2, (120,300))
            line3 = font.render("Images and sounds are used from the Internet", True, (227, 93, 16))
            self.surface.blit(line3, (180,380))


            back_font = pygame.font.SysFont("Arial" , 50, bold = True)
            BACK = Button(image=None, pos=(100, 700), 
                                text_input="BACK", font= back_font, base_color=(18, 119, 201), hovering_color= "white")

            BACK.changeColor(RULES_MOUSE_POS)
            BACK.update(self.surface)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK.checkForInput(RULES_MOUSE_POS):
                        self.main_menu()

            pygame.display.flip()

        pygame.quit()
        quit()




    def pause(self, value):
        if value == 'pause':
            pygame.mixer.music.pause()
            font = pygame.font.SysFont('arial',100)
            line= font.render("Pause", True , (247, 247, 247) )
            self.surface.blit(line, (400,300))
            pygame.display.flip()
        
        if value == 'resume':
            pygame.mixer.music.unpause()
            

         

    def show_game_over(self):
        bg = pygame.image.load("resources/game_over_background.png")
        self.surface.blit(bg,(0,0))
        font = pygame.font.SysFont('arial',30)
        line_1 = font.render(f"Your score is {self.score}", True , (247, 247, 247) )
        self.surface.blit(line_1, (410,550))
        line_2 = font.render("Press Enter to go the Menu. To exit press Escape", True, (247, 247, 247) )
        self.surface.blit(line_2, (240,600))
        sound = pygame.mixer.Sound("resources/game_over_sound.mp3")
        pygame.mixer.music.pause()
        pygame.mixer.Sound.play(sound)
        pygame.display.flip()
 

    def run(self):
        self.play_background_music()
        pause = False 
        running =  True 
        game_over = False
        FPS = 60
        clock = pygame.time.Clock()
        DIRECTION = ""
        while running: 
            if len(self.enemies) == 0:
                if self.player.live != 0:
                    level_up = pygame.mixer.Sound("resources/level_up_effect.mp3")
                    self.player.new_live()
                    self.level += 1
                    if self.level > 1:
                        pygame.mixer.Sound.play(level_up)
                    self.wave_length += 5
                for i in range(self.wave_length - self.level):
                    DIRECTION = random.choice(["vertical" , "left","right"])
                    if DIRECTION == "vertical":
                        self.enemy = Enemy(random.randrange(50, 950), random.randrange(-1500, -100, 50) , random.choice(["spider" , "shipv1" ]),self.surface , DIRECTION)
                        self.enemies.append(self.enemy)
                    elif DIRECTION == "left":
                        self.enemy = Enemy(random.randrange(1100, 2500 , 50), random.randrange(450, 600 , 50) , random.choice(["spider" , "shipv1" ]),self.surface, DIRECTION)
                        self.enemies.append(self.enemy)
                    elif DIRECTION == "right":
                        self.enemy = Enemy(random.randrange(-1500, -100, 50), random.randrange(200, 400 , 50) , random.choice(["spider" , "shipv1" ]),self.surface, DIRECTION)
                        self.enemies.append(self.enemy)

                # Append Big Enemy Ship
                for i in range(self.level):
                    DIRECTION = random.choice(["vertical" , "left","right"])
                    if DIRECTION == "vertical":
                        self.enemy = Enemy(random.randrange(50, 950) , random.randrange(-1500, -100 , 75), "shipv2", self.surface, DIRECTION)
                        self.enemies.append(self.enemy)
                    elif DIRECTION == "left":
                        self.enemy = Enemy(random.randrange(1100, 2500, 75), random.randrange(450, 550 ) , "shipv2" ,self.surface, DIRECTION)
                        self.enemies.append(self.enemy)
                    elif DIRECTION == "right":
                        self.enemy = Enemy(random.randrange(-1500, -100, 75), random.randrange(200, 400 ) , "shipv2" ,self.surface, DIRECTION)
                        self.enemies.append(self.enemy)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if game_over:
                        if event.key == K_RETURN:
                            main()
                    if event.key == K_p :
                        if pause == False:
                            pause = True
                            self.pause("pause")
                        elif pause == True:
                            pause = False
                            self.pause("resume")


            if not pause:
                if pygame.key.get_pressed()[K_w]:
                    self.player.moveUp()
                if pygame.key.get_pressed()[K_s]:
                    self.player.moveDown()
                if pygame.key.get_pressed()[K_d]:
                    self.player.moveRight()
                if pygame.key.get_pressed()[K_a]:
                    self.player.moveLeft()
                if pygame.key.get_pressed()[K_SPACE]:
                    self.player.shoot()
                
            try:
                if not pause:   
                    self.play()
            except Exception as e:
                    self.show_game_over()
                    pause = True 
                    game_over = True

            if not pause:
                for self.enemy in self.enemies[:]:
                    self.enemy.move(self.level)
                    self.enemy.move_laser(5,self.player)


                    if self.enemy.x < window_x + 75 and self.enemy.x > 0:
                        if self.enemy.y < window_y + 75 and self.enemy.y > 0:
                            if self.level < 10:
                                if random.randrange(0, 3*60) == 1:
                                    self.enemy.shoot()
                                    laser_sound = pygame.mixer.Sound("resources/enemy_laser.mp3")
                                    pygame.mixer.Sound.play(laser_sound)
                            else:
                                if random.randrange(0, 2*60) == 1:
                                    self.enemy.shoot()
                                    pygame.mixer.Sound.play(laser_sound)

                    if collide(self.enemy , self.player):
                        sound = pygame.mixer.Sound("resources/get_hit_sound_effect.mp3")
                        pygame.mixer.Sound.play(sound)
                        if self.enemy.type == 'shipv1' or  self.enemy.type == 'spider':
                            self.player.live -= 1
                            self.enemies.remove(self.enemy)
                        else:
                            self.player.live -= 2
                            self.enemies.remove(self.enemy)

                    if self.enemy.direction == "vertical":
                        if self.enemy.y > window_y:
                            temp = self.enemy.type
                            if temp == "shipv2" or temp == "shipv1":
                                health_temp = self.enemy.live

                            self.enemies.remove(self.enemy)
                            if temp == "shipv2":
                                self.enemy = Enemy(random.randrange(50, 950) , random.randrange(-1150, -100 , 75), "shipv2", self.surface, "vertical")
                                self.enemy.live = health_temp
                                self.enemies.append(self.enemy)
                            elif temp == "spider":
                                self.enemy = Enemy(random.randrange(50, 950), random.randrange(-1150, -100 , 100 ) , "spider" ,self.surface, "vertical")
                                self.enemies.append(self.enemy)
                            elif temp == "shipv1":
                                self.enemy = Enemy(random.randrange(50, 950), random.randrange(-1150, -100, 100) , "shipv1" ,self.surface, "vertical")
                                self.enemies.append(self.enemy)
                                self.enemy.live = health_temp

                    elif self.enemy.direction == "left":
                        if self.enemy.x < 0 - 75 :
                            temp = self.enemy.type
                            if temp == "shipv2" or temp == "shipv1":
                                health_temp = self.enemy.live
                            self.enemies.remove(self.enemy)
                            if temp == "shipv2":
                                self.enemy = Enemy(random.randrange(1100, 2500 , 75), random.randrange(450, 600, 50 ) , "shipv2" ,self.surface, "left")
                                self.enemy.live = health_temp
                                self.enemies.append(self.enemy)
                            elif temp == "spider":
                                self.enemy = Enemy(random.randrange(1100, 2500, 100), random.randrange(450, 600 , 50) , "spider" ,self.surface, "left")
                                self.enemies.append(self.enemy)
                            elif temp == "shipv1":
                                self.enemy = Enemy(random.randrange(1100, 2500, 100), random.randrange(450, 600 , 50) , "shipv1" ,self.surface, "left")
                                self.enemies.append(self.enemy)
                                self.enemy.live = health_temp
                    
                    elif self.enemy.direction == "right":
                        if self.enemy. x > window_x + 75:
                            temp = self.enemy.type
                            if temp == "shipv2" or temp == "shipv1":
                                health_temp = self.enemy.live
                            self.enemies.remove(self.enemy)

                            if temp == "shipv2":
                                self.enemy = Enemy(random.randrange(-1500, -100, 75), random.randrange(200, 400 , 50 ) , "shipv2" ,self.surface, "right")
                                self.enemy.live = health_temp
                                self.enemies.append(self.enemy)
                            elif temp == "spider":
                                self.enemy = Enemy(random.randrange(-1500, -100, 100), random.randrange(200, 400 , 50 ) , "spider" ,self.surface, "right")
                                self.enemies.append(self.enemy)
                            elif temp == "shipv1":
                                self.enemy = Enemy(random.randrange(-1500, -100, 100), random.randrange(200, 400, 50) , "shipv1" ,self.surface, "right")
                                self.enemies.append(self.enemy)
                                self.enemy.live = health_temp

            
            self.player.level_up(self.level) 

            self.player.move_laser(-8,self.enemies)

            clock.tick(FPS)

        pygame.quit()
        quit()

    def main_menu(self):
        run = True

        while run:
            self.surface.blit(BG , (0,0))
           
            MOUSE_POSITION = pygame.mouse.get_pos()
            main_menu = pygame.font.SysFont("Arial" , 110, bold  = True)
            menu_font = pygame.font.SysFont("Arial" , 50, bold  = True)

            MENU_TEXT = main_menu.render("MAIN MENU" , True, (227, 93, 16) )
            MENU_RECT = MENU_TEXT.get_rect(center=(500, 100))
            PLAY_BUTTON = Button(image = RECT, pos=(500, 250), 
                                text_input="PLAY", font = menu_font, base_color=(18, 119, 201), hovering_color="White")

            INSTRUCTION_BUTTON = Button(image = RECT, pos=(500, 400), 
                                text_input="INSTRUCTIONS", font = menu_font, base_color=(18, 119, 201), hovering_color="White")

            CREDIT_BUTTON =  Button(image = RECT, pos=(500, 550), 
                                text_input="CREDITS", font = menu_font, base_color=(18, 119, 201), hovering_color="White")

            QUIT_BUTTON = Button(image = RECT, pos=(500, 700), 
                                text_input="QUIT", font = menu_font, base_color=(18, 119, 201), hovering_color="White")

            self.surface.blit(MENU_TEXT , MENU_RECT)

            for button in [PLAY_BUTTON, INSTRUCTION_BUTTON, CREDIT_BUTTON,QUIT_BUTTON]:
                button.changeColor(MOUSE_POSITION)
                button.update(self.surface)
            
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MOUSE_POSITION):
                        pygame.mixer.music.stop()
                        self.run()
                    if INSTRUCTION_BUTTON.checkForInput(MOUSE_POSITION):
                        self.instruction()
                    if CREDIT_BUTTON.checkForInput(MOUSE_POSITION):
                        self.credit()
                    if QUIT_BUTTON.checkForInput(MOUSE_POSITION):
                        run = False

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        run = False

            pygame.display.flip()

        pygame.quit()
        quit()

# Check for collision
def collide(obj1,obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask , (offset_x,offset_y)) != None 

    
def main():
    game = Game()
    game.main_menu()
    

if __name__ == "__main__":
    main()