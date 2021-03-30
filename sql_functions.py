"""
查找是否已存在玩家名
    是→是否为最高分
        是→更新最高分
        否→pass
    否→插入玩家成绩
↓
获取前10名信息
"""


def check_player(stats, mysql_helper):
    sql = "SELECT * FROM total WHERE player_name='%s'" % stats.player_name
    result = mysql_helper.query_one(sql)
    if result:
        check_higher_score(stats, mysql_helper)
    else:
        insert_result(stats, mysql_helper)


def check_higher_score(stats, mysql_helper):
    # 检查剩余弹药最高分
    sql = "SELECT score FROM bullet WHERE player_name='%s'" % stats.player_name
    result = mysql_helper.query_one(sql)
    if stats.bullet_left_score > int(result['score']):
        sql = "UPDATE bullet SET bullet_left='%s', score='%s' WHERE player_name='%s'" \
              % (stats.bullet_left, stats.bullet_left_score, stats.player_name)
        mysql_helper.execute(sql)
    # 检查耗时最高分
    sql = "SELECT score FROM speed WHERE player_name='%s'" % stats.player_name
    result = mysql_helper.query_one(sql)
    if stats.time_used_score > int(result['score']):
        sql = "UPDATE speed SET time_used='%s', score='%s' WHERE player_name='%s'" \
              % (stats.time_used, stats.time_used_score, stats.player_name)
        mysql_helper.execute(sql)
    # 检查总分最高分
    sql = "SELECT total_score FROM total WHERE player_name='%s'" % stats.player_name
    result = mysql_helper.query_one(sql)
    if stats.total_score > int(result['total_score']):
        sql = "UPDATE total SET total_score='%s' WHERE player_name='%s'" \
              % (stats.total_score, stats.player_name)
        mysql_helper.execute(sql)


def insert_result(stats, mysql_helper):
    # 插入速度成绩表
    sql = "INSERT INTO speed(player_name, time_used, score) VALUES ('%s', '%s', '%s')" \
          % (stats.player_name, stats.time_used, stats.time_used_score)
    mysql_helper.execute(sql)
    # 插入剩余弹药成绩表
    sql = "INSERT INTO bullet(player_name, bullet_left, score) VALUES ('%s', '%s', '%s')" \
          % (stats.player_name, stats.bullet_left, stats.bullet_left_score)
    mysql_helper.execute(sql)
    # 插入总分表
    sql = "INSERT INTO total(player_name, total_score) VALUES ('%s', '%s')" \
          % (stats.player_name, stats.total_score)
    mysql_helper.execute(sql)


def update_result(stats, mysql_helper):
    pass
