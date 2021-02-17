import os
import sys

import pygame
import pygame.midi

pygame.init()
pygame.midi.init()

screen = pygame.display.set_mode([640, 480])
clock = pygame.time.Clock()

for i in range(pygame.midi.get_count()):
    info = pygame.midi.get_device_info(i)
    if info[2]:  # only if input
        print("Device: ", i, info)

midi = pygame.midi.Input(3)


class NotesView(object):
    lineColor = (0, 0, 0)
    lineLength = 200
    sLineLength = 40
    sLineOffset = 110
    lineGap = 20
    bassOffset = 120
    noteColor = (255, 0, 0)
    noteRadius = 20
    noteOffset = 130

    def __init__(self, topleft):
        self.x, self.y = topleft
        self.violinkey = pygame.image.load(os.path.join("img", "violinkey.png"))
        self.violinkey = pygame.transform.scale(self.violinkey, (64, 120))
        self.basskey = pygame.image.load(os.path.join("img", "basskey.png"))
        self.basskey = pygame.transform.scale(self.basskey, (46, 96))

        self.notes = {k: 0 for k in range(36, 84)}

    def setNote(self, key, val):
        self.notes[key] = val

    def draw(self, surf):
        for i in range(5):
            pygame.draw.line(surf, NotesView.lineColor, (self.x, self.y + NotesView.lineGap * i),
                (self.x + NotesView.lineLength, self.y + NotesView.lineGap * i))
        pygame.draw.line(surf, NotesView.lineColor, (self.x + NotesView.sLineOffset, self.y - NotesView.lineGap),
            (self.x + NotesView.sLineOffset + NotesView.sLineLength, self.y - NotesView.lineGap))
        pygame.draw.line(surf, NotesView.lineColor, (self.x + NotesView.sLineOffset, self.y - 2 * NotesView.lineGap),
            (self.x + NotesView.sLineOffset + NotesView.sLineLength, self.y - 2 * NotesView.lineGap))
        pygame.draw.line(surf, NotesView.lineColor, (self.x + NotesView.sLineOffset, self.y + NotesView.lineGap * 5),
            (self.x + NotesView.sLineOffset + NotesView.sLineLength, self.y + NotesView.lineGap * 5))
        surf.blit(self.violinkey, (self.x, self.y - 16))

        for i in range(5):
            pygame.draw.line(surf, NotesView.lineColor, (self.x, self.y + NotesView.bassOffset + NotesView.lineGap * i),
                (self.x + NotesView.lineLength, self.y + NotesView.bassOffset + NotesView.lineGap * i))

        pygame.draw.line(surf, NotesView.lineColor,
            (self.x + NotesView.sLineOffset, self.y + NotesView.bassOffset + NotesView.lineGap * 5),
            (self.x + NotesView.sLineOffset + NotesView.sLineLength,
             self.y + NotesView.bassOffset + NotesView.lineGap * 5))
        pygame.draw.line(surf, NotesView.lineColor,
            (self.x + NotesView.sLineOffset, self.y + NotesView.bassOffset + NotesView.lineGap * 6),
            (self.x + NotesView.sLineOffset + NotesView.sLineLength,
             self.y + NotesView.bassOffset + NotesView.lineGap * 6))
        surf.blit(self.basskey, (self.x, self.y + NotesView.bassOffset + 4))

        for key, val in self.notes.items():
            if val:
                n = key - 36
                pygame.draw.circle(surf, NotesView.noteColor,
                    (self.x + NotesView.noteOffset, self.y + NotesView.lineGap * n))


view = NotesView((100, 100))

try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit()

        screen.fill((255, 255, 255))
        view.draw(screen)
        pygame.display.update()
        clock.tick(24)
finally:
    midi.close()
