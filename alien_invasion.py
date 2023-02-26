import sys
import pygame
import time
from settings import Settings
from my_ship import Ship
from bullet import Bullet
from alien import Alien
from animation_boom import Explosion
from game_stats import GameStats
from buttons import Button
from blure import blure_bg

FPS = 60
clock = pygame.time.Clock()


class AlienInvansion:
    """Класс для управления ресурсами и поведением игры."""

    def __init__(self):
        """Инициализируем игру и создаём игровые ресурсы"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption('Alien Invansion')
        pygame.display.set_icon(pygame.image.load('images/galaxy.png'))
        # экземпляр для хранения игровой статистики
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.bull = Bullet(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.booms = pygame.sprite.Group()
        self._create_fleet()
        # создание 2-х кнопок
        self.button_play = Button(self, 'Play', 'images/buttons/button_play.png',
                                  self.screen_rect.center[0] - 100, self.screen_rect.center[1])
        self.button_quit = Button(self, 'Quit', 'images/buttons/button_quit.png',
                                  self.screen_rect.center[0] - 100, self.screen_rect.center[1] + 100)
        # изначально устанавливаем фон загрузки игры
        self.screen.blit(self.settings.start_bg, (0, 0))

    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            # отслеживание событий клавиатуры и мыши
            self._check_events()

            if self.stats.game_active:
                # отрисовка группы пуль и удаление вылетевших за экран
                self.settings.first_start = False
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
            elif event.type == pygame.KEYUP and event.key == pygame.K_p:
                # если кнопка p нажата в главном меню -> начинаем игру
                if not self.stats.game_active:
                    self.stats.game_active = True
                else: # размываем фон
                    self.stats.game_active = False
                    sub = self.screen.subsurface(self.screen_rect)
                    pygame.image.save(sub, 'images/stop_blure_bg/screenshot.jpg')
                    blure_bg()

            elif event.type == pygame.KEYUP:
                if (event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or
                        event.key == pygame.K_UP or event.key == pygame.K_DOWN):
                    self.ship.fl_move_right, self.ship.fl_move_left = False, False
                    self.ship.fl_move_up, self.ship.fl_move_down = False, False
                if event.key == pygame.K_SPACE:
                    self.ship.shoot = False
            elif not self.stats.game_active:
                # проверяем находится ли мышка на кнопке play/quit
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_quit_button(mouse_pos, event)

        # проверяем стреляет ли корабль в данный момент
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            self.ship.shoot = True
        self._create_bullet()

        self._ship_move()

    def _check_play_quit_button(self, mouse_pos, event):
        """Проверяем нахождение мыши над кнопкой Play/Quit"""
        # нажата play
        if self.button_play.button_rect.collidepoint(mouse_pos):
            self.button_play = Button(self, 'Play', 'images/buttons/button_play.png',
                                      self.screen_rect.center[0] - 100, self.screen_rect.center[1], self.settings.dark)
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                self.stats.game_active = True
                self.stats.reset_stats()

        # нажата quit
        elif self.button_quit.button_rect.collidepoint(mouse_pos):
            self.button_quit = Button(self, 'Quit', 'images/buttons/button_quit.png',
                                      self.screen_rect.center[0] - 100, self.screen_rect.center[1] + 100,
                                      self.settings.dark)
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                sys.exit()
        # не нажаты play/quit
        else:
            self.button_play = Button(self, 'Play', 'images/buttons/button_play.png',
                                      self.screen_rect.center[0] - 100, self.screen_rect.center[1])
            self.button_quit = Button(self, 'Quit', 'images/buttons/button_quit.png',
                                      self.screen_rect.center[0] - 100, self.screen_rect.center[1] + 100)
        # прячем курсор если началась игра
        if self.stats.game_active:
            pygame.mouse.set_visible(False)
        else:
            pygame.mouse.set_visible(True)

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

    def _ship_hit(self):
        """Уничтожение корабля при столкновении"""
        # конец игры если кончились жизни
        if self.stats.ship_left > 0:
            # у пользователя исчезла 1 жизнь
            self.stats.ship_left -= 1
            # убираем пришельцев и пули
            self.aliens.empty()
            self.bullets.empty()

            # создание нового флота и размещение корабля в центре
            self._create_fleet()
            self.ship.center_ship()

            # пауза
            time.sleep(0.25)
        if self.stats.ship_left <= 0:
            # делаем игру не активной и открываем главное меню
            self.stats.game_active = False
            self.settings.first_start = True
            self.aliens.empty()
            self.bullets.empty()

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

        # проверка коллизий пришелец-корабль
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # добрались пришельцы до низа
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Если пришельцы добрались до низа экрана то чистим пули и флот и забираем 1 жизнь у игрока"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.screen_rect[3]:
                self._ship_hit()
                break

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
        # отображаем эти элементы только если игра активна
        if self.stats.game_active:
            # устaнавливаем цвет фона
            self.screen.blit(self.settings.bg_color, (0, 0))
            # отображаем корабль
            self.ship.blitme()
            # прорисовываем пули
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            # изображаем флот вторжения
            self.aliens.draw(self.screen)
        # отображаем эти элементы если игра стоит на паузе
        elif not self.settings.first_start:
            # устaнавливаем цвет размытого фона
            self.blure_fon_pause = pygame.image.load('images/stop_blure_bg/bg.jpg')
            self.screen.blit(self.blure_fon_pause, (0, 0))
            # 2 кнопки
            self.button_play.draw_button()
            self.button_quit.draw_button()
        # главное меню
        else:
            self.screen.blit(self.settings.start_bg, (0, 0))
            # 2 кнопки
            self.button_play.draw_button()
            self.button_quit.draw_button()

        self.booms.update()
        # отображение последнего прорисованного экрана
        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvansion()
    ai.run_game()
