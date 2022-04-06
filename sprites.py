import pygame
from settings import *


class Button(pygame.sprite.Sprite):
    def __init__(self, width, height, img):
        self.width = width
        self.height = height
        self.img = img
        self.surf = pygame.Surface((self.width, self.height))


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.surf.fill(BLACK)
        self.rect = self.surf.get_rect()
        self.rect.x = x
        self.rect.y = y


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.surf.fill(RED)
        self.rect = self.surf.get_rect()
        self.rect.x = x+1
        self.rect.y = y
        self.x_velo = 0
        self.y_velo = 0
        self.collide_rt = False
        self.collide_lt = False

        self.jumping = False
        self.falling = False
        # self.max_jump = 2*TILE_SIZE

    def update(self):
        self.get_keys()
        self.add_gravity()

        # move the updates below to collision detection in the Layout class
        # self.rect.x += self.x_velo
        # self.rect.y += self.y_velo

    def add_gravity(self):
        self.y_velo += 1

        if self.y_velo > 10:
            self.y_velo = 10

    def get_keys(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and not self.collide_lt:
            self.x_velo = -5
            self.collide_rt = False
        elif keys[pygame.K_RIGHT] and not self.collide_rt:
            self.x_velo = 5
            self.collide_lt = False
        else:
            self.x_velo = 0

        if keys[pygame.K_SPACE] and not self.jumping and not self.falling:
            self.jump()

    def jump(self):
        # if self.y_velo == 0:
        self.jumping = True
        self.y_velo = -20


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.surf.fill(GREEN)
        self.rect = self.surf.get_rect()
        self.rect.x = x
        self.rect.y = y


class Layout:
    def __init__(self):
        self.layout = None
        self.level = 1
        self.block_grp = pygame.sprite.Group()
        self.player_grp = pygame.sprite.GroupSingle()
        self.exit_grp = pygame.sprite.GroupSingle()
        self.all_sprites = pygame.sprite.Group()
        self.create_layout()

    def create_layout(self):
        self.layout = LEVELS[self.level-1]

        self.block_grp.empty()
        self.player_grp.empty()
        self.exit_grp.empty()
        self.all_sprites.empty()

        for row_index, rows in enumerate(self.layout):
            for col_index, column in enumerate(rows):

                x_pos = col_index * TILE_SIZE
                y_pos = row_index * TILE_SIZE

                if column == "1":
                    block = Block(x_pos, y_pos)
                    self.block_grp.add(block)
                    self.all_sprites.add(block)
                elif column == "P":
                    player = Player(x_pos, y_pos)
                    self.player_grp.add(player)
                    self.all_sprites.add(player)
                elif column == "E":
                    player = Exit(x_pos, y_pos)
                    self.exit_grp.add(player)
                    self.all_sprites.add(player)

    def update(self, display):

        for sprite in self.all_sprites.sprites():
            display.blit(sprite.surf, sprite.rect)

        self.vert_collide()
        self.horiz_collide()
        self.exit_collide()
        self.player_grp.update()
        self.exit_grp.update()

    def horiz_collide(self):
        # move the player horizontally, then check for collision
        player = self.player_grp.sprite
        player.rect.x += player.x_velo

        collide_list = pygame.sprite.spritecollide(
            player, self.block_grp, False)
        if collide_list:
            if player.x_velo < 0:
                player.rect.left = collide_list[0].rect.right
                player.collide_lt = True

            if player.x_velo > 0:
                player.rect.right = collide_list[0].rect.left
                player.collide_rt = True

            # player.y_velo = 0
            player.x_velo = 0
        else:
            player.collide_rt, player.collide_lt = False, False

    def vert_collide(self):
        # move the player vertically, then check for collision
        player = self.player_grp.sprite
        player.rect.y += player.y_velo

        collide_list = pygame.sprite.spritecollide(
            player, self.block_grp, False)

        if collide_list:
            # going up, check for collision with player top and platform bottom
            if player.y_velo < 0:
                player.rect.top = collide_list[0].rect.bottom
                player.y_velo = 0
                player.falling = True
                player.jumping = False

            # going down, check for collision with player bottom and platform top
            elif player.y_velo > 0:
                player.rect.bottom = collide_list[0].rect.top
                player.y_velo = 0
                player.jumping = False
                player.falling = False

    def exit_collide(self):

        player = self.player_grp.sprite
        player_exit = pygame.sprite.spritecollide(player, self.exit_grp, True)
        if player_exit and self.level < MAX_LEVELS:
            self.level += 1
            self.create_layout()
        elif player_exit and self.level == MAX_LEVELS:
            quit()


