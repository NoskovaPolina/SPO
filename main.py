import pygame
from libs import *
import datetime

# инициализация модуля pygame
pygame.init()

""" Функция запускает игру и обрабатывает игровые события"""
def game():

	# Отрисова игрового пространства, обработка столкновений и определение позиций элементов
	display = Display()

	done = False 

	# Ограничение количества итераций основного цикла
	clock = pygame.time.Clock()

	# Переменная, для определения перемещения платформы
	mov = 0

	# Основной цикл
	while not done:

		clock.tick(30)

		# Обработка клавиш
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done=True
			elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						pygame.quit()

					elif event.key == pygame.K_LEFT:
						mov = -10
					elif event.key == pygame.K_RIGHT:
						mov = 10

					elif event.key == pygame.K_SPACE:
						display.ball_released = True
					elif event.key == pygame.K_r:
						display.reset()

			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					mov = 0
					
		# Обновление игрового поля
		display.update(mov)

	pygame.quit()


if __name__ == '__main__':
	game()