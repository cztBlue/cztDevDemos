from global_res.gvar import otprefabinfo
from vector import Vector2
import copy


class Map:
    def __init__(
        self,
        prefabname="defaultmap", 
        mapid=0,
        birthpos=Vector2(1, 1),
        basegrid=[
            ["⬛", "⬛", "⬛"],
            ["⬛", "⬜", "⬛"],
            ["⬛", "😡", "⬛"],
        ],
    ):
        """
        现在的Map不再继承prefab,但仍然拥有save/load接口
        prefabname:必须填,最好不要重复,
        mapid:必须填,不能重复
        basegrid:必须填,关键信息
        birthpos:最好填,不然都在(1,1)出现
        """
        self.name = prefabname
        self.mapid = mapid
        self.prefablist = []
        self.mategrid = copy.deepcopy(basegrid)  # 只有空气的地图
        self.maze_size: Vector2 = Vector2(len(basegrid), len(basegrid[0]))
        self.birthpos: Vector2 = birthpos or Vector2(1, 1)
        self.basegrid = basegrid  # 资源地图，包含地图上的怪物，物品，NPC等icon
        
        for i in range(len(self.basegrid)):
            for j in range(len(self.basegrid[i])):
                if self.basegrid[i][j] in list(otprefabinfo):
                    self.prefablist.append(
                        Map.icon_to_prefab(self.basegrid[i][j], Vector2(i, j))
                    )
                    self.mategrid[i][j] = "⬜"
    
    @staticmethod
    def icon_to_prefab(icon, vec: Vector2):
        from global_res.gfunc import find_and_create_class as findclass
        if icon in list(otprefabinfo):
            thisclass = findclass(otprefabinfo[icon]["type"],directory=".")
            if thisclass != None:
                return thisclass.create_self_by_vec_icon(vec = vec,icon = icon)
        else:
            return None

    def save():
        pass

    def load():
        pass
