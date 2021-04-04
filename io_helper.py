import json
import os


class IOHelper:
    def __init__(self, stats):
        self.stats = stats
        self.player_name = 'Shooter'
        self.file_name = 'rank_test.txt'
        self.results = {}
        self.bullet_results = {}
        self.speed_results = {}
        self.total_results = {}
        self.load_data()

    def load_data(self):
        if os.path.getsize(self.file_name) != 0:
            with open(self.file_name, 'r') as file:
                self.results = json.load(file)
            self.bullet_results = self.results['bullet_results']
            self.speed_results = self.results['speed_results']
            self.total_results = self.results['total_results']

    def check_player(self):
        """检查是否有该玩家的记录"""
        self.player_name = self.stats.player_name
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

    def check_higher_score(self):
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
            with open(self.file_name, 'w') as file:
                json.dump(self.results, file)

    def update_bullet_result(self):
        self.bullet_results[self.player_name] = {'bullet_left': self.stats.bullet_left,
                                                 'score': self.stats.bullet_left_score}
        self.results['bullet_results'] = self.bullet_results

    def update_speed_result(self):
        self.speed_results[self.player_name] = {'time_used': self.stats.time_used,
                                                'score': self.stats.time_used_score}
        self.results['speed_results'] = self.speed_results

    def update_total_result(self):
        self.total_results[self.player_name] = {'bullet_left_score': self.stats.bullet_left_score,
                                                'time_used_score': self.stats.time_used_score,
                                                'score': self.stats.total_score}
        self.results['total_results'] = self.total_results

    def get_bullet_top10(self):
        pass

    def get_speed_top10(self):
        pass

    def get_total_top10(self):
        pass
