import pygame
from random import randint

HEIGHT = 600
WIDTH = HEIGHT * 1.618
H_KB = HEIGHT // 2
W_KEY = WIDTH // 9
H_BKEY = H_KB // 1.618
W_BKEY = W_KEY // 1.618
WKEYS = 'qwertyuiozxcvbnm,.'
BKEYS = '23578sdgjk'


class Bkey(pygame.sprite.Sprite):
    def __init__(self):
        super(Bkey, self).__init__()
        self.surf = pygame.Surface((W_BKEY, H_BKEY))
        self.up_color = (0, 0, 0)
        self.down_color = (157, 0, 0)
        self.rect = None
        self.letter = None
        self.note = None
        self.pos = None
        self.lpos = None
        self.played = False
        self.sustain = True

    def key_up(self, sustain):
        self.played = False
        self.surf.fill(self.up_color)
        if not sustain:
            self.note.stop()

    def key_down(self):
        pygame.mixer.Channel(randint(0,7)).play(self.note)
        self.note.play()
        self.played = True
        self.surf.fill(self.down_color)


class Wkey(Bkey):
    def __init__(self):
        super(Wkey, self).__init__()
        self.surf = pygame.Surface((W_KEY - 4, H_KB - 4))
        self.up_color = (157, 157, 157)
        self.down_color = (255, 255, 255)
        self.surf.fill(self.up_color)
