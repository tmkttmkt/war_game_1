from enum import Enum
class cldt(Enum):
    mu=(0,0,0)
    plains=(0,255,0)
    river=(0,128,255)
    rail=(32,32,32)
    road=(128,64,0)
    woods=(0,128,0)
    urban=(128,128,128)
#0mu 1heiya 2kawa 3tetudou 4douro 5mori 6mati
class goal(Enum):
    move=1
    speed_move=2
    fire=3
    precision_fire=4
    defense=5
class title_mode(Enum):
    START=0
    execution=1
    CONTINUATION=2
    EXPLANATION=3
class unit_type(Enum):
    tank=1
    artillery=2
    infantry=3
class bullet_type(Enum):
    #wartherで確認
    HE=1
    AP=2
    ki_rifles=3
    rifles=4


