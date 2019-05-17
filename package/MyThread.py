from threading import Thread

# 自定义线程类，用于执行算法


class MyThread(Thread):

    def __init__(self, p, r):
        Thread.__init__(self)
        self.p = p
        self.r = r
        self.step = 0
        self.path = []

    def run(self):
        self.path = self.r.run(self.p)
        self.step = self.r.run_infor()

    # 获得运算结果的路径
    def get_result(self):
        return self.path

    # 获得步数
    def get_Infor(self):
        return self.step
