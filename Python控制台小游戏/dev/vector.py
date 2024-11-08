class Vector2:
    def __init__(self, x=-1, y=-1, listinit=None):
        self.pos_x = x
        self.pos_y = y
        if listinit is not None:
            self.pos_x = listinit[0]
            self.pos_y = listinit[1]

    """
    ──────o y方向
    |
    |
    o
    x方向
    """

    def tolist(self):
        return [self.pos_x, self.pos_y]

    # 根据输入的key和当前的坐标返回推断的坐标
    def cal_inputmov_vec(self, key):
        nextvx = self.pos_x
        nextvy = self.pos_y
        if key == "w":
            nextvx = self.pos_x - 1
        elif key == "s":
            nextvx = self.pos_x + 1
        elif key == "a":
            nextvy = self.pos_y - 1
        elif key == "d":
            nextvy = self.pos_y + 1
        else:
            return False
        return Vector2(nextvx, nextvy)

    def __eq__(self, ot):
        if ("Vector2" in str(type(ot))):
            return ot.pos_x == self.pos_x and ot.pos_y == self.pos_y
        else:
            return False
