#coding:utf-8
import pygame
import sys
import traceback 
from random import *
from pygame.locals import *
import myplane
import enemy

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


#===========敌方小飞机控制生成函数============
def add_small_enemies(group1,group2,num):
	for i in range(num):
		e1=enemy.SmallEnemy(bg_size)
		group1.add(e1)
		group2.add(e1)

#===========敌方中飞机控制生成函数============
def add_mid_enemies(group1,group2,num):
	for i in range(num):
		e2=enemy.MidEnemy(bg_size)
		group1.add(e2)
		group2.add(e2)

#===========敌方大飞机控制生成函数============
def add_big_enemies(group1,group2,num):
	for i in range(num):
		e3=enemy.BigEnemy(bg_size)
		group1.add(e3)
		group2.add(e3)

#===========main()============
def main():
	pygame.mixer.music.play(-1)
	running=True
	me=myplane.MyPlane(bg_size)		#生成我方飞机
	clock=pygame.time.Clock()	#帧率
	clock.tick(60)	#帧数
	switch_image=False #控制图片切换的标志位
	delay=60	#延时参数
	#=======实例化敌方飞机=======
	enemies=pygame.sprite.Group()
	small_enemies=pygame.sprite.Group()
	add_small_enemies(small_enemies,enemies,1)
	mid_enemies=pygame.sprite.Group()
	add_mid_enemies(mid_enemies,enemies,1)
	big_enemies=pygame.sprite.Group()
	add_big_enemies(big_enemies,enemies,1)
	#=======飞机损毁图像索引=======
	e1_destroy_index=0
	e2_destroy_index=0
	e3_destroy_index=0
	me_destroy_index=0

	while  running:
		#将surface对象绘制在内存中
		#绘制背景
		screen.blit(background,(0,0))
		#控制帧率
		if delay==0:
			delay=60
		else:
			delay-=1
		if not delay%3:
			switch_image=not switch_image
		#绘制我方飞机
		if me.active:
			if switch_image:
				screen.blit(me.image1,me.rect)
			else:
				screen.blit(me.image2,me.rect)
		else:
			if not delay%3:
				screen.blit(me.destroy_images[me_destroy_index],me.rect)
				me_destroy_index=(me_destroy_index+1)%4
				if me_destroy_index==0:
					me_down_sound.play()
					me.reset()
		#绘制敌机
		for each in small_enemies:
			if each.active:
				each.move()
				screen.blit(each.image,each.rect)
			else:
				if e1_destroy_index==0:
					enemy1_down_sound.play()
				if not delay%3:
					screen.blit(each.destroy_images[e1_destroy_index],each.rect)
					e1_destroy_index=(e1_destroy_index+1)%4
					if e1_destroy_index==0:
						each.reset()

		for each in mid_enemies:
			if each.active:
				each.move()
				screen.blit(each.image,each.rect)
			else:
				if e2_destroy_index==0:
					enemy2_down_sound.play()
				if not delay%3:
					screen.blit(each.destroy_images[e2_destroy_index], each.rect)
					e2_destroy_index=(e2_destroy_index+1)%4
					if e2_destroy_index==0:
						each.reset()

		for each in big_enemies:
			if each.active:
				each.move()
				if switch_image:
					screen.blit(each.image1,each.rect)
				else:
					screen.blit(each.image2,each.rect)
				if each.rect.bottom==-50:
					big_enemy_flying_sound.play(-1)
			else:
				big_enemy_flying_sound.stop()
				if e3_destroy_index == 0:
					enemy3_down_sound.play()  # 播放飞机撞毁音效
				if not (delay % 3):  # 每三帧播放一张损毁图片
					screen.blit(each.destroy_images[e3_destroy_index], each.rect)
					e3_destroy_index = (e3_destroy_index + 1) % 6  # 大型敌机有六张损毁图片
					if e3_destroy_index == 0:  # 如果损毁图片播放完毕，则重置飞机属性
						each.reset()

		#实时检测是否发生碰撞
		enemies_down=pygame.sprite.spritecollide(me,enemies,False,pygame.sprite.collide_mask)
		if enemies_down:
			me.active=False
			for e in enemies_down:
				e.active=False


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
