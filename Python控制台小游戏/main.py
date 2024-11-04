from globalvar import *
from base import *
from prefab import *
import os,copy,msvcrt,json,sys,random,time

# 再完成传送逻辑，str重击技能一个（带耗蓝逻辑），升级逻辑 即可上交作业

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

# 状态保存在world和player里，game是不保存状态的
if __name__ == "__main__":
    init_game()
    gGame = Game(gWorld, gPlayer)
    gGame.start()