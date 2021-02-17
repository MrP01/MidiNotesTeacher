import os

import pygame


def init():
    pygame.init()
    pygame.midi.init()
    screen = pygame.display.set_mode([640, 480])
    clock = pygame.time.Clock()
    for i in range(pygame.midi.get_count()):
        info = pygame.midi.get_device_info(i)
        if info[2]:  # only if input
            print("Device: ", i, info)
    midi = pygame.midi.Input(3)
    return screen, clock, midi


class BaseNotesView(object):
    lineGap = 11.15
    noteColor = (255, 0, 0)
    noteRadius = 12
    noteOffset = 140
    noteNames = ["c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "hb", "h"]
    whites = ["c", "d", "e", "f", "g", "a", "h"]

    def __init__(self, center):
        self.sheet = pygame.image.load(os.path.join("img", "sheet.png"))
        self.rect = self.sheet.get_rect(center=center)

        self.sharp = pygame.image.load(os.path.join("img", "sharp.png"))
        self.flat = pygame.image.load(os.path.join("img", "flat.png"))

        self.notes = {k: 0 for k in range(36, 84)}

    def setNote(self, key, val):
        self.notes[key] = val

    def noteName(self, key):
        note = (key - 36) % 12
        return self.noteNames[note]

    @staticmethod
    def noteOctave(key):
        return int((key - 36) / 12)

    def whiteNoteIndex(self, key):
        return self.whites.index(self.noteName(key)[0]) + self.noteOctave(key) * 7

    def draw(self, surf):
        surf.blit(self.sheet, self.rect.topleft)
        for key, val in self.notes.items():
            if val:
                pos = self.rect.left + self.noteOffset, self.rect.bottom - int(self.lineGap * self.whiteNoteIndex(key))
                pygame.draw.circle(surf, self.noteColor, pos, self.noteRadius)
                if self.noteName(key).endswith("#"):
                    surf.blit(self.sharp, (pos[0] - 28, pos[1] - 18))
                if self.noteName(key).endswith("b"):
                    surf.blit(self.flat, (pos[0] - 28, pos[1] - 20))
