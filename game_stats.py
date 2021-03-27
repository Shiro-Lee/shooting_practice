from enum import Enum


class GameState(Enum):
    """枚举游戏状态"""
    PREGAME = 0     # 游戏开始前
    RUNNING = 1     # 游戏进行中
    GAMEOVER = 2    # 游戏结束


class GameStats:
    """跟踪游戏的统计信息"""
    bullet_left: int
    time: float

    def __init__(self, settings, timer):
        """初始化统计信息"""
        self.settings = settings
        self.timer = timer
        self.game_state = GameState.PREGAME    # 游戏状态
        self.player_name = ''   # 玩家名
        self.round = 1  # 轮数
        self.target_left = True
        self.reset_stats()

    def reset_stats(self):
        """重置统计信息"""
        self.round = 1
        self.bullet_left = self.settings.bullet_limit
        self.target_left = True
        self.timer.reset()

    def start_timer(self):
        self.timer.begin()

    def reset_timer(self):
        self.timer.reset()

    def stop_timer(self):
        self.timer.stop()

    def new_timer(self):
        self.timer.new_timer()

    def set_time_change(self, flag):
        self.timer.time_change = flag

    def get_time_str(self):
        return self.timer.time_str
