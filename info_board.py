import pygame
from button import Button
from enum import Enum
from pygame import gfxdraw
from os import path

dir_path = path.dirname(path.abspath(__file__))


class RankState(Enum):
    """枚举游戏状态"""
    WIN_INFO = 0
    BULLET_TOP10 = 1    # 显示剩余弹药排名
    SPEED_TOP10 = 2     # 显示耗时排名
    TOTAL_TOP10 = 3     # 显示总分排名


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
        self.logo_image = pygame.image.load(dir_path + r'\images\logo.png')
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
        if event.key == pygame.K_BACKSPACE:     # 退格键
            if len(self.player_name) > 0:
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
        self.bullet_image = pygame.image.load(dir_path + r'\images\bullet_sample.png')
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
        """准备剩余弹药信息"""
        # 将剩余弹药数转换为渲染图像
        bullet_str = str(self.stats.bullet_left)
        self.bullet_left_image = self.bullet_font.render(bullet_str, True, self.text_color, None)
        # 将剩余弹药数显示在弹药图案右方
        self.bullet_left_rect = self.bullet_left_image.get_rect()
        self.bullet_left_rect.left = self.bullet_rect.right + 10
        self.bullet_left_rect.centery = self.bullet_rect.centery

    def prep_timer(self):
        """准备计时信息"""
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
        """显示剩余弹药数、计时"""
        self.screen.blit(self.bullet_image, self.bullet_rect)
        self.screen.blit(self.bullet_left_image, self.bullet_left_rect)
        self.screen.blit(self.timer_image, self.timer_rect)


class WinInfo:
    """游戏胜利信息显示"""
    def __init__(self, settings, screen, stats, io_helper):
        self.settings = settings
        self.screen = screen
        self.stats = stats
        self.io_helper = io_helper
        self.rank_state = RankState.WIN_INFO
        self.screen_rect = screen.get_rect()
        self.win_font = pygame.font.SysFont('华文琥珀', 60)
        self.results_font = pygame.font.SysFont('方正姚体', 30)
        self.column_font = pygame.font.SysFont('方正姚体', 36)
        self.text_color = (0, 0, 0)
        self.bullet_left, self.bullet_left_image, self.bullet_left_rect = None, None, None
        self.time_used, self.time_used_image, self.time_used_rect = None, None, None
        self.total_score, self.total_score_image, self.total_score_rect = None, None, None
        self.rank_bg_rect = pygame.Rect(0, 0, 0, 0)  # 排行榜半透明矩形
        self.rank_bg_rect.height, self.rank_bg_rect.top = 410, 125

        # 排行榜标题
        self.rank_title = ''
        self.rank_title_image, self.rank_title_rect = None, None
        self.columns = None
        self.column_images = []
        self.column_rects = []
        self.results = None
        self.result_images = []
        self.result_rects = []

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
        self.show_tops_button = Button(screen, '- Show Top 10 -')
        self.show_tops_button.rect.centerx = self.win_rect.centerx
        self.show_tops_button.rect.bottom = self.restart_button.rect.top - 10
        self.show_tops_button.prep_msg()

    def prep_score(self):
        """准备各项得分"""
        # 剩余弹药得分
        self.bullet_left = 'Bullet Left Score: ' + str(self.stats.bullet_left_score)
        self.bullet_left_image = self.results_font.render(self.bullet_left, True, self.text_color)
        self.bullet_left_rect = self.bullet_left_image.get_rect()
        self.bullet_left_rect.centerx = self.win_rect.centerx
        self.bullet_left_rect.top = self.win_rect.bottom + 10
        # 耗时得分
        self.time_used = 'Time Used Score: ' + str(self.stats.time_used_score)
        self.time_used_image = self.results_font.render(self.time_used, True, self.text_color)
        self.time_used_rect = self.time_used_image.get_rect()
        self.time_used_rect.centerx = self.win_rect.centerx
        self.time_used_rect.top = self.bullet_left_rect.bottom
        # 总分
        self.total_score = 'Total Score: ' + str(self.stats.total_score)
        self.total_score_image = self.results_font.render(self.total_score, True, self.text_color)
        self.total_score_rect = self.total_score_image.get_rect()
        self.total_score_rect.centerx = self.win_rect.centerx
        self.total_score_rect.top = self.time_used_rect.bottom

    def prep_title(self):
        """准备排行标题"""
        self.rank_title_image = self.win_font.render(self.rank_title, True, self.text_color)
        self.rank_title_rect = self.rank_title_image.get_rect()
        self.rank_title_rect.centerx = self.screen.get_rect().centerx
        self.rank_title_rect.top = self.settings.y_target_boundary

    def show_info(self):
        """显示得分/排行榜"""
        if self.rank_state == RankState.WIN_INFO:
            self.screen.blit(self.win_image, self.win_rect)
            self.screen.blit(self.bullet_left_image, self.bullet_left_rect)
            self.screen.blit(self.time_used_image, self.time_used_rect)
            self.screen.blit(self.total_score_image, self.total_score_rect)
        else:
            self.screen.blit(self.rank_title_image, self.rank_title_rect)
            gfxdraw.box(self.screen, self.rank_bg_rect, (255, 255, 255, 128))
            # 显示列名
            for image, rect in zip(self.column_images, self.column_rects):
                self.screen.blit(image, rect)
            for image, rect in zip(self.result_images, self.result_rects):
                self.screen.blit(image, rect)
        self.restart_button.draw_button()
        self.show_tops_button.draw_button()

    def switch_top10(self):
        """切换显示排行榜"""
        self.result_images.clear()
        self.result_rects.clear()
        if self.rank_state == RankState.WIN_INFO:
            self.prep_button_msg('- Switch Top10 -')
            self.prep_bullet_rank()
        elif self.rank_state == RankState.TOTAL_TOP10:
            self.prep_bullet_rank()
        elif self.rank_state == RankState.BULLET_TOP10:
            self.prep_speed_rank()
        elif self.rank_state == RankState.SPEED_TOP10:
            self.prep_total_rank()
        self.prep_title()
        self.prep_columns(self.columns)
        self.show_tops_button.prep_msg()

    def prep_button_msg(self, msg):
        """更新排行显示切换按钮"""
        self.show_tops_button.msg = msg
        self.show_tops_button.prep_msg()
        self.show_tops_button.rect.centerx = self.win_rect.centerx

    def prep_bullet_rank(self):
        """玩家名 剩余弹药数 剩余弹药得分 排名"""
        self.rank_state = RankState.BULLET_TOP10
        self.rank_title = 'Bullet Left Top10'
        self.columns = ['Player', 'Bullet Left', 'Score', 'Rank']
        self.rank_bg_rect.width = 0.8 * self.settings.screen_width
        self.rank_bg_rect.centerx = self.screen_rect.centerx
        self.results = self.io_helper.get_bullet_top10()
        self.prep_rank()

    def prep_speed_rank(self):
        """玩家名 耗时 耗时得分 排名"""
        self.rank_state = RankState.SPEED_TOP10
        self.rank_title = 'Time Used Top10'
        self.columns = ['Player', 'Time Used', 'Score', 'Rank']
        self.rank_bg_rect.width = 0.8 * self.settings.screen_width
        self.rank_bg_rect.centerx = self.screen_rect.centerx
        self.results = self.io_helper.get_speed_top10()
        self.prep_rank()

    def prep_total_rank(self):
        """玩家名 剩余弹药得分 耗时得分 总分 排名"""
        self.rank_state = RankState.TOTAL_TOP10
        self.rank_title = 'Total Top10'
        self.columns = ['Player', 'Bullet Left Score', 'Time Used Score', 'Total Score', 'Total Rank']
        self.rank_bg_rect.width = 0.95 * self.settings.screen_width
        self.rank_bg_rect.centerx = self.screen_rect.centerx
        self.results = self.io_helper.get_total_top10()
        self.prep_rank()

    def prep_rank(self):
        """准备排行榜数据"""
        interval_x = self.settings.screen_width * 0.2
        interval_y = 35
        start_x = self.settings.screen_width * 0.2 if len(self.columns) == 4 else self.settings.screen_width * 0.1
        start_y = 200
        i, j = 0, 0
        # 准备显示玩家名
        for result in self.results:
            player_name_image = self.results_font.render(result[0], True, self.text_color)
            player_name_rect = player_name_image.get_rect()
            player_name_rect.centerx = start_x
            player_name_rect.centery = start_y + j * interval_y
            self.result_images.append(player_name_image)
            self.result_rects.append(player_name_rect)
            j += 1
        j = 0
        # 准备显示得分数据
        for result in self.results:
            i = 1
            centery = start_y + j * interval_y
            for value in result[1].values():
                result_image = self.results_font.render(str(value), True, self.text_color)
                result_rect = result_image.get_rect()
                result_rect.centerx = start_x + i * interval_x
                result_rect.centery = centery
                self.result_images.append(result_image)
                self.result_rects.append(result_rect)
                i += 1
            j += 1

    def prep_columns(self, columns):
        """准备列名"""
        interval_x = self.settings.screen_width * 0.2
        start_x = self.settings.screen_width * 0.2 if len(columns) == 4 else self.settings.screen_width * 0.1
        self.column_images.clear()
        self.column_rects.clear()
        i = 0
        for column in columns:
            column_image = self.column_font.render(column, True, self.text_color)
            column_rect = column_image.get_rect()
            column_rect.centery = 150
            column_rect.centerx = start_x + i * interval_x
            i += 1
            self.column_images.append(column_image)
            self.column_rects.append(column_rect)


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
        """显示游戏失败提示及重新开始按钮"""
        self.screen.blit(self.failed_image, self.failed_rect)
        self.restart_button.draw_button()
