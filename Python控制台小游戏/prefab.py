from globalvar import *
from base import *
from prefab import *
import os,copy,msvcrt,json,sys,random,time

class Prefab:
    def __init__(self, prefabname, icon="⬜", initpos=Vector2(-1, -1)):
        global entityid
        self.prefabname = prefabname
        self.icon = icon
        self.position: Vector2 = initpos
        self.id = entityid
        self.listeners = {}
        self.can_interaction = False # 设置预制体是否壳交互，待完成...

        entityid = entityid + 1

    def setpos(self, vec: Vector2) -> bool:
        if isinstance(vec, Vector2):
            self.position.pos_x = vec.pos_x
            self.position.pos_y = vec.pos_y
            return True
        else:
            return False

    def handle_event(self, event: Event):
        for k, v in self.listeners.items():
            if k != event.event_name:
                continue
            else:
                for k, v in v.items():
                    v["event_handler"](event)

    # mounter.listeners
    # ├── "event1"
    # │   ├── "id1"
    # │   │   ├── "event_handler":function
    # │   │   └── "listener":prefab
    # │   └── "id2"
    # │       ├── "event_handler":function
    # │       └── "listener":prefab
    # └── "event2"
    #     └── ...
    def listen_for_event(self, event_name: str, event_handler, mounter, list_id):
        """
        event_handler(self,event:Event)
        """
        if event_name not in mounter.listeners:
            mounter.listeners[event_name] = {}

        mounter.listeners[event_name][str(list_id)] = {
            "event_handler": event_handler,
            "listener": self,
        }

    def push_event(self, mounter, event: Event):
        mounter.handle_event(event)

    # 待完成...
    # 设定了一个物品的可交互后，设置状态UI和按键状态机与物品进行逻辑交互
    def set_inaction_UI(self,):
        return 

    # 在子类完成...
    def set_inaction_keystate_handler(self, key):
        if self.can_interaction == False:
            return 


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
        self.birthpos: Vector2 = birthpos
        self.prefablist = []
        self.basegrid = basegrid  # 包含地图上的怪物，物品，NPC

        for i in range(len(self.basegrid)):
            for j in range(len(self.basegrid[i])):
                if self.basegrid[i][j] in otprefabicondectet:
                    self.prefablist.append(
                        icon_to_prefab(self.basegrid[i][j], Vector2(i, j))
                    )
                    self.mategrid[i][j] = "⬜"


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
        # get_player().setpos(self.currentmap.birthpos)

    def eventhandler_DYING(self, event: Event):
        if isinstance(event.data[1], Player):
            ENDGAME(
                f"{event.data[1].prefabname}被{deadcause[random.randint(0, 3)]}了,死因是{event.data[0].prefabname}"
            )
        if isinstance(event.data[1], Enemy) and isinstance(event.data[0], Player):
            event.data[1].Dead()
            gGame.widget.describeset.append(f"{event.data[1].prefabname}被打败了")
            if get_player().interaction_obj == None:
                get_player().interaction_status_set("NORMAL")

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
        if gPlayer.interaction_obj != None:
            self.arena[2][1] = gPlayer.icon
            self.arena[2][4] = gPlayer.interaction_obj.icon

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
            if curicon in otprefabicondectet:
                info[1] = "PREFAB"
                info.append(otprefabinfo[curicon]["type"])
                return info
        return self.type_mategridpos(vec)

    # 把玩家载入grid
    def setplayer(self):
        self.set_prefab_grid(get_player())

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

        if self.mategrid[vec.pos_x][vec.pos_y] == "⬜":
            info[0] = "IN_MAP"
            info[1] = "REACHABLE"
            return info

        if self.mategrid[vec.pos_x][vec.pos_y] == "⬛":
            info[0] = "IN_MAP"
            info[1] = "BLOCKABLE"
            return info

        if self.mategrid[vec.pos_x][vec.pos_y] == get_player().icon:
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


class Character(Prefab):
    def __init__(
        self,
        name,
        icon="❔",
        baseattack=10,
        basedefense=10,
        basehealth=100,
        level=1,
        exp=10,
        basemana=200,
        isAlive=True,
        postion: Vector2 = Vector2(-1, -1),
    ):
        super().__init__(name, icon, postion)
        self.baseattack = baseattack
        self.basedefense = basedefense
        self.basehealth = basehealth
        self.basemana = basemana
        self._exp = exp
        self._level = level
        self.isAlive = isAlive

    def exp_set(self, value):
        self._exp = value
        self.canlevelup()

    def exp_get(self):
        return self._exp

    def level_set(self, value):
        self._level = value
        self.level_add_property()

    def level_get(self):
        return self._level

    # XPneed = 10*(level^2 + 1)
    # XPearmed = 10*(mob_level/player_level)*mob_type
    def canlevelup(self):
        if self.exp >= 10 * (self.level**2 + 1) and self.level < 30:
            self.level = self.level + 1
            self.exp = self.exp - 10 * (self.level**2 + 1)
        else:
            return

    # baseproper = baseproper + level * proper_levle_rate
    # 先设定所有生物共用一套proper_levle_rate
    def level_add_property(self):
        self.baseattack = self.baseattack + self.level * 2.0
        self.basedefense = self.basedefense + self.level * 1.4
        self.basehealth = self.basehealth + self.level * 15
        self.basemana = self.basemana + self.level * 20

    def Dead(self):
        if self in gGame.world.r_prefablist:
            gGame.world.r_prefablist.remove(self)
        if get_player().interaction_obj.id == self.id:
            get_player().interaction_obj = None

class Player(Character):
    def __init__(
        self,
        prefabname="冒险者a",
        icon="😐",  # 普通模式😐, 心眼模式:😑
        postion: Vector2 = Vector2(1, 1),
        health=100,
        mana=200,
        level=1,
        exp=0,
        basemana=200,
        baseattack=9,
        basedefense=6,
        basehealth=80,
        isAlive=True,
    ):
        """
        prefabname:必填
        postion:必填
        health:必填
        mana:必填
        level:必填
        exp:必填
        """
        super().__init__(
            prefabname,
            icon,
            baseattack,
            basedefense,
            basehealth,
            level,
            exp,
            basemana,
            isAlive,
            postion,
        )
        self.health = health or basehealth
        self.mana = mana or basemana
        self.attack = self.baseattack
        self.defense = self.basedefense
        self._interaction_status: str = "NORMAL"
        self.interaction_obj: Prefab = None
        """
        _interaction_status:"NORMAL","ENEMY","BUILDING","COMBAT","NPC","FOOD"...
        """

    def interaction_status_set(self, value):
        self._interaction_status = value
        self.change_interaction_status()

    def interaction_status_get(self):
        return self._interaction_status

    def change_interaction_status(self):
        if self.interaction_obj == None:
            self._interaction_status == "NORMAL"

        if self._interaction_status == "NORMAL":
            self.interaction_obj = None

class Enemy(Character):
    def __init__(
        self,
        prefabname="腐化蝙蝠",
        icon="🦇",
        postion: Vector2 = Vector2(-1, -1),
        health=30,
        mana=100,
        level=1,
        exp=0,
        basemana=50,
        baseattack=5,
        basedefense=3,
        basehealth=30,
        isAlive=True,
    ):
        super().__init__(
            prefabname,
            icon,
            baseattack,
            basedefense,
            basehealth,
            level,
            exp,
            basemana,
            isAlive,
            postion,
        )
        self.health = health or basehealth
        self.mana = mana or basemana
        self.attack = self.baseattack
        self.defense = self.basedefense

class Building(Prefab):
    def __init__(
        self,
        name,
        icon="❔",
        postion: Vector2 = Vector2(-1, -1),
    ):
        super().__init__(name, icon, postion)
