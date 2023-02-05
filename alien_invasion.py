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
            self._check_events()
            # вызываем метод перемещения корабля
            self.ship.update()
            # метод для обновления экрана
            self._update_screen()
            clock.tick(FPS)

    def _check_events(self):
        '''Метод для обработки нажатия клавиш и событий мыши'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # Обработка движения корабля влево и вправо
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = True
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True
                elif event.key == pygame.K_UP:
                    self.ship.moving_up = True
                elif event.key == pygame.K_DOWN:
                    self.ship.moving_down = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False
                elif event.key == pygame.K_UP:
                    self.ship.moving_up = False
                elif event.key == pygame.K_DOWN:
                    self.ship.moving_down = False

    def _update_screen(self):
        # устaнавливаем цвет фона
        self.screen.blit(self.settings.bg_color, (0, 0))
        self.ship.blitme()
        # отображение последнего прорисованного экрана
        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvansion()
    ai.run_game()
