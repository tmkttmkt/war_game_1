
from pgzero.rect import Rect
def rerect(rect:Rect):
    #print(rect.x,rect.y,rect.w,rect.h)
    if rect.h<0:
        rect.y+=rect.h
        rect.h*=-1
    if rect.w<0:
        rect.x+=rect.h
        rect.w*=-1
    #print(rect.x,rect.y,rect.w,rect.h)
    return rect