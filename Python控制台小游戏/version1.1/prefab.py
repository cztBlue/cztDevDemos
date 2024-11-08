from vector import Vector2
from event import Event
import gvar

class Prefab:
    def __init__(self, prefabname, icon="⬜", initpos=Vector2(-1, -1), isAlive=True):
        self.prefabname = prefabname
        self.icon = icon
        self.position: Vector2 = initpos
        self.id = gvar.entityid
        self.listeners = {}
        self.can_interaction = False  # 设置预制体是否可交互
        gvar.entityid = gvar.entityid + 1
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
