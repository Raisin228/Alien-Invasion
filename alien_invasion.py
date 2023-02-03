import sys
import pygame
from settings import Settings
from my_ship import Ship

FPS = 60
clock = pygame.time.Clock()


class AlienInvansion():
    '''Класс для управления ресурсами и поведением игры.'''

    def __init__(self):
        '''Инициализируем игру и создаём игровые ресурсы'''
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Alien Invansion')
        self.ship = Ship(self)

    def run_game(self):
        '''Запуск основного цикла игры.'''
        while True:
            # отслеживание событий клавиатуры и мыши
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # устaнавливаем цвет фона
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()

            # отображение последнего прорисованного экрана
            pygame.display.flip()
            clock.tick(FPS)


if __name__ == '__main__':
    ai = AlienInvansion()
    ai.run_game()
