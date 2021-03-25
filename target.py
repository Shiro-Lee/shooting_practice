import pygame
from pygame.sprite import Sprite
from my_timer import MyTimer
from music_and_sound import target_broken_sound, shield_broken_sound


class TargetSample:
    """靶机示例类"""

    def __init__(self):
        # 加载靶机图像并获取其rect属性
        self.image = pygame.image.load('images/target.png')
        self.rect = self.image.get_rect()


class Target(TargetSample, Sprite):
    """靶机类"""

    def __init__(self, settings, screen, *args):
        """初始化靶机并设置其起始位置"""

        TargetSample.__init__(self)
        Sprite.__init__(self)
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.args = args

        # 靶机初始位置
        self.rect.x = self.settings.x_target_position + args[0] * self.rect.width * 2
        self.rect.y = self.settings.y_target_boundary

        # 存储靶机准确位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.timer = MyTimer()
        self.shield_timer = MyTimer()
        self.moving = False

        self.delay = self.args[4]   # 靶机延时启动时长
        if self.args[3]:    # 带盾
            self.image = pygame.image.load('images/target_shield.png')
            self.life = 2
        else:   # 无盾
            self.life = 1

    def update_shield(self):
        if self.args[3] and self.shield_timer.pass_time > 5:    # 带盾靶机每5秒会重新生成护盾
            self.shield_timer.reset()
            if self.life < 2:
                self.image = pygame.image.load('images/target_shield.png')
                self.life = 2

    def check_edges(self):
        """如果靶机位于活动范围边缘，就返回True"""
        if self.rect.bottom > self.screen_rect.bottom - self.settings.y_target_boundary:
            return True
        elif self.rect.top < self.settings.y_target_boundary:
            return True
        return False

    def blitme(self):
        """在指定位置绘制靶机"""
        self.screen.blit(self.image, self.rect)

    def kill(self):
        """重写kill()，响应靶机被击中"""
        if self.timer.pass_time > 0.5:  # 0.5秒内的碰撞视为击中同一个靶机
            if self.life > 1:   # 击破护盾
                shield_broken_sound.play()
                self.life -= 1
                self.image = pygame.image.load('images/target.png')
                self.timer.reset()
            else:   # 击破靶机
                target_broken_sound.play()
                self.timer.stop()
                self.shield_timer.stop()
                super().kill()

    def start_timer(self):
        self.timer.begin()

    def stop_timer(self):
        self.timer.stop()

    def reset_timer(self):
        self.timer.reset()

    def start_shield_timer(self):
        self.shield_timer.begin()

    def stop_shield_timer(self):
        self.shield_timer.stop()

    def reset_shield_timer(self):
        self.shield_timer.reset()


class UniformTarget(Target):
    """匀速靶"""
    def __init__(self, settings, screen, *args):
        super().__init__(settings, screen, *args)

        # 速度、方向
        self.speed = self.args[2]
        self.direction = 1

    def update(self):
        """向上或向下移动靶机"""
        self.update_shield()
        if self.moving:
            self.y += (self.speed * self.direction)
            self.rect.y = self.y
        elif self.timer.pass_time > 1 + self.delay:
            self.moving = True


class AccelerateTarget(Target):
    """变加速靶"""
    def __init__(self, settings, screen, *args):
        super().__init__(settings, screen, *args)
        self.speed = 0
        self.a = self.args[2]   # 加速度

    def update(self):
        """（重载）移动靶机，到达中间位置时改变加速度方向"""
        self.update_shield()
        if self.moving:
            if self.rect.centery >= self.settings.screen_height / 2 and self.a > 0 \
                    or self.rect.centery < self.settings.screen_height / 2 and self.a < 0:
                self.a = -self.a
            self.speed += self.a
            self.y += self.speed
            self.rect.y = self.y
        elif self.timer.pass_time > 1 + self.delay:
            self.moving = True

    def check_edges(self):
        pass
