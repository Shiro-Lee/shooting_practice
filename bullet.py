import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):

    def __init__(self, settings, screen, gun):
        super().__init__()
        self.screen = screen

        # 在(0,0)处创建一个表示子弹的矩形，再设置正确的位置（从枪口发射）
        self.rect = pygame.Rect(0, 0, settings.bullet_width, settings.bullet_height)
        self.rect.centery = gun.rect.centery
        self.rect.right = gun.rect.right

        # 存储用小数表示的子弹位置
        self.x = float(self.rect.x)

        self.color = settings.bullet_color
        self.speed = settings.bullet_speed

    def update(self):
        """向右移动子弹"""

        # 更新表示子弹位置的小数值
        self.x += self.speed
        # 更新表示子弹的rect的位置
        self.rect.x = self.x

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)
