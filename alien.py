import pygame
from pygame.sprite import Sprite
from settings import Settings


class Alien(Sprite):
    """Класс представляющий одного пришельца"""

    def __init__(self, ai_game):
        """Инициализирует пришельца и задаёт его начальную позицию"""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = Settings()

        # загрузка изображения пришельца и получение rect
        self.image = pygame.image.load('images/zergs/zergling.png')
        self.rect = self.image.get_rect()

        # каждый пришелец появляется в левом верхнем углу
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # сохранение точной горизонтальной позиции пришельца
        self.position_x = float(self.rect.x)

        # влаг для определения направления движения флота
        self.flag_move = True

    def update(self):
        # движение всего флота вправо
        if self.flag_move:
            if (self.rect.right + self.settings.alien_speed) <= self.screen_rect[2]:
                self.position_x += self.settings.alien_speed
            else:
                self.flag_move = False
                self.rect.y += self.settings.zergling_height
        # движение всего флота влево
        elif not self.flag_move:
            if (self.rect.left - self.settings.alien_speed) >= 0:
                self.position_x -= self.settings.alien_speed
            else:
                self.flag_move = True
                self.rect.y += self.settings.zergling_height

        self.rect.x = self.position_x