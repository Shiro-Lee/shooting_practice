from enum import Enum


class GameState(Enum):
    """枚举游戏状态"""
    PREGAME = 0     # 游戏开始前
    RUNNING = 1     # 游戏进行中
    GAME_OVER = 2   # 游戏失败
    GAME_FINISH = 3     # 游戏正常结束


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

    def game_finish(self):
        self.stop_timer()
        self.time_used = int(self.overall_timer.pass_time*100)/100
        self.new_timer()
        self.cal_score()
        print(self.overall_timer.pass_time)

    def reset_stats(self):
        """重置统计信息"""
        self.round = 1
        self.bullet_left = self.settings.bullet_limit
        self.time_used = 0
        self.target_left = True
        self.reset_timer()

    def cal_score(self):
        """计算得分"""
        # 剩余弹药得分=剩余弹药数*100
        self.bullet_left_score = self.bullet_left * 100
        # 耗时得分=(200-耗时)*50
        self.time_used_score = int((200-self.time_used)*50) if self.time_used < 200 else 0
        # 总分=剩余弹药分+耗时得分
        self.total_score = self.bullet_left_score + self.time_used_score

    def start_timer(self):
        self.overall_timer.begin()

    def reset_timer(self):
        self.overall_timer.reset()

    def stop_timer(self):
        self.overall_timer.stop()

    def new_timer(self):
        self.overall_timer.new_timer()
