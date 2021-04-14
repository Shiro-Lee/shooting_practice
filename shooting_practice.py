import pygame
import os
import game_functions as func
from pygame.sprite import Group
from gun import Gun
from game_stats import GameStats, GameState
from settings import Settings
from info_board import PregameInfo, RunningInfo, WinInfo, FailedInfo
from my_timer import MyTimer
from target import TargetSample
from io_helper import IOHelper


def run_game():

    pygame.init()

    # 设置窗口
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (128, 60)
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Shooting Practice")

    # 背景图
    dir_path = os.path.dirname(os.path.abspath(__file__))
    background = pygame.image.load(dir_path + r'\images\background.jpg').convert()

    # 创建枪支、子弹编组
    gun = Gun(settings, screen)
    bullets = Group()

    # 创建全局计时器
    overall_timer = MyTimer()

    # 创建靶机编组、提示条编组
    target_sample = TargetSample()
    targets = Group()
    notice_bars = Group()

    # 创建用于存储游戏统计信息的实例
    stats = GameStats(settings, overall_timer)

    # 文件读写
    io_helper = IOHelper(stats)

    # 创建信息显示板
    running_info = RunningInfo(settings, screen, stats)
    win_info = WinInfo(settings, screen, stats, io_helper)
    failed_info = FailedInfo(screen, stats)

    # 创建输入框
    pregame_info = PregameInfo(settings, screen, stats)

    # 开始游戏主循环
    while True:
        # 检查事件
        func.check_events(settings, screen, stats, running_info, win_info, failed_info,
                          gun, targets, bullets, pregame_info, notice_bars)
        # 更新屏幕
        func.common_update_screen(background, settings, screen, stats, running_info, gun,
                                  target_sample, targets, bullets, notice_bars)
        # 游戏进行中，更新枪支、子弹、靶机提示条、靶机位置
        if stats.game_state == GameState.RUNNING:
            gun.update()
            func.update_bullets(settings, screen, stats, targets, bullets, notice_bars, win_info, io_helper)
            func.update_notice(notice_bars)
            func.update_targets(targets)
        elif stats.game_state == GameState.PREGAME:
            pregame_info.draw_pregame_info()
        elif stats.game_state == GameState.GAME_OVER:
            failed_info.show_info()
        elif stats.game_state == GameState.GAME_FINISH:
            win_info.show_info()
        # 让最近绘制的屏幕可见
        pygame.display.flip()


run_game()
