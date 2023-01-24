import sys
import pygame

class AlienInvansion():
    '''Класс для управления ресурсами и поведением игры.'''

    def __init__(self):
        '''Инициализируем игру и создаём игровые ресурсы'''
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption('Alien Invansion')

    def run_game(self):
        '''Запуск основного цикла игры.'''
        while True:
            # отслеживание событий клавиатуры и мыши
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # отображение последнего прорисованного экрана
            pygame.display.flip()

if __name__ == '__main__':
    ai = AlienInvansion()
    ai.run_game()



