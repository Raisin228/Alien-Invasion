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
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                sys.exit()
            elif event.type == pygame.KEYUP and (event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or
                                                 event.key == pygame.K_UP or event.key == pygame.K_DOWN):
                self.ship.fl_move_right, self.ship.fl_move_left = False, False
                self.ship.fl_move_up, self.ship.fl_move_down = False, False

        self._ship_move()

    def _ship_move(self):
        '''Обработка движения корабля влево|вправо|верх|низ'''
        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT] and self.ship.rect.right <= self.ship.screen_rect.right:
            self.ship.rect.x += 3
            self.ship.frame += 0.2
            self.ship.fl_move_right = True
            self.ship.d_fl = 2
        if key[pygame.K_LEFT] and self.ship.rect.left > self.ship.screen_rect.left:
            self.ship.rect.x -= 3
            self.ship.frame += 0.2
            self.ship.fl_move_left = True
            self.ship.d_fl = 0
        if key[pygame.K_UP] and self.ship.rect.y > self.ship.screen_rect.y:
            self.ship.rect.y -= 3
            self.ship.frame_up += 0.1
            self.ship.fl_move_up = True
        if key[pygame.K_DOWN] and self.ship.rect.bottom < self.ship.screen_rect.bottom:
            self.ship.rect.y += 3
            self.ship.fl_move_down = True

    def _update_screen(self):
        # устaнавливаем цвет фона
        self.screen.blit(self.settings.bg_color, (0, 0))
        self.ship.blitme()
        # отображение последнего прорисованного экрана
        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvansion()
    ai.run_game()
