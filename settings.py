from target_list import target_list


class Settings:
    """游戏设置类"""
    def __init__(self):
        """初始化游戏的静态设置"""
        # 屏幕设置
        self.screen_width = 1280
        self.screen_height = 720
        self.bg_color = (180, 180, 180)
        # 枪支、靶机边界设置
        self.x_gun_position = self.screen_width / 5
        self.y_gun_boundary = self.screen_height / 4
        self.x_target_position = self.screen_width * 2/5
        self.y_target_boundary = self.screen_height / 12
        # 枪支设置
        self.gun_speed = 1
        # 子弹速度、发射上限设置
        self.bullet_speed = 10
        self.bullets_allowed = 1
        # 初始弹药数
        self.bullet_limit = 100
        # 轮数
        self.max_round = len(target_list)
