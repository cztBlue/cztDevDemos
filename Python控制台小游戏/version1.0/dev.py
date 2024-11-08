import os, time, copy, msvcrt, json, sys, random

# 再完成传送逻辑， 即可上交作业

gGame = None

gPlayer = None

gWorld = None

nextvecdebug = None

dt = 0.33

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

visited_map = {}
"""
visited_map
├── "1" (mapid to str):{"prefablist":[prefab..],"grid":grid}
└── "2":...
"""

entityid = random.randint(10000, 99999)

debugstr = []

# otprefabicondectet = ["🦇", "👿", "👹", "👺", "'💀", "👻", "🤡",
# "🤠", "😇", "🤖","🍖","💖","❗","🚪","🔑",]

# 先只做一些怪
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
    "🚪": {
        "type": "Door",
        "prefabname": "普通门",
    },
    "🎒": {
        "type": "Backpack",
        "prefabname": "背包",
    },
    "🔑": {
        "type": "Key",
        "prefabname": "普通钥匙",
    },
    "⬆️ ": {
        "type": "TelePortal",
        "prefabname": "上行方块_B",
    },
    "⬇️ ": {
        "type": "TelePortal",
        "prefabname": "下行方块_B",
    },
    "⬆️": {
        "type": "TelePortal",
        "prefabname": "上行方块",
    },
    "⬇️": {
        "type": "TelePortal",
        "prefabname": "下行方块",
    },
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
    def __init__(self, prefabname, icon="⬜", initpos=Vector2(-1, -1), isAlive=True):
        global entityid
        self.prefabname = prefabname
        self.icon = icon
        self.position: Vector2 = initpos
        self.id = entityid
        self.listeners = {}
        self.can_interaction = False  # 设置预制体是否壳交互
        entityid = entityid + 1
        self.isAlive = isAlive

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

    # 子类中实现...
    # 不做抽象方法了不然要改写好多prefab，历史债
    def inaction_UI_update(self, is_in):
        return

    def inaction_keystate_handler(self, key):
        return

    @staticmethod
    def create_self_by_vec_icon(vec,icon):
        return Prefab(prefabname="UNKNOWN", icon="❌", position=vec)


class Widget:
    def __init__(
        self,
    ):
        self.operationsplit = "——————————————————操 作——————————————————"
        self.header = ""
        self.status = f"{get_player().prefabname}的血量{get_player().health}/{get_player().basehealth}  蓝量{get_player().mana}/{get_player().basemana} "
        self.describe = ""
        self.operation = "请使用W/A/S/D移动 | 保存(X) 保存并退出(Z)"
        self.split = len(self.operationsplit) * "—"
        self.describeset = []
        self.prefabcontrol = False  # True本次渲染show跳过update
        self.frenderstatus = ("NORMAL", "COMBAT", "ENEMY")  # 历史遗留补丁

    # 先后关系这里调
    def show_widget(self, is_in_animation=False):
        if (
            get_player().interaction_status_get() in self.frenderstatus
        ) or get_player().interaction_obj == None:
            self.update_widget(is_in_animation)
        else:
            get_player().interaction_obj.inaction_UI_update(self, is_in_animation)

        if self.header != "":  # A top1
            print(self.header)

        if self.status != "":  # A
            print(self.status)

        if self.describe != "\n":  # A
            print(self.describe)

        if self.operationsplit != "":  # B top
            print(self.operationsplit)

        if self.operation != "":  # B
            print(self.operation)
        if self.split != "":
            print(self.split)

        self.prefabcontrol = False

    def update_widget(self, is_in_animation=False):
        self.status = f"{get_player().prefabname}的血量{get_player().health}/{get_player().basehealth}  蓝量{get_player().mana}/{get_player().basemana} "
        if gPlayer.interaction_status_get() == "NORMAL":
            self.operation = "W/A/S/D移动 查看背包(E) | 保存(X) 保存并退出(Z)"
            self.header = "——————————————————状 态——————————————————"

        if gPlayer.interaction_status_get() == "ENEMY":
            self.operation = "选择操作: 战斗(A) 离开(Q) | 保存(X) 保存并退出(Z)"
            self.header = "——————————————————状 态——————————————————"

        if gPlayer.interaction_status_get() == "COMBAT":
            self.header = "————————————————————————战🗡 斗————————————————————————"
            self.operation = (
                "选择操作: 平A(A) 蓄力一击(S) 逃跑(Q) | 保存(X) 保存并退出(Z)"
            )

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

        for i in range(len(self.basegrid)):
            for j in range(len(self.basegrid[i])):
                if self.basegrid[i][j] in list(otprefabinfo):
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
            if curicon in list(otprefabinfo):
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


class Door(Prefab):
    def __init__(
        self,
        name="普通门",
        icon="🚪",
        position: Vector2 = Vector2(-1, -1),
        isAlive=True,
    ):
        """
        创建这个对象只要传入postion即可
        """
        super().__init__(name, icon, position, isAlive)
        self.can_interaction = True

    # save retrun列表必须是可json列表
    # data的第一位必须包含自身类型字符串
    def save(self):
        return ["Door", self.position.tolist(), self.isAlive]

    @staticmethod
    def load(data):
        return Door(position=Vector2(listinit=data[1]), isAlive=data[2])

    @staticmethod
    def create_self_by_vec_icon(vec,icon):
        return Door(name="普通门", icon="🚪", position=vec)

    def inaction_UI_update(self, widget: Widget, is_in_animation):
        widget.operation = "离开(Q) 开门(R): 消耗普通钥匙 x1"
        widget.status = f"{get_player().prefabname}的血量{get_player().health}  蓝量{get_player().mana} "
        widget.header = "——————————————————状 态——————————————————"
        return

    def inaction_keystate_handler(self, key):
        if key == "q":  # 离开
            gGame.player.interaction_status_set("NORMAL")
            return
        if key == "r":  # 打开
            for prefab in get_player().backpack.item:
                if prefab.prefabname == "普通钥匙":
                    get_player().backpack.remove_item_by_id(prefab.id)
                    self.isAlive = False
            if self.isAlive == True:
                gGame.widget.describe = "没有对应的钥匙"
                return
            gGame.player.interaction_status_set("NORMAL")


class Backpack(Prefab):
    def __init__(
        self, name="背包", icon="🎒", position: Vector2 = Vector2(-1, -1), item=None
    ):
        """
        创建这个对象只要传入postion即可
        """
        super().__init__(name, icon, position)
        self.can_interaction = True
        self.item = item or []

    def add_item(self, prefab: Prefab):
        self.item.append(prefab)

    # 待完成
    def remove_item_by_key(self, prefab: Prefab):
        pass

    def remove_item_by_id(self, id):
        for index, value in enumerate(self.item):
            if value.id == id:
                del self.item[index]

    def save(self):
        dat = ["Backpack", self.position.tolist()]
        for prefab in self.item:
            if prefab.save != None:
                dat.append(prefab.save())
        return dat

    @staticmethod
    def load(data):
        itemlist = []
        for genprefabdat in data[2:]:
            pclass = globals()[genprefabdat[0]]
            if pclass.load != None:
                itemlist.append(pclass.load(genprefabdat))
            else:
                continue
        return Backpack(position=Vector2(listinit=data[0]), item=itemlist)

    @staticmethod
    def create_self_by_vec_icon(vec,icon):
        return Backpack()

    def inaction_UI_update(self, widget: Widget, is_in_animation):
        widget.operation = "关闭背包(Q)"
        widget.status = f"{get_player().prefabname}的血量{get_player().health}/{get_player().basehealth}  蓝量{get_player().mana}/{get_player().basemana} \n 等级：{get_player()._level} 当前经验：{get_player().exp_get()}"
        widget.header = "——————————————————状 态——————————————————"
        # 显示效果不好，以后再写
        # 待完成...
        widget.describe = ""
        for prefab in self.item:
            widget.describe = widget.describe + " " + prefab.prefabname
        return

    def inaction_keystate_handler(self, key):
        if key == "q":  # 离开
            gGame.player.interaction_status_set("NORMAL")
            return


class Key(Prefab):
    def __init__(
        self,
        name="普通钥匙",
        icon="🔑",
        position: Vector2 = Vector2(-1, -1),
    ):
        """
        创建这个对象需传入postion
        必须实现save, load, create_self_by_vec_icon, inaction_UI_update, inaction_keystate_handler
        """
        super().__init__(name, icon, position)
        self.can_interaction = True

    def save(self):
        return ["Key", self.position.tolist()]

    @staticmethod
    def load(data):
        return Key(position=Vector2(listinit=data[1]))

    @staticmethod
    def create_self_by_vec_icon(vec,icon):
        return Key(position=vec)

    def inaction_UI_update(self, widget: Widget, is_in_animation):
        widget.operation = "拾起 普通钥匙(R) 离开(Q)"
        widget.status = f"{get_player().prefabname}的血量{get_player().health}  蓝量{get_player().mana} "
        widget.header = "——————————————————状 态——————————————————"
        return

    def inaction_keystate_handler(self, key):
        if key == "r":  # 拾起
            gGame.player.backpack.add_item(self)
            # self.isAlive = False
            self.position = Vector2(-1, -1)
            gGame.player.interaction_status_set("NORMAL")
            return
        if key == "q":  # 离开
            self.isAlive = False
            gGame.player.interaction_status_set("NORMAL")


class TelePortal(Prefab):
    def __init__(
        self,
        name="上行方块_B",
        icon="⬆️ ",
        position: Vector2 = Vector2(-1, -1),
    ):
        """
        创建这个对象要传入icon,name,position
        上行方块_B,下行方块_B,下行方块,上行方块
        """
        super().__init__(name, icon, position)
        self.can_interaction = True

    def save(self):
        return ["TelePortal",self.prefabname, self.icon ,self.position.tolist()]

    @staticmethod
    def load(data):
        return TelePortal(name= data[1],position=Vector2(listinit=data[3]),icon=data[2])

    @staticmethod
    def create_self_by_vec_icon(vec,icon):
        return TelePortal(icon =icon, position=vec,name=otprefabinfo[icon]["prefabname"])

    def inaction_UI_update(self, widget: Widget, is_in_animation):
        widget.operation = "激活传送装置（有bug还没修）？(R) 离开(Q)"
        widget.status = f"{get_player().prefabname}的血量{get_player().health}  蓝量{get_player().mana} "
        widget.header = "——————————————————状 态——————————————————"
        return

    def inaction_keystate_handler(self, key):
        if key == "r":  # 传送
            
            if self.prefabname == "上行方块_B" or self.prefabname =="上行方块":
                distid = gGame.world.currentmap.mapid - 1
            else:
                distid = gGame.world.currentmap.mapid + 1

            if gpreload_entitylist["map_prefab_list_byid"][str(distid)] != None:
                # 保存当前世界
                visited_map[str(gGame.world.currentmap.mapid)] = {}
                visited_map[str(gGame.world.currentmap.mapid)]["grid"] = gGame.world.grid
                visited_map[str(gGame.world.currentmap.mapid)]["prefablist"] = gGame.world.r_prefablist
                # 更改world挂载
                if visited_map.get(str(distid)) is not None:
                    gGame.world.currentmap = gpreload_entitylist["map_prefab_list_byid"][str(distid)]
                    gGame.world.r_prefablist = visited_map[str(distid)]["prefablist"]
                    gGame.world.grid = visited_map[str(distid)]["grid"]
                else:
                    gGame.world.currentmap = gpreload_entitylist["map_prefab_list_byid"][str(distid)]
                    gGame.world.init_world_bymap()

                gGame.player.setpos(Vector2(1,1)) 
                gGame.player.interaction_status_set("NORMAL")
            else:
                gGame.widget.describe = "到尽头了"
            return
        if key == "q":  # 离开
            gGame.player.interaction_status_set("NORMAL")
            return


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
            if isinstance(receiver, Player):
                dat = [
                    [(Vector2(2, 1), "🎇")],
                ]
            else:
                dat = [
                    [(Vector2(2, 4), "🎇")],
                ]

        gGame.render_frame(
            isdebug=False,
            animation=Animation.gen_animation(data=dat, para="ARENA"),
        )
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
            if isinstance(sender, Player):
                sender.exp_add(receiver.exp_get())
        return [
            True,
            f"{sender.prefabname}普通攻击了{receiver.prefabname} 造成了{delta}点伤害",
        ]

    # 蓄力一击
    def dfaction_attack_player_charge(sender: Character, receiver: Character):
        # 动作阻断逻辑...
        if isinstance(sender, Character) and isinstance(receiver, Character) == False:
            return [False, "不可攻击对象"]
        else:
            if sender == None or receiver == None:
                return [False, "对象消失"]
            if isinstance(sender, Player) == False:
                return [False, "非玩家使用"]
        consume = 35
        if sender.mana < consume:
            return [False, "蓝量不足"]

        # 动作动画...
        dat1 = [
            [(Vector2(2, 4), "💥")],
        ]
        dat2 = """
⠀  ⠀   (\__/)
       (•ㅅ•)      
    ＿ノヽ ノ＼＿    
`/　`/ ⌒Ｙ⌒ Ｙ ヽ    
( 　(三ヽ人　 /　 |
|　ﾉ⌒＼ ￣￣ヽ  ノ
ヽ＿＿＿＞､＿_／
     ｜( 王 ﾉ〈  
       /ﾐ`ー―彡\  
      / ╰    ╯ \ 
"""
        gGame.render_frame(
            isdebug=False,
            animation=Animation.gen_animation(data=dat2, para="SKILL"),
        )
        time.sleep(dt * 2)
        gGame.render_frame(
            isdebug=False,
            animation=Animation.gen_animation(data=dat1, para="ARENA"),
        )

        # 动作效果逻辑...
        delta = (sender.attack * 2 or sender.baseattack * 2) - receiver.basedefense
        delta = delta if delta > 0 else 0
        receiver.health = receiver.health - delta
        sender.mana = sender.mana - consume
        if receiver.health <= 0:
            receiver.push_event(
                mounter=gWorld,
                event=Event(
                    event_name="DYING",
                    message=f"{receiver.prefabname}濒死",
                    data=[sender, receiver],
                ),
            )
            if isinstance(sender, Player):
                sender.exp_add(receiver.exp_get())
        return [
            True,
            f"{sender.prefabname}重击了{receiver.prefabname} 造成了{delta}点伤害",
        ]


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
            gGame.world.setarena()
            ani.grid_orderframe_base = gGame.world.arena
            for frame in data:
                ani.tolframe = ani.tolframe + 1
                curframe = copy.deepcopy(ani.grid_orderframe_base)
                for aset in frame:
                    curframe[aset[0].pos_x][aset[0].pos_y] = aset[1]
                ani.grid_orderframe.append(curframe)
            return ani
        if para == "SKILL":
            return Animation(type="SKILL", str=data, tolframe=1)


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
            debugstr.append("chan")
            self.player.interaction_status_set(dist_info[2].upper())
            self.player.interaction_obj = self.world.get_prefab_by_postition(
                dist_postition
            )
        else:  # 撞墙
            return False

    # 单帧渲染逻辑
    def render_frame(self, isdebug=False, animation: Animation = None):
        self.clear_screen()

        ################## debug##################
        if isdebug == True:
            global debugstr
            print("--------------debug--------------")
            print("当前坐标:(", self.player.position.pos_x, end=" ")
            print(self.player.position.pos_y, ")")
            print(self.world.type_gridpos(nextvecdebug))  # nextkey位置检查s
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
            self.render_frame(isdebug=False)
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
    # 由于历(需)史(重)原(构)因ENEMY和COMBAT不用inaction_keystate_handler处理
    if gGame.player.interaction_status_get() == "NORMAL":
        if key in move:
            gGame.move_keydown_handler(key)
        elif key == "e":  # 查看背包
            gGame.player.interaction_status_set("BACKPACK")
            gGame.player.interaction_obj = gGame.player.backpack
            # key_dwon_handler(key)
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
            gGame.render_frame(isdebug=False)
            time.sleep(dt)
            Action(
                sender=get_player().interaction_obj,
                receiver=get_player(),
                actionhandler=Action.dfaction_attack_AA,
            ).do_action()
        elif key == "s":
            Action(
                sender=get_player(),
                receiver=get_player().interaction_obj,
                actionhandler=Action.dfaction_attack_player_charge,
            ).do_action()
            gGame.render_frame(isdebug=False)
            time.sleep(dt)
            Action(
                sender=get_player().interaction_obj,
                receiver=get_player(),
                actionhandler=Action.dfaction_attack_AA,
            ).do_action()
    elif gGame.player.interaction_obj.can_interaction == True:  # 其他状态
        gGame.widget.prefabcontrol = True
        gGame.player.interaction_obj.inaction_keystate_handler(key)

    if key == "x":  # 保存
        save_and_exit(False)
    elif key == "z":  # 保存并退出
        save_and_exit(True)
    # 有bug，不开放
    # elif key == "c": #读档
    # init_game()


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
            "backpack": gPlayer.backpack.save(),
        },
        "worlddat": {
            "prefabname": gWorld.prefabname,
            "currentmapid": gWorld.currentmap.mapid,
            "grid": gWorld.grid,
            # 待完成...
            # 要实现预制体的save(),load()模块才能完整保存预制体，这里只存储icon，pos，和alive做权宜之计
            "r_prefablist_live_3v": [
                [prefab.icon, prefab.position.tolist(), prefab.isAlive]
                for prefab in gWorld.r_prefablist
            ],
        },
        # save把当前世界按mapid存到visited_world_bymap
        # load把所有"visited_world_bymap"存入visited_map变量
        "visited_world_bymap": {
            f"{gWorld.currentmap.mapid}": {
                "grid": gWorld.grid,
                "r_prefablist_live_3v": [
                    [prefab.icon, prefab.position.tolist(), prefab.isAlive]
                    for prefab in gWorld.r_prefablist
                ],
            }
        },
    }

    """
    visited_map
    ├── "1" (mapid to str):{"prefablist":[prefab..],"grid":grid}
    └── "2":...
    """
    # 把visited_map变量中除了当前的currentmap存储到到"visited_world_bymap"
    for key, value in visited_map.items():
        if data["visited_world_bymap"][key] == None:
            data["visited_world_bymap"][key] = {}
            data["visited_world_bymap"][key]["grid"] = value["grid"]
            data["visited_world_bymap"][key]["r_prefablist_live_3v"] = [
                    [prefab.icon, prefab.position.tolist(), prefab.isAlive]
                    for prefab in value["prefablist"]
                ]


    with open("data.json", "w") as json_file:
        json.dump(data, json_file)

    if isexit:
        sys.exit()


def icon_to_prefab(icon, vec: Vector2) -> Prefab:
    if icon in list(otprefabinfo):
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
        elif globals()[otprefabinfo[icon]["type"]] != None:
            if otprefabinfo[icon]["type"] == "TelePortals":
                getch()
                print(otprefabinfo[icon]["type"])
            curclass = globals()[otprefabinfo[icon]["type"]]
            return curclass.create_self_by_vec_icon(vec = vec,icon = icon)
        else:
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
                backpack=Backpack.load(dat["playerdat"]["backpack"]),
            )

            r_prefablist = []
            # prefab_3v (icon,position,isAlive)权宜之计
            for prefab_3v in dat["worlddat"]["r_prefablist_live_3v"]:
                prefab = icon_to_prefab(prefab_3v[0], Vector2(listinit=prefab_3v[1]))
                prefab.isAlive = prefab_3v[2]
                r_prefablist.append(prefab)
            
            # 新写的visited_map
            for key, vis_world in dat["visited_world_bymap"].items():
                visited_map[key] = {}
                r_prefablist = []
                for prefab_3v in vis_world["r_prefablist_live_3v"]:
                    prefab = icon_to_prefab(prefab_3v[0], Vector2(listinit=prefab_3v[1]))
                    prefab.isAlive = prefab_3v[2]
                    r_prefablist.append(prefab)
                visited_map[key]["prefablist"] = r_prefablist
                visited_map[key]["grid"] = vis_world["grid"]


            # gWorld = World(
            #     name=dat["worlddat"]["prefabname"],
            #     map=gpreload_entitylist["map_prefab_list_byid"][
            #         str(dat["worlddat"]["currentmapid"])
            #     ],
            #     grid=dat["worlddat"]["grid"],
            #     r_prefablist=r_prefablist,
            # )

            if visited_map.get(str(dat["worlddat"]["currentmapid"])) is not None:
                gWorld = World(
                    name=dat["worlddat"]["prefabname"],
                    map=gpreload_entitylist["map_prefab_list_byid"][
                        str(dat["worlddat"]["currentmapid"])
                    ],
                    grid=visited_map[str(dat["worlddat"]["currentmapid"])]["grid"],
                    r_prefablist=visited_map[str(dat["worlddat"]["currentmapid"])]["prefablist"],
                )
            else:
                gWorld = World(
                    name=dat["worlddat"]["prefabname"],
                    map=gpreload_entitylist["map_prefab_list_byid"][
                        str(dat["worlddat"]["currentmapid"])
                    ],
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

    time.sleep(2 * dt)
    gGame.clear_screen()
    print(cause)
    sys.exit()


# 制作Prefab流程 用key做模板，继承prefab，实现它的接口->在otprefabinfo添加生成参数
# 状态保存在world和player里，game是不保存状态的
if __name__ == "__main__":
    init_game()
    gGame = Game(gWorld, gPlayer)
    gGame.start()
