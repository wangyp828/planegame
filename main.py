#coding:utf-8
import pygame
import sys
import traceback 
from random import *
from pygame.locals import *
import myplane
import enemy
import bullet
import supply
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
#===========提升敌机速度============
def inc_speed(target,inc):
	for each in target:
		each.speed+=inc
#===========main()============
def main():
	pygame.mixer.music.play(-1)
	running=True
	me=myplane.MyPlane(bg_size)		#生成我方飞机
	clock=pygame.time.Clock()	#帧率
	clock.tick(60)	#帧数
	switch_image=False #控制图片切换的标志位
	delay=60	#延时参数
	score=0		#统计用户得分
	score_font=pygame.font.SysFont("arial",28)
	level=1		#游戏难度级别
	bomb_num=3		#初始有三个炸弹
	bomb_image=pygame.image.load("image/bomb.png")  # 加载全屏炸弹图标
	bomb_rect=bomb_image.get_rect()
	bomb_front=score_font
	supply_timer=USEREVENT	#补给包发送定时器
	pygame.time.set_timer(supply_timer,10*1000)		#每10s一次补给包
	is_double_bullet = False   # 是否使用超级子弹标志位
	double_bullet_timer = USEREVENT + 1  # 超级子弹持续时间定时器
	life_image=pygame.image.load("image/life.png").convert()
	life_rect=life_image.get_rect()
	life_num=3		#3条生命
	invincible_time=USEREVENT+2		#我方飞机无敌时间定时器
	paused=False		#暂停标志位
	pause_nor_image = pygame.image.load("image/game_pause_nor.png")  # 加载暂停相关按钮
	pause_pressed_image = pygame.image.load("image/game_pause_pressed.png")
	resume_nor_image = pygame.image.load("image/game_resume_nor.png")
	resume_pressed_image = pygame.image.load("image/game_resume_pressed.png")
	paused_rect = pause_nor_image.get_rect()
	paused_rect.left, paused_rect.top = width - paused_rect.width - 10, 10  # 设置暂停按钮位置
	paused_image = pause_nor_image  # 设置默认显示的暂停按钮
	gameover_image=pygame.image.load("image/game_over.png")		#游戏结束背景
	gameover_rect=gameover_image.get_rect()
	flag_recorded = False  # 是否已经打开记录文件标志位
	
	#=======实例化补给包=======
	bullet_supply=supply.BulletSupply(bg_size)
	bomb_supply=supply.BombSupply(bg_size)
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
	#========实例化普通子弹===========
	bullet1=[]
	bullet1_index=0
	bullet1_num=6	#子弹6颗
	for i in range(bullet1_num):
		b=bullet.Bullet1(me.rect.midtop)
		bullet1.append(b)
	#==========实例化超级子弹=========
	bullet2 = []
	bullet2_index = 0
	bullet2_num = 10  # 子弹10颗
	for i in range(bullet2_num//2):
		b1=bullet.Bullet2((me.rect.centerx - 33, me.rect.centery))
		bullet2.append(b1)
		b2=bullet.Bullet2((me.rect.centerx + 30, me.rect.centery))
		bullet2.append(b2)
	#=========血槽颜色==============
	color_black=(0,0,0)
	color_green=(0,220,0)
	color_red=(220,0,0)
	color_white=(255,255,255)

	while  running:
		#=======定义难度递进操作========
		if level==1 and score >500:
			level=2
			level_up_sound.play()
			add_small_enemies(small_enemies,enemies,3)
			add_mid_enemies(mid_enemies,enemies,2)
			add_big_enemies(big_enemies,enemies,1)
			inc_speed(small_enemies,1)
		elif level ==2 and score>3000:
			level=3
			level_up_sound.play()
			add_small_enemies(small_enemies,enemies,3)
			add_mid_enemies(mid_enemies,enemies,2)
			add_big_enemies(big_enemies,enemies,1)
			inc_speed(small_enemies,1)
			inc_speed(mid_enemies,1)
		elif level==3 and score>6000:
			level=4
			level_up_sound.play()
			add_small_enemies(small_enemies,enemies,3)
			add_mid_enemies(mid_enemies,enemies,2)
			add_big_enemies(big_enemies,enemies,1)
			inc_speed(small_enemies,1)
			inc_speed(mid_enemies,1)
			inc_speed(big_enemies,1)
		#将surface对象绘制在内存中
		#=========绘制背景=========
		screen.blit(background,(0,0))
		score_text=score_font.render("Score:%s" %str(score),True,color_white)
		screen.blit(score_text,(10,5))
		screen.blit(paused_image,paused_rect)
		#=========处理用户退出及暂停事件=========
		for event in pygame.event.get():
			if event.type==QUIT:
				pygame.quit()
				sys.exit()
			elif event.type==MOUSEMOTION:
				if paused_rect.collidepoint(event.pos):		# 如果鼠标悬停在按钮区域
					if paused:
						paused_image=resume_pressed_image
					else:
						paused_image=pause_pressed_image
				else:
					if paused:
						paused_image=resume_nor_image
					else:
						paused_image=pause_nor_image
			elif event.type==MOUSEBUTTONDOWN:
				button_down_sound.play()
				if event.button==1 and paused_rect.collidepoint(event.pos):	# 如果检测到用户在指定按钮区域按下鼠标左键
					paused= not paused
					if paused:
						paused_image=resume_pressed_image
						pygame.time.set_timer(supply_timer,0)
						pygame.mixer.music.pause()
						pygame.mixer.pause()
					else:
						paused_image=pause_pressed_image
						pygame.time.set_timer(supply_timer,30*1000)
						pygame.mixer.music.unpause()
						pygame.mixer.unpause()

			elif event.type==invincible_time:
				me.invincible=False
				pygame.time.set_timer(invincible_time,0)
			
			elif event.type==supply_timer:
				if choice([True, False]):
					bomb_supply.reset()
				else:
					bullet_supply.reset()
			
			elif event.type==double_bullet_timer:
				is_double_bullet=False
				pygame.time.set_timer(double_bullet_timer,0)

			elif event.type==KEYDOWN:
				if event.key==K_SPACE:		# 如果检测到用户按下空格键
					if bomb_num:		# 如果炸弹数量大于零，则引爆一颗超级炸弹
						bomb_num-=1
						bomb_sound.play()
						for each in enemies:
							if each.rect.bottom>0:		# 屏幕上的所有敌机均销毁
								each.active=False	
		if life_num and (not paused):		#有>0条生命
			# ========绘制全屏炸弹数量和剩余生命数量========
			bomb_text=bomb_front.render("x %d"%bomb_num,True,color_black)
			bomb_text_rect=bomb_text.get_rect()
			screen.blit(bomb_image,(10,bg_size[1]-10-bomb_rect.height))
			screen.blit(bomb_text,(20+bomb_rect.width,bg_size[1]-10-bomb_text_rect.height))
			#=========控制帧率=========
			if not delay%3:
				switch_image=not switch_image
			#=========绘制我方飞机=========
			if me.active:
				if switch_image:
					screen.blit(me.image1,me.rect)
				else:
					screen.blit(me.image2,me.rect)
				for i in range(life_num):		#右下角显示飞机生命
						screen.blit(life_image,(bg_size[0]-10-(i+1)*life_rect.width,bg_size[1]-10-life_rect.height))
			else:
				if not delay%3:
					screen.blit(me.destroy_images[me_destroy_index],me.rect)
					me_destroy_index=(me_destroy_index+1)%4
					if me_destroy_index==0:
						life_num-=1
						me_down_sound.play()
						me.reset()
						pygame.time.set_timer(invincible_time,3*1000)
					
			#=========绘制敌机=========
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
							score+=50
							each.reset()

			for each in mid_enemies:
				if each.active:		#飞机正常存在
					each.move()
					if not each.hit:
						screen.blit(each.image,each.rect)
					else:
						screen.blit(each.image_hit,each.rect)
						each.hit=False
					#========绘制血槽=========
					pygame.draw.line(screen,color_black,
									(each.rect.left,each.rect.top-5),
									(each.rect.right,each.rect.top-5),
									2)
					energy_remain=each.energy/enemy.MidEnemy.energy
					if energy_remain>0.2:
						energy_color=color_green
					else:
						energy_color=color_red
					pygame.draw.line(screen,energy_color,
									(each.rect.left,each.rect.top-5),
									(each.rect.left+each.rect.width*energy_remain,each.rect.top-5),
									2)
					if each.rect.bottom==-50:
							big_enemy_flying_sound.play(-1)
				else:		#飞机已撞毁
					if e2_destroy_index==0:
						enemy2_down_sound.play()
					if not delay%3:
						screen.blit(each.destroy_images[e2_destroy_index], each.rect)
						e2_destroy_index=(e2_destroy_index+1)%4
						if e2_destroy_index==0:
							score+=200
							each.reset()

			for each in big_enemies:
				if each.active:		#飞机正常存在
					each.move()
					if not each.hit:	#飞机未被击中
						if switch_image:
							screen.blit(each.image1,each.rect)
						else:
							screen.blit(each.image2,each.rect)		
					else:
						screen.blit(each.image_hit,each.rect)
						each.hit=False
					#========绘制血槽=========
					pygame.draw.line(screen,color_black,
									(each.rect.left,each.rect.top-5),
									(each.rect.right,each.rect.top-5),
									2)
					energy_remain=each.energy/enemy.BigEnemy.energy
					if energy_remain>0.2:
						energy_color=color_green
					else:
						energy_color=color_red
					pygame.draw.line(screen,energy_color,
									(each.rect.left,each.rect.top-5),
									(each.rect.left+each.rect.width*energy_remain,each.rect.top-5),
									2)
					if each.rect.bottom==-50:
							big_enemy_flying_sound.play(-1)
				
				else:		#飞机已撞毁
					big_enemy_flying_sound.stop()
					if e3_destroy_index == 0:
						enemy3_down_sound.play()	# 播放飞机撞毁音效
					if not (delay % 3):		# 每三帧播放一张损毁图片
						screen.blit(each.destroy_images[e3_destroy_index], each.rect)
						e3_destroy_index = (e3_destroy_index + 1) % 6	# 大型敌机有六张损毁图片
						if e3_destroy_index == 0:	# 如果损毁图片播放完毕，则重置飞机属性
							score+=600
							each.reset()
			# ==========绘制补给并检测玩家是否获得==========
			if bomb_supply.active:  # 如果是超级炸弹补给包
				bomb_supply.move()
				screen.blit(bomb_supply.image, bomb_supply.rect)
				if pygame.sprite.collide_mask(bomb_supply, me):  # 如果玩家获得超级炸弹补给包
					get_bomb_sound.play()
					if bomb_num < 3:
						bomb_num += 1
					bomb_supply.active = False
			# ==========如果是超级子弹补给包==========
			if bullet_supply.active:
				bullet_supply.move()
				screen.blit(bullet_supply.image, bullet_supply.rect)
				if pygame.sprite.collide_mask(bullet_supply, me):
					get_bullet_sound.play()
					is_double_bullet = True
					bullet_supply.active = False
					pygame.time.set_timer(double_bullet_timer, 18 * 1000)
			#=========绘制子弹=========
			if not(delay%10):
				bullet_sound.play()
				if not is_double_bullet:
					bullets=bullet1
					bullets[bullet1_index].reset(me.rect.midtop)
					bullet1_index=(bullet1_index+1)%bullet1_num
				else:
					bullets=bullet2
					bullets[bullet2_index].reset((me.rect.centerx - 33, me.rect.centery))
					bullets[bullet2_index+1].reset((me.rect.centerx + 30, me.rect.centery))
					bullet2_index=(bullet2_index+2)%bullet2_num
			# =========子弹与敌机的碰撞检测========
			for b in bullets:
				if b.active:	#子弹激活状态
					b.move()
					screen.blit(b.image,b.rect)
					enemies_hit=pygame.sprite.spritecollide(b,enemies,False,pygame.sprite.collide_mask)
					if enemies_hit:		#子弹击中飞机
						b.active=False
						for e in enemies_hit:
							if e in big_enemies or e in mid_enemies:
								e.energy-=1
								e.hit=True	#飞机被击中
								if e.energy==0:
									e.active=False	#大中敌机损毁
							else:
								e.active=False	#小敌机损毁

			#=========实时检测是否发生碰撞=========
			enemies_down=pygame.sprite.spritecollide(me,enemies,False,pygame.sprite.collide_mask)
			if enemies_down and not me.invincible:
				me.active=False
				for e in enemies_down:
					e.active=False
			#=========处理用户键盘操作事件=========	
			key_pressed=pygame.key.get_pressed()
			if key_pressed[K_w] or key_pressed[K_UP]:
				me.move_up()
			if key_pressed[K_a] or key_pressed[K_LEFT]:
				me.move_left()
			if key_pressed[K_s] or key_pressed[K_DOWN]:
				me.move_down()
			if key_pressed[K_d] or key_pressed[K_RIGHT]:
				me.move_right()
		elif life_num==0:		#生命为0
			screen.blit(gameover_image,gameover_rect)
			pygame.mixer.music.stop()		#关闭背景音乐
			pygame.mixer.stop()		#关闭音效
			pygame.time.set_timer(supply_timer,0)	#关闭补给机制
			
			if not flag_recorded:
				with open("score_record.txt","r") as f:
					content=f.read()
					if content=='':
						record_score=0
					else:
						record_score=int(content)
				flag_recorded=True
				if score>record_score:
					with open("score_record.txt","w") as f:
						f.write(str(score))

			record_score_text=score_font.render("%d"%record_score,True,color_white)
			screen.blit(record_score_text,(150,40))
			game_over_score_text=score_font.render("%d"%score,True,color_white)
			screen.blit(game_over_score_text,(220,370))
		#=========将内存中的surface对象刷新到屏幕上=========
		pygame.display.flip()

		#=========控制帧率=========
		if delay==0:
			delay=60
		else:
			delay-=1

	



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
