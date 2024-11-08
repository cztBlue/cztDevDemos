import random

gGame = None

gPlayer = None

gWorld = None

dt = 0.33

debugstr = []

entityid = random.randint(10000, 99999)

gpreload_entitylist = {"map_prefab_list_byid": {}}
"""
preload prefab to use

gpreload_entitylist
└── "map_prefab_list_byid"
    ├── "1": mapprefab1
    ├── "2": mapprefab2
    └── ...
"""

visited_map = {}
"""
save all map visited

visited_map
├── "1" (mapid to str):{"prefablist":[prefab..],"grid":grid}
└── "2":...
"""


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
    "🚪": {
        "type": "Door",
        "prefabname": "普通门",
    },
    "🎒": {
        "type": "Backpack",
        "prefabname": "背包",
    },
    "🔑": {
        "type": "Key",
        "prefabname": "普通钥匙",
    },
    "⬆️ ": {
        "type": "TelePortal",
        "prefabname": "上行方块_B",
    },
    "⬇️ ": {
        "type": "TelePortal",
        "prefabname": "下行方块_B",
    },
    "⬆️": {
        "type": "TelePortal",
        "prefabname": "上行方块",
    },
    "⬇️": {
        "type": "TelePortal",
        "prefabname": "下行方块",
    },
}

deadcause = ("枭首", "撕成两半", "融化了", "撕成两半", "撕成两半", "撕成两半")
