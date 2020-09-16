import pygame, sys

from pygame import *
pygame.init()
clock = pygame.time.Clock()
RESOLUTION = (1280, 720)
display = pygame.Surface((304, 190))
pygame.display.set_caption("The most frustrating game ever")
screen = pygame.display.set_mode(RESOLUTION, 0, 32)
dirt = pygame.image.load('data/image/dirt_no_grass.png')
grass = pygame.image.load('data/image/dirt.png')
water = pygame.image.load('data/image/water.png')
water_top = pygame.image.load('data/image/water_top.png')
player_img = pygame.image.load('data/image/frog_man.png')
portal = [pygame.image.load('data/image/portal_1.png'), pygame.image.load('data/image/portal_2.png'),
          pygame.image.load('data/image/portal_3.png'), pygame.image.load('data/image/portal_4.png'),
          pygame.image.load('data/image/portal_5.png')]
lava = pygame.image.load('data/image/lava.png')
chest_open = False
true_scroll = [0, 0]
win_text = pygame.font.SysFont('arial', 16)
text = win_text.render('YOU WIN!', True, (255, 0, 0))
textRect = text.get_rect()
textRect.center = (300 // 2, 50)
level = 1
jump_pen = True
die = False
win = False
portal_tick = 20
portal_img = 0
tick = 0



def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map_1 = []
    for row_1 in data:
        game_map_1.append(list(row_1))
    return game_map_1


class Player:
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.jump = False
        self.use = False
        self.movement = [0, 0]
        self.img = image
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


player = Player(32, 32, player_img.get_width(), player_img.get_height(), player_img)


def check_collision(rect, block_list):
    collision_list = []
    for block in block_list:
        if rect.colliderect(block):
            collision_list.append(block)
    return collision_list


def check_chest(rect, portal_list):
    portal = []
    for block in portal_list:
        if rect.colliderect(block):
            portal.append(block)
    return portal


def move(rect, block_list, player, portal_list, lava_list):
    global chest_open, level, game_map, die, win
    collision_type = {'left': False, 'right': False, 'bottom': False, 'top': False}
    player.rect.x += player.movement[0]
    hit_list = check_collision(rect, block_list)
    for block in hit_list:
        if player.movement[0] > 0:
            rect.right = block.left
        if player.movement[0] < 0:
            rect.left = block.right
    player.rect.y += int(player.movement[1])
    hit_list = check_collision(rect, block_list)
    for block in hit_list:
        if player.movement[1] > 0:
            rect.bottom = block.top
            collision_type['bottom'] = True
        if player.movement[1] < 0:
            rect.top = block.bottom
            collision_type['top'] = True
    hit_chest = check_chest(rect, portal_list)
    for chest in hit_chest:
        if not chest_open:
            if player.use:
                level += 1
                if level == 1:
                    game_map = map_1
                if level == 2:
                    game_map = map_2
                if level == 3:
                    win = True
    hit_lava = check_collision(rect, lava_list)
    if len(hit_lava) != 0:
        die = True
    return collision_type


map_1 = load_map('data/map/map')
map_2 = load_map('data/map/map_1')
game_map = map_1

while True:
    display.fill((0, 255, 255))
    true_scroll[0] += (player.rect.x - true_scroll[0] - 155)/2
    true_scroll[1] += (player.rect.y - true_scroll[1] - 90)/2
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])
    tiles = []
    portal_list = []
    lava_list = []
    water_list = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(grass, (x * 16 - scroll[0], y * 16 - scroll[1]))
            if tile == '2':
                display.blit(dirt, (x * 16 - scroll[0], y * 16 - scroll[1]))
            if tile == '3':
                display.blit(water, (x * 16 - scroll[0], y * 16 - scroll[1]))
            if tile == '4':
                display.blit(water_top, (x * 16 - scroll[0], y * 16 - scroll[1]))
            if tile == '5':
                tick += 1
                if tick == portal_tick:
                    portal_img += 1
                    tick = 0
                if portal_img == len(portal):
                    portal_img = 0
                display.blit(portal[portal_img], (x * 16 - scroll[0], y * 16 - scroll[1]))
            if tile == "6":
                display.blit(lava, (x * 16 - scroll[0], y * 16 - scroll[1]))
            if tile == '1' or tile == '2':
                tiles.append(pygame.Rect(x * 16, y * 16, 16, 16))
            if tile == '5':
                portal_list.append(pygame.Rect(x * 16, y * 16, 32, 16))
            if tile == '6':
                lava_list.append(pygame.Rect(x * 16, y * 16, 16, 16))
            x += 1
        y += 1
    if die:
        if game_map == map_1:
            player.rect.x = 16
            player.rect.y = 16
        if game_map == map_2:
            player.rect.x = 25 * 16
            player.rect.y = 16
        die = False
    player.rect = pygame.Rect(player.rect.x, player.rect.y, player.rect.width, player.rect.height)
    display.blit(player.img, (player.rect.x - scroll[0], player.rect.y - scroll[1]))
    collision = move(player.rect, tiles, player, portal_list, lava_list)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not jump_pen:
        player.jump = True
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                player.left = True
            if event.key == K_RIGHT:
                player.right = True
            if event.key == K_e:
                player.use = True
        if event.type == KEYUP:
            if event.key == K_LEFT:
                player.left = False
            if event.key == K_RIGHT:
                player.right = False
            if event.key == K_e:
                player.use = False

    if player.jump:
        player.movement[1] = -5
        player.jump = False
        jump_pen = True
    if player.right and not player.left:
        player.movement[0] = 2
    if player.left and not player.right:
        player.movement[0] = -2
    if not player.right and not player.left:
        player.movement[0] = 0
    if player.right and player.left:
        player.movement[0] = 0
    if not collision['bottom']:
        player.movement[1] += 0.15
        jump_pen = True
    else:
        jump_pen = False
        player.movement[1] = 0
    if collision['top']:
        player.movement[1] = 0.2
    if win:
        display.blit(text, textRect)
    screen.blit(pygame.transform.scale(display, RESOLUTION), (0, 0))
    pygame.display.update()
    clock.tick(60)
