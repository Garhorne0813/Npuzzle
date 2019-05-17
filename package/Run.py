from Puzzle import Puzzle
import random
import copy

# 运行算法类


class Run:

    def __init__(self, m, n):
        self.m = m
        self.n = n
        self.hard = 60
        self.open_list = []
        self.close_list = set()
        self.aim = []
        self.path_list = []
        self.direction = [1, 2, 3, 4]   # 上左下右
        self.step = 0

    # 设置m 和n
    def set_mn(self, m, n, hard):
        self.m = m
        self.n = n
        self.hard = hard

    # 根据m n的大小获得目标状态
    def init_aim(self):
        self.aim = list(range(0, self.m ** 2))

    def random_state(self):
        count = 0
        p = Puzzle()
        if self.aim is None:
            self.init_aim()
        p.state = self.aim
        # l = p.state
        i = self.hard
        b = 0
        while i != 0:
            a = random.randint(0, 3)
            while (a % 2 == b % 2 and a != b) or (a == b and count == 2):
                a = random.randint(0, 3)
            b = a
            p = self.move(p, a)
            i = i - 1
        return p

    # 计算hn函数
    def cal_hn(self, p):
        s = 0
        h = 0
        g = 0
        d = 0
        count = 0
        l = p.state
        for i in l:
            y = count % self.m
            x = (count - y) / self.m
            aim_y = i % 3
            aim_x = (i - aim_y) / 3
            s = s + abs(x - aim_x) + abs(y - aim_y)
            # s为总的曼哈顿距离
            if i != self.aim[count]:
                h += 1
            # h为不在终态位置的数字个数
            if count < len(l)-2:
                if i + 1 != l[count + 1]:
                    g += 1
            # 左右相邻两个数字，若前者加一不等于后者，则g++
            if count < len(l) - self.m -1:
                if i + self.m != l[count + self.m]:
                    d += 1
            # 上下相邻两个数字，若前者加n不等于后者，则d++
            count = count + 1
        return s + h + g + d

    # 设置初始状态，并加入open表
    def set_origin_state(self, p):
        p.gn = 0
        p.hn = self.cal_hn(p)
        p.fn = p.gn + p.hn
        p.father = None
        self.open_list.append(p)

    # 生成子状态函数
    def move(self, p, d):
        s = Puzzle()
        s.state = p.state[:]
        pos = s.state.index(0)
        if d == 1:
            if (pos - self.m) >= 0:
                s.state[pos], s.state[pos - self.m] = s.state[pos - self.m], s.state[pos]
        elif d == 2:
            if pos % self.m != 0:
                s.state[pos], s.state[pos - 1] = s.state[pos - 1], s.state[pos]
        elif d == 3:
            if (pos + self.m) <= self.m ** 2 - 1:
                s.state[pos], s.state[pos + self.m] = s.state[pos + self.m], s.state[pos]
        else:
            if (pos + 1) % self.m != 0:
                s.state[pos], s.state[pos + 1] = s.state[pos + 1], s.state[pos]
        return s

    # 判断含有某个属性的元素是否在表中
    @staticmethod
    def is_contains(s, list):
        flag = False
        for i in list:
            if i.state == s.state:
                flag = True
                break
        return flag

    # 计算完成后，获得路径
    def get_path(self, p):
        w = p.father
        self.path_list.append(p.state)
        while w is not None:
            self.path_list.append(w.state)
            w = w.father
        self.path_list.reverse()

    # 自定义list排序方式
    @staticmethod
    def cmp(s):
        return s.fn

    # 启发式搜索函数
    def heuristic_search(self):
        self.init_aim()
        t = []
        count = 0
        while self.open_list:
            count += 1
            if count > 3000:
                self.path_list = []
                break
            # 如果循环运行3000次则认为计算不出，退出循环
            x = self.open_list[0]
            del self.open_list[0]
            # 取得open第一个元素，并将其从open表中删除
            if x.state == self.aim:
                self.get_path(x)
                self.step = x.gn
                break
            # 如果当前状态为目标状态，则退出循环
            for i in self.direction:
                s = self.move(x, i)
                # 当前状态产生子状态
                # 若子状态与当前状态或前一个状态相同，则重新产生子状态
                if s.state == x.state or s.state == t:
                    continue
                s.gn = x.gn + 1
                s.hn = self.cal_hn(s)
                s.fn = s.gn + s.hn
                s.father = copy.deepcopy(x)
                # 计算当前子状态各个属性

                if (not self.is_contains(s, self.open_list)) \
                        and (not tuple(s.state) in self.close_list):
                    self.open_list.append(s)
                    # 如果该子状态不在open表中或close表中，则加入open表
            self.close_list.add(tuple(x.state))
            # 将当前节点加入close表中
            self.open_list.sort(key=self.cmp)
            # 重新对open表排序
            t = x.state[:]

    # 返回步数
    def run_infor(self):
        return self.step

    # 作为外部调用的接口
    def run(self, p):
        self.open_list.clear()
        self.close_list.clear()
        self.path_list.clear()
        self.set_origin_state(p)
        self.heuristic_search()
        return self.path_list



