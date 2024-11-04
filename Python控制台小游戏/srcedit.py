import json
from dev import Map,Vector2,Animation

# 这个代码用来生成map，动画，立绘等数据，打包成json,格式
'''
src.json结构:
data
├── map
│   ├── mapid1
│   │   ├── name:str
│   │   ├── basegrid:list
│   │   ├── mapid:int
│   │   └── birthpos:list
│   ├── mapid2
│   └── ...
└── character
'''

data= {
    "map":{},
    "character":{}
}

# 传入map对象,向data中添加一个json包
def add_map_package(imap:Map):
    data["map"][str(imap.mapid)] ={
        "name": imap.prefabname,
        "mapid": imap.mapid,
        "basegrid": imap.basegrid,
        "birthpos": imap.maze_size.tolist(),
    }


#RUN
g1 = [
        ["⬛", "⬆️ ", "⬛", "⬛", "⬛", "⬛", "⬛", "⬛", "⬛", "⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛"],
        ["⬛", "⬜", "🦇", "⬜", "⬜", "🦇", "⬜", "⬜", "🦇", "⬜","⬜","⬜","⬛","👺","⬜","⬜","⬛"],
        ["⬛", "⬜", "⬛", "⬜", "⬛", "⬛", "⬛", "⬛", "⬛", "⬛","⬛","⬜","⬛","⬛","⬛","⬜","⬛"],
        ["⬛", "⬛", "⬛", "⬜", "⬜", "⬜", "⬛", "⬜", "⬜", "⬜","⬜","⬜","⬜","⬜","⬜","⬜","⬛"],
        ["⬛", "⬜", "⬜", "⬜", "⬜", "⬜", "⬛", "👹", "⬜", "⬛","⬜","⬜","⬜","⬜","⬜","⬜","⬛"],
        ["⬛", "🦇", "⬛", "👿", "⬛", "👺", "⬛", "👺", "👹", "⬛","👿","⬛","⬜","⬛","⬛","⬛","⬛"],
        ["⬛", "⬜", "⬛", "⬜", "⬛", "⬜", "⬛", "⬜", "⬜", "⬛","⬜","⬛","⬜","⬛","⬜","⬜","⬛"],
        ["⬛", "⬜", "⬛", "⬜", "⬛", "⬜", "⬛", "⬜", "⬜", "🦇","⬜","⬛","⬜","⬛","⬜","⬜","⬛"],
        ["⬛", "⬜", "⬛", "⬜", "⬛", "⬜", "⬛", "⬜", "⬜", "⬛","⬜","⬜","⬜","👿","⬜","⬜","⬇️"],
        ["⬛", "⬛", "⬛", "⬛", "⬛", "⬛", "⬛", "⬛", "⬛", "⬛","⬛","⬛","⬛","⬛","⬛","⬛","⬛"],
    ]

g2 = [
        ["⬛", "⬆️", "⬛", "⬛", "⬛", "⬛", "⬛", "⬛", "⬛", "⬛","⬛","⬛","⬛"],
        ["⬛", "⬜", "⬜", "⬜", "⬜", "⬛", "⬜", "⬜", "⬜", "⬜","⬜","⬜","⬛"],
        ["⬛", "⬜", "⬛", "⬜", "⬜", "⬛", "⬜", "⬜", "⬛", "⬛","⬛","⬜","⬛"],
        ["⬛", "⬛", "⬜", "⬜", "⬜", "⬛", "⬛", "⬛", "⬜", "⬛","⬜","⬜","⬛"],
        ["⬛", "⬜", "⬜", "⬛", "⬛", "⬛", "⬜", "⬜", "⬜", "⬛","⬜","⬜","⬛"],
        ["⬛", "⬜", "⬛", "⬜", "⬜", "⬛", "⬜", "⬛", "⬜", "⬛","⬛","⬛","⬛"],
        ["⬛", "⬜", "⬛", "⬛", "⬜", "⬛", "⬛", "⬛", "⬜", "⬛","⬜","⬜","⬛"],
        ["⬛", "⬜", "🦇", "⬛", "⬜", "⬜", "⬜", "⬛", "⬜", "⬜","⬜","⬜","⬛"],
        ["⬛", "⬜", "⬜", "⬜", "⬜", "⬛", "⬜", "⬜", "⬜", "⬛","⬜","⬜","⬛"],
        ["⬛", "⬛", "⬛", "⬛", "⬛", "⬛", "⬛", "⬛", "⬜", "⬛","⬜","⬜","⬛"],
        ["⬛", "⬜", "⬜", "⬛", "⬜", "⬜", "⬜", "⬛", "⬜", "⬛","⬜","⬜","⬛"],
        ["⬛", "⬜", "⬜", "⬛", "⬜", "⬜", "⬜", "⬛", "⬛", "⬛","⬜","⬜","⬛"],
        ["⬛", "⬜", "⬜", "⬛", "⬜", "⬜", "⬜", "⬛", "⬛", "⬛","⬜","⬜","⬛"],
        ["⬛", "⬛", "⬛", "⬛", "⬛", "⬛", "⬛", "⬛", "⬛", "⬛","⬛","⬛","⬛"],
    ]

add_map_package(Map(prefabname="地下一层",mapid = 1,basegrid=g1,birthpos=Vector2(1,1)))
add_map_package(Map(prefabname="地下二层",mapid = 2,basegrid=g2,birthpos=Vector2(1,1)))

def Save(data):
    with open("src.json", "w") as json_file:
        json.dump(data, json_file)
Save(data)


    
