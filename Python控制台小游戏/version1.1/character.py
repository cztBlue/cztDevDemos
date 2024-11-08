from vector import Vector2
from prefab import Prefab
import gvar
from item import Backpack

class Character(Prefab):
    def __init__(
        self,
        name,
        icon="❔",
        baseattack=10,
        basedefense=10,
        basehealth=100,
        level=0,
        exp=10,
        basemana=200,
        isAlive=True,
        postion: Vector2 = Vector2(-1, -1),
        health=None,
        mana=None,
    ):
        super().__init__(name, icon, postion)
        self.baseattack = baseattack
        self.basedefense = basedefense
        self.basehealth = basehealth
        self.basemana = basemana
        self._exp = exp or 10
        self._level = level
        self.isAlive = isAlive
        self.level_add_property()
        self.attack = self.baseattack
        self.defense = self.baseattack
        self.mana = mana or self.basemana
        self.health = health or self.basehealth
        self.valid_prop()

    def valid_prop(self):
        if self.health > self.basehealth:
            self.health = self.basehealth
        if self.mana > self.basemana:
            self.mana = self.basemana
        if self._exp < 0:
            self._exp = 0
        if self._level > 30:
            self._level = 30
        if self._level < 0:
            self._level = 0

    def exp_add(self, value):
        self.exp_set(self.exp_get() + value)

    def exp_set(self, value):
        self._exp = value
        self.canlevelup()

    def exp_get(self):
        return self._exp

    def level_set(self, value):
        self._level = value
        self.level_add_property()

    def level_get(self):
        return self._level

    # XPneed = 10*(level^2 + 1)
    # XPearmed = 10*(mob_level/player_level)*mob_type
    def canlevelup(self):
        if self._exp >= 10 * (self._level**2 + 1) and self._level < 30:
            self._exp = self._exp - 10 * (self._level**2 + 1)
            self.level_set(self.level_get() + 1)
            # 升级回状态
            self.mana = self.basemana
            self.health = self.health
        else:
            return

    # baseproper = baseproper + level * proper_levle_rate
    # 先设定所有生物共用一套proper_levle_rate
    def level_add_property(self):
        self.baseattack = self.baseattack + self._level * 2.0
        self.basedefense = self.basedefense + self._level * 1.4
        self.basehealth = self.basehealth + self._level * 15
        self.basemana = self.basemana + self._level * 20

    def Dead(self):
        if self in gvar.gGame.world.r_prefablist:
            gvar.gGame.world.r_prefablist.remove(self)
        if gvar.gGame.player.interaction_obj.id == self.id:
            gvar.gGame.player.interaction_obj = None


class Player(Character):
    def __init__(
        self,
        prefabname="冒险者a",
        icon="😐",  # 普通模式😐, 心眼模式:😑
        postion: Vector2 = Vector2(1, 1),
        health=100,
        mana=200,
        level=1,
        exp=0,
        basemana=200,
        baseattack=9,
        basedefense=6,
        basehealth=80,
        isAlive=True,
        backpack=None,
    ):
        """
        prefabname:必填
        postion:必填
        health:必填
        mana:必填
        level:必填
        exp:必填
        """
        super().__init__(
            name=prefabname,
            icon=icon,
            baseattack=baseattack,
            basedefense=basedefense,
            basehealth=basehealth,
            level=level,
            exp=exp,
            basemana=basemana,
            isAlive=isAlive,
            postion=postion,
            health=health,
            mana=mana,
        )
        self._interaction_status: str = "NORMAL"
        self.interaction_obj: Prefab = None
        self.backpack = backpack or Backpack()
        """
        interaction_status:"NORMAL","ENEMY","BUILDING","COMBAT","NPC","FOOD"...
        """

    def interaction_status_set(self, value):
        self._interaction_status = value
        self.change_interaction_status()

    def interaction_status_get(self):
        return self._interaction_status

    def change_interaction_status(self):
        if self.interaction_obj == None:
            self._interaction_status == "NORMAL"

        if self._interaction_status == "NORMAL":
            self.interaction_obj = None


class Enemy(Character):
    def __init__(
        self,
        prefabname="腐化蝙蝠",
        icon="🦇",
        postion: Vector2 = Vector2(-1, -1),
        health=None,
        mana=100,
        level=1,
        exp=0,
        basemana=50,
        baseattack=5,
        basedefense=3,
        basehealth=30,
        isAlive=True,
    ):
        super().__init__(
            name=prefabname,
            icon=icon,
            baseattack=baseattack,
            basedefense=basedefense,
            basehealth=basehealth,
            level=level,
            exp=exp,
            basemana=basemana,
            isAlive=isAlive,
            postion=postion,
            health=health,
            mana=mana,
        )
