class GameStats:
    """跟踪游戏的统计信息"""
    bullet_left: int
    time: float

    def __init__(self, settings, timer):
        """初始化统计信息"""
        self.settings = settings
        self.timer = timer
        self.game_active = False    # 游戏开始标记
        self.player_name = ''   # 玩家名
        self.round = 1  # 轮数
        self.reset_stats()

    def reset_stats(self):
        """重置统计信息"""
        self.bullet_left = self.settings.bullet_limit
        self.timer.reset()

    def start_timer(self):
        self.timer.begin()

    def reset_timer(self):
        self.timer.reset()

    def stop_timer(self):
        self.timer.stop()
