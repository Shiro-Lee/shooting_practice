import pygame
from pygame.sprite import Sprite
from my_timer import MyTimer


class NoticeBar(Sprite):
    """靶机启动提示条"""
    def __init__(self, settings, screen, target):
        super().__init__()
        self.settings = settings
        self.screen = screen
        self.rect = pygame.Rect(target.rect.left, target.rect.bottom, target.rect.width, 3)
        self.y = float(self.rect.y)
        self.color = (0, 0, 0)
        self.speed = 3
        self.timer = MyTimer()

    def update(self):
        """向下移动提示条"""
        if self.speed != 0:
            if self.y >= self.screen.get_rect().bottom - self.settings.y_target_boundary:   # 到达底端时停止移动
                self.speed = 0
            else:
                self.y += self.speed
                self.rect.y = self.y

    def draw_bar(self):
        """绘制提示条"""
        pygame.draw.rect(self.screen, self.color, self.rect)

    def start_timer(self):
        self.timer.begin()

    def stop_timer(self):
        self.timer.stop()

    def reset_timer(self):
        self.timer.reset()
