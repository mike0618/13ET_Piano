import pygame

HEIGHT = 600
WIDTH = HEIGHT * 1.618
H_KB = HEIGHT // 2
W_KEY = WIDTH // 9
H_BKEY = H_KB // 1.618
W_BKEY = W_KEY // 1.618
WKEYS = 'qwertyuiozxcvbnm,.'
BKEYS = '23578sdgjk'
ch = 0


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
        global ch
        pygame.mixer.Channel(ch).play(self.note)
        ch += 1
        if ch == 8:
            ch = 0
        self.played = True
        self.surf.fill(self.down_color)


class Wkey(Bkey):
    def __init__(self):
        super(Wkey, self).__init__()
        self.surf = pygame.Surface((W_KEY - 2, H_KB - 2))
        self.up_color = (157, 157, 157)
        self.down_color = (255, 255, 255)
        self.surf.fill(self.up_color)
