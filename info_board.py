import pygame.font
from button import Button
from game_stats import GameState


class RunningInfo:
    """显示游戏进行时的时间、剩余弹药等信息的类"""

    def __init__(self, settings, screen, stats):
        """初始化时间、弹药属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.stats = stats
        self.timer = stats.overall_timer

        self.bullet_image = pygame.image.load('images/bullet.png')
        self.bullet_rect = self.bullet_image.get_rect()
        self.bullet_rect.left, self.bullet_rect.top = self.settings.screen_width/15, settings.y_target_boundary
        self.timer_image, self.timer_rect = None, None
        self.bullet_left_image, self.bullet_left_rect = None, None

        # 字体设置
        self.text_color = (0, 0, 0)
        self.bullet_font = pygame.font.SysFont('华文彩云', 70)
        self.timer_font = pygame.font.SysFont('华文琥珀', 48)

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

    def show_info(self):
        self.screen.blit(self.bullet_image, self.bullet_rect)
        self.screen.blit(self.bullet_left_image, self.bullet_left_rect)
        self.screen.blit(self.timer_image, self.timer_rect)

    def new_timer(self):
        self.timer = self.stats.overall_timer


class WinInfo:
    """游戏胜利信息显示"""

    def __init__(self, settings, screen, stats):
        self.screen = screen
        self.stats = stats
        self.win_font = pygame.font.SysFont('华文琥珀', 60)
        self.stats_font = pygame.font.SysFont('黑体', 28)
        self.text_color = (0, 0, 0)
        self.bullet_left_info, self.bullet_left_info_image, self.bullet_left_info_rect = None, None, None
        self.time_used_info, self.time_used_info_image, self.time_used_info_rect = None, None, None
        self.total_score_info, self.total_score_info_image, self.total_score_rect = None, None, None
        self.win_image = self.win_font.render('YOU WIN', True, self.text_color)
        self.win_rect = self.win_image.get_rect()
        self.win_rect.centerx, self.win_rect.top = self.screen.get_rect().centerx, settings.y_target_boundary

    def prep_score(self):
        # 剩余弹药得分
        self.bullet_left_info = 'Bullet left score: ' + str(self.stats.bullet_left_score)
        self.bullet_left_info_image = self.stats_font.render(self.bullet_left_info, True, self.text_color)
        self.bullet_left_info_rect = self.bullet_left_info_image.get_rect()
        self.bullet_left_info_rect.centerx = self.win_rect.centerx
        self.bullet_left_info_rect.top = self.win_rect.bottom + 10
        # 耗时得分
        self.time_used_info = 'Time used score: ' + str(self.stats.time_used_score)
        self.time_used_info_image = self.stats_font.render(self.time_used_info, True, self.text_color)
        self.time_used_info_rect = self.time_used_info_image.get_rect()
        self.time_used_info_rect.centerx = self.win_rect.centerx
        self.time_used_info_rect.top = self.bullet_left_info_rect.bottom
        # 总分
        self.total_score_info = 'Total score: ' + str(self.stats.total_score)
        self.total_score_info_image = self.stats_font.render(self.total_score_info, True, self.text_color)
        self.total_score_rect = self.total_score_info_image.get_rect()
        self.total_score_rect.centerx = self.win_rect.centerx
        self.total_score_rect.top = self.time_used_info_rect.bottom

    def show_info(self):
        self.screen.blit(self.win_image, self.win_rect)
        self.screen.blit(self.bullet_left_info_image, self.bullet_left_info_rect)
        self.screen.blit(self.time_used_info_image, self.time_used_info_rect)
        self.screen.blit(self.total_score_info_image, self.total_score_rect)


class FailedInfo:
    """游戏失败信息显示"""
    def __init__(self, screen, stats, start_game=None, *args):

        self.screen = screen
        self.stats = stats
        self.start_game = start_game
        self.args = args

        self.failed_text = 'YOU FAILED'
        self.failed_font = pygame.font.SysFont('华文琥珀', 60)
        self.text_color = (0, 0, 0)
        self.text_image = self.failed_font.render(self.failed_text, True, self.text_color)
        self.failed_rect = self.text_image.get_rect()
        self.failed_rect.center = self.screen.get_rect().center

        self.restart_button = Button(screen, '- Restart -')
        self.restart_button.rect.centerx = self.failed_rect.centerx
        self.restart_button.rect.top = self.failed_rect.bottom + 10
        self.restart_button.prep_msg()

    def key_down(self, event):
        if self.stats.game_state == GameState.GAME_OVER:
            if event.key == pygame.K_RETURN:  # 回车键
                self.start_game(*self.args)

    def show_info(self):
        self.screen.blit(self.text_image, self.failed_rect)
        self.restart_button.draw_button()
