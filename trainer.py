import pygame, pygame.midi, pygame.mixer, sys, random
pygame.init()
pygame.midi.init()
pygame.mixer.init()

from notesview import *

for i in range(pygame.midi.get_count()):
	info=pygame.midi.get_device_info(i)
	if info[2]: #only if input
		print("Device: ", i, info)


screen=pygame.display.set_mode([960, 480])
clock=pygame.time.Clock()

midi=pygame.midi.Input(3)
kbd=NotesView((240, 200))
task=NotesView((710, 200))

right=pygame.mixer.Sound(os.path.join("sfx", "right.wav"))
wrong1=pygame.mixer.Sound(os.path.join("sfx", "wrong_1.wav"))
wrong2=pygame.mixer.Sound(os.path.join("sfx", "wrong_2.wav"))

nextNote=random.randint(36, 84)
task.setNote(nextNote, True)

try:
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				sys.exit()

		for event in midi.read(100):
			if event[0][0] == 144:
				if event[0][2]:
					kbd.setNote(event[0][1], True)
					if event[0][1] == nextNote:
						right.play()
						task.setNote(nextNote, False)
						nextNote=random.randint(36, 84)
						task.setNote(nextNote, True)
					else:
						random.choice([wrong1, wrong2]).play()
				else:
					kbd.setNote(event[0][1], False)

		screen.fill((255, 255, 255))
		kbd.draw(screen)
		task.draw(screen)
		pygame.display.update()
		clock.tick(24)
finally:
	midi.close()
