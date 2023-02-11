import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    '''Класс для управления снарядами, выпущенными кораблём'''

    def __init__(self, ai_game):
        '''Создаёт объект снарядов в текущей позиции корабля.'''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # создание снаряда в позиции (0, 0) и назначение правильной позиции.
        self.image = pygame.image.load('images/drednought/fire/shoot.png')
        self.rect = self.image.get_rect()
        self.rect.midbottom = ai_game.ship.rect.midtop

        # позиция снаряда хранится в вещественном формате
        self.y = float(self.rect.y)

    def update(self):
        '''Перемещает снаряд вверх по экрану'''
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        '''рисуем пулю на экране'''
        self.screen.blit(self.image, self.rect)
