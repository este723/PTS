import os
import random
import math
from time import *
import pygame
from os import listdir
from os.path import isfile, join
pygame.init()
#toutes les importations 


pygame.display.set_caption("Platformer") #inithialisation des variables 

WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 5
blk = "bloc"
ItsRetry = 0

window = pygame.display.set_mode((WIDTH, HEIGHT))
heart = pygame.transform.scale(pygame.image.load(join("assets","heart.png")),(30,30))
BlScreen = pygame.image.load(join("assets","noir.png"))
WinScreen = pygame.image.load(join("assets","WinScreen.png"))

# class et fonction ##############################################################

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]



def load_sprite_sheets(dir1, dir2, width, height, direction=False): # charger les ressource visuel
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites


def get_block(size,end=False): # gestion ressource visuel sol
    if end : path = join("assets", "Terrain", "fin.png")
    else : path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)


class Player(pygame.sprite.Sprite):#joueur 
    COLOR = (255, 0, 0)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("MainCharacters", "MaskDude", 32, 32, True)
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.hp = 5
        self.hit_process = True
        self.mask = None
        self.direction = "right"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0

    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        self.hit = True

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
            if self.hit_process :
                self.hit_process = False
                self.hp = self.hp -1
                global dead
                if self.hp <= 0 :
                    
                    dead = True

        if self.hit_count > fps * 1 :
            self.hit = False
            self.hit_process = True
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def update_sprite(self): # gestion de l'annimation
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x): 
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))
        for N in range(10) :
                if self.hp > N :  win.blit(heart, (20*(N+1) , 30))



class Object(pygame.sprite.Sprite): # gestion des élement "non joueur"
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Block(Object): # block simple
    def __init__(self, x, y, size, end=False):
        super().__init__(x, y, size, size)
        block = get_block(size,end)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)


class Fire(Object): # piège simple 
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")
        self.fire = load_sprite_sheets("Traps", "Fire", width, height)
        self.image = self.fire["on"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "on"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0


def get_background(name): #generation du fond 
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image


def draw(window, background, bg_image, player, objects, offset_x): #fonction d'affichage 
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x)
    
    pygame.display.update()


def handle_vertical_collision(player, objects, dy): #collision verticale 
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects


def collide(player, objects, dx): #collision
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()
    return collided_object


def handle_move(player, objects):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)

    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]

    for obj in to_check:
        if obj and obj.name == "fire":
            player.make_hit()

######### JEU ################################################################


def main(window): 
    # initialisation (map et timer et +)
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")
    MODIF = 0
    TEMP = time()
    BS = 96
    global retry, ItsRetry,dead,feu
    player = Player(-1200+MODIF, 100, 50, 50)
    fire = Fire(100, HEIGHT - BS - 64, 16, 32)
    map = [Block(i * BS, HEIGHT - BS, BS) for i in range((-WIDTH // BS)-5, (-WIDTH // BS)+3)]+[Block(i * BS, HEIGHT - BS, BS) for i in range(2, 4)]
    feu = []
    
    objects = [*map]

    def MapAdd(map:list,obj,cordo) :

        if len(cordo) > 2 :
            if obj == blk :
                map.append( Block(cordo[0]*BS,HEIGHT - cordo[1]*BS, BS,True))
            else : 
                feu.append(Fire((cordo[0])*BS+BS/2-16, HEIGHT - cordo[1]*BS-64, 16, 32))
        else :
        
            if obj == blk :
                map.append( Block(cordo[0]*BS,HEIGHT - cordo[1]*BS, BS))
            else : 
                feu.append(Fire((cordo[0])*BS+BS/2-16, HEIGHT - cordo[1]*BS-64, 16, 32))
            
        return(objects)
    
    objBLK = [(-9,2),(-7,3),(-7,4),(-4,1),(-3,3),(-1,3),(5,3),(7,5),(9,1),(12,1),(14,1),(16,1),(17,2),(18,3),(19,4),(20,5),(21,6),(26,1),(30,1),(34,1,1)]
    for cordo in objBLK :
        objects = MapAdd(objects,blk,cordo)

    objFEU = [(-8,1),(-1,5),(-3,5),(0,3),(2,1),(8,6),(9,5),(9,4),(9,3),(13,1),(13,2),(15,1),(15,2),(26,2)]
    for cordo in objFEU :
        objects = MapAdd(objects,"feu",cordo)

    objects= objects + feu
    
    offset_x = -1700+MODIF
    scroll_area_width = 400
    
    retry = False
    dead = False

    run = True
    while run: #lancement du Jeu
        clock.tick(FPS)        
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT  :
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()

        player.loop(FPS)
        fire.loop()
        handle_move(player, objects)
        draw(window, background, bg_image, player, objects, offset_x)

        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel


        if dead or offset_x >= 2700 or player.rect.y > 840  : #menu win / death 
            if  dead or player.rect.y > 840:   window.blit(BlScreen, (0 , 0))
            else : window.blit(WinScreen, (0 , 0))


            font=pygame.font.Font(None, 40)
            text = font.render(str(time()-TEMP).split(".")[0]+"s "+str(time()-TEMP).split(".")[1][:2],1,(255,255,255))

            window.blit(text, (440, 200))         

            pygame.display.update()
            while run : # attendre que le joueur quitte ou relance une partie 
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.pos[0] > 395 and event.pos[0] < 570 and event.pos[1] >666 and event.pos[1] <696 : 
                            retry = True
                            ItsRetry = 1
                            run = False
                            break
                    if event.type == pygame.QUIT  :
                            run = False
                            break

            break

            

    
 

retry = False
if __name__ == "__main__": #lancer le jeu 
    main(window)

    while retry : main(window)
