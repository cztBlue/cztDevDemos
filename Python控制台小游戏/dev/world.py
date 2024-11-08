import copy,random
from global_res.gvar import deadcause,otprefabinfo
from prefab import Prefab
from vector import Vector2
from event import Event
from character import Player,Enemy
from map import Map
from global_res.gfunc import ENDGAME,getch
import global_res.gvar as gvar

class World(Prefab):
    def __init__(self, name, map: Map, grid=None, r_prefablist=None,dat=None):
        super().__init__(name)
        self.currentmap: Map = map
        self.maze_size: Vector2 = self.currentmap.maze_size       
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

    def init_world_bymap(self):
        self.grid = copy.deepcopy(self.currentmap.basegrid) 
        self.r_prefablist = self.currentmap.prefablist

    def eventhandler_DYING(self, event: Event):
        if ("Player" in str(type(event.data[1]))):
            ENDGAME(
                f"{event.data[1].prefabname}被{deadcause[random.randint(0, 3)]}了,死因是{event.data[0].prefabname}"
            )

        # isinstance 判断不对，艹
        if "Enemy" in str(type(event.data[1])) and "Player" in str(type(event.data[0])):
            event.data[1].Dead()
            gvar.gGame.widget.describeset.append(f"{event.data[1].prefabname}被打败了")
            if gvar.gPlayer.interaction_obj == None:
                gvar.gPlayer.interaction_status_set("NORMAL")

    # 清空网格
    def clear_grid(self):
        self.grid = copy.deepcopy(self.currentmap.mategrid)

    # 清空竞技场
    def clear_arena(self):
        self.arena[2][1] = "⬜"
        self.arena[2][4] = "⬜"

    # 渲染地图
    def show_grid(self):
        for i in self.grid:
            for j in i:
                print(f"{j}", end="")
            print()

    # 渲染竞技场
    def show_arena(self):
        self.setarena()
        for i in self.arena:
            for j in i:
                print(f"{j}", end="")
            print()
        self.clear_arena()

    # 在地图中放置预制体
    def set_prefab_grid(self, prefab: Prefab) -> bool:
        if prefab is None:
            return False

        if self.type_mategridpos(prefab.position)[0] == "IN_MAP":

            self.grid[prefab.position.pos_x][prefab.position.pos_y] = prefab.icon
            return True
        else:
            return False

    # 把玩家载入grid
    def setplayer(self):
        self.set_prefab_grid(gvar.gPlayer)

    # 把map的prefablist注入grid
    def setallpreafb(self):
        for prefab in self.r_prefablist:
            if prefab.isAlive == True:
                self.set_prefab_grid(prefab)
    
    # 放置敌我
    def setarena(self):
        if gvar.gPlayer.interaction_obj != None:
            self.arena[2][1] = gvar.gPlayer.icon
            self.arena[2][4] = gvar.gPlayer.interaction_obj.icon

    # 完全地图位置类型检查 ：可以检测预制体 
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

    # 元地图位置类型检查 :只检测 空气，边界，玩家
    def type_mategridpos(self, vec: Vector2) -> list:
        info = ["NOT_IN_MAP", "UNKNOWN"]
        
        if ("Vector2" in str(type(vec))) == False:
            info[0] = "NOT_IN_MAP"
            info[1] = "NOT_VECTOR"
            return info

        if (
            vec.pos_x > self.currentmap.maze_size.pos_x - 1
            or vec.pos_y > self.currentmap.maze_size.pos_y - 1
            or vec.pos_x < 0
            or vec.pos_y < 0
        ):
            info[0] = "NOT_IN_MAP"
            info[1] = "OUT_BOUND"
            return info
        else:
            info[0] = "IN_MAP"

        if self.currentmap.mategrid[vec.pos_x][vec.pos_y] == "⬜":
            info[0] = "IN_MAP"
            info[1] = "REACHABLE"
            return info
        
        if self.currentmap.mategrid[vec.pos_x][vec.pos_y] == "⬛":
            info[0] = "IN_MAP"
            info[1] = "BLOCK"
            return info

        if self.currentmap.mategrid[vec.pos_x][vec.pos_y] == gvar.gPlayer.icon:
            info[0] = "IN_MAP"
            info[1] = "PLAYER"
            return info

        return info

    def get_prefab_by_postition(self, vec: Vector2) ->Prefab:
        if vec == None:
            return None

        for prefab in self.r_prefablist:
            if prefab.position == vec:
                return prefab
        return None
    

    ############## Prefab接口 ##############
    def save(self):
        dat = [
            "World",
            self.prefabname, 
            self.currentmap.mapid,
            self.grid,
            [prefab.save() for prefab in self.r_prefablist]
        ]
        return dat

    @staticmethod
    def load(data):
        from global_res.gfunc import find_and_create_class as findclass

        return World(name = data[1],
                     map= gvar.gpreload_entitylist["map_prefab_list_byid"][str(data[2])],
                     grid= data[3],
                     r_prefablist=[findclass(class_name=prefabdat[0],directory=".").load(prefabdat) for prefabdat in data[4]]
                    )

    def inaction_UI_update(self, is_in):
        return

    def inaction_keystate_handler(self, key):
        return
    
    @staticmethod
    def create_self_by_vec_icon(vec,icon):
        return Prefab(prefabname="UNKNOWN", icon="❌", position=vec)
