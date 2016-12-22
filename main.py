#coding:utf-8
import pygame
import sys
import traceback 
from random import *
from pygame.locals import *
import myplane

#===========initialize============
pygame.init()
pygame.mixer.init()				
bg_size=width,heigh=480,852		
screen=pygame.display.set_mode(bg_size)
pygame.display.set_caption("飞机大战  @ping")
background=pygame.image.load("image/background.png")

#===========laod music============
pygame.mixer.music.load("sound/game_music.wav")
pygame.mixer.music.set_volume(0.2)
bullet_sound=pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(0.2)
big_enemy_flying_sound=pygame.mixer.Sound("sound/big_spaceship_flying.wav")
big_enemy_flying_sound.set_volume(0.2)
enemy1_down_sound=pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound=pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound=pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.2)
me_down_sound=pygame.mixer.Sound("sound/use_bomb.wav")
me_down_sound.set_volume(0.2)
button_down_sound=pygame.mixer.Sound("sound/button.wav")
button_down_sound.set_volume(0.2)
level_up_sound=pygame.mixer.Sound("sound/achievement.wav")
level_up_sound.set_volume(0.2)
bomb_sound=pygame.mixer.Sound("sound/use_bomb.wav")
bomb_sound.set_volume(0.2)
get_bomb_sound=pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound=pygame.mixer.Sound("sound/get_double_laser.wav")
get_bullet_sound.set_volume(0.2)

#===========main()============
def main():
	pygame.mixer.music.play(-1)
	running=True
	me=myplane.MyPlane(bg_size)		#生成我方飞机
	clock=pygame.time.Clock()	#帧率
	clock.tick(60)	#帧数
	switch_image=False #控制图片切换的标志位
	delay=60	#延时参数

	while  running:
		
		if delay==0:
			delay=60
		else:
			delay-=1
		if not delay%3:
			switch_image=not switch_image
		#将surface对象绘制在内存中
		screen.blit(background,(0,0))
		if switch_image:
			screen.blit(me.image1,me.rect)
		else:
			screen.blit(me.image2,me.rect)

		#处理用户退出事件
		for event in pygame.event.get():
			if event.type==QUIT:
				pygame.quit()
				sys.exit()

		#处理用户键盘操作事件		
		key_pressed=pygame.key.get_pressed()
		if key_pressed[K_w] or key_pressed[K_UP]:
			me.move_up()
		if key_pressed[K_a] or key_pressed[K_LEFT]:
			me.move_left()
		if key_pressed[K_s] or key_pressed[K_DOWN]:
			me.move_down()
		if key_pressed[K_d] or key_pressed[K_RIGHT]:
			me.move_right()

		#将内存中的surface对象刷新到屏幕上
		pygame.display.flip()

	



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
