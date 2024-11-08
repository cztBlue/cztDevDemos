import copy
import gvar

class Animation:
    def __init__(
        self,
        tolframe=0,
        type=0,
        grid_orderframe=None,
        str=None,
        grid_orderframe_base=None,
    ):
        self.curframe = 0  # 当前帧数序号,从0开始
        self.tolframe = tolframe  # 总帧数
        self.type = type  # ARENA,SKILL
        self.grid_orderframe = grid_orderframe or []  # 竞技场emoji动画
        self.str = str or ""  # 字符画，用来放技能帧
        self.grid_orderframe_base = grid_orderframe_base or []

    def render_curframe(self):
        if self.type == "ARENA":
            for i in self.grid_orderframe[self.curframe]:
                for j in i:
                    print(f"{j}", end="")
                print()
        if self.type == "SKILL":
            print(self.str)

    # 低参数的生成法,用于简单动画
    @staticmethod
    def gen_animation(
        data=None,
        para="ARENA",
    ):
        """
        基本动画生成器,用坐标+icon生成动画,进入COMBAT才可以使用,不然无法生成正常的序列帧

        data:list
        ├── frame1:list
        │   ├── (Vector2,icon)
        │   ├── (Vector2,icon)
        │   └── ...
        ├── frame2:list
        └── ...

        """
        if para == "ARENA":
            ani = Animation(type="ARENA")
            gvar.gGame.world.setarena()
            ani.grid_orderframe_base = gvar.gGame.world.arena
            for frame in data:
                ani.tolframe = ani.tolframe + 1
                curframe = copy.deepcopy(ani.grid_orderframe_base)
                for aset in frame:
                    curframe[aset[0].pos_x][aset[0].pos_y] = aset[1]
                ani.grid_orderframe.append(curframe)
            return ani
        if para == "SKILL":
            return Animation(type="SKILL", str=data, tolframe=1)
