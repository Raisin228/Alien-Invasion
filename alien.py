import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Класс представляющий одного пришельца"""

    def __init__(self, ai_game):
        """Инициализирует пришельца и задаёт его начальную позицию"""
        super().__init__()
        self.screen = ai_game.screen

        # загрузка изображения пришельца и получение rect
        self.image = pygame.image.load('images/zergs/zergling.png')
        self.rect = self.image.get_rect()

        # каждый пришелец появляется в левом верхнем углу
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # сохранение точной горизонтальной позиции пришельца
        self.position_x = float(self.rect.x)
        
