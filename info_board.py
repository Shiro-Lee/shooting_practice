import pygame.font


class InfoBoard:
    """显示时间、剩余弹药等文本信息的类"""

    def __init__(self, settings, screen, stats):
        """初始化时间、弹药属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.stats = stats
        self.timer = stats.timer

        self.bullet_image = pygame.image.load('images/bullet.png')
        self.bullet_rect = self.bullet_image.get_rect()
        self.bullet_rect.left, self.bullet_rect.top = self.settings.screen_width/15, settings.screen_height/15
        self.timer_image, self.timer_rect = None, None
        self.bullet_left_image, self.bullet_left_rect = None, None

        # 字体设置
        self.text_color = (0, 0, 0)
        self.bullet_font = pygame.font.SysFont('arial', 70)
        self.timer_font = pygame.font.SysFont('arial', 48)

        self.prep_bullets()
        self.prep_timer()

    def prep_bullets(self):
        # 将剩余弹药数转换为渲染图像
        bullet_str = str(self.stats.bullet_left)
        self.bullet_left_image = self.bullet_font.render(bullet_str, True, self.text_color, None)
        # 将剩余弹药数显示在弹药图案右方
        self.bullet_left_rect = self.bullet_left_image.get_rect()
        self.bullet_left_rect.left = self.bullet_rect.right + 10
        self.bullet_left_rect.centery = self.bullet_rect.centery

    def prep_timer(self):
        self.timer.time_change = False
        self.timer.set_time_str()
        # 将计时数转换为渲染图像
        time_str = self.timer.time_str
        self.timer_image = self.timer_font.render(time_str, True, self.text_color, None)
        # 将计时数显示在左下角
        self.timer_rect = self.timer_image.get_rect()
        self.timer_rect.left = self.settings.screen_width/15
        self.timer_rect.bottom = self.screen_rect.bottom - self.settings.screen_height/15

    def show_infos(self):
        self.screen.blit(self.bullet_image, self.bullet_rect)
        self.screen.blit(self.bullet_left_image, self.bullet_left_rect)
        self.screen.blit(self.timer_image, self.timer_rect)

    def new_timer(self):
        self.timer = self.stats.timer
