from gvar import dt,otprefabinfo
import msvcrt,time,os,json,sys,os
from vector import Vector2
from prefab import Prefab
import gvar

def get_player() :
    return gvar.gPlayer


def getch():
    return msvcrt.getch().decode("utf-8")


def key_dwon_handler(key):
    from action import Action
    move = ("w", "a", "s", "d")
    if key == None:
        return
    # key状态机青春版
    # 由于历(需)史(重)原(构)因ENEMY和COMBAT不用inaction_keystate_handler处理
    if gvar.gGame.player.interaction_status_get() == "NORMAL":
        if key in move:
            gvar.gGame.move_keydown_handler(key)
        elif key == "e":  # 查看背包
            gvar.gGame.player.interaction_status_set("BACKPACK")
            gvar.gGame.player.interaction_obj = gvar.gGame.player.backpack
            # key_dwon_handler(key)
    elif gvar.gGame.player.interaction_status_get() == "ENEMY":
        if key == "q":
            gvar.gGame.player.interaction_status_set("NORMAL")
            return
        elif key == "a":
            gvar.gGame.player.interaction_status_set("COMBAT")
    elif gvar.gGame.player.interaction_status_get() == "COMBAT":
        if key == "q":
            gvar.gGame.player.interaction_status_set("NORMAL")
            return
        elif key == "a":
            Action(
                sender=get_player(),
                receiver=get_player().interaction_obj,
                actionhandler=Action.dfaction_attack_AA,
            ).do_action()
            gvar.gGame.render_frame(isdebug=False)
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
            gvar.gGame.render_frame(isdebug=False)
            time.sleep(dt)
            Action(
                sender=get_player().interaction_obj,
                receiver=get_player(),
                actionhandler=Action.dfaction_attack_AA,
            ).do_action()
    elif gvar.gGame.player.interaction_obj.can_interaction == True:  # 其他状态
        gvar.gGame.widget.prefabcontrol = True
        gvar.gGame.player.interaction_obj.inaction_keystate_handler(key)

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
            "prefabname": gvar.gPlayer.prefabname,
            "icon": gvar.gPlayer.icon,
            "position": gvar.gPlayer.position.tolist(),
            "health": gvar.gPlayer.health,
            "mana": gvar.gPlayer.mana,
            "exp": gvar.gPlayer.exp_get(),
            "level": gvar.gPlayer.level_get(),
            "basemana": gvar.gPlayer.basemana,
            "baseattack": gvar.gPlayer.baseattack,
            "basedefense": gvar.gPlayer.basedefense,
            "basehealth": gvar.gPlayer.basehealth,
            "isAlive": gvar.gPlayer.isAlive,
            "backpack": gvar.gPlayer.backpack.save(),
        },
        "worlddat": {
            "prefabname": gvar.gWorld.prefabname,
            "currentmapid": gvar.gWorld.currentmap.mapid,
            "grid": gvar.gWorld.grid,
            # 待完成...
            # 要实现预制体的save(),load()模块才能完整保存预制体，这里只存储icon，pos，和alive做权宜之计
            "r_prefablist_live_3v": [
                [prefab.icon, prefab.position.tolist(), prefab.isAlive]
                for prefab in gvar.gWorld.r_prefablist
            ],
        },
        # save把当前世界按mapid存到visited_world_bymap
        # load把所有"visited_world_bymap"存入visited_map变量
        "visited_world_bymap": {
            f"{gvar.gWorld.currentmap.mapid}": {
                "grid": gvar.gWorld.grid,
                "r_prefablist_live_3v": [
                    [prefab.icon, prefab.position.tolist(), prefab.isAlive]
                    for prefab in gvar.gWorld.r_prefablist
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
    for key, value in gvar.visited_map.items():
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
    # from ... import Enemy
    import item
    if icon in list(otprefabinfo):
        if otprefabinfo[icon]["type"] == "Enemy":
            from character import Enemy
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
        elif getattr(item, otprefabinfo[icon]["type"]) != None:
            curclass = getattr(item, otprefabinfo[icon]["type"])
            return curclass.create_self_by_vec_icon(vec = vec,icon = icon)
        else:
            return None
    else:
        return None


def init_game():
    loaddata = load()
    from character import Player
    from world import World
    if (loaddata is not None) and loaddata[1] != []:
        # scr是固定asset，dat是保存的player和world的状态
        src = loaddata[1]
        dat = loaddata[0]

        # src资源处理
        for k, v in src["map"].items():
            from map import Map
            objmap = Map(
                prefabname=v["name"],
                mapid=v["mapid"],
                basegrid=v["basegrid"],
                birthpos=Vector2(listinit=v["birthpos"]),
            )
            gvar.gpreload_entitylist["map_prefab_list_byid"][f"{objmap.mapid}"] = objmap

        # dat资源处理，注入gPlayer和gWorld
        if dat != []:
            from item import Backpack 
            gvar.gPlayer = Player(
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
                gvar.visited_map[key] = {}
                r_prefablist = []
                for prefab_3v in vis_world["r_prefablist_live_3v"]:
                    prefab = icon_to_prefab(prefab_3v[0], Vector2(listinit=prefab_3v[1]))
                    prefab.isAlive = prefab_3v[2]
                    r_prefablist.append(prefab)
                gvar.visited_map[key]["prefablist"] = r_prefablist
                gvar.visited_map[key]["grid"] = vis_world["grid"]

            if gvar.visited_map.get(str(dat["worlddat"]["currentmapid"])) is not None:
                from world import World
                gvar.gWorld = World(
                    name=dat["worlddat"]["prefabname"],
                    map=gvar.gpreload_entitylist["map_prefab_list_byid"][
                        str(dat["worlddat"]["currentmapid"])
                    ],
                    grid=gvar.visited_map[str(dat["worlddat"]["currentmapid"])]["grid"],
                    r_prefablist=gvar.visited_map[str(dat["worlddat"]["currentmapid"])]["prefablist"],
                )
            else:
                gvar.gWorld = World(
                    name=dat["worlddat"]["prefabname"],
                    map=gvar.gpreload_entitylist["map_prefab_list_byid"][
                        str(dat["worlddat"]["currentmapid"])
                    ],
                )
                
                

        else:
            gvar.gPlayer = Player("cztBlue@tao", "😐")
            gvar.gWorld = World("大迷宫", gvar.gpreload_entitylist["map_prefab_list_byid"]["1"])
    else:
        gvar.gPlayer = Player("cztBlue@tao", "😐")
        gvar.gWorld = World("大迷宫", Map("迷宫入口", 0))



    return [gvar.gWorld,gvar.gPlayer]


def ENDGAME(cause):
    # 删存档
    file_path = "data.json"
    if os.path.exists(file_path):
        os.remove(file_path)

    time.sleep(2 * dt)
    gvar.gGame.clear_screen()
    print(cause)
    sys.exit()