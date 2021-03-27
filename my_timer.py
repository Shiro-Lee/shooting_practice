import time
from threading import Timer


class RepeatingTimer(Timer):
    """"自定义循环定时器，继承自threading.Timer"""

    def run(self):
        """重写run方法，使function在单个线程内循环执行"""
        while not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
            self.finished.wait(self.interval)


class MyTimer:
    """打靶计时器"""

    def __init__(self):
        self.start_time = 0.0       # 开始时间设为 0
        self.pass_time = 0.0        # 已经过去了的时间设为 0
        self.is_running = False     # 秒表是否在运行，默认为否
        self.time_change = False    # 标志是否已经过0.1秒
        self.time_str = ''          # 时间字符串
        self.timer = RepeatingTimer(0.01, self.update)  # 每0.01秒更新一次

    def set_time_str(self):
        """设定时间"""
        seconds = int(self.pass_time)
        mseconds = (self.pass_time - seconds) * 100
        self.time_str = '%d″%d' % (seconds, mseconds)

    def update(self):
        """更新时间"""
        self.pass_time = time.time() - self.start_time
        self.time_change = True

    def begin(self):
        """开始"""
        if not self.is_running:
            self.is_running = True
            self.start_time = time.time() - self.pass_time
            self.timer.start()

    def stop(self):
        """停止"""
        if self.is_running:
            self.timer.cancel()
            self.pass_time = time.time() - self.start_time
            self.time_change = True
            self.is_running = False

    def reset(self):
        """重设"""
        self.start_time = time.time()
        self.pass_time = 0.0

    def new_timer(self):
        self.timer = RepeatingTimer(0.01, self.update)
