from gvar import otprefabinfo
from prefab import Prefab
from vector import Vector2
import copy

class Map(Prefab):
    def __init__(
        self,
        prefabname="defaultmap",
        mapid=0,
        maze_size=None,  # 这个参数即将弃用
        mategrid=[
            ["⬛", "⬛", "⬛"],
            ["⬛", "⬜", "⬛"],
            ["⬛", "⬛", "⬛"],
        ],  # 这个参数即将弃用
        birthpos=Vector2(1, 1),
        basegrid=[
            ["⬛", "⬛", "⬛"],
            ["⬛", "⬜", "⬛"],
            ["⬛", "😡", "⬛"],
        ],
    ):
        """
        prefabname:必须填,最好不要重复
        mapid:必须填,不能重复
        basegrid:必须填,关键信息
        birthpos:最好填,不然都在(1,1)出现
        mategrid: 你可以不填了
        maze_size: 你可以不填了
        """
        super().__init__(prefabname)
        self.mapid = mapid
        self.mategrid = copy.deepcopy(basegrid)  # 只有墙和空气的地图
        self.maze_size: Vector2 = maze_size or Vector2(
            len(basegrid), len(basegrid[0])
        )  # 网格容量上限
        self.birthpos: Vector2 = birthpos or Vector2(1,1)
        self.prefablist = []
        self.basegrid = basegrid  # 包含地图上的怪物，物品，NPC

        from gfunc import icon_to_prefab
        for i in range(len(self.basegrid)):
            for j in range(len(self.basegrid[i])):
                if self.basegrid[i][j] in list(otprefabinfo):
                    self.prefablist.append(
                        icon_to_prefab(self.basegrid[i][j], Vector2(i, j))
                    )
                    self.mategrid[i][j] = "⬜"
