from globalvar import *
from base import *
from prefab import *
import os,copy,msvcrt,json,sys,random,time


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