from global_res.gvar import dt
import msvcrt,time,os,json,sys
from vector import Vector2
import global_res.gvar as gvar

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
            gvar.gGame.render_frame(isdebug=True)
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
            gvar.gGame.render_frame(isdebug=True)
            time.sleep(dt)
            Action(
                sender=get_player().interaction_obj,
                receiver=get_player(),
                actionhandler=Action.dfaction_attack_AA,
            ).do_action()
    
    if (gvar.gGame.player.interaction_obj is not None) and gvar.gGame.player.interaction_obj.can_interaction == True:  # 其他状态
        gvar.gGame.widget.prefabcontrol = True
        gvar.gGame.player.interaction_obj.inaction_keystate_handler(key)

    if key == "x":  # 保存
        save_and_exit(False)
    elif key == "z":  # 保存并退出
        save_and_exit(True)
    # 有bug，不开放
    # elif key == "c": #读档
    # init_game()

# 获取当前目录中的所有 .py 文件中的指定名称的类
def find_and_create_class(class_name, directory="."):
    import importlib.util
    for filename in os.listdir(directory):
        if filename.endswith(".py"):
            module_name = filename[:-3] 
            file_path = os.path.join(directory, filename)
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            if hasattr(module, class_name):
                class_ = getattr(module, class_name)
                return class_
            
    raise ImportError(f"Class {class_name} not found in any .py file in {directory}")

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
        "playerdat": gvar.gPlayer.save(),
        "worlddat": gvar.gWorld.save(),
        "visited_world": {
            f"{gvar.gWorld.currentmap.mapid}": gvar.gWorld.save()
        }
    }
    
    # dump other visited_world
    for key, value in gvar.visited_world.items():
        if key != str(gvar.gWorld.currentmap.mapid):
            data["visited_world"][key] = value.save()

    with open("data.json", "w") as json_file:
        json.dump(data, json_file)

    if isexit:
        sys.exit()


def init_game():
    from character import Player
    from world import World
    loaddata = load()
    if (loaddata is not None) and loaddata[1] != []:
        # scr是asset，dat是存档
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
            gvar.gPlayer = Player.load(dat["playerdat"])
            gvar.gWorld = World.load(dat["worlddat"])
        else:
            gvar.gPlayer = Player("cztBlue@tao", "😐")
            gvar.gWorld = World("大迷宫", gvar.gpreload_entitylist["map_prefab_list_byid"]["1"])
    else:
        print("src.json资源丢失,无法载入地图,请重新生成。")


def ENDGAME(cause):
    # 删存档
    file_path = "data.json"
    if os.path.exists(file_path):
        os.remove(file_path)

    time.sleep(2 * dt)
    gvar.gGame.clear_screen()
    print(cause)
    sys.exit()