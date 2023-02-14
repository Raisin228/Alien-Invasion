# import pygame
# from pygame.sprite import Sprite
# from settings import Settings
#
#
# class Explosion(Sprite):
#     """Класс для анимации взрыва инопланетян"""
#
#     def __init__(self, center):
#         super().__init__()
#         self.settings = Settings()
#         self.frame = 0
#         self.image = self.settings.boom_list[self.frame]
#         self.rect_boom = self.image.get_rect()
#         self.rect_boom.center = center
#         self.last_update = pygame.time.get_ticks()
#         self.frame_rate = 50
#
#     def update(self):
#         now = pygame.time.get_ticks()
#         if now - self.last_update >= self.frame_rate:
#             self.last_update = now
#             self.frame += 1
#             if self.frame == len(self.settings.boom_list):
#                 self.kill()
#             else:
#                 center = self.rect.center
#                 self.image = self.settings.boom_list[self.frame]
#                 self.rect_boom = self.image.get_rect()
#                 self.rect_boom.center = center