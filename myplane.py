#coding:utf-8
import pygame
import sys
import traceback 
from random import *
from pygame.locals import *


class MyPlane(pygame.sprite.Sprite):
	"""docstring for MyPlane"""
	#==========初始化飞机（精灵）===========
	def __init__(self, bg_size):
		pygame.sprite.Sprite.__init__(self)
		
		self.image1=pygame.image.load("image/hero1.png")
		self.image2=pygame.image.load("image/hero2.png")
		self.width,self.height=bg_size[0],bg_size[1]		#本地化背景图片尺寸
		self.mask = pygame.mask.from_surface(self.image1)		#掩模：用于精确的碰撞检测
		self.active=True	#设置飞机存在属性：True表正常飞行，False表损毁
		self.rect=self.image1.get_rect()		#获得当前我方飞机的位置
		self.rect.left,self.rect.top=(self.width-self.rect.width)//2,(self.height-self.rect.height-60)
										#定义飞机初始化位置，底部预留60像素
		self.speed=10
		self.destroy_images=[]		#加载飞机毁损图片
		self.destroy_images.extend([pygame.image.load("image/hero_blowup_n1.png"),
									pygame.image.load("image/hero_blowup_n2.png"),
									pygame.image.load("image/hero_blowup_n3.png"),
									pygame.image.load("image/hero_blowup_n4.png")])

	#==========定义飞机的上下左右移动==========
	def move_up(self):
		if self.rect.top>0:
			self.rect.top-=self.speed
		else:
			self.rect.top=0
	def move_left(self):
		if self.rect.left>0:
			self.rect.left-=self.speed
		else:
			self.rect.left=0
	def move_right(self):
		if self.rect.right<self.width:
			self.rect.right+=self.speed
		else:
			self.rect.right=self.width
	def move_down(self):
		if self.rect.bottom<self.height-60:
			self.rect.top+=self.speed
		else:
			self.rect.bottom=self.height-60
	def reset(self):
		self.rect.left,self.rect.top=(self.width-self.rect.width)//2,(self.height-self.rect.height-60)
		self.active=True