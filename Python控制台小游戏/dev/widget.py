import global_res.gvar as gvar
from global_res.gfunc import getch

class Widget:
    def __init__(
        self,
    ):
        self.operationsplit = "——————————————————操 作——————————————————"
        self.header = ""
        self.describe = ""
        self.operation = "请使用W/A/S/D移动 | 保存(X) 保存并退出(Z)"
        self.split = len(self.operationsplit) * "—"
        self.describeset = []
        self.prefabcontrol = False  # True本次渲染show跳过update
        self.frenderstatus = ("NORMAL", "COMBAT", "ENEMY")  # 历史遗留补丁
        if gvar.gPlayer is not None:
            self.status = f"{gvar.gPlayer.prefabname}的血量{gvar.gPlayer.health}/{gvar.gPlayer.basehealth}  蓝量{gvar.gPlayer.mana}/{gvar.gPlayer.basemana} "
        else:
            self.status = ""
    # 先后关系这里调
    def show_widget(self, is_in_animation=False):
        if (
            gvar.gPlayer.interaction_status_get() in self.frenderstatus
        ) or gvar.gPlayer.interaction_obj == None:
            self.update_widget(is_in_animation)
        else:
            gvar.gPlayer.interaction_obj.inaction_UI_update(self, is_in_animation)

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
        self.status = f"{gvar.gPlayer.prefabname}的血量{gvar.gPlayer.health}/{gvar.gPlayer.basehealth}  蓝量{gvar.gPlayer.mana}/{gvar.gPlayer.basemana} "
        if gvar.gPlayer.interaction_status_get() == "NORMAL":
            self.operation = "W/A/S/D移动 查看背包(E) | 保存(X) 保存并退出(Z)"
            self.header = "——————————————————状 态——————————————————"

        if gvar.gPlayer.interaction_status_get() == "ENEMY":
            self.operation = "选择操作: 战斗(A) 离开(Q) | 保存(X) 保存并退出(Z)"
            self.header = "——————————————————状 态——————————————————"

        if gvar.gPlayer.interaction_status_get() == "COMBAT":
            self.header = "————————————————————————战🗡 斗————————————————————————"
            self.operation = "选择操作: 平A(A) 蓄力一击(S) 逃跑(Q) | 保存(X) 保存并退出(Z)"
            self.status = f"{gvar.gPlayer.prefabname}的血量{gvar.gPlayer.health}/{gvar.gPlayer.basehealth}  蓝量{gvar.gPlayer.mana}/{gvar.gPlayer.basemana} |  {gvar.gPlayer.interaction_obj.prefabname}的血量{gvar.gPlayer.interaction_obj.health}"

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
