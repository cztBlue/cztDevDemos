from vector import Vector2
from prefab import Prefab
from gvar import otprefabinfo
from widget import Widget
import gvar

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
        widget.status = f"{gvar.gGame.player.prefabname}的血量{gvar.gGame.player.health}  蓝量{gvar.gGame.player.mana} "
        widget.header = "——————————————————状 态——————————————————"
        return

    def inaction_keystate_handler(self, key):
        if key == "q":  # 离开
            gvar.gGame.player.interaction_status_set("NORMAL")
            return
        if key == "r":  # 打开
            for prefab in gvar.gGame.player.backpack.item:
                if prefab.prefabname == "普通钥匙":
                    gvar.gGame.player.backpack.remove_item_by_id(prefab.id)
                    self.isAlive = False
            if self.isAlive == True:
                gvar.gGame.widget.describe = "没有对应的钥匙"
                return
            gvar.gGame.player.interaction_status_set("NORMAL")


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
        widget.status = f"{gvar.gGame.player.prefabname}的血量{gvar.gGame.player.health}/{gvar.gGame.player.basehealth}  蓝量{gvar.gGame.player.mana}/{gvar.gGame.player.basemana} \n 等级：{gvar.gGame.player._level} 当前经验：{gvar.gGame.player.exp_get()}"
        widget.header = "——————————————————状 态——————————————————"
        # 显示效果不好，以后再写
        # 待完成...
        widget.describe = ""
        for prefab in self.item:
            widget.describe = widget.describe + " " + prefab.prefabname
        return

    def inaction_keystate_handler(self, key):
        if key == "q":  # 离开
            gvar.gGame.player.interaction_status_set("NORMAL")
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
        widget.status = f"{gvar.gGame.player.prefabname}的血量{gvar.gGame.player.health}  蓝量{gvar.gGame.player.mana} "
        widget.header = "——————————————————状 态——————————————————"
        return

    def inaction_keystate_handler(self, key):
        if key == "r":  # 拾起
            gvar.gGame.player.backpack.add_item(self)
            # self.isAlive = False
            self.position = Vector2(-1, -1)
            gvar.gGame.player.interaction_status_set("NORMAL")
            return
        if key == "q":  # 离开
            self.isAlive = False
            gvar.gGame.player.interaction_status_set("NORMAL")


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
        widget.status = f"{gvar.gGame.player.prefabname}的血量{gvar.gGame.player.health}  蓝量{gvar.gGame.player.mana} "
        widget.header = "——————————————————状 态——————————————————"
        return

    def inaction_keystate_handler(self, key):
        if key == "r":  # 传送
            
            if self.prefabname == "上行方块_B" or self.prefabname =="上行方块":
                distid = gvar.gGame.world.currentmap.mapid - 1
            else:
                distid = gvar.gGame.world.currentmap.mapid + 1

            if gvar.gpreload_entitylist["map_prefab_list_byid"][str(distid)] != None:
                # 保存当前世界
                gvar.visited_map[str(gvar.gGame.world.currentmap.mapid)] = {}
                gvar.visited_map[str(gvar.gGame.world.currentmap.mapid)]["grid"] = gvar.gGame.world.grid
                gvar.visited_map[str(gvar.gGame.world.currentmap.mapid)]["prefablist"] = gvar.gGame.world.r_prefablist
                # 更改world挂载
                if gvar.visited_map.get(str(distid)) is not None:
                    gvar.gGame.world.currentmap = gvar.gpreload_entitylist["map_prefab_list_byid"][str(distid)]
                    gvar.gGame.world.r_prefablist = gvar.visited_map[str(distid)]["prefablist"]
                    gvar.gGame.world.grid = gvar.visited_map[str(distid)]["grid"]
                else:
                    gvar.gGame.world.currentmap = gvar.gpreload_entitylist["map_prefab_list_byid"][str(distid)]
                    gvar.gGame.world.init_world_bymap()

                gvar.gGame.player.setpos(Vector2(1,1)) 
                gvar.gGame.player.interaction_status_set("NORMAL")
            else:
                gvar.gGame.widget.describe = "到尽头了"
            return
        if key == "q":  # 离开
            gvar.gGame.player.interaction_status_set("NORMAL")
            return

