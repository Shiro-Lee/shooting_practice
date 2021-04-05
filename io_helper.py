import json
import os


class IOHelper:
    """文件读写类，用以保存玩家记录"""
    def __init__(self, stats):
        self.stats = stats
        self.player_name = ''
        self.file_name = 'data_test.txt'
        self.new_result = False     # 若产生新纪录则重新加载
        self.results = {}   # 全部记录列表
        self.bullet_results = {}    # 剩余弹药得分列表
        self.speed_results = {}     # 耗时得分列表
        self.total_results = {}     # 总得分列表

    def load_data(self):
        """读取数据"""
        try:
            if os.path.getsize(self.file_name) != 0:
                with open(self.file_name, 'r') as file:
                    self.results = json.load(file)
                self.bullet_results = self.results['bullet_results']
                self.speed_results = self.results['speed_results']
                self.total_results = self.results['total_results']
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            with open(self.file_name, 'w'):     # 若文件不存在或读取失败则新建文件
                pass

    def check_player(self):
        """检查是否有该玩家的记录"""
        self.load_data()
        self.player_name = self.stats.player_name
        self.new_result = False
        # 是则检查最高分
        if self.stats.player_name in self.total_results.keys():
            self.check_higher_score()
        # 否则插入本次记录
        else:
            self.update_bullet_result()
            self.update_speed_result()
            self.update_total_result()
            with open(self.file_name, 'w') as file:
                json.dump(self.results, file)
            self.new_result = True

    def check_higher_score(self):
        """检查是否产生最高分"""
        higher_score = False
        if self.stats.bullet_left_score > self.bullet_results[self.player_name]['score']:
            self.update_bullet_result()
            higher_score = True
        if self.stats.time_used_score > self.speed_results[self.player_name]['score']:
            self.update_speed_result()
            higher_score = True
        if self.stats.total_score > self.total_results[self.player_name]['score']:
            self.update_total_result()
            higher_score = True
        if higher_score:
            self.new_result = True
            with open(self.file_name, 'w') as file:
                json.dump(self.results, file)

    def update_bullet_result(self):
        """更新剩余弹药记录"""
        self.bullet_results[self.player_name] = {'bullet_left': self.stats.bullet_left,
                                                 'score': self.stats.bullet_left_score}
        self.results['bullet_results'] = self.bullet_results

    def update_speed_result(self):
        """更新耗时记录"""
        self.speed_results[self.player_name] = {'time_used': self.stats.time_used,
                                                'score': self.stats.time_used_score}
        self.results['speed_results'] = self.speed_results

    def update_total_result(self):
        """更新总分记录"""
        self.total_results[self.player_name] = {'bullet_left_score': self.stats.bullet_left_score,
                                                'time_used_score': self.stats.time_used_score,
                                                'score': self.stats.total_score}
        self.results['total_results'] = self.total_results

    def get_bullet_top10(self):
        """获取剩余弹药得分排行"""
        if self.new_result:
            self.load_data()
        sorted_results = sorted(self.bullet_results.items(), key=lambda results: (results[1]['score']), reverse=True)
        self.add_rank(sorted_results)
        return sorted_results

    def get_speed_top10(self):
        """获取耗时得分排行"""
        if self.new_result:
            self.load_data()
        sorted_results = sorted(self.speed_results.items(), key=lambda results: (results[1]['score']), reverse=True)
        self.add_rank(sorted_results)
        return sorted_results

    def get_total_top10(self):
        """获取总得分排行"""
        if self.new_result:
            self.load_data()
        sorted_results = sorted(self.total_results.items(), key=lambda results: (results[1]['score']), reverse=True)
        self.add_rank(sorted_results)
        return sorted_results

    @classmethod
    def add_rank(cls, sorted_results):
        """为玩家记录添加排行"""
        pre_rank, inc_rank, pre_score = 1, 1, sorted_results[0][1]['score']
        for result in sorted_results:
            if result[1]['score'] == pre_score:
                result[1]['rank'] = pre_rank
            else:
                result[1]['rank'] = inc_rank
                pre_score = result[1]['score']
                pre_rank = inc_rank
            inc_rank += 1
