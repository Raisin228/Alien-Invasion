import sys
import pygame
from settings import Settings
from my_ship import Ship
from bullet import Bullet
from alien import Alien
from animation_boom import Explosion

FPS = 60
clock = pygame.time.Clock()


class AlienInvansion:
    """Класс для управления ресурсами и поведением игры."""

    def __init__(self):
        """Инициализируем игру и создаём игровые ресурсы"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Alien Invansion')
        pygame.display.set_icon(pygame.image.load('images/galaxy.png'))
        self.ship = Ship(self)
        self.bull = Bullet(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.booms = pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            # отслеживание событий клавиатуры и мыши
            self._check_events()
            # отрисовка группы пуль и удаление вылетевших за экран
            self._update_bullets()
            # обновление позиций пришельцев
            self._update_aliens()
            # метод для обновления экрана
            self._update_screen()
            clock.tick(FPS)

    def _check_events(self):
        """Метод для обработки нажатия клавиш и событий мыши"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                sys.exit()
            elif event.type == pygame.KEYUP:
                if (event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or
                        event.key == pygame.K_UP or event.key == pygame.K_DOWN):
                    self.ship.fl_move_right, self.ship.fl_move_left = False, False
                    self.ship.fl_move_up, self.ship.fl_move_down = False, False
                if event.key == pygame.K_SPACE:
                    self.ship.shoot = False

        # проверяем стреляет ли корабль в данный момент
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            self.ship.shoot = True
        self._create_bullet()

        self._ship_move()

    def _ship_move(self):
        """Обработка движения корабля влево|вправо|верх|низ"""
        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT] and self.ship.rect.right <= self.ship.screen_rect.right:
            self.ship.rect.x += self.settings.ship_speed
            self.ship.frame += 0.2
            self.ship.fl_move_right = True
            self.ship.d_fl = 2
        if key[pygame.K_LEFT] and self.ship.rect.left > self.ship.screen_rect.left:
            self.ship.rect.x -= self.settings.ship_speed
            self.ship.frame += 0.2
            self.ship.fl_move_left = True
            self.ship.d_fl = 0
        if key[pygame.K_UP] and self.ship.rect.y > self.ship.screen_rect.y:
            self.ship.rect.y -= self.settings.ship_speed
            self.ship.frame_up += 0.1
            self.ship.fl_move_up = True
        if key[pygame.K_DOWN] and self.ship.rect.bottom < self.ship.screen_rect.bottom:
            self.ship.rect.y += self.settings.ship_speed
            self.ship.fl_move_down = True

    def _create_bullet(self):
        '''Вспомогательный метод для создания пуль и включения её в группу'''
        if self.ship.shoot and (pygame.time.get_ticks() - self.ship.timer_for_bullets) > 500:
            new_bullet = Bullet(self)
            self.ship.timer_for_bullets = pygame.time.get_ticks()
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        '''Обновляет позиции снарядов и уничтожает старые снаряды'''
        self.bullets.update()
        for bullet in self.bullets:
            if bullet.rect.bottom <= 0:
                bullet.kill()

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Проверка колизий пуль и пришельцев"""
        # проверка попаданий в пришельцев
        # при обнаружении попадания удалить снаряд и пришельца
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        for enamy in collisions:
            self.boom = Explosion(enamy.rect.center, self)
            self.booms.add(self.boom)

        # создание флота если все умерли
        if len(self.aliens) <= 0:
            self.bullets.empty()
            self._create_fleet()

    def _update_aliens(self):
        """Обновляет позиции всех пришельцев"""
        self.aliens.update()

    def _create_alien(self, number_alien, row):
        """Метод для создания одного пришельца в конкретной позиции"""
        self.new_alien = Alien(self)
        new_alien_width, new_alien_height = self.new_alien.rect.size
        self.new_alien.position_x = 0.5 * new_alien_width + 2 * new_alien_width * number_alien
        self.new_alien.rect.x = self.new_alien.position_x
        self.new_alien.rect.y = new_alien_height + row * (new_alien_height * 2)
        self.aliens.add(self.new_alien)

    def _create_fleet(self):
        """Создание флота вторжения"""
        self.new_alien = Alien(self)
        # кол-во пришельцев в одном ряду
        available_space_x = self.settings.screen_width - self.new_alien.rect.width
        numbers_aliens_x = available_space_x // (2 * self.new_alien.rect.width)
        # кол-во рядов флота на экране
        available_space_y = self.settings.screen_height - 3 * self.new_alien.rect.height - self.ship.rect.height
        number_rows = available_space_y // (self.new_alien.rect.height * 2)

        # создание флота
        for i in range(int(number_rows)):
            for j in range(numbers_aliens_x):
                alien = self._create_alien(j, i)

    def _update_screen(self):
        # устaнавливаем цвет фона
        self.screen.blit(self.settings.bg_color, (0, 0))
        # отображаем корабль
        self.ship.blitme()
        # прорисовываем пули
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # изображаем флот вторжения
        self.aliens.draw(self.screen)

        self.booms.update()
        # отображение последнего прорисованного экрана
        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvansion()
    ai.run_game()
