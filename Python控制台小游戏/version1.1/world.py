import copy,random
from gvar import deadcause,otprefabinfo
from prefab import Prefab
from vector import Vector2
from event import Event
from character import Player,Enemy
from map import Map
from gfunc import ENDGAME
import gvar

class World(Prefab):
    def __init__(self, name, map: Map, grid=None, r_prefablist=None):
        super().__init__(name)
        self.currentmap: Map = map
        # 兼容性写法，因为不想改了留下了这三个变量
        self.maze_size: Vector2 = self.currentmap.maze_size
        self.mategrid = self.currentmap.mategrid  # 原始网格
        self.grid = grid or copy.deepcopy(self.currentmap.basegrid)  # runtime网格
        self.r_prefablist = r_prefablist or self.currentmap.prefablist
        self.arena = [
            ["⬛", "⬛", "⬛", "⬛", "⬛", "⬛"],
            ["⬛", "⬜", "⬜", "⬜", "⬜", "⬛"],
            ["⬛", "⬜", "⬜", "⬜", "⬜", "⬛"],
            ["⬛", "⬜", "⬜", "⬜", "⬜", "⬛"],
            ["⬛", "⬛", "⬛", "⬛", "⬛", "⬛"],
        ]
        self.listen_for_event(
            event_name="DYING",
            event_handler=self.eventhandler_DYING,
            mounter=self,
            list_id="world",
        )
        # 出生点特化，待完成...
        # gPlayer.setpos(self.currentmap.birthpos)

    def init_world_bymap(self):
        self.maze_size: Vector2 = self.currentmap.maze_size
        self.mategrid = self.currentmap.mategrid 
        self.grid = copy.deepcopy(self.currentmap.basegrid) 
        self.r_prefablist = self.currentmap.prefablist


    def eventhandler_DYING(self, event: Event):
        if isinstance(event.data[1], Player):
            ENDGAME(
                f"{event.data[1].prefabname}被{deadcause[random.randint(0, 3)]}了,死因是{event.data[0].prefabname}"
            )
        if isinstance(event.data[1], Enemy) and isinstance(event.data[0], Player):
            event.data[1].Dead()
            gvar.gGame.widget.describeset.append(f"{event.data[1].prefabname}被打败了")
            if gvar.gPlayer.interaction_obj == None:
                gvar.gPlayer.interaction_status_set("NORMAL")

    # 清空网格
    def clear_grid(self):
        self.grid = copy.deepcopy(self.mategrid)

    def clear_arena(self):
        self.arena[2][1] = "⬜"
        self.arena[2][4] = "⬜"

    # 在地图中放置预制体
    def set_prefab_grid(self, prefab: Prefab) -> bool:
        if prefab is None:
            return False

        if self.type_mategridpos(prefab.position)[0] == "IN_MAP":

            self.grid[prefab.position.pos_x][prefab.position.pos_y] = prefab.icon
            return True
        else:
            return False

    # 渲染地图
    def show_grid(self):
        for i in self.grid:
            for j in i:
                print(f"{j}", end="")
            print()

    def setarena(self):
        if gvar.gPlayer.interaction_obj != None:
            self.arena[2][1] = gvar.gPlayer.icon
            self.arena[2][4] = gvar.gPlayer.interaction_obj.icon

    # 渲染竞技场
    def show_arena(self):
        self.setarena()
        for i in self.arena:
            for j in i:
                print(f"{j}", end="")
            print()
        self.clear_arena()

    # 完全地图位置类型检查 ：检测预制体 -- 分开写是因为历史原因
    def type_gridpos(self, vec: Vector2) -> list:
        info = self.type_mategridpos(vec)
        if info[0] == "NOT_IN_MAP":
            return info
        else:
            curicon = self.grid[vec.pos_x][vec.pos_y]
            if curicon in list(otprefabinfo):
                info[1] = "PREFAB"
                info.append(otprefabinfo[curicon]["type"])
                return info
        return self.type_mategridpos(vec)

    # 把玩家载入grid
    def setplayer(self):
        self.set_prefab_grid(gvar.gPlayer)

    # 把map的prefablist注入grid
    def setallpreafb(self):
        for prefab in self.r_prefablist:
            if prefab.isAlive == True:
                self.set_prefab_grid(prefab)

    # 元地图位置类型检查 :只检测墙，空气，边界，玩家
    def type_mategridpos(self, vec: Vector2) -> list:
        info = ["NOT_IN_MAP", "UNKNOWN"]
        if isinstance(vec, Vector2) == False:
            info[0] = "NOT_IN_MAP"
            info[1] = "NOT_VECTOR"
            return info

        if (
            vec.pos_x > self.maze_size.pos_x - 1
            or vec.pos_y > self.maze_size.pos_y - 1
            or vec.pos_x < 0
            or vec.pos_y < 0
        ):
            info[0] = "NOT_IN_MAP"
            info[1] = "OUT_BOUND"
            return info
        else:
            info[0] = "IN_MAP"

        if self.mategrid[vec.pos_x][vec.pos_y] == "⬜":
            info[0] = "IN_MAP"
            info[1] = "REACHABLE"
            return info

        if self.mategrid[vec.pos_x][vec.pos_y] == "⬛":
            info[0] = "IN_MAP"
            info[1] = "BLOCKABLE"
            return info

        if self.mategrid[vec.pos_x][vec.pos_y] == gvar.gPlayer.icon:
            info[0] = "IN_MAP"
            info[1] = "PLAYER"
            return info

        return info

    def get_prefab_by_postition(self, vec: Vector2):
        if vec == None:
            return None

        for prefab in self.r_prefablist:
            if prefab.position == vec:
                return prefab
        return None
