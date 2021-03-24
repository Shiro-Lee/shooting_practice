import pygame


class Gun:

    def __init__(self, settings, screen):
        """初始化枪支并设置初始位置"""
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # 加载枪支图像并获取其外接矩形
        self.image = pygame.image.load('images/gun.png')
        self.rect = self.image.get_rect()

        # 枪支初始位置在左侧中央
        self.rect.centery = self.screen_rect.centery
        self.rect.centerx = self.settings.x_gun_position

        # 在枪支的属性center中存储小数值
        self.centery = float(self.rect.centery)

        # 移动标志
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """根据移动标志调整枪支的位置"""
        if self.moving_up and self.rect.top >= self.settings.y_gun_boundary:
            self.centery -= self.settings.gun_speed
        if self.moving_down and self.rect.bottom <= self.screen_rect.bottom - self.settings.y_gun_boundary:
            self.centery += self.settings.gun_speed
        self.rect.centery = self.centery

    def blitme(self):
        """在指定位置绘制枪支"""
        self.screen.blit(self.image, self.rect)
