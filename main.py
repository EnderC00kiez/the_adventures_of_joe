# create graphics window
# import pygame
from email.errors import InvalidMultipartContentTransferEncodingDefect
import pygame
from pygame.locals import *
from sys import exit
import time
import random
import savelib

current_charimg_rot = "default"

try:
    import pyi_splash

    if pyi_splash.is_alive():
        pyi_splash.update_text("Welcome to... The Adventures of Joe!")
except ImportError:
    pass

blacklisted_colors = ["#121212", "#054d05", "#64b5f6"]
# sounds = ["Bridge.mp3"]
sounds = ["Bridge.mp3", "plains.wav"]
bgname = "plains"


def plains(background):
    bgname = "plains"
    sounds = ["Bridge.mp3"]
    blacklisted_colors = ["#121212", "#054d05", "#64b5f6"]
    # remove character
    screen.blit(background, (0, 0))
    # clear old background
    background.fill((0, 0, 0, 0))
    # set background to desert.png
    bgobj = pygame.transform.scale(pygame.image.load("assets/plains.png"), (800, 600))
    background = bgobj
    character = pygame.image.load("assets/character.png")
    # load the character's sprite at 0,0
    character_x = 0
    character_y = 0
    # create the character sprite
    character_sprite = pygame.sprite.Sprite()
    character_sprite.image = character
    character_sprite.rect = character_sprite.image.get_rect()
    character_sprite.rect.x = character_x
    character_sprite.rect.y = character_y
    # draw background
    screen.blit(background, (0, 0))
    # draw character
    screen.blit(
        character_sprite.image, (character_sprite.rect.x, character_sprite.rect.y)
    )
    # update screen
    pygame.display.update()
    # create a character
    character = pygame.image.load("assets/character.png")
    # create a background


can_move = True

# create the window
pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(1)
# set window size to big enough to hold the whole map
screen = pygame.display.set_mode((800, 600), 0, 32)
# set window title
pygame.display.set_caption("The Adventures of Joe")
# set window icon
icon = pygame.image.load("assets/icon.png")
pygame.display.set_icon(icon)
# create a character
character = pygame.image.load("assets/character.png")
# create a background
# load the character's sprite at 0,0
character_x = 0
character_y = 0
# create the character sprite
character_sprite = pygame.sprite.Sprite()
character_sprite.image = character
character_sprite.rect = character_sprite.image.get_rect()
character_sprite.rect.x = character_x
character_sprite.rect.y = character_y

# create a clock
clock = pygame.time.Clock()
# create a timer
timer = pygame.time.get_ticks()
# make background not black empty void
background = pygame.Surface(screen.get_size())
background = background.convert()
bgobj = pygame.transform.scale(pygame.image.load("assets/background.png"), (800, 600))
# set background to background.png
background = bgobj
screen.blit(background, (0, 0))
pygame.display.update()
# render character over background
screen.blit(character_sprite.image, (character_sprite.rect.x, character_sprite.rect.y))
pygame.display.update()


def find_hex(x, y, cannot_step_on):
    try:
        # get pos of feet
        x = int(x + (character_sprite.rect.width / 2))
        y = int(y + (character_sprite.rect.height / 2))
        # cannot_step_on is a list of tuples containing rgb values
        value = background.get_at((x, y))
        # convert rgb to hex
        hex_value = "#{:02x}{:02x}{:02x}".format(value[0], value[1], value[2])
        # check if hex value is in the list of blacklisted colors
        if hex_value in cannot_step_on:
            return False
        else:
            return True
    except IndexError:
        pass


# create custom background class
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location



def draw_text(text, font, surface, x, y):
    textobj = font.render(text, 1, (0, 0, 0))
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
    pygame.display.update()


# create a function to move the player, supporting custom backgrounds
def move_player(background, x, y, direction):
    global current_charimg_rot
    if direction == "up":
        if find_hex(x, y - 5, blacklisted_colors):
            if not current_charimg_rot == "up":
                # change image to character.png
                character = pygame.image.load("assets/character_back.png")
                # set character image
                character_sprite.image = character
                current_charimg_rot = "up"
            character_sprite.rect.y -= 5
            screen.blit(background, (0, 0))
            screen.blit(
                character_sprite.image,
                (character_sprite.rect.x, character_sprite.rect.y),
            )
            pygame.display.update()
    elif direction == "down":
        if find_hex(x, y + 5, blacklisted_colors):
            if not current_charimg_rot == "default":
                # change image to character.png
                character = pygame.image.load("assets/character.png")
                # set character image
                character_sprite.image = character
                current_charimg_rot = "default"
            character_sprite.rect.y += 5
            screen.blit(background, (0, 0))
            screen.blit(
                character_sprite.image,
                (character_sprite.rect.x, character_sprite.rect.y),
            )
            pygame.display.update()
    elif direction == "left":
        if find_hex(x - 5, y, blacklisted_colors):
            if not current_charimg_rot == "left":
                # change image to character.png
                character = pygame.image.load("assets/character_left.png")
                # set character image
                character_sprite.image = character
                current_charimg_rot = "left"
            character_sprite.rect.x -= 5
            screen.blit(background, (0, 0))
            screen.blit(
                character_sprite.image,
                (character_sprite.rect.x, character_sprite.rect.y),
            )
            pygame.display.update()
    elif direction == "right":
        if find_hex(x + 5, y, blacklisted_colors):
            if not current_charimg_rot == "right":
                # change image to character.png
                character = pygame.image.load("assets/character_right.png")
                # set character image
                character_sprite.image = character
                current_charimg_rot = "right"
            character_sprite.rect.x += 5
            screen.blit(background, (0, 0))
            screen.blit(
                character_sprite.image,
                (character_sprite.rect.x, character_sprite.rect.y),
            )
            pygame.display.update()
    else:
        raise InvalidMultipartContentTransferEncodingDefect("Invalid direction")


def die(text, background):
    # create a new layer with transparent red
    background.fill((255, 0, 0, 100))
    screen.blit(background, (0, 0))
    # draw text
    draw_text(
        text + " Press ESC to exit.", pygame.font.Font(None, 32), screen, 100, 100
    )
    pygame.display.flip()
    # destroy joe's legs
    character_sprite.image = pygame.image.load("assets/dead.png")
    screen.blit(
        character_sprite.image, (character_sprite.rect.x, character_sprite.rect.y)
    )
    pygame.display.update()
    # wait 5 seconds
    time.sleep(5)
    # remove red tint
    # but dont remove background
    background.fill((0, 0, 0, 0))
    # set background to background.png
    background = pygame.transform.scale(
        pygame.image.load("assets/background.png"), (800, 600)
    )
    # draw background
    screen.blit(background, (0, 0))
    # fix character having duplicates after death
    character_sprite.image = pygame.image.load("assets/character.png")
    # fix character's position
    character_sprite.rect.x = 0
    character_sprite.rect.y = 0
    # REMOVE OLD DUPES
    # draw character
    screen.blit(
        character_sprite.image, (character_sprite.rect.x, character_sprite.rect.y)
    )
    # update screen
    pygame.display.update()


def randsoundgen(sounds):
    # use randint (2% chance of triggering)
    if random.randint(1, 10000) == 1:
        # use random.choice to pick a sound
        if pygame.mixer.get_busy() is False:
            soundObj = pygame.mixer.Sound("assets/" + random.choice(sounds))
            soundObj.play()


clock.tick(30)

# allow the player to move the character with WASD
while True:
    randsoundgen(sounds)
    # allow quit and fullscreen
    for event in pygame.event.get():
        pressed = pygame.key.get_pressed()
        if event.type == QUIT:
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()
            # if f11 is pressed, toggle fullscreen
            elif event.key == K_F11:
                draw_text(
                    "Sorry, fullscreen has not been implemented yet.",
                    pygame.font.Font(None, 30),
                    screen,
                    200,
                    300,
                )

            # if the player presses W, move the character up
        if pressed[pygame.K_w]:
            move_player(
                background, character_sprite.rect.x, character_sprite.rect.y, "up"
            )
            # if the player presses S, move the character down
        elif pressed[pygame.K_s]:
            move_player(
                background, character_sprite.rect.x, character_sprite.rect.y, "down"
            )
            # if the player presses A, move the character left
        elif pressed[pygame.K_a]:
            move_player(
                background, character_sprite.rect.x, character_sprite.rect.y, "left"
            )
            # if the player presses D, move the character right
        elif pressed[pygame.K_d]:
            move_player(
                background, character_sprite.rect.x, character_sprite.rect.y, "right"
            )
            """
            if event.key == K_F4:
                die("MANUALLY_TRIGGERED", background)
            elif event.key == K_SCROLLLOCK:
                print("WINDOW_CRASH")
                while True:
                    pass
            elif event.key == K_F12:
                Desert(background)"""
