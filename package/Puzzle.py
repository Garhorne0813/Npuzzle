class Puzzle:

    def __init__(self):
        self.fn = 0
        # f是从初始点经由节点n到目标点的估价函数
        self.gn = 0
        # gn是在状态空间中从初始节点到n节点的实际代价
        self.hn = 0
        # hn是从n到目标节点最佳路径的估计代价
        self.state = []     # 拼图
        self.father = None  # 父节点

