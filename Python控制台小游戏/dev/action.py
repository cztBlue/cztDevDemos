import time
import global_res.gvar as gvar
from prefab import Prefab
from vector import Vector2
from event import Event
from character import Character,Player
from animation import Animation
from global_res.gfunc import getch

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
            gvar.gGame.widget.describeset.append(res[1])
        return res

    # 平A
    def dfaction_attack_AA(sender: Character, receiver: Character):
        
        if ("Character" in str(type(sender))) and ("Character" in str(type(receiver))) == False:
            return [False, "不可攻击对象"]
        else:
            if sender == None or receiver == None:
                return [False, "对象消失"]
            if ("Player" in str(type(receiver))):
                dat = [
                    [(Vector2(2, 1), "🎇")],
                ]
            else:
                dat = [
                    [(Vector2(2, 4), "🎇")],
                ]

        gvar.gGame.render_frame(
            isdebug=True,
            animation=Animation.gen_animation(data=dat, para="ARENA"),
        )
        delta = (sender.attack or sender.baseattack) - receiver.basedefense
        delta = delta if delta > 0 else 0
        receiver.health = receiver.health - delta
        if receiver.health <= 0:
            receiver.push_event(
                mounter=gvar.gGame.world,
                event=Event(
                    event_name="DYING",
                    message=f"{receiver.prefabname}濒死",
                    data=[sender, receiver],
                ),
            )
            
            if ("Player" in str(type(sender))):
                sender.exp_add(receiver.exp_get())
        return [
            True,
            f"{sender.prefabname}普通攻击了{receiver.prefabname} 造成了{delta}点伤害",
        ]

    # 蓄力一击
    def dfaction_attack_player_charge(sender: Character, receiver: Character):

        # 动作阻断逻辑...
        if ("Character" in str(type(sender))) and ("Character" in str(type(receiver))) == False:
            return [False, "不可攻击对象"]
        else:
            if sender == None or receiver == None:
                return [False, "对象消失"]
            if ("Player" in str(type(sender))) == False:
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
        print("cope2")
        getch()
        gvar.gGame.render_frame(
            isdebug=True,
            animation=Animation.gen_animation(data=dat2, para="SKILL"),
        )
        time.sleep(gvar.dt * 2)
        gvar.gGame.render_frame(
            isdebug=True,
            animation=Animation.gen_animation(data=dat1, para="ARENA"),
        )

        # 动作效果逻辑...
        delta = (sender.attack * 2 or sender.baseattack * 2) - receiver.basedefense
        delta = delta if delta > 0 else 0
        receiver.health = receiver.health - delta
        sender.mana = sender.mana - consume
        if receiver.health <= 0:
            receiver.push_event(
                mounter=gvar.gGame.world,
                event=Event(
                    event_name="DYING",
                    message=f"{receiver.prefabname}濒死",
                    data=[sender, receiver],
                ),
            )
            if ("Player" in str(type(sender))):
                sender.exp_add(receiver.exp_get())
        return [
            True,
            f"{sender.prefabname}重击了{receiver.prefabname} 造成了{delta}点伤害",
        ]
