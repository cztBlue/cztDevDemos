import os
import copy
import msvcrt
import json
import sys
import random
import time
# 再完成传送逻辑，str重击技能一个（带耗蓝逻辑），升级逻辑 即可上交作业


gGame = None

gPlayer = None

gWorld = None

nextvecdebug = None

dt = .33

Decidekey = [0, None]  # 状态，交互对象
"""
Decidekey结构:
Decidekey
├── 0(一般模式)
│   └── None
└── 1(交互模式，锁动作)
    └── prefabobj(交互对象)
"""
describeset = []

gpreload_entitylist = {"map_prefab_list_byid": {}}

entityid = random.randint(10000, 99999)

debugstr = []

# otprefabicondectet = ["🦇", "👿", "👹", "👺", "'💀", "👻", "🤡",
# "🤠", "😇", "🤖","🍖","💖","❗","🚪","🔑",]

# 先只做一些怪
otprefabicondectet = ["🦇","👿", "👹", "👺",
                    #   "⬆️ ","⬇️ ","⬆️","⬇️"
                      ]
otprefabinfo = {
    "🦇": {
        "type": "Enemy",
        "prefabname": "腐化蝙蝠",
        "baseattack": 5,
        "basedefense": 3,
        "basehealth": 30,
        "basemana": 50,
        "exp": 10,
    },
    "👿": {
        "type": "Enemy",
        "prefabname": "低阶恶魔",
        "baseattack": 15,
        "basedefense": 3,
        "basehealth": 60,
        "basemana": 100,
        "exp": 10,
    },
    "👹": {
        "type": "Enemy",
        "prefabname": "中阶恶魔",
        "baseattack": 30,
        "basedefense": 20,
        "basehealth": 150,
        "basemana": 250,
        "exp": 10,
    },
    "👺": {
        "type": "Enemy",
        "prefabname": "高阶恶魔",
        "baseattack": 50,
        "basedefense": 37,
        "basehealth": 300,
        "basemana": 600,
        "exp": 10,
    },
    # "⬆️ ": {
    #     "type": "Building",
    #     "prefabname": "上层传送阵",
    # },
    # "⬇️ ": {
    #     "type": "Building",
    #     "prefabname": "下层传送阵",
    # },
    # "⬆️": {
    #     "type": "Building",
    #     "prefabname": "上层传送阵",
    # },
    # "⬇️": {
    #     "type": "Building",
    #     "prefabname": "下层传送阵",
    # },
}

deadcause = ("枭首", "撕成两半", "融化了", "撕成两半", "撕成两半", "撕成两半")


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

    def tolist(self):
        return [self.pos_x, self.pos_y]

    # 根据输入的key和当前的坐标返回推断的坐标
    def cal_inputmov_vec(self, key):
        global nextvecdebug
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
        nextvecdebug = Vector2(nextvx, nextvy)
        return nextvecdebug

    def __eq__(self, ot):
        if isinstance(ot, Vector2):
            return ot.pos_x == self.pos_x and ot.pos_y == self.pos_y
        else:
            return False


class Event:
    def __init__(
        self, event_name, data=None, message="", cause="", sender=None, receiver=None
    ):
        self.event_name = event_name
        self.message = message
        self.cause = cause
        self.data = data
        self.sender = sender
        self.receiver = receiver

    """
    sender → Mounter → receiver(do eventhandler)
    """


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

class Action:
    def __init__(self, sender: Prefab, receiver: Prefab, actionhandler):
        self.sender: Prefab = sender
        self.receiver: Prefab = receiver
        self.actionhandler = actionhandler

    """
    actionhandler的接口为 actionhandler(sender,receiver)->[bool,describe]   
    describe is a str belike   f"{sender.prefabname}xxx(sender,receiver),xxxxxxx"  
    """

    def do_action(self):
        res = self.actionhandler(self.sender, self.receiver)
        if res[0] == True:
            gGame.widget.describeset.append(res[1])
        return res

    # 平A
    def dfaction_attack_AA(sender: Character, receiver: Character):
        if isinstance(sender, Character) and isinstance(receiver, Character) == False:
            return [False, "不可攻击对象"]
        else:
            if sender == None or receiver == None:
                return [False, "对象消失"]
            
            delta = (sender.attack or sender.baseattack) - receiver.basedefense
            delta = delta if delta > 0 else 0
            receiver.health = receiver.health - delta
            if receiver.health <= 0:
                receiver.push_event(
                    mounter=gWorld,
                    event=Event(
                        event_name="DYING",
                        message=f"{receiver.prefabname}濒死",
                        data=[sender, receiver],
                    ),
                )
            if isinstance(receiver,Player):
                dat = [
                    [(Vector2(2,1),"🎇")],
                    [(Vector2(2,1),receiver.icon)],
                    [(Vector2(2,1),"🎇")],
                ]
            else:
                dat = [
                    [(Vector2(2,4),"🎇")],
                    [(Vector2(2,4),receiver.icon)],
                    [(Vector2(2,4),"🎇")],
                ]
            gGame.render_frame(isdebug=True, animation = Animation().gen_animation(data=dat,para="ARENA"))
            return [
                True,
                f"{sender.prefabname}普通攻击了{receiver.prefabname} 造成了{delta}点伤害",
            ]

class Widget:
    def __init__(
        self,
    ):
        self.operationsplit = "——————————————————操 作——————————————————"
        self.header = ""
        self.status = ""
        self.describe = ""
        self.operation = "请使用W/A/S/D移动 | 保存(X) 保存并退出(Z)"
        self.split = len(self.operationsplit) * "—"
        self.describeset = []

    # 先后关系这里调
    def show_widget(self,is_in_animation = False):
        self.update_widget(is_in_animation)
        if self.header != "":  # A top1
            print(self.header)

        if self.status != "":  # A
            print(self.status)

        if self.describe != "":  # A
            print(self.describe)

        if self.operationsplit != "":  # B top
            print(self.operationsplit)

        if self.operation != "":  # B
            print(self.operation)
        if self.split != "":
            print(self.split)

    def update_widget(self,is_in_animation = False):
        if gPlayer.interaction_status_get() == "NORMAL":
            self.operation = "W/A/S/D移动 查看背包(E) | 保存(X) 保存并退出(Z)"
            self.status = f"{get_player().prefabname}的血量{get_player().health}  蓝量{get_player().mana} "
            self.header = "——————————————————状 态——————————————————"

        if gPlayer.interaction_status_get() == "ENEMY":
            self.operation = "选择操作: 战斗(A) 离开(Q) | 保存(X) 保存并退出(Z)"
            self.status = f"{get_player().prefabname}的血量{get_player().health}  蓝量{get_player().mana} "
            self.header = "——————————————————状 态——————————————————"

        if gPlayer.interaction_status_get() == "COMBAT":
            self.header = "————————————————————————战🗡 斗————————————————————————"
            self.status = f"{get_player().prefabname}的血量{get_player().health}  蓝量{get_player().mana} | {get_player().interaction_obj.prefabname}的血量{get_player().interaction_obj.health}  蓝量{get_player().interaction_obj.mana}"
            self.operation = "选择操作: 平A(A) 蓄力(S) 逃跑(Q) | 保存(X) 保存并退出(Z)"
        
        # if gPlayer.interaction_status_get() == "COMBAT":
        #     self.header = "————————————————————————战🗡 斗————————————————————————"
        #     self.status = f"{get_player().prefabname}的血量{get_player().health}  蓝量{get_player().mana} | {get_player().interaction_obj.prefabname}的血量{get_player().interaction_obj.health}  蓝量{get_player().interaction_obj.mana}"
        #     self.operation = "选择操作: 平A(A) 蓄力(S) 逃跑(Q) | 保存(X) 保存并退出(Z)"

        if is_in_animation == True:
            self.operation = "选择操作: ——————————————"

        self.describe = ""
        for des in self.describeset:
            if des == "":
                continue
            else:
                if self.describe == "":
                    self.describe = des
                else:
                    self.describe = self.describe + "\n" + des

        self.describeset = []

class Animation:
    def __init__(self, tolframe = 0, type = 0, grid_orderframe=None, str=None):
        self.curframe = 0  # 当前帧数序号,从0开始
        self.tolframe = 0  # 总帧数
        self.type = "ARENA"  # ARENA,SKILL
        self.grid_orderframe = []  # 竞技场emoji动画
        self.str = None  # 字符画，用来放技能帧
        self.grid_orderframe_base = []

    def render_curframe(self):
        if self.type == "ARENA":
            for i in self.grid_orderframe[self.curframe]:
                for j in i:
                    print(f"{j}", end="")
                print()
        if self.type == "SKILL":
            print(self.str)
    
    def gen_animation(self,data = None,para = "ARENA",):
        '''
        基本动画生成器,用坐标+icon生成动画,进入COMBAT才可以使用,不然无法生成正常的序列帧
        
        data:list
        ├── frame1:list
        │   ├── (Vector2,icon)
        │   ├── (Vector2,icon)
        │   └── ...
        ├── frame2:list
        └── ...

        '''
        if para == "ARENA":
            gGame.world.setarena()
            self.grid_orderframe_base = gGame.world.arena
            for frame in data:
                self.tolframe = self.tolframe + 1
                curframe = copy.deepcopy(self.grid_orderframe_base)
                for aset in frame:
                    curframe[aset[0].pos_x][aset[0].pos_y] = aset[1]
                self.grid_orderframe.append(curframe)
            return self
        if para == "SKILL":
            self.tolframe = 1
            self.str = data


class Game:
    def __init__(self, world, player) -> None:
        self.world: World = world
        self.player: Player = player
        self.widget = Widget()

    def getch(self):
        return msvcrt.getch().decode("utf-8")

    # 清空控制台
    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    # 鉴定按下按键后玩家是否能移动
    def move_keydown_handler(self, key) -> bool:
        """
        NORMAL 交互模式才会被调用
        True:玩家正常移动了
        False:玩家没有移动
        """
        dist_postition = self.player.position.cal_inputmov_vec(key)
        dist_info = self.world.type_gridpos(dist_postition)

        # 玩家移动
        if dist_info[0] == "IN_MAP" and dist_info[1] == "REACHABLE":
            self.player.setpos(dist_postition)
            return True
        # 检测到Prefab，更改交互模式
        elif dist_info[0] == "IN_MAP" and dist_info[1] == "PREFAB":
            self.player.interaction_status_set(dist_info[2].upper())
            self.player.interaction_obj = self.world.get_prefab_by_postition(
                dist_postition
            )
        else:  # 撞墙
            return False

    # 单帧渲染逻辑
    def render_frame(self, isdebug=False, animation:Animation=None):
        self.clear_screen()

        isdebug = False
        ################## debug##################
        if isdebug == True:
            global debugstr
            print("--------------debug--------------")
            print("当前坐标:(", self.player.position.pos_x, end=" ")
            print(self.player.position.pos_y, ")")
            print(self.world.type_gridpos(nextvecdebug))  # nextkey位置检查
            for str in debugstr:
                if str != "":
                    print(str)
            debugstr = []
            print("--------------debug--------------\n")
        ################## debug##################

        # 渲染动画逻辑
        if animation != None:
            while animation.curframe < animation.tolframe:
                self.clear_screen()
                Animation.render_curframe(animation)
                animation.curframe = animation.curframe + 1
                self.widget.show_widget(is_in_animation=True)
                time.sleep(dt)
            return     

        # 后渲染的层次覆盖前面的
        if self.player.interaction_status_get() != "COMBAT":
            # 地图渲染逻辑
            self.world.clear_grid()  # 网道层
            self.world.setallpreafb()  # Prefab层
            self.world.setplayer()  # 玩家层 --历史原因留下了这个层，有在考虑合并
            self.world.show_grid()  # 开始渲染
            self.widget.show_widget()  # UI层的逻辑写在geme里，不和world交互
        else:
            # 战斗渲染逻辑
            self.world.show_arena()
            self.widget.show_widget()

    def start(self):
        while self.player.isAlive:
            self.render_frame(isdebug=True)
            key_dwon_handler(getch())


def get_player() -> Player:
    return gPlayer

def getch():
    return msvcrt.getch().decode("utf-8")

def key_dwon_handler(key):
    move = ("w", "a", "s", "d")
    if key == None:
        return
    # key状态机青春版
    if gGame.player.interaction_status_get() == "NORMAL":
        if key in move:
            gGame.move_keydown_handler(key)

    elif gGame.player.interaction_status_get() == "ENEMY":
        if key == "q":
            gGame.player.interaction_status_set("NORMAL")
            return
        elif key == "a":
            gGame.player.interaction_status_set("COMBAT")

    elif gGame.player.interaction_status_get() == "COMBAT":
        if key == "q":
            gGame.player.interaction_status_set("NORMAL")
            return
        elif key == "a":
            Action(
                sender=get_player(),
                receiver=get_player().interaction_obj,
                actionhandler=Action.dfaction_attack_AA,
            ).do_action()
            gGame.render_frame(isdebug=True)
            time.sleep(dt)
            Action(
                sender=get_player().interaction_obj,
                receiver=get_player(),
                actionhandler=Action.dfaction_attack_AA,
            ).do_action()

    if key == "x":  # 保存
        save_and_exit(False)
    elif key == "z":  # 保存并退出
        save_and_exit(True)
    # elif key == "c": #读档
    # load()


def load():
    data = [[], []]
    if os.path.exists("./data.json"):
        with open("./data.json", "r") as json_file:
            loaded_data = json.load(json_file)
            data[0] = loaded_data

    if os.path.exists("./src.json"):
        with open("./src.json", "r") as json_file:
            loaded_src = json.load(json_file)
            data[1] = loaded_src

    return data


def save_and_exit(isexit: bool = True):
    data = {
        "playerdat": {
            "prefabname": gPlayer.prefabname,
            "icon": gPlayer.icon,
            "position": gPlayer.position.tolist(),
            "health": gPlayer.health,
            "mana": gPlayer.mana,
            "exp": gPlayer.exp_get(),
            "level": gPlayer.level_get(),
            "basemana": gPlayer.basemana,
            "baseattack": gPlayer.baseattack,
            "basedefense": gPlayer.basedefense,
            "basehealth": gPlayer.basehealth,
            "isAlive": gPlayer.isAlive,
        },
        "worlddat": {
            "prefabname": gWorld.prefabname,
            "currentmapid": gWorld.currentmap.mapid,
            "grid": gWorld.grid,
            # 待完成... 保存prefab
            # "r_prefablist": gWorld.r_prefablist,
        },
    }

    with open("data.json", "w") as json_file:
        json.dump(data, json_file)

    if isexit:
        sys.exit()


def icon_to_prefab(icon, vec: Vector2) -> Prefab:
    if icon in otprefabicondectet:
        if otprefabinfo[icon]["type"] == "Enemy":
            return Enemy(
                prefabname=otprefabinfo[icon]["prefabname"],
                icon=icon,
                postion=vec,
                health=otprefabinfo[icon]["basehealth"],
                mana=otprefabinfo[icon]["basemana"],
                level=1,
                exp=otprefabinfo[icon]["exp"],
                basemana=otprefabinfo[icon]["basemana"],
                baseattack=otprefabinfo[icon]["baseattack"],
                basedefense=otprefabinfo[icon]["basedefense"],
                basehealth=otprefabinfo[icon]["basehealth"],
            )
        
        # 建筑，暂时只有传送阵
        if otprefabinfo[icon]["type"] == "Building":
            return Building(
                prefabname=otprefabinfo[icon]["prefabname"],
                icon=icon,
                postion=vec,
            )

        # 装备 待完成...
        if otprefabinfo[icon]["type"] == "Equipment":
            return None

        # NPC 待完成...
        if otprefabinfo[icon]["type"] == "Equipment":
            return None

        
    else:
        return None


def init_game():
    global gPlayer
    global gWorld
    global gpreload_entitylist
    loaddata = load()
    if (loaddata is not None) and loaddata[1] != []:
        # scr是固定asset，dat是保存的player和world的状态
        src = loaddata[1]
        dat = loaddata[0]

        # src资源处理
        for k, v in src["map"].items():
            objmap = Map(
                prefabname=v["name"],
                mapid=v["mapid"],
                basegrid=v["basegrid"],
                birthpos=Vector2(listinit=v["birthpos"]),
            )
            gpreload_entitylist["map_prefab_list_byid"][f"{objmap.mapid}"] = objmap

        # dat资源处理，注入gPlayer和gWorld
        if dat != []:
            gPlayer = Player(
                prefabname=dat["playerdat"]["prefabname"],
                postion=Vector2(listinit=dat["playerdat"]["position"]),
                health=dat["playerdat"]["health"],
                mana=dat["playerdat"]["mana"],
                level=dat["playerdat"]["level"],
                exp=dat["playerdat"]["exp"],
            )

            gWorld = World(
                name=dat["worlddat"]["prefabname"],
                map=gpreload_entitylist["map_prefab_list_byid"][
                    str(dat["worlddat"]["currentmapid"])
                ],
                grid=dat["worlddat"]["grid"],
                # 待完成... 保存prefab
                # r_prefablist=dat["worlddat"]["r_prefablist"]
            )
        else:
            gPlayer = gPlayer = Player("cztBlue@tao", "😐")
            gWorld = World("大迷宫", gpreload_entitylist["map_prefab_list_byid"]["1"])

    else:
        gPlayer = gPlayer = Player("cztBlue@tao", "😐")
        gWorld = World("大迷宫", Map("迷宫入口", 0))


def ENDGAME(cause):
    # 删存档
    file_path = "data.json"
    if os.path.exists(file_path):
        os.remove(file_path)

    time.sleep(2*dt)
    gGame.clear_screen()
    print(cause)
    sys.exit()


# 状态保存在world和player里，game是不保存状态的
if __name__ == "__main__":
    init_game()
    gGame = Game(gWorld, gPlayer)
    gGame.start()
