from globalvar import *
from base import *
from prefab import *
import os,copy,msvcrt,json,sys,random,time

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
            globalvar.gGame.widget.describeset.append(res[1])
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
