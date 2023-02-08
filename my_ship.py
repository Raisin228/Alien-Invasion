import pygame


class Ship():
    '''Класс для управления кораблем'''

    def __init__(self, ai_game):
        '''Инициализирует корабль и задает его начальную позицию'''
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        # Загружает изображение корабля и получает прямоугольник
        self.image = pygame.image.load('images/drednought/right/0.png')
        self.rect = self.image.get_rect()
        # Каждый новый корабль появляется у нижнего края экрана
        self.rect.midbottom = self.screen_rect.midbottom

        # флаги для анимации движения корабля
        self.fl_move_right, self.fl_move_left, self.fl_move_up, self.fl_move_down = False, False, False, False
        self.animation_set_right = [pygame.image.load(f'images/drednought/right/{i}.png') for i in range(0, 3)]
        self.animation_set_left = [pygame.image.load(f'images/drednought/left/{i}.png') for i in range(0, 3)]
        self.animation_set_up = [pygame.image.load(f'images/drednought/up/{i}.png') for i in range(0, 4)]
        self.frame, self.frame_up = 0, 0
        self.d_fl = 1

    def blitme(self):
        '''Выбираем нужную анимацию для корабля и рисуем в нужной позиции'''
        if self.frame > 2:
            self.frame = 2
        if self.frame_up > 4:
            self.frame_up = 0

        if self.fl_move_right:
            self.image = self.animation_set_right[int(self.frame)]
        elif self.fl_move_left:
            self.image = self.animation_set_left[int(self.frame)]
        elif self.fl_move_up:
            self.image = self.animation_set_up[int(self.frame_up)]
        elif self.fl_move_down:
            self.image = pygame.image.load('images/drednought/down/-1.png')
        else:
            if self.frame > 0:
                self.frame -= 0.2
                if self.frame < 0:
                    self.frame = 0
                if self.d_fl == 2:
                    self.image = self.animation_set_right[int(self.frame)]
                else:
                    self.image = self.animation_set_left[int(self.frame)]
                if self.frame == 0:
                    self.d_fl = 1
            else:
                self.image = pygame.image.load(f'images/drednought/right/{int(self.frame)}.png')
        self.screen.blit(self.image, self.rect)
