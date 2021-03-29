from random import choice

# 最后一轮靶机的随机属性：加速度、是否带盾、延迟运动
random_attr = [(0.1, 0.2), (True, False), (0, 0.5)]

# 定义每轮的靶机属性
# 参数说明：靶机初始位置、是否变加速、初始速度(匀速)/加速度(变速)、是否带盾、该轮开始后经过多长时间开始移动
target_list = [
    # 匀速靶
    [(0, False, 2, False, 0)],
    # [(1, False, 2, False, 0)],
    # [(2, False, 2, False, 0)],
    # [(3, False, 2, False, 0)],
    # [(1, False, 2, False, 0), (2, False, 2, False, 1)],
    # [(2, False, 2, False, 0), (3, False, 2, False, 1)],
    # [(0, False, 2, False, 1), (3, False, 2, False, 0)],
    # # 变速靶
    # [(1, True, 0.05, False, 0)],
    # [(1, True, 0.05, False, 0), (2, True, 0.05, False, 0.8)],
    # [(2, True, 0.05, False, 0), (3, True, 0.05, False, 0.8)],
    # [(0, True, 0.05, False, 1), (1, True, 0.05, False, 0.8), (2, True, 0.05, False, 0.4), (3, True, 0.05, False, 0)],
    # # 带盾靶
    # [(1, False, 2, True, 0)],
    # [(2, True, 0.05, True, 0)],
    # [(1, False, 2, True, 0), (2, True, 0.05, True, 1)],
    # # 高速靶
    # [(1, False, 4, False, 0)],
    # [(3, False, 4, False, 0)],
    # [(2, False, 4, False, 0), (3, False, 4, False, 0.5)],
    # [(3, False, 4, True, 0)],
    # # 随机靶
    # [(0, True, choice(random_attr[0]), choice(random_attr[1]), choice(random_attr[2])),
    #  (1, True, choice(random_attr[0]), choice(random_attr[1]), choice(random_attr[2])),
    #  (2, True, choice(random_attr[0]), choice(random_attr[1]), choice(random_attr[2])),
    #  (3, True, choice(random_attr[0]), choice(random_attr[1]), choice(random_attr[2]))]
]
