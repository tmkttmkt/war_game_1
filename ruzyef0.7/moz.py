from enum import Enum
from time import time

class cldt(Enum):
    mu=(0,0,0)
    plains=(0,255,0)
    river=(0,128,255)
    rail=(32,32,32)
    road=(128,64,0)
    woods=(0,128,0)
    urban=(128,128,128)
class goal(Enum):
    move=1
    speed_move=2
    fire=3
    defense=4
def henkan(em):
    if cldt.mu==em:
        return 0
    elif cldt.plains==em:
        return 1
    elif cldt.river==em:
        return 2
    elif cldt.rail==em:
        return 3
    elif cldt.road==em:
        return 4
    elif cldt.woods==em:
        return 5
    else:
        return 0
if __name__=='__main__':
    date=[[cldt.plains for i in range(1000)] for j in range(1000)]


    start=time()
    dat=[]
    for obj in date:
        dat+=list(map(henkan,obj))
    print(time()-start)
    start=time()
    dat=[]
    da=[]
    wei=len(date[0])
    hei=len(date)
    max=range(wei)
    for y in range(hei):
        for x in max:
            if date[y][x].name==cldt.mu:
                da+=[1]
            if date[y][x].name==cldt.plains:
                da+=[2]
            if date[y][x].name==cldt.rail:
                da+=[3]
            if date[y][x].name==cldt.road:
                da+=[4]
            if date[y][x].name==cldt.woods:
                da+=[5]
            if date[y][x].name==cldt.urban:
                da+=[6]
        dat+=da
        da=[]
    print(time()-start)

    start=time()
    dat=[[0 if cldt.mu==em else (1 if cldt.plains==em else (2 if cldt.rail==em else (3 if cldt.road==em else(4 if cldt.woods==em else 6)))) for em in lis] for lis in date]

    print(time()-start)
