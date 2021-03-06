import sys
from game_stats import GameState
from bullet import Bullet
from target import UniformTarget, AccelerateTarget
from notice_bar import NoticeBar
from target_list import target_list as tl
from music_and_sound import *
from info_board import RankState


def check_events(settings, screen, stats, running_info, win_info, failed_info,
                 gun, targets, bullets, pregame_info, notice_bars):
    """处理事件"""
    for event in pygame.event.get():
        # 游戏未开始
        if stats.game_state == GameState.PREGAME:
            check_pregame_events(event, settings, screen, stats, targets, pregame_info, notice_bars)
        # 游戏进行中
        elif stats.game_state == GameState.RUNNING:
            check_running_events(event, settings, screen, stats, running_info, gun, bullets)
        # 游戏胜利或失败
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    reset_game(stats, running_info, targets, bullets, notice_bars, gun)
                elif event.key == pygame.K_SPACE and stats.game_state == GameState.GAME_FINISH:
                    win_info.switch_top10()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if stats.game_state == GameState.GAME_FINISH:
                    check_restart_button(stats, win_info, running_info,
                                         targets, bullets, notice_bars, gun, mouse_x, mouse_y)
                    check_show_tops_button(win_info, mouse_x, mouse_y)
                elif stats.game_state == GameState.GAME_OVER:
                    check_restart_button(stats, failed_info, running_info,
                                         targets, bullets, notice_bars, gun, mouse_x, mouse_y)
        # 关闭窗口或按esc键时退出游戏
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            stop_timers(stats, targets, notice_bars)
            sys.exit()


def check_pregame_events(event, settings, screen, stats, targets, pregame_info, notice_bars):
    """检查开始界面事件"""
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            if pregame_info.player_name != '':  # 按下回车且输入玩家昵称不为空时开始游戏
                stats.player_name = pregame_info.player_name
                start_game(settings, screen, stats, targets, notice_bars)
        else:  # 输入玩家名
            pregame_info.key_down(event)
            pregame_info.prep_player_name()
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 单击鼠标左键
        mouse_x, mouse_y = pygame.mouse.get_pos()
        check_sound_button(pregame_info, mouse_x, mouse_y)
        check_play_button(settings, screen, stats, targets, pregame_info, mouse_x, mouse_y, notice_bars)


def check_running_events(event, settings, screen, stats, running_info, gun, bullets):
    """检查游戏中事件"""
    if event.type == pygame.KEYDOWN:  # 按下按键
        if event.key == pygame.K_UP or event.key == pygame.K_w:  # 按上方向键或w键向上移动枪支
            gun.moving_up = True
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:  # 按下方向键或s键向下移动枪支
            gun.moving_down = True
        elif event.key == pygame.K_z:  # 按z键发射子弹
            fire_bullet(settings, screen, stats, running_info, gun, bullets)
    elif event.type == pygame.KEYUP:  # 放开按键
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            gun.moving_up = False
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            gun.moving_down = False
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 单击发射子弹
        fire_bullet(settings, screen, stats, running_info, gun, bullets)


def check_play_button(settings, screen, stats, targets, pregame_info, mouse_x, mouse_y, notice_bars):
    """在玩家单击Play按钮时开始新游戏"""
    button_clicked = pregame_info.play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and pregame_info.player_name != '':   # 开始按钮被点击且输入玩家昵称不为空时开始游戏
        stats.player_name = pregame_info.player_name
        start_game(settings, screen, stats, targets, notice_bars)


def check_sound_button(pregame_info, mouse_x, mouse_y):
    """检查声音按钮是否被按下"""
    button_clicked = pregame_info.sound_rect.collidepoint(mouse_x, mouse_y)
    if button_clicked:   # 开始按钮被点击且输入玩家昵称不为空时开始游戏
        pregame_info.switch_sound()


def check_restart_button(stats, finish_over_info, running_info, targets, bullets, notice_bars, gun, mouse_x, mouse_y):
    """检查重新开始按钮"""
    button_clicked = finish_over_info.restart_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked:
        reset_game(stats, running_info, targets, bullets, notice_bars, gun)
        stats.game_state = GameState.PREGAME


def stop_timers(stats, targets, notice_bars):
    """停止所有计时器"""
    stats.stop_timer()
    for target in targets.sprites():
        target.stop_timer()
        target.stop_shield_timer()
    for notice_bar in notice_bars.sprites():
        notice_bar.stop_timer()


def reset_game(stats, running_info, targets, bullets, notice_bars, gun):
    """重置游戏信息"""
    # 设置游戏状态为准备
    stats.game_state = GameState.PREGAME
    # 重置游戏统计信息
    stats.reset_stats()
    # 停止bgm
    pygame.mixer.music.stop()
    # 重置游戏数据图像
    running_info.prep_bullets()
    running_info.prep_timer()
    # 清空靶机列表、子弹列表和提示条列表
    targets.empty()
    bullets.empty()
    notice_bars.empty()
    # 重置剩余弹药数提示条
    running_info.bullet_left_bar.width = stats.bullet_left
    running_info.bullet_left_bar_color = (0, 180, 0)
    # 枪支居中
    gun.center_gun()


def start_game(settings, screen, stats, targets, notice_bars):
    """开始游戏"""
    # 设置游戏状态为进行中
    stats.game_state = GameState.RUNNING
    # 隐藏光标
    pygame.mouse.set_visible(False)
    # 播放背景音乐
    if stats.sound_state:
        pygame.mixer.music.play(-1)
    # 创建第一轮靶机
    create_targets(settings, screen, stats, targets, tl)
    # 靶机移动提示
    prep_new_round(settings, screen, targets, notice_bars)
    # 开始计时
    stats.start_timer()


def game_over(stats, targets, notice_bars):
    """弹药用尽，游戏失败"""
    stats.game_state = GameState.GAME_OVER
    pygame.mouse.set_visible(True)
    stop_timers(stats, targets, notice_bars)
    stats.new_timer()


def game_finish(stats, win_info, io_helper):
    """击破全部靶机，游戏胜利"""
    stats.game_state = GameState.GAME_FINISH
    stats.game_finish()
    win_info.rank_state = RankState.WIN_INFO
    win_info.prep_button_msg('- Show Top10 -')
    pygame.mouse.set_visible(True)
    win_info.prep_score()
    io_helper.check_player()


def prep_new_round(settings, screen, targets, notice_bars):
    """靶机移动提示条"""
    for target in targets.sprites():
        notice_bar = NoticeBar(settings, screen, target)
        notice_bar.start_timer()
        notice_bars.add(notice_bar)


def fire_bullet(settings, screen, stats, running_info, gun, bullets):
    """如果还没有达到限制，就发射一颗子弹"""
    # 创建新子弹，并将其加入到编组bullets中
    if len(bullets) < settings.bullets_allowed and stats.bullet_left > 0:
        if stats.sound_state:
            fire_sound.play()
        stats.bullet_left -= 1
        running_info.prep_bullet_left_bar()
        running_info.prep_bullets()
        new_bullet = Bullet(settings, screen, gun)
        bullets.add(new_bullet)


def check_bullet_target_collisions(stats, targets, bullets):
    """响应子弹和靶机的碰撞"""
    collisions = pygame.sprite.groupcollide(bullets, targets, False, True)
    target_life = 0
    if collisions:
        for target in targets.sprites():    # 统计总的靶机生命值
            target_life += target.life
        if target_life == 0:  # 该轮靶机全部击破
            stats.target_left = False


def create_targets(settings, screen, stats, targets, target_list=tl):
    """创建靶机"""
    stats.target_left = True
    for target_attribute in target_list[stats.round-1]:
        if target_attribute[1]:     # target_attribute[1]为True，创建变速靶
            target = AccelerateTarget(settings, stats, screen, *target_attribute)
        else:   # 否则创建匀速靶
            target = UniformTarget(settings, stats, screen, *target_attribute)
        if target.args[3]:  # target_attribute[3]为True，靶机带盾
            target.start_shield_timer()
        target.start_timer()
        targets.add(target)


def check_show_tops_button(win_info, mouse_x, mouse_y):
    """检查显示排行榜按钮"""
    button_clicked = win_info.show_tops_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked:
        win_info.switch_top10()


def update_bullets(settings, screen, stats, targets, bullets, notice_bars, win_info, io_helper):
    """更新子弹位置，并删除已消失的子弹，同时判定游戏是否结束"""
    bullets.update()
    check_bullet_target_collisions(stats, targets, bullets)
    for bullet in bullets.copy():
        if bullet.rect.left >= screen.get_rect().right:
            bullets.remove(bullet)
            if stats.bullet_left <= 0:
                if stats.target_left or stats.round != settings.max_round:    # 最后一枚子弹消失时若还有靶机未击破，则游戏失败
                    game_over(stats, targets, notice_bars)
                    return
            if not stats.target_left:
                if stats.round == settings.max_round:   # 当前为最后一轮
                    game_finish(stats, win_info, io_helper)
                else:   # 进入下一轮
                    stats.round += 1
                    create_targets(settings, screen, stats, targets, tl)
                    prep_new_round(settings, screen, targets, notice_bars)


def update_targets(targets):
    """检查靶机是否到达边缘，并更新靶机位置"""
    for target in targets.sprites():
        if target.check_edges():
            target.direction *= -1
    targets.update()


def update_notice(notice_bars):
    """更新提示条"""
    for notice_bar in notice_bars.sprites():
        if notice_bar.timer.pass_time > 1:  # 提示条出现1秒后消失
            notice_bar.stop_timer()
            notice_bars.remove(notice_bar)
    notice_bars.update()


def draw_target_sample(settings, target_sample, screen):
    """绘制靶机示例"""
    x = settings.x_target_position
    y = settings.y_target_boundary
    target_width = target_sample.rect.width
    for i in range(4):
        screen.blit(target_sample.image, [x+i*target_width*2, y])


def common_update_screen(background, settings, screen, stats, running_info,
                         gun, target_sample, targets, bullets, notice_bars):
    """更新屏幕上的图像，并切换到新屏幕"""
    screen.blit(background, (0, 0))
    if stats.round != settings.max_round:   # 未到最后一轮则绘制四个靶机示例（最后一轮必须为四个靶机）
        draw_target_sample(settings, target_sample, screen)
    gun.blitme()
    targets.draw(screen)
    for notice_bar in notice_bars.sprites():
        notice_bar.draw_bar()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    if stats.overall_timer.time_change:
        running_info.prep_timer()
    running_info.show_info()
