import pygame
from math import sqrt
import datetime

MAX_SPEED = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RESTAR_INFO_POSITION = (600, 775)
TIME_INFO_POSITION = (100, 775)
CONTROL_INFO_POSITION = (730, 775)

"""Класс для платформы, которой управляет юзер"""
class Paddle:
	
	"""Конструктор класса для платформы"""
	def __init__(self):
		self.color = [255, 0, 0]
		self.size = [100, 20]
		self.position = [512, 740]
		self.rect = pygame.Rect([self.position[0] - self.size[0]/2, self.position[1] - self.size[1]/2, self.size[0], self.size[1] ])

	"""Функция, отвечающая за движение платформы"""
	def update_position(self, mov):
		if ( self.position[0] - self.size[0]/2 + mov ) > 0 and ( self.position[0] + self.size[0]/2 + mov ) < 1024:
			self.position[0] += mov 
			self.rect = pygame.Rect([self.position[0] - self.size[0]/2, self.position[1] - self.size[1]/2, self.size[0], self.size[1] ])

	"""Опеделение координат граней"""
	def get_edges(self):
		edges = dict()

		edges['left'] = self.position[0] - self.size[0]/2
		edges['right'] = self.position[0] + self.size[0]/2
		edges['top'] = self.position[1] - self.size[1]/2
		edges['bottom'] = self.position[1] + self.size[1]/2

		return edges

"""Класс для мячика"""
class Ball:

	"""Конструктор мячика"""
	def __init__(self):
		self.color = [255, 255, 0]
		self.radius = 10
		self.position = [512, 721]
		self.vel = [0, 0]

	"""Обновление скорости мячика"""
	def update_velocities(self, s1, s2):
		self.vel = [ s1*self.vel[0], s2*self.vel[1] ]

	"""Функция, задающая движение мячику"""
	def move(self):
		self.position[0] += self.vel[0]
		self.position[1] += self.vel[1]

	"""Определение координат описанного вокруг мячика квадрата"""
	def get_edges(self):
		edges = dict()
		
		edges['left'] = self.position[0] - self.radius
		edges['right'] = self.position[0] + self.radius
		edges['top'] = self.position[1] - self.radius
		edges['bottom'] = self.position[1] + self.radius

		return edges

"""Класс для кирпичика"""
class Brick:

	"""Конструктор кирпичика"""
	def __init__(self, color, position):
		self.color = color
		self.size = [50, 20]
		self.position = position
		self.rect = pygame.Rect([self.position[0] - self.size[0]/2, self.position[1] - self.size[1]/2, self.size[0], self.size[1] ])

	"""Определение координат для кирпичика"""
	def get_edges(self):
		edges = dict()
		
		edges['left'] = self.position[0] - self.size[0]/2
		edges['right'] = self.position[0] + self.size[0]/2
		edges['top'] = self.position[1] - self.size[1]/2
		edges['bottom'] = self.position[1] + self.size[1]/2

		return edges 

"""Класс описывает само игровое окно"""
class Display:

	"""Конструктор для дисплея"""
	def __init__(self):

		# Звук удара мячика
		self.hit_sound = pygame.mixer.Sound('sounds/bip.wav')

		# Настраиваем шрифты
		pygame.font.init()
		self.font = pygame.font.Font(None, 30)
		self.font_big = pygame.font.Font(None, 60)
		self.restart_info = self.font.render('R - restart', True, BLACK)
		self.control_info = self.font.render('Press Q/ESC to exit', True, BLACK)
		self.win_message = self.font_big.render('You won! Press R to start over.', True, WHITE)
		self.lose_message = self.font_big.render('You lost! Press R to start over.', True, WHITE)

		# Переменная, определяющая кличество оставшихся кирпичиков
		self.bricks_left = 0

		# Создаем игровое окно и заливаем его белым цветом
		self.screen = pygame.display.set_mode((1024, 800))
		pygame.display.set_caption('Polyanoid')
		self.screen.fill( (255, 255, 255) )

		# Ставим фоновую картинку
		self.background = pygame.image.load('images/background.jpg').convert()
		self.screen.blit(self.background, (0, 0))

		# Логическая переменная, котороя следит за тем, отпущен ли мачик или примагничем к ракетке
		self.ball_released = False

		# Задаём кирпичик
		self.brick_size = [50, 20]

		# Переменные равные 1 когда юзер победил или проиграл
		self.user_won = False
		self.user_lost = False

		# Запалняем массив кирпичиков
		self.brick_map = [ [], [], [], [], [], [], [], [] ]
		for i in range( int( 1024 / self.brick_size[0] ) ):
			self.brick_map[0].append( Brick( (74, 148, 0), [ 2 + i + int(self.brick_size[0]*(i + 0.5)), 100 ] ) )
			self.brick_map[1].append( Brick( (0, 0, 255), [ 2 + i + int(self.brick_size[0]*(i + 0.5)), 100 + self.brick_size[1] + 3 ] ) )
			self.brick_map[2].append( Brick( (255, 0, 255), [ 2 + i + int(self.brick_size[0]*(i + 0.5)), 100 + self.brick_size[1]*2 + 6 ] ) )
			self.brick_map[3].append( Brick( (255, 255, 0), [ 2 + i + int(self.brick_size[0]*(i + 0.5)), 100 + self.brick_size[1]*3 + 9 ] ) )
			self.brick_map[4].append( Brick( (74, 148, 0), [ 2 + i + int(self.brick_size[0]*(i + 0.5)), 100 + self.brick_size[1]*4 + 12] ) )
			self.brick_map[5].append( Brick( (0, 0, 255), [ 2 + i + int(self.brick_size[0]*(i + 0.5)), 100 + self.brick_size[1]*5 + 15 ] ) )
			self.brick_map[6].append( Brick( (255, 0, 255), [ 2 + i + int(self.brick_size[0]*(i + 0.5)), 100 + self.brick_size[1]*6 + 18 ] ) )
			self.brick_map[7].append( Brick( (255, 255, 0), [ 2 + i + int(self.brick_size[0]*(i + 0.5)), 100 + self.brick_size[1]*7 + 21 ] ) )
			self.bricks_left += 8

		# Создаем объекты пэда и мячика
		self.pad = Paddle()
		self.ball = Ball()

		# Отрисовываем кирпичики
		for row in self.brick_map:
			for brick in row:
				if brick:
					pygame.draw.rect( self.screen, brick.color, brick.rect )

		# Отрисовываем пэд и мячик, текст
		pygame.draw.rect(self.screen, self.pad.color, self.pad.rect)
		self.ball_hitbox =  pygame.draw.circle(self.screen, self.ball.color, self.ball.position, self.ball.radius)
		self.screen.blit(self.restart_info, RESTAR_INFO_POSITION)
		self.screen.blit(self.control_info, CONTROL_INFO_POSITION)

		# Обновляем экран
		pygame.display.update()

	"""Функция полностью откраывает уровень в первоначальное состояние (Мячик на пэде, блоки на местах)"""
	def reset(self):

		self.start_time = datetime.datetime.now()

		self.user_won = False
		self.user_lost = False
		self.bricks_left = 0
		self.ball_released = False

		self.screen = pygame.display.set_mode((1024, 800))
		self.screen.fill( (255, 255, 255) )
		self.background = pygame.image.load('images/background.jpg').convert()
		self.screen.blit(self.background, (0, 0))

		self.brick_map = [ [], [], [], [], [], [], [], [] ]
		for i in range( int( 1024 / self.brick_size[0] ) ):
			self.brick_map[0].append( Brick( (74, 148, 0), [ 2 + i + int(self.brick_size[0]*(i + 0.5)), 100 ] ) )
			self.brick_map[1].append( Brick( (0, 0, 255), [ 2 + i + int(self.brick_size[0]*(i + 0.5)), 100 + self.brick_size[1] + 3 ] ) )
			self.brick_map[2].append( Brick( (255, 0, 255), [ 2 + i + int(self.brick_size[0]*(i + 0.5)), 100 + self.brick_size[1]*2 + 6 ] ) )
			self.brick_map[3].append( Brick( (255, 255, 0), [ 2 + i + int(self.brick_size[0]*(i + 0.5)), 100 + self.brick_size[1]*3 + 9 ] ) )
			self.brick_map[4].append( Brick( (74, 148, 0), [ 2 + i + int(self.brick_size[0]*(i + 0.5)), 100 + self.brick_size[1]*4 + 12] ) )
			self.brick_map[5].append( Brick( (0, 0, 255), [ 2 + i + int(self.brick_size[0]*(i + 0.5)), 100 + self.brick_size[1]*5 + 15 ] ) )
			self.brick_map[6].append( Brick( (255, 0, 255), [ 2 + i + int(self.brick_size[0]*(i + 0.5)), 100 + self.brick_size[1]*6 + 18 ] ) )
			self.brick_map[7].append( Brick( (255, 255, 0), [ 2 + i + int(self.brick_size[0]*(i + 0.5)), 100 + self.brick_size[1]*7 + 21 ] ) )
			self.bricks_left += 8

		self.pad = Paddle()
		self.ball = Ball()

		for row in self.brick_map:
			for brick in row:
				if brick:
					pygame.draw.rect( self.screen, brick.color, brick.rect )

		pygame.draw.rect(self.screen, self.pad.color, self.pad.rect)
		self.ball_hitbox = pygame.draw.circle(self.screen, self.ball.color, self.ball.position, self.ball.radius)
		self.screen.blit(self.restart_info, RESTAR_INFO_POSITION)
		self.screen.blit(self.control_info, CONTROL_INFO_POSITION)

		pygame.display.update()

	""" Функция обновляет игровое поле"""
	def update(self, mov):

		# Выводит сообщение, если пользователь выйграл 
		if self.user_won:
			self.screen.blit(self.win_message, (200, 400))

		# Выводит сообщение, если пользователь проиграл
		elif self.user_lost:
			self.screen.blit(self.lose_message, (200, 400))

		# Если идет игра
		else:

			# Обновляем позицию пэда
			self.pad.update_position(mov)

			# Отрисовываем фон, пэд
			self.screen.fill( (255, 255, 255) )
			self.screen.blit(self.background, (0, 0))
			pygame.draw.rect(self.screen, self.pad.color, self.pad.rect)

			# Если мячик примагничем, передвигаем его вместе с пэдом
			if not self.ball_released:
				self.ball.position[0] = self.pad.position[0]
				self.start_time = datetime.datetime.now()

			# Иначе проверяем столкновения и передвигаем мяч
			else:
				self.collision_check()
				self.ball.move()

			# Обновление счетчика времени
			current_time = datetime.datetime.now()
			delta = current_time - self.start_time

			minutes = delta.seconds // 60
			seconds = delta.seconds - minutes * 60
			time_info = self.font.render( "Time: {}:{}".format(minutes, seconds), True, BLACK )

			# Отрисовка курпичиков
			for row in self.brick_map:
				for brick in row:
					if brick:
						pygame.draw.rect( self.screen, brick.color, brick.rect )

			# Отрисовка мячика
			self.ball_hitbox = pygame.draw.circle(self.screen, self.ball.color, self.ball.position, self.ball.radius)

			# Отрисовка меню
			self.screen.blit(self.restart_info, RESTAR_INFO_POSITION)
			self.screen.blit(time_info, TIME_INFO_POSITION)
			self.screen.blit(self.control_info, CONTROL_INFO_POSITION)

		# Обновление дисплея
		pygame.display.update()
			
	""" Функция проверяет на столкновение"""
	def collision_check(self):
		
		ball_edges = self.ball.get_edges()
		pad_edges = self.pad.get_edges()

		# Проверяем шарик на столкновение с пэдом
		if ball_edges['bottom'] >= pad_edges['top']:
			if ball_edges['right'] >= pad_edges['left'] and ball_edges['left'] <= pad_edges['right']:
				self.ball_bounce_pad()
				self.hit_sound.play()

		# Проверяем шарик на столкновение с границами
		boundaries = self.get_boundaries()
		if ( ball_edges['top'] < ( boundaries['top'] )) or ( ball_edges['bottom'] > boundaries['bottom'] ):
			if ( ball_edges['bottom'] > boundaries['bottom'] ):
				self.ball.update_velocities(0, 0)
				self.user_lost = True

			self.ball.update_velocities(1, -1)
			self.hit_sound.play()

		elif ball_edges['left'] < boundaries['left'] or ball_edges['right'] > boundaries['right']:
			self.ball.update_velocities(-1, 1)
			self.hit_sound.play()

		# Переменая для проверки было ли столкновение
		hit = False
		# Проверяем шарик на столкновение с кирпичем
		for i in range( len(self.brick_map) ):
			for j in range( len(self.brick_map[i]) ):
				if self.brick_map[i][j]:
					if self.ball_hitbox.colliderect( self.brick_map[i][j].rect ):
						self.ball_bounce_brick( self.brick_map[i][j], ball_edges )
						self.brick_map[i][j] = None
						self.bricks_left -= 1

						if not self.bricks_left:
							self.user_won = True

						hit = True
						break
			if hit:
				break
						

	""" нахождение скорости мячика при ударе о платформу"""
	def ball_bounce_pad(self):
		if self.ball.position[0] < self.pad.position[0]:
			x_sign = -1
		else:
			x_sign = 1

		ball_vel = [0, 0]
		v_x = int( x_sign * abs( self.ball.position[0] - self.pad.position[0] ) / ( self.pad.size[0] / 2 ) * MAX_SPEED  )
		v_y_sq = MAX_SPEED**2 - v_x**2
		if v_y_sq >= 0:
			v_y = int( - sqrt(MAX_SPEED**2 - v_x**2) )
		else:
			v_y = 0

		self.ball.vel = [v_x, v_y]	

	""" нахождение знака скорости мячика при ударе о кирпичик"""
	def ball_bounce_brick(self, brick, ball_edges):
		brick_edges = brick.get_edges()

		if ( ball_edges['bottom'] > ( brick_edges['top'] )) or ( ball_edges['top'] > brick_edges['bottom'] ):
			self.ball.update_velocities(1, -1)
			self.hit_sound.play()
		elif ball_edges['left'] < brick_edges['right'] or ball_edges['right'] > brick_edges['left']:
			self.ball.update_velocities(-1, 1)
			self.hit_sound.play()

	""" Определение координат стен"""
	def get_boundaries(self):
		edges = dict()

		edges['top'] = 0
		edges['bottom'] = 752
		edges['left'] = 0
		edges['right'] = 1024

		return edges
