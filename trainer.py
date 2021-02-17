import os

import pygame.midi
import pygame.mixer
import random
import sys

pygame.init()
pygame.midi.init()
pygame.mixer.init()

from notesview import BaseNotesView

IGNOREOCTAVES = False
NOTEMIN, NOTEMAX = 36, 84  # c1 to c5


class Bar:
    def __init__(self, rect, color, maxval, val=0):
        self.rect = rect
        self.maxval = maxval
        self.color = color
        self.val = val

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, pygame.Rect(self.rect.topleft,
            (self.val / self.maxval * self.rect.width, self.rect.height)))


for i in range(pygame.midi.get_count()):
    info = pygame.midi.get_device_info(i)
    if info[2]:  # only if input
        print("Device: ", i, info)

screen = pygame.display.set_mode([960, 480])
clock = pygame.time.Clock()

midi = pygame.midi.Input(3)
kbd = BaseNotesView((240, 240))
task = BaseNotesView((710, 240))

right = pygame.mixer.Sound(os.path.join("sfx", "right.wav"))
wrong1 = pygame.mixer.Sound(os.path.join("sfx", "wrong_1.wav"))
wrong2 = pygame.mixer.Sound(os.path.join("sfx", "wrong_2.wav"))

nextNote = random.randint(NOTEMIN, NOTEMAX)
task.setNote(nextNote, True)

bar = Bar(pygame.Rect(30, 20, 900, 20), (123, 123, 0), 30000, 30000)
score = 0

bgcolor = (255, 255, 255)

try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                sys.exit()

        for event in midi.read(100):
            if event[0][0] == 144:
                if event[0][2]:
                    kbd.setNote(event[0][1], True)
                    if event[0][1] == nextNote or (
                            IGNOREOCTAVES and kbd.noteName(event[0][1]) == kbd.noteName(nextNote)):
                        right.play()
                        score += 1
                        bar.val += 1000
                        bgcolor = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
                        task.setNote(nextNote, False)
                        nextNote = random.randint(NOTEMIN, NOTEMAX)
                        task.setNote(nextNote, True)
                    else:
                        bar.val -= 1000
                        random.choice([wrong1]).play()
                else:
                    kbd.setNote(event[0][1], False)

        screen.fill(bgcolor)
        kbd.draw(screen)
        task.draw(screen)
        bar.draw(screen)
        pygame.display.update()
        bar.val -= clock.tick(24)
        if bar.val <= 0:
            print("Score:", score)
            break
finally:
    midi.close()
