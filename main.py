#coding:utf-8
import pygame
import sys
import traceback from random import *
from pygame.locals import *

#===========initialize============
pygame.init()
pygame.mixer.init()				
bg_size=width,heigh=480,852		
screen=pygame.disaplay.set_mode(bg_size)
pygame.disaplay.set_caption("飞机大战  @ping")
background=pygame.image.load("image/background.png")

#===========laod music============
pygame.mixer.music.laod("sound/game_music.wav")
pygame.mixer.music.set_volume(0.2)
bullet_sound=pygame.mixer.sound("sound/bullet.wav")
bullet_sound.set_volume(0.2)
big_enemy_flying_sound=pygame.mixer.sound("sound/big_spaceship_flying.wav")
big_enemy_flying_sound.set_volume(0.2)
enemy1_down_sound=pygame.mixer.sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound=pygame.mixer.sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound=pygame.mixer.sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.2)
me_down_sound=pygame.mixer.sound("sound/use_bomb.wav")
me_down_sound.set_volume(0.2)
button_down_sound=pygame.mixer.sound("sound/button.wav")
button_down_sound.set_volume(0.2)
level_up_sound=pygame.mixer.sound("sound/achievement.wav")
level_up_sound.set_volume(0.2)
bomb_sound=pygame.mixer.sound("sound/use_bomb.wav")
bomb_sound.set_volume(0.2)
get_bomb_sound=pygame.mixer.sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound==pygame.mixer.sound("sound/get_double_laser.wav")
get_bullet_sound.set_volume(0.2)

#===========program entrance============
if __name__ == '__main__':
	try:
		main()
	except SystemExit:
		pass
	except:
		traceback.print_exc()
		pygame.quit()
		input()

#===========main()============
def main():
	pygame.mixer.music.play(-1)
	running=True
	while  running:
		screen.blit(background,(0,0))
		for event in pygame.event.get():
			if event.type==QUIT:
				pygame.quit()
				sys.exit()
		pygame.disaplay.flip()
