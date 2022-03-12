import pygame
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_SPACE, K_LSHIFT, K_RSHIFT
from time import sleep
from classes import Wkey, Bkey, HEIGHT, WIDTH, H_KB, W_KEY, H_BKEY, W_BKEY, WKEYS, BKEYS

pygame.init()
pygame.display.set_caption("13ET Piano")
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
screen.fill((36, 36, 36))
myfont = pygame.font.SysFont('arial', HEIGHT // 26)
notes = [pygame.mixer.Sound(f'notes/{i}-1.ogg') for i in range(14)] + \
        [pygame.mixer.Sound(f'notes/{i}.ogg') for i in range(14)]
[note.set_volume(0.4) for note in notes]
# SET PIANO
keys_dict = {}
i = 0
for n, ltr in enumerate(WKEYS):
    if n in (1, 2, 4, 6, 7, 10, 11, 13, 15, 16):
        i += 1
    k = Wkey()
    k.note = notes[i]
    k.letter = myfont.render(ltr.upper(), True, (0, 0, 0))
    keys_dict[ltr] = k
    i += 1
    if n < 9:
        k.pos = (n * W_KEY + 2, 2)
        k.lpos = ((n + 0.382) * W_KEY, H_KB - W_KEY * 0.382)
    else:
        k.pos = ((n - 9) * W_KEY + 2, H_KB + 2)
        k.lpos = ((n - 9 + 0.382) * W_KEY, 2 * H_KB - W_KEY * 0.382)
i = m = 1
for n, ltr in enumerate(BKEYS):
    if n in (2, 3, 7, 8):
        i += 1
        m += 1
    if n == 5:
        i += 2
    k = Bkey()
    k.note = notes[i]
    k.letter = myfont.render(ltr.upper(), True, (255, 255, 255))
    keys_dict[ltr] = k
    i += 2
    if n < 5:
        k.pos = (m * W_KEY - W_BKEY // 2, 2)
        k.lpos = ((m + 0.236) * W_KEY - W_BKEY // 2, H_BKEY - W_KEY * 0.382)
    else:
        k.pos = (W_KEY - W_BKEY // 2 + (m - 8) * W_KEY, H_KB + 2)
        k.lpos = (W_KEY - W_BKEY // 2 + (m - 8 + 0.236) * W_KEY, H_BKEY + H_KB - W_KEY * 0.382)
    m += 1


# DRAW PIANO
def draw_piano():
    for key in keys_dict.values():
        screen.blit(key.surf, key.pos)
        key.rect = key.surf.get_rect(topleft=key.pos)
        screen.blit(key.letter, key.lpos)
    pygame.display.flip()


w_keys = [key for key in keys_dict.values() if type(key).__name__ == 'Wkey']
b_keys = [key for key in keys_dict.values() if type(key).__name__ == 'Bkey']


draw_piano()
sustain = white = True
pygame.init()
while True:
    sleep(0.01)
    for event in pygame.event.get():
        btn = event.__dict__.get('unicode')
        if event.type == QUIT:
            pygame.quit()
            break

        if event.type == KEYDOWN:
            if event.key == K_SPACE or event.key == K_RSHIFT:
                sustain = False
            if event.key == K_LSHIFT:
                sustain = True
            key = keys_dict.get(btn)
            if key:
                key.key_down()
                draw_piano()
        if event.type == KEYUP:
            if event.key == K_SPACE:
                sustain = True
            key = keys_dict.get(btn)
            if key:
                key.key_up(sustain)
                draw_piano()

        if pygame.mouse.get_pressed()[0]:
            for key in b_keys:
                if key.rect.collidepoint(pygame.mouse.get_pos()) and not key.played:
                    white = False
                    key.key_down()
                    for k in w_keys:
                        k.key_up(sustain)
                    draw_piano()
                    break
                if not key.rect.collidepoint(pygame.mouse.get_pos()) and key.played:
                    white = True
                    key.key_up(sustain)
                    draw_piano()
                    break

            if white:
                for key in w_keys:
                    if key.rect.collidepoint(pygame.mouse.get_pos()) and not key.played:
                        key.key_down()
                        draw_piano()
                        break
                    if not key.rect.collidepoint(pygame.mouse.get_pos()) and key.played:
                        key.key_up(sustain)
                        draw_piano()
                        break

        if event.type == pygame.MOUSEBUTTONUP:
            white = True
            for key in keys_dict.values().__reversed__():
                key.key_up(sustain)
                draw_piano()
