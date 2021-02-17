import sys

import pygame.midi

from notesview import BaseNotesView, init

screen, clock, midi = init()
view = BaseNotesView((300, 200))

if __name__ == '__main__':
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit()

        for event in midi.read(100):
            if event[0][0] == 144:
                if event[0][2]:
                    view.setNote(event[0][1], True)
                else:
                    view.setNote(event[0][1], False)

        screen.fill((255, 255, 255))
        view.draw(screen)
        pygame.display.update()
        clock.tick(24)
