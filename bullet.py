import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """子弹类"""

    def __init__(self, settings, screen, gun):
        super().__init__()
        self.screen = screen

        # 从枪口发射子弹
        self.image = pygame.image.load('images/bullet.png')
        self.rect = self.image.get_rect()
        self.rect.centery = gun.rect.centery
        self.rect.right = gun.rect.right

        # 存储用小数表示的子弹位置
        self.x = float(self.rect.x)
        self.speed = settings.bullet_speed

    def update(self):
        """向右移动子弹"""
        # 更新表示子弹位置的小数值
        self.x += self.speed
        # 更新表示子弹的rect的位置
        self.rect.x = self.x

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        self.screen.blit(self.image, self.rect)
