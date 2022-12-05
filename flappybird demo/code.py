# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This test will initialize the display using displayio and draw a solid green
background, a smaller purple rectangle, and some yellow text.
"""

import board
import digitalio
import terminalio
import displayio
from adafruit_display_text import label
from adafruit_ssd1351 import SSD1351
import time
import random

# Release any resources currently in use for the displays
displayio.release_displays()

# ------------------hardware setup------------------
spi = board.SPI()
tft_cs = board.D2
tft_dc = board.D0

display_bus = displayio.FourWire(
    spi, command=tft_dc, chip_select=tft_cs, reset=board.D1, baudrate=16000000
)

display = SSD1351(display_bus, width=128, height=96)

control = digitalio.DigitalInOut(board.BUTTON)
control.direction = digitalio.Direction.INPUT


# --------------------background---------------------
bg = displayio.Group()
display.show(bg)

bg_bitmap = displayio.Bitmap(128, 96, 1)
bg_palette = displayio.Palette(1)
bg_palette[0] = 0x77FFFF
bg_sprite = displayio.TileGrid(bg_bitmap, pixel_shader=bg_palette, x=0, y=0)
bg.append(bg_sprite)

# -----------------------pillar----------------------
# ---------------------parameters--------------------
pillar_x = 128
pillar_x_2 = 202
space_height = random.randint(24,35)
space_y = random.randint(8,96-space_height)
space_height_2 = random.randint(24,35)
space_y_2 = random.randint(8,96-space_height)
# ----------------------drawing----------------------
pillar_bitmap = displayio.Bitmap(20, 96, 1)
pillar_palette = displayio.Palette(1)
pillar_palette[0] = 0x00FF00  # Bright Green
pillar_sprite = displayio.TileGrid(pillar_bitmap, pixel_shader=pillar_palette, x=pillar_x, y=0)
bg.append(pillar_sprite)

space_bitmap = displayio.Bitmap(20, space_height, 1)
space_sprite = displayio.TileGrid(space_bitmap, pixel_shader=bg_palette, x=pillar_x, y=space_y)
bg.append(space_sprite)

pillar_sprite_2 = displayio.TileGrid(pillar_bitmap, pixel_shader=pillar_palette, x=pillar_x_2, y=0)
bg.append(pillar_sprite_2)

space_bitmap = displayio.Bitmap(20, space_height_2, 1)
space_sprite_2 = displayio.TileGrid(space_bitmap, pixel_shader=bg_palette, x=pillar_x_2, y=space_y_2)
bg.append(space_sprite_2)
# ----------------------function---------------------
def draw_pillar(number, xp, yp, hp):
    global bg
    bg[number*2-1] = displayio.TileGrid(pillar_bitmap, pixel_shader=pillar_palette, x=xp, y=0)
    space_bitmap = displayio.Bitmap(20, hp, 1)
    bg[number*2] = displayio.TileGrid(space_bitmap, pixel_shader=bg_palette, x=xp, y=yp)

# -----------------------bird------------------------
# ---------------------parameters--------------------
bird_y = 80
# ----------------------drawing----------------------
bird_bitmap = displayio.Bitmap(4,4,1)
bird_palette = displayio.Palette(1)
bird_palette[0] = 0xFF77FF
bird_sprite = displayio.TileGrid(bird_bitmap, pixel_shader=bird_palette, x=20, y=bird_y)
bg.append(bird_sprite)
# ----------------------function---------------------
def draw_bird(yb):
    global bg    
    bg[5] = displayio.TileGrid(bird_bitmap, pixel_shader=bird_palette, x=20, y=yb)

# -----------------------score-----------------------
text = "0"
text_area = label.Label(terminalio.FONT, text=text, color=0x000000, x=10, y=10)
bg.append(text_area)
def draw_score(score):
    global bg
    text = str(score)
    bg[6] = label.Label(terminalio.FONT, text=text, color=0x000000, x=10, y=10)


# ----------------------gameover---------------------
def gameover():
    global bg,restart
    text = "Game Over!"
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=30, y=64)
    bg.append(text_area)
    time.sleep(2)
    while control.value:
        time.sleep(0.1)
    bg.pop(7)
    restart = True

# -------------------loop parameters-----------------
movingrate = 1      # scrolling per loop
fallrateint = 0     # int drop per loop
fallrate = 0        # float drop per loop
pressed = False     # flag for input button
restart = False     # flag for restart game
score = 0           # score
score_added = False



while True:
    pillar_x -= movingrate
    pillar_x_2 -= movingrate
    draw_pillar(number=1, xp=pillar_x, yp=space_y, hp=space_height)
    draw_pillar(number=2, xp=pillar_x_2, yp=space_y_2, hp=space_height_2)

    # bird position changing with a certain acceleration
    bird_y = bird_y + fallrateint
    fallrate = fallrate + 0.6
    fallrateint = int(fallrate)

    if ((pillar_x < 0) or (pillar_x_2 < 0)) and (not score_added):
        score_added = True
        score += 1
        draw_score(score=score)
    elif ((pillar_x > 120) or (pillar_x_2 > 120)) and score_added:
        score_added = False
    
    # check survive before drawing the bird
    if bird_y >= 96:
        gameover()
    if (pillar_x <=21) and (pillar_x > 0) and (bird_y <= space_y):
        gameover()
    if (pillar_x <=21) and (pillar_x > 0) and (bird_y+4 >= (space_y + space_height)):
        gameover()

    if bird_y >= 96:
        gameover()
    if (pillar_x_2 <=21) and (pillar_x_2 > 0) and (bird_y <= space_y_2):
        gameover()
    if (pillar_x_2 <=21) and (pillar_x_2 > 0) and (bird_y+2 >= (space_y_2 + space_height_2)):
        gameover()
    # counting score
    
    if restart == True:
        pillar_x = -30
        pillar_x_2 = 202
        bird_y = 80
        score = 0
        restart = False
        draw_score(score=score)

    draw_bird(yb=bird_y)
    print (control.value)

    # Contorl the bird, only tap is valid
    if (not control.value) and (not pressed):
        fallrate = -5
        pressed = True
    elif control.value and pressed:
        pressed = False

    # when one pillar disappear, generate another random one
    if pillar_x <= -20:
        space_height = random.randint(24,35)
        space_y = random.randint(5,96-space_height)
        pillar_x = 128
    if pillar_x_2 <= -20:
        space_height_2 = random.randint(24,35)
        space_y_2 = random.randint(5,96-space_height)
        pillar_x_2 = 128
    # loop rate
    time.sleep(0.013)
