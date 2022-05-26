import pygame
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_SPACE, K_LSHIFT, K_DOWN, K_UP
from time import sleep
from classes17 import Key, HEIGHT, WIDTH, H_KB, W_KEY, KEYS17

color = (36, 36, 36)
pygame.init()
pygame.display.set_caption("17ET Piano")
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
screen.fill(color)
font_size = HEIGHT // 26
myfont = pygame.font.SysFont('arial', font_size)
myfont2 = pygame.font.SysFont('mono', font_size, True)
notes = [pygame.mixer.Sound(f'notes17/{400 + i}.ogg') for i in range(18)] + \
        [pygame.mixer.Sound(f'notes17/{500 + i}.ogg') for i in range(18)]
volume = 4


def set_volume(vol):
    [note.set_volume(vol / 10) for note in notes]


set_volume(volume)
# SET PIANO
keys_dict = {}
y2 = H_KB + 2
yl1 = H_KB - W_KEY * 0.382
yl2 = H_KB + yl1
hb = W_KEY // 3
yadd = 0
for n, ltr in enumerate(KEYS17):
    i = n
    k = Key()
    k.note = notes[n]
    k.letter = myfont.render(ltr.upper(), True, (0, 0, 0))
    if n == 18:
        yadd = HEIGHT // 2
    if n >= 18:
        i -= 18
        k.up_color = (197, 197, 157)
    k.surf.fill(k.up_color)
    keys_dict[ltr] = k
    if n % 2:
        k.pos = ((i // 2 + 0.5) * W_KEY + 2, H_KB + 2 + yadd)
        k.lpos = ((i // 2 + 0.882) * W_KEY, yl2 + yadd)
    else:
        k.pos = ((i // 2) * W_KEY + 2, 2 + yadd)
        k.lpos = ((i // 2 + 0.382) * W_KEY, yl1 + yadd)

# DRAW PIANO
vol_clear = pygame.Surface((W_KEY // 2, H_KB))
vol_clear.fill(color)
text_xpos = WIDTH - hb
vol_ypos = hb // 2
sus_ypos = hb * 1.3


def draw_key(key):
    screen.blit(key.surf, key.pos)
    screen.blit(key.letter, key.lpos)
    pygame.display.flip()


def draw_text(s=False):
    screen.blit(vol_clear, (WIDTH - W_KEY // 2, 2))
    screen.blit(myfont2.render(f'{volume}', True, (255, 255, 255)), (text_xpos, vol_ypos))
    if s:
        screen.blit(myfont2.render('S', True, (255, 255, 255)), (text_xpos, sus_ypos))
    pygame.display.flip()


def draw_piano():
    for key in keys_dict.values():
        draw_key(key)
        key.rect = key.surf.get_rect(topleft=key.pos)
    draw_text()


draw_piano()

sustain = False
pygame.init()

while True:
    sleep(0.01)
    for event in pygame.event.get():
        btn = event.__dict__.get('unicode')
        if btn:
            btn = btn.lower()
        if event.type == QUIT:
            pygame.quit()
            break

        if event.type == KEYDOWN:
            if event.key == K_DOWN and volume:
                volume -= 1
                set_volume(volume)
                draw_text()
            if event.key == K_UP and volume < 10:
                volume += 1
                set_volume(volume)
                draw_text()
            if event.key == K_SPACE:
                sustain = True

            if event.key == K_LSHIFT:
                sustain = not sustain
            key = keys_dict.get(btn)
            if key:
                key.key_down()
                draw_key(key)
        if event.type == KEYUP:
            if event.key == K_SPACE:
                sustain = False
            key = keys_dict.get(btn)
            if key:
                key.key_up(sustain)
                draw_key(key)
        draw_text(sustain)

        if pygame.mouse.get_pressed()[0]:
            for key in keys_dict.values():
                if key.rect.collidepoint(pygame.mouse.get_pos()) and not key.played:
                    key.key_down()
                    draw_key(key)
                    break
                if not key.rect.collidepoint(pygame.mouse.get_pos()) and key.played:
                    key.key_up(sustain)
                    draw_key(key)
                    break

        if event.type == pygame.MOUSEBUTTONUP:
            for key in keys_dict.values().__reversed__():
                key.key_up(sustain)
                draw_key(key)
