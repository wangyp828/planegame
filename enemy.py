#coding:utf-8
import pygame
import sys
import traceback 
from random import *
from pygame.locals import *

class SmallEnemy(pygame.sprite.Sprite):
	"""docstring for SmallEnemy"""
	def __init__(self, bg_size):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.image.load("image/enemy1.png")
		self.mask = pygame.mask.from_surface(self.image)		#掩模：用于精确的碰撞检测
		self.active=True	#设置飞机存在属性：True表正常飞行，False表损毁
		self.rect=self.image.get_rect()
		self.width,self.height=bg_size[0],bg_size[1]
		self.speed=2
		#定义初始化位置 -5保证不会在程序开始就出现
		self.rect.left,self.rect.top=(randint(0,self.width-self.rect.width),
										randint(-5*self.rect.height,-5)) 
		self.destroy_images = []  # 加载飞机损毁图片
		self.destroy_images.extend([pygame.image.load("image/enemy1_down1.png"),
									pygame.image.load("image/enemy1_down2.png"),
									pygame.image.load("image/enemy1_down3.png"),
									pygame.image.load("image/enemy1_down4.png")])

	def move(self):
		if self.rect.top<self.height:
			self.rect.top+=self.speed
		else:
			self.reset()
	def reset(self):
		self.active=True
		self.rect.left,self.rect.top=(randint(0,self.width-self.rect.width),
										randint(-5*self.rect.height,0))


class MidEnemy(pygame.sprite.Sprite):
	"""docstring for MidEnemy"""
	def __init__(self, bg_size):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.image.load("image/enemy2.png")
		self.mask = pygame.mask.from_surface(self.image)		#掩模：用于精确的碰撞检测
		self.active=True	#设置飞机存在属性：True表正常飞行，False表损毁
		self.rect=self.image.get_rect()
		self.width,self.height=bg_size[0],bg_size[1]
		self.speed=1
		self.rect.left,self.rect.top=(randint(0,self.width-self.rect.width),
										randint(-10*self.rect.height,-self.rect.height))
		self.destroy_images = []  # 加载飞机损毁图片
		self.destroy_images.extend([pygame.image.load("image/enemy2_down1.png"),
									pygame.image.load("image/enemy2_down2.png"),
									pygame.image.load("image/enemy2_down3.png"),
									pygame.image.load("image/enemy2_down4.png")])
	def move(self):
		if self.rect.top<self.height:
			self.rect.top+=self.speed
		else:
			self.reset()
	def reset(self):
		self.active=True
		self.rect.left,self.rect.top=(randint(0,self.width-self.rect.width),
										randint(-10*self.rect.height,-self.rect.height))		


class BigEnemy(pygame.sprite.Sprite):
	"""docstring for BigEnemy"""
	def __init__(self, bg_size):
		pygame.sprite.Sprite.__init__(self)
		self.image1=pygame.image.load("image/enemy3_n1.png")
		self.image2=pygame.image.load("image/enemy3_n2.png")
		self.mask = pygame.mask.from_surface(self.image1)		#掩模：用于精确的碰撞检测
		self.active=True	#设置飞机存在属性：True表正常飞行，False表损毁
		self.rect=self.image1.get_rect()
		self.width,self.height=bg_size[0],bg_size[1]
		self.speed=2
		self.rect.left,self.rect.top=(randint(0,self.width-self.rect.width),
										randint(-15*self.rect.height,-5*self.rect.height))
		self.destroy_images = []  # 加载飞机损毁图片
		self.destroy_images.extend([pygame.image.load("image/enemy3_down1.png"),
									pygame.image.load("image/enemy3_down2.png"),
									pygame.image.load("image/enemy3_down3.png"),
									pygame.image.load("image/enemy3_down4.png"),
									pygame.image.load("image/enemy3_down5.png"),
									pygame.image.load("image/enemy3_down6.png")])
	def move(self):
		if self.rect.top<self.height:
			self.rect.top+=self.speed
		else:
			self.reset()
	def reset(self):
		self.active=True
		self.rect.left,self.rect.top=(randint(0,self.width-self.rect.width),
										randint(-15*self.rect.height,-5*self.rect.height))
		