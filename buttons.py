import pygame


class Button:

    def __init__(self, ai_game, msg, path, x, y, color_text=(255, 255, 255)):
        """Инициализирует атрибуты кнопки"""

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen_rect

        # Назначение размеров и свойств кнопок
        self.width, self.height = 200, 50
        self.button_color = self.settings.green
        self.text_color = color_text
        self.font = pygame.font.SysFont(None, 48)

        # Построение rect кнопки и выравнивание по центру
        self.button = pygame.image.load(path)
        self.button_rect = self.button.get_rect()
        self.button_rect.x = x
        self.button_rect.y = y

        # Сообщение кнопки создается только 1 раз
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Преобразует msg в прямоугольник и выравнивает текст по центру"""
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.button_rect.center

    def draw_button(self):
        """Отображение пустой кнопки и вывод текста"""
        self.screen.blit(self.button, self.button_rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
