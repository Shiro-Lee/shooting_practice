import pygame
import os
import game_functions as func
from pygame.sprite import Group
from gun import Gun
from game_stats import GameStats, GameState
from settings import Settings
from info_board import InfoBoard
from my_timer import MyTimer
from button import Button
from text_box import TextBox
from target import TargetSample


def run_game():

    pygame.init()

    # 设置窗口
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (128, 60)
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Shooting Practice")

    # 背景图
    background = pygame.image.load('images/background.jpg').convert()

    # 创建枪支、子弹编组
    gun = Gun(settings, screen)
    bullets = Group()

    # 创建全局计时器
    timer = MyTimer()

    # 创建用于存储游戏统计信息的实例，并创建信息显示板
    stats = GameStats(settings, timer)
    infos = InfoBoard(settings, screen, stats)

    # 创建靶机编组、提示条编组
    target_sample = TargetSample()
    targets = Group()
    notice_bars = Group()

    # 创建输入框、开始按钮
    text_box = TextBox(screen, stats, func.start_game, settings, screen,
                       stats, infos, gun, targets, bullets, notice_bars)
    play_button = Button(screen, text_box, '- Play -')

    # 开始游戏主循环
    while True:

        func.check_events(settings, screen, stats, infos, gun, targets, bullets, text_box, play_button, notice_bars)
        if stats.game_state == GameState.RUNNING:
            gun.update()
            func.update_bullets(settings, screen, stats, infos, gun, targets, bullets, notice_bars)
            func.update_notice(notice_bars)
            func.update_targets(targets)
        func.update_screen(background, settings, screen, stats, infos, gun,
                           target_sample, targets, bullets, notice_bars, text_box, play_button)


run_game()
