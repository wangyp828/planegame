#coding:utf-8
import pygame
import sys
import traceback 
from random import *
from pygame.locals import *

#===========普通子弹==============
class Bullet1(pygame.sprite.Sprite):
	"""docstring for Bullet1"""
	def __init__(self, position):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.image.load("image/bullet1.png")
		self.rect=self.image.get_rect()
		self.rect.left,self.rect.top=position
		self.speed=12
		self.active=True
		self.mask=pygame.mask.from_surface(self.image)

	def move(self):
		if self.rect.top<0:
			self.active=False
		else:
			self.rect.top-=self.speed

	def reset(self,position):
		self.rect.left,self.rect.top=position
		self.active=True


# ====================定义超级子弹====================
class Bullet2(pygame.sprite.Sprite):
	def __init__(self, position):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.image.load("image/bullet2.png")
		self.rect=self.image.get_rect()
		self.rect.left, self.rect.top=position
		self.speed=14
		self.active=True
		self.mask=pygame.mask.from_surface(self.image)

	def move(self):
		if self.rect.top<0:
			self.active=False
		else:
			self.rect.top-=self.speed

	def reset(self, position):
		self.rect.left, self.rect.top=position
		self.active=True