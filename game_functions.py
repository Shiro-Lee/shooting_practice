import sys
from game_stats import GameState
from bullet import Bullet
from target import UniformTarget, AccelerateTarget
from notice_bar import NoticeBar
from target_list import target_list as tl
from music_and_sound import *


def check_events(settings, screen, stats, infos, gun, targets, bullets, textbox, play_button, notice_bars):
    """处理事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # 关闭窗口时退出游戏
            stop_timers(stats, targets, notice_bars)
            sys.exit()
        elif event.type == pygame.KEYDOWN:  # 按下按键
            check_keydown_events(event, settings, screen, stats, infos, gun, targets, bullets, textbox, notice_bars)
        elif event.type == pygame.KEYUP:    # 放开按键
            check_keyup_events(event, gun)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:    # 单击鼠标左键
            if stats.game_state == GameState.PREGAME:   # 游戏未开始时，单击按钮开始游戏
                mouse_x, mouse_y = pygame.mouse.get_pos()
                check_play_button(settings, screen, stats, infos, gun, targets, bullets, textbox, play_button, mouse_x, mouse_y, notice_bars)
            elif stats.game_state == GameState.RUNNING:   # 游戏开始时，单击发射子弹
                fire_bullet(settings, screen, stats, infos, gun, bullets)


def check_play_button(settings, screen, stats, infos, gun, targets, bullets, textbox, play_button, mouse_x, mouse_y, notice_bars):
    """在玩家单击Play按钮时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and textbox.text != '':   # 开始按钮被点击且输入玩家昵称不为空时开始游戏
        stats.player_name = textbox.text
        start_game(settings, screen, stats, infos, gun, targets, bullets, notice_bars)


def check_keydown_events(event, settings, screen, stats, infos, gun, targets, bullets, textbox, notice_bars):
    """响应按下按键"""
    if stats.game_state == GameState.PREGAME:   # 游戏未开始，输入玩家昵称
        textbox.key_down(event)
        textbox.prep_text()
    elif stats.game_state == GameState.RUNNING:   # 游戏开始，处理相应事件
        if event.key == pygame.K_UP or event.key == pygame.K_w:     # 按上方向键或w键向上移动枪支
            gun.moving_up = True
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:     # 按下方向键或s键向下移动枪支
            gun.moving_down = True
        elif event.key == pygame.K_z:   # 按z键发射子弹
            fire_bullet(settings, screen, stats, infos, gun, bullets)
    if event.key == pygame.K_ESCAPE:    # 按esc键退出游戏
        stop_timers(stats, targets, notice_bars)
        sys.exit()


def check_keyup_events(event, gun):
    """响应松开按键"""
    if event.key == pygame.K_UP or event.key == pygame.K_w:
        gun.moving_up = False
    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
        gun.moving_down = False


def stop_timers(stats, targets, notice_bars):
    """停止所有计时器"""
    stats.stop_timer()
    for target in targets.sprites():
        target.stop_timer()
        target.stop_shield_timer()
    for notice_bar in notice_bars.sprites():
        notice_bar.stop_timer()


def start_game(settings, screen, stats, infos, gun, targets, bullets, notice_bars):
    # 隐藏光标
    pygame.mouse.set_visible(False)
    # 重置游戏统计信息
    stats.game_state = GameState.RUNNING
    stats.reset_stats()
    # 重置游戏数据图像
    infos.prep_bullets()
    infos.prep_timer()
    # 清空靶机列表、子弹列表和提示条列表
    targets.empty()
    bullets.empty()
    notice_bars.empty()
    # 播放背景音乐
    pygame.mixer.music.play(-1)
    # 创建第一轮靶机
    create_targets(settings, screen, stats, targets, tl)
    # 枪支居中
    gun.center_gun()
    # 靶机移动提示
    prep_new_round(settings, screen, targets, notice_bars)
    # 开始计时
    stats.start_timer()


def game_over(stats, infos, targets, notice_bars):
    """弹药用尽，游戏结束"""
    stats.game_state = GameState.PREGAME    # 应改为GameState.GAMEOVER！！
    pygame.mouse.set_visible(True)
    stop_timers(stats, targets, notice_bars)
    stats.new_timer()
    infos.new_timer()


def prep_new_round(settings, screen, targets, notice_bars):
    """靶机移动提示条"""
    for target in targets.sprites():
        notice_bar = NoticeBar(settings, screen, target)
        notice_bar.start_timer()
        notice_bars.add(notice_bar)


def fire_bullet(settings, screen, stats, infos, gun, bullets):
    """如果还没有达到限制，就发射一颗子弹"""
    # 创建新子弹，并将其加入到编组bullets中
    if len(bullets) < settings.bullets_allowed:
        fire_sound.play()
        stats.bullet_left -= 1
        infos.prep_bullets()
        new_bullet = Bullet(settings, screen, gun)
        bullets.add(new_bullet)


def update_bullets(settings, screen, stats, infos, gun, targets, bullets, notice_bars):
    """更新子弹位置，并删除已消失的子弹"""
    bullets.update()
    check_bullet_target_collisions(settings, screen, stats, gun, targets, bullets, notice_bars)
    for bullet in bullets.copy():
        if bullet.rect.left >= screen.get_rect().right:
            bullets.remove(bullet)
            if stats.bullet_left <= 0 and stats.target_left:
                game_over(stats, infos, targets, notice_bars)


def update_targets(targets):
    """检查靶机是否到达边缘，并更新靶机位置"""
    check_target_edges(targets)
    targets.update()


def update_notice(notice_bars):
    """更新提示条"""
    for notice_bar in notice_bars.sprites():
        if notice_bar.timer.pass_time > 1:  # 提示条出现1秒后消失
            notice_bar.stop_timer()
            notice_bars.remove(notice_bar)
    notice_bars.update()


def check_bullet_target_collisions(settings, screen, stats, gun, targets, bullets, notice_bars):
    """响应子弹和靶机的碰撞"""
    collisions = pygame.sprite.groupcollide(bullets, targets, False, True)
    target_life = 0
    if collisions:
        for target in targets.sprites():    # 统计总的靶机生命值
            target_life += target.life
        if target_life == 0:  # 该轮靶机全部击破，进入下一轮
            stats.target_left = False
            if stats.round == settings.max_round:
                stats.stop_timer()
                show_result(stats)
            else:
                stats.round += 1
                create_targets(settings, screen, stats, targets, tl)
                prep_new_round(settings, screen, targets, notice_bars)


def create_targets(settings, screen, stats, targets, target_list=tl):
    """创建靶机"""
    stats.target_left = True
    for target_attribute in target_list[stats.round-1]:
        if target_attribute[1]:     # target_attribute[1]为True，创建变速靶
            target = AccelerateTarget(settings, screen, *target_attribute)
        else:   # 否则创建匀速靶
            target = UniformTarget(settings, screen, *target_attribute)
        if target.args[3]:  # target_attribute[3]为True，靶机带盾
            target.start_shield_timer()
        target.start_timer()
        targets.add(target)


def draw_target_sample(settings, target_sample, screen):
    """绘制靶机示例"""
    x = settings.x_target_position
    y = settings.y_target_boundary
    target_width = target_sample.rect.width
    for i in range(4):
        screen.blit(target_sample.image, [x+i*target_width*2, y])


def check_target_edges(targets):
    """有靶机到达边缘时更换方向"""
    for target in targets.sprites():
        if target.check_edges():
            target.direction *= -1


def show_result(stats):
    print(round(stats.timer.pass_time, 2), stats.bullet_left)


def update_screen(settings, screen, stats, infos, gun, target_sample, targets, bullets, notice_bars, text_box, play_button):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环时重绘屏幕
    screen.fill(settings.bg_color)
    if stats.round != settings.max_round:
        draw_target_sample(settings, target_sample, screen)
    gun.blitme()
    targets.draw(screen)
    for notice_bar in notice_bars.sprites():
        notice_bar.draw_bar()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    if stats.timer.time_change:
        infos.prep_timer()
    infos.show_infos()

    # 如果游戏处在非活动状态就绘制Play按钮
    if stats.game_state == GameState.PREGAME:
        play_button.draw_button()
        text_box.draw_textbox()

    # 让最近绘制的屏幕可见
    pygame.display.flip()
