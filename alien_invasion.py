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
        pygame.display.set_icon(pygame.image.load('images/icon.png'))
        self.ship = Ship(self)

    def run_game(self):
        '''Запуск основного цикла игры.'''
        while True:
            # отслеживание событий клавиатуры и мыши
            self._check_events()
            # метод для обновления экрана
            self._update_screen()
            clock.tick(FPS)

    def _check_events(self):
        '''Метод для обработки нажатия клавиш и событий мыши'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        key = pygame.key.get_pressed()
        if key[pygame.K_q]:
            sys.exit()
        # Обработка движения корабля влево и вправо
        if (key[pygame.K_RIGHT] or key[pygame.K_d]) and self.ship.rect.right <= self.ship.screen_rect.right:
            self.ship.rect.x += 3
        if (key[pygame.K_LEFT] or key[pygame.K_a]) and self.ship.rect.left > self.ship.screen_rect.left:
            self.ship.rect.x -= 3
        if (key[pygame.K_UP] or key[pygame.K_w]) and self.ship.rect.y > self.ship.screen_rect.y:
            self.ship.rect.y -= 3
        if (key[pygame.K_DOWN] or key[pygame.K_s]) and self.ship.rect.bottom < self.ship.screen_rect.bottom:
            self.ship.rect.y += 3

    def _update_screen(self):
        # устaнавливаем цвет фона
        self.screen.blit(self.settings.bg_color, (0, 0))
        self.ship.blitme()
        # отображение последнего прорисованного экрана
        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvansion()
    ai.run_game()
