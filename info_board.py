import pygame
from button import Button
from sql_functions import *


class PregameInfo:
    """游戏开始界面"""
    def __init__(self, screen, stats):
        self.width, self.height = 300, 50
        self.text_color = (0, 0, 0)
        self.box_color = (255, 255, 255)
        self.screen = screen
        self.stats = stats
        self.screen_rect = screen.get_rect()
        self.player_name_image, self.player_name_rect = None, None
        self.max_length = 10    # 玩家id最长为10个字符
        # 创建文本框的rect对象，并使其居中
        self.player_name = ''
        self.player_name_font = pygame.font.SysFont('华文琥珀', 32)
        self.box_rect = pygame.Rect(0, 0, self.width, self.height)
        self.box_rect.centerx = self.screen_rect.centerx
        self.box_rect.top = self.screen_rect.centery
        self.prep_player_name()
        # 标题，放在界面上方
        self.title = 'Shooting Practice'
        self.title_font = pygame.font.SysFont('华文琥珀', 72)
        self.title_image = self.title_font.render(self.title, True, self.text_color)
        self.title_rect = self.title_image.get_rect()
        self.title_rect.centerx = self.box_rect.centerx
        self.title_rect.bottom = self.box_rect.top - 64
        # logo，和标题放在一起
        self.logo_image = pygame.image.load('images/logo.png')
        self.logo_rect = self.logo_image.get_rect()
        self.logo_rect.center = self.title_rect.center
        # 创建开始按钮，放在文本框下方
        self.play_button = Button(screen, '- Play -')
        self.play_button.rect.centerx = self.box_rect.centerx
        self.play_button.rect.top = self.box_rect.bottom + 20
        self.play_button.prep_msg()
        # 提示输入玩家名，放在文本框上方
        self.notice = 'Input your name:'
        self.notice_font = pygame.font.SysFont('华文彩云', 28)
        self.notice_image = self.notice_font.render(self.notice, True, self.text_color, None)
        self.notice_rect = self.notice_image.get_rect()
        self.notice_rect.centerx = self.box_rect.centerx
        self.notice_rect.bottom = self.player_name_rect.top - 15

    def prep_player_name(self):
        """将输入玩家名转化为图像"""
        self.player_name_image = self.player_name_font.render(self.player_name, True, self.text_color, self.box_color)
        self.player_name_rect = self.player_name_image.get_rect()
        self.player_name_rect.center = self.box_rect.center

    def draw_pregame_info(self):
        """绘制游戏开始界面"""
        self.screen.blit(self.logo_image, self.logo_rect)
        self.screen.blit(self.title_image, self.title_rect)
        self.screen.blit(self.notice_image, self.notice_rect)
        self.screen.fill(self.box_color, self.box_rect)
        self.screen.blit(self.player_name_image, self.player_name_rect)
        self.play_button.draw_button()

    def key_down(self, event):
        """响应按键"""
        if event.key == pygame.K_BACKSPACE and len(self.player_name) > 0:     # 退格键
            self.player_name = self.player_name[:-1]
        elif event.unicode != ' ':   # 输入除空格以外的字符
            if len(self.player_name) < self.max_length:
                char = event.unicode
                self.player_name += char


class RunningInfo:
    """显示游戏进行时的时间、剩余弹药等信息的类"""
    def __init__(self, settings, screen, stats):
        """初始化时间、弹药属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.stats = stats
        self.timer = stats.overall_timer
        self.bullet_image = pygame.image.load('images/bullet_sample.png')
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
        self.timer_rect.bottom = self.screen_rect.bottom - self.settings.y_target_boundary

    def show_info(self):
        self.screen.blit(self.bullet_image, self.bullet_rect)
        self.screen.blit(self.bullet_left_image, self.bullet_left_rect)
        self.screen.blit(self.timer_image, self.timer_rect)


class WinInfo:
    """游戏胜利信息显示"""
    def __init__(self, settings, screen, stats):
        self.screen = screen
        self.stats = stats
        self.screen_rect = screen.get_rect()
        self.win_font = pygame.font.SysFont('华文琥珀', 60)
        self.stats_font = pygame.font.SysFont('黑体', 36)
        self.text_color = (0, 0, 0)
        self.bullet_left_info, self.bullet_left_info_image, self.bullet_left_info_rect = None, None, None
        self.time_used_info, self.time_used_info_image, self.time_used_info_rect = None, None, None
        self.total_score_info, self.total_score_info_image, self.total_score_rect = None, None, None
        # 游戏胜利提示
        self.win_image = self.win_font.render('YOU WIN', True, self.text_color)
        self.win_rect = self.win_image.get_rect()
        self.win_rect.centerx, self.win_rect.bottom = self.screen_rect.centerx, self.screen_rect.centery
        # 重新开始按钮
        self.restart_button = Button(screen, '- Restart -')
        self.restart_button.rect.centerx = self.win_rect.centerx
        self.restart_button.rect.bottom = self.screen_rect.bottom - settings.y_target_boundary
        self.restart_button.prep_msg()
        # 显示各项得分排行按钮
        self.show_tops_button = Button(screen, '- Show Top10 -')
        self.show_tops_button.rect.centerx = self.win_rect.centerx
        self.show_tops_button.rect.bottom = self.restart_button.rect.top - 20
        self.show_tops_button.prep_msg()

    def prep_score(self):
        # 剩余弹药得分
        self.bullet_left_info = 'Bullet Left Score: ' + str(self.stats.bullet_left_score)
        self.bullet_left_info_image = self.stats_font.render(self.bullet_left_info, True, self.text_color)
        self.bullet_left_info_rect = self.bullet_left_info_image.get_rect()
        self.bullet_left_info_rect.centerx = self.win_rect.centerx
        self.bullet_left_info_rect.top = self.win_rect.bottom + 10
        # 耗时得分
        self.time_used_info = 'Time Used Score: ' + str(self.stats.time_used_score)
        self.time_used_info_image = self.stats_font.render(self.time_used_info, True, self.text_color)
        self.time_used_info_rect = self.time_used_info_image.get_rect()
        self.time_used_info_rect.centerx = self.win_rect.centerx
        self.time_used_info_rect.top = self.bullet_left_info_rect.bottom
        # 总分
        self.total_score_info = 'Total Score: ' + str(self.stats.total_score)
        self.total_score_info_image = self.stats_font.render(self.total_score_info, True, self.text_color)
        self.total_score_rect = self.total_score_info_image.get_rect()
        self.total_score_rect.centerx = self.win_rect.centerx
        self.total_score_rect.top = self.time_used_info_rect.bottom

    def show_info(self):
        self.screen.blit(self.win_image, self.win_rect)
        self.screen.blit(self.bullet_left_info_image, self.bullet_left_info_rect)
        self.screen.blit(self.time_used_info_image, self.time_used_info_rect)
        self.screen.blit(self.total_score_info_image, self.total_score_rect)
        self.restart_button.draw_button()
        self.show_tops_button.draw_button()


class FailedInfo:
    """游戏失败信息显示"""
    def __init__(self, screen, stats):
        self.screen = screen
        self.stats = stats
        self.text_color = (0, 0, 0)
        # 游戏失败提示
        self.failed_text = 'YOU FAILED'
        self.failed_font = pygame.font.SysFont('华文琥珀', 60)
        self.failed_image = self.failed_font.render(self.failed_text, True, self.text_color)
        self.failed_rect = self.failed_image.get_rect()
        self.failed_rect.center = self.screen.get_rect().center
        # 重新开始按钮
        self.restart_button = Button(screen, '- Restart -')
        self.restart_button.rect.centerx = self.failed_rect.centerx
        self.restart_button.rect.top = self.failed_rect.bottom + 10
        self.restart_button.prep_msg()

    def show_info(self):
        self.screen.blit(self.failed_image, self.failed_rect)
        self.restart_button.draw_button()


class Top10Info:
    def __init__(self, settings, screen, mysql_helper):
        self.settings = settings
        self.screen = screen
        self.mysql_helper = mysql_helper
        self.title_font = pygame.font.SysFont('华文琥珀', 60)
        self.text_color = (0, 0, 0)


class BulletTop10(Top10Info):
    """玩家名 剩余弹药数 剩余弹药得分 排名"""
    """1/5 2/5 3/5 4/5"""
    def __init__(self, settings, screen, mysql_helper):
        super().__init__(settings, screen, mysql_helper)
        self.title = 'Bullet Left Top 10'
        self.results = get_top10_bullet(mysql_helper)
        self.columns = ['Player Name', 'Bullet Left', 'Score', 'Rank']
        self.images = []
        self.rects = []
        self.positions = []
        for i in range(1, 5):
            self.positions.append((self.settings.screen_width/5*i, 50))
        for column_num in range(4):
            column_image = self.title_font.render(self.columns[column_num], True, self.text_color)
            self.images.append(column_image)
            rect = column_image.get_rect()
            rect.centerx = self.positions[column_num][0]
            rect.centery = self.positions[column_num][1]
            self.rects.append(rect)

    def show_rank(self):
        for i in range(4):
            self.screen.blit(self.images[i], self.rects[i])


class TimeTop10(Top10Info):
    """玩家名 耗时 耗时得分 排名"""
    """1/5 2/5 3/5 4/5"""
    def __init__(self, settings, screen, mysql_helper):
        super().__init__(settings, screen, mysql_helper)
        self.title = 'Time Used Top 10'
        self.results = get_top10_speed(mysql_helper)

    def show_rank(self):
        pass


class TotalTop10(Top10Info):
    """玩家名 剩余弹药得分 耗时得分 总分 排名"""
    """1/10 3/10 5/10 7/10 9/10"""
    def __init__(self, settings, screen, mysql_helper):
        super().__init__(settings, screen, mysql_helper)
        self.title = 'Total Top 10'
        self.results = get_top10_total(mysql_helper)

    def show_rank(self):
        pass
