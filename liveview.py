import pygame, pygame.midi, sys
pygame.init()
pygame.midi.init()

from notesview import *

screen=pygame.display.set_mode([640, 480])
clock=pygame.time.Clock()

for i in range(pygame.midi.get_count()):
	info=pygame.midi.get_device_info(i)
	if info[2]: #only if input
		print("Device: ", i, info)

midi=pygame.midi.Input(3)

view=NotesView((300, 200))

try:
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				sys.exit()

		for event in midi.read(100):
			if event[0][0] == 144:
				if event[0][2]: view.setNote(event[0][1], True)
				else: view.setNote(event[0][1], False)

		screen.fill((255, 255, 255))
		view.draw(screen)
		pygame.display.update()
		clock.tick(24)
finally:
	midi.close()
