# 参数说明：靶机初始位置、是否变加速、初始速度(匀速)/加速度(变速)、是否带盾、该轮开始后经过多长时间开始移动
from random import choice

random_attribute = [(0.1, 0.2), (True, False)]

target_list = [
    # 匀速靶
    [(0, False, 2, False, 0)],
    [(1, False, 2, False, 0)],
    [(2, False, 2, False, 0)],
    [(3, False, 2, False, 0)],
    [(1, False, 2, False, 0), (2, False, 2, False, 1.1)],
    [(2, False, 2, False, 0), (3, False, 2, False, 1.1)],
    [(0, False, 2, False, 1.1), (3, False, 2, False, 0)],
    # 变速靶
    [(1, True, 0.05, False, 0)],
    [(1, True, 0.05, False, 0), (2, True, 0.05, False, 0.8)],
    [(2, True, 0.05, False, 0), (3, True, 0.05, False, 0.8)],
    [(0, True, 0.05, False, 1.2), (1, True, 0.05, False, 0.8), (2, True, 0.05, False, 0.4), (3, True, 0.05, False, 0)],
    # 带盾靶
    [(1, False, 2, True, 0)],
    [(2, True, 0.05, True, 0)],
    [(1, False, 2, True, 0), (2, True, 0.05, True, 1.1)],
    # 高速靶
    [(1, False, 4, False, 0)],
    [(3, False, 4, False, 0)],
    [(2, False, 4, False, 0), (3, False, 4, False, 0.5)],
    [(3, False, 4, True, 0)],
    # 随机靶
    [(0, True, choice(random_attribute[0]), choice(random_attribute[1]), 0),
     (1, True, choice(random_attribute[0]), choice(random_attribute[1]), 0),
     (2, True, choice(random_attribute[0]), choice(random_attribute[1]), 0),
     (3, True, choice(random_attribute[0]), choice(random_attribute[1]), 0)]
]
