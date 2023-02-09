import pygame


class Settings():
    '''Класс для хранения настроек конфигурации игры'''

    def __init__(self):
        '''Инициализируем настройки игры'''
        # параметры экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = pygame.image.load('images/фон1.png')
        self.ship_speed = 3
        # настройки для создания пуль
        self.bullet_speed = 3.1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (30, 144, 255)
