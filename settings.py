import pygame


class Settings():
    '''Класс для хранения настроек конфигурации игры'''

    def __init__(self):
        '''Инициализируем настройки игры'''
        # параметры экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = pygame.image.load('images/фон1.png')
        self.start_bg = pygame.image.load('images/start_background.png')
        # настройки корабля
        self.ship_speed = 3
        self.ship_limit = 3
        # настройки для создания пуль
        self.bullet_speed = 3.1
        # параметры пришельцов
        self.alien_speed = 0.5
        self.zergling_width = 66
        self.zergling_height = 62
        # список спрайтов взрывов
        self.boom_list = [pygame.image.load(f'images/boom/{i}.png') for i in range(8)]
        # первое включение/pause
        self.first_start = True
        # цвета
        self.green = (0, 128, 0)
        self.white = (255, 255, 255)
        self.dark = (0, 0, 0)