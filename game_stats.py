from enum import Enum


class GameState(Enum):
    """枚举游戏状态"""
    PREGAME = 0     # 游戏开始前
    RUNNING = 1     # 游戏进行中
    GAME_OVER = 2   # 游戏失败
    GAME_FINISH = 3     # 游戏正常结束
    SHOW_TOPS = 4   # 显示得分排行榜


class GameStats:
    """跟踪游戏的统计信息"""

    def __init__(self, settings, timer):
        """初始化统计信息"""
        self.settings = settings
        self.overall_timer = timer
        self.game_state = GameState.PREGAME    # 游戏状态
        self.player_name = ''   # 玩家名
        self.round = 1  # 轮数
        self.target_left = True
        self.bullet_left = self.settings.bullet_limit
        self.time_used = 0
        self.bullet_left_score = 0
        self.time_used_score = 0
        self.total_score = 0

    def reset_stats(self):
        """重置统计信息"""
        self.round = 1
        self.bullet_left = self.settings.bullet_limit
        self.time_used = 0
        self.target_left = True
        self.reset_timer()

    def start_timer(self):
        self.overall_timer.begin()

    def reset_timer(self):
        self.overall_timer.reset()

    def stop_timer(self):
        self.overall_timer.stop()

    def new_timer(self):
        self.overall_timer.new_timer()
